
import pandas as pd
import openpyxl
import typing
import os

from .typing import Box
from .pandas import deduplicate
from .excel import format
from .util import (
    log,
    _arg_to_list,
    ensure_unique_string,
    GREEN,
    RED,
    GREEN_LIGHT,
    ORANGE_LIGHT,
    RED_LIGHT,
    )




class Diff:
    """
    Stores differences between 2 dfs.
    For more detailed documentation see diff() or Diffs.
    """

    def __init__(
            self,
            old: pd.DataFrame,
            new: pd.DataFrame,
            uid=None,
            mode='mix',
            rename_cols: dict = None,
            retain_cols=None,
            remove_cols=None,
            remove_cols_by_suffix=None,
            ignore_cols=None,
            name='data',
            verbosity=3,
            ):

        old = old.convert_dtypes()
        new = new.convert_dtypes()

        #rename cols
        old, new, renamed_old, renamed_new = _rename_cols(
            old,
            new,
            rename_cols,
            )

        #remove cols then readd
        #to the diff result later
        old, new, retained = _retain_cols(
            old,
            new,
            retain_cols,
            )

        #remove cols by name
        old, new, removed_old, removed_new = _remove_cols(
            old,
            new,
            remove_cols,
            )

        #remove cols by suffix
        old, new, removed_by_suffix_old, removed_by_suffix_new = _remove_cols_by_suffix(
            old,
            new,
            remove_cols_by_suffix,
            )

        #ignore for diffing but dont remove
        ignore_cols = _ignore_cols(
            old,
            new,
            ignore_cols,
            )

        #set or find uid col to uniquely
        #identify rows between old and new dfs
        old, new, uid = _set_uid(
            old,
            new,
            uid,
            name,
            verbosity,
            )


        self.old = old
        self.new = new
        self.uid = uid
        self.mode = mode

        self.cols_renamed_old = renamed_old
        self.cols_renamed_new = renamed_new
        self.cols_retained = retained
        self.cols_removed_old = removed_old
        self.cols_removed_new = removed_new
        self.cols_removed_by_suffix_old = removed_by_suffix_old
        self.cols_removed_by_suffix_new = removed_by_suffix_new
        self.cols_ignore = ignore_cols

        self.name = name
        self.verbosity = verbosity


    def details(self):
        """
        Detailed information about differences between datasets.
        """
        cols_shared = (
            self.new
            .columns
            .intersection(self.old.columns)
            .difference(self.cols_ignore)
            )
        cols_added = (
            self.new
            .columns
            .difference(self.old.columns)
            .difference(self.cols_ignore)
            )
        cols_removed = (
            self.old
            .columns
            .difference(self.new.columns)
            .difference(self.cols_ignore)
            )

        rows_shared = (
            self.new
            .index
            .intersection(self.old.index)
            )
        rows_added = (
            self.new
            .index
            .difference(self.old.index)
            )
        rows_removed = (
            self.old
            .index
            .difference(self.new.index)
            )

        dtypes_changed = {}
        for col in cols_shared:
            if self.old[col].dtype != self.new[col].dtype:
                changed = {
                    'old': self.old[col].dtype.name,
                    'new': self.new[col].dtype.name
                    }
                dtypes_changed[col] = changed

        details = Box()

        #basic info
        details.name = self.name
        details.uid = self.uid

        #numerical summary of changes
        details.cols_shared = len(cols_shared)
        details.cols_added = len(cols_added)
        details.cols_removed = len(cols_removed)
        details.rows_shared = len(rows_shared)
        details.rows_added = len(rows_added)
        details.rows_removed = len(rows_removed)
        details.dtypes_changed = len(dtypes_changed)

        #all changes
        details.cols_shared_all = cols_shared
        details.cols_added_all = cols_added
        details.cols_removed_all = cols_removed
        details.rows_shared_all = rows_shared
        details.rows_added_all = rows_added
        details.rows_removed_all = rows_removed
        details.dtypes_changed_all = dtypes_changed

        return details


    def summary(self):
        """
        Summary of differences between datasets.
        """
        details = self.details()
        summary = Box()
        for key, val in details.items():
            if key.endswith('_all'):
                continue
            summary[key] = val
        return summary


    def show(
            self,
            mode='mix',
            suffix_old=' *old',
            linebreak='\n',
            ):
        """
        Generate a styled DataFrame showing differences between datasets.
        For more detailed documentation see diff() or Diffs.
        """

        old = self.old
        new = self.new
        uid = self.uid
        details = self.details()
        cols_added = details.cols_added_all
        cols_removed = details.cols_removed_all
        cols_shared = details.cols_shared_all
        rows_added = details.rows_added_all
        rows_removed = details.rows_removed_all
        rows_shared = details.rows_shared_all
        self.cols_shared_mapping = {}


        if mode not in ('new', 'new+', 'old', 'mix'):
            log(f'error: unknown mode: {mode}', 'du.Diff', self.verbosity)
            raise ValueError(f'Unknown mode: {mode}')


        if old.empty and new.empty:
            df_diff = pd.DataFrame({'diff': ['empty datasets']})
            df_diff.index.name = 'index'
            diff_styled = df_diff.style
            return diff_styled

        elif old.empty:
            df_diff = new.copy()
            df_diff_style = pd.DataFrame(
                f'background-color: {GREEN}',
                index=df_diff.index,
                columns=df_diff.columns,
                )
            col_diff = ensure_unique_string('diff', df_diff.columns)
            df_diff.insert(0, col_diff, 'dataset added')
            diff_styled = df_diff.style.apply(lambda x: df_diff_style, axis=None)
            diff_styled = diff_styled.set_properties(white_space='pre-wrap')
            return diff_styled

        elif new.empty:
            df_diff = old.copy()
            df_diff_style = pd.DataFrame(
                f'background-color: {RED}',
                index=df_diff.index,
                columns=df_diff.columns,
                )
            col_diff = ensure_unique_string('diff', df_diff.columns)
            df_diff.insert(0, col_diff, 'dataset removed')
            diff_styled = df_diff.style.apply(lambda x: df_diff_style, axis=None)
            diff_styled = diff_styled.set_properties(white_space='pre-wrap')
            return diff_styled


        elif mode in ['new', 'new+']:
            df_diff = new.copy()
            df_diff_style = pd.DataFrame(
                '',
                index=df_diff.index,
                columns=df_diff.columns,
                dtype='string',
                )

            #add metadata columns
            cols_shared_mapping = {}
            if mode == 'new+':
                cols_reorder = []
                for col in df_diff.columns:
                    cols_reorder.append(col)
                    if col != uid and col in cols_shared:
                        col_meta = ensure_unique_string(
                            col + suffix_old,
                            taken=df_diff.columns,
                            strategy=f'suffix={suffix_old}',
                            )
                        cols_reorder.append(col_meta)
                        cols_shared_mapping[col] = col_meta
                self.cols_shared_mapping = cols_shared_mapping

                df_diff_meta = pd.DataFrame(
                    pd.NA,
                    index=df_diff.index,
                    columns=cols_shared_mapping.values(),
                    dtype=object,
                    )
                df_diff_style_meta = pd.DataFrame(
                    'font-style: italic',
                    index=df_diff.index,
                    columns=cols_shared_mapping.values(),
                    dtype='string',
                    )

                df_diff = pd.concat(
                    [df_diff, df_diff_meta],
                    axis=1,
                    )
                df_diff_style = pd.concat(
                    [df_diff_style, df_diff_style_meta],
                    axis=1,
                    )

                df_diff = df_diff[cols_reorder]
                df_diff_style = df_diff_style[cols_reorder]

            df_diff_style.loc[:, cols_added] = f'background-color: {GREEN}'
            df_diff_style.loc[rows_added, :] = f'background-color: {GREEN}'

            if self.cols_retain is not None:
                df_diff = _add_cols_retain(df_diff, self.cols_retain)
            col_diff = ensure_unique_string('diff', df_diff.columns)
            df_diff.insert(0, col_diff, '')
            df_diff[col_diff] = df_diff[col_diff].astype('string')
            df_diff.loc[rows_added, col_diff] += 'row added'


        elif mode == 'old':
            df_diff = old.copy()
            df_diff_style = pd.DataFrame(
                '',
                index=df_diff.index,
                columns=df_diff.columns,
                )

            df_diff_style.loc[:, cols_removed] = f'background-color: {RED}'
            df_diff_style.loc[rows_removed, :] = f'background-color: {RED}'

            if self.cols_retain is not None:
                df_diff = _add_cols_retain(df_diff, self.cols_retain)
            col_diff = ensure_unique_string('diff', df_diff.columns)
            df_diff.insert(0, col_diff, '')
            df_diff.loc[rows_removed, col_diff] += 'row removed'


        elif mode == 'mix':
            inds_old = old.index.difference(new.index)
            cols_old = old.columns.difference(new.columns)

            df_diff = pd.concat([new, old.loc[:, cols_old]], axis=1)
            df_diff.loc[inds_old, :] = old.loc[inds_old, :]

            df_diff_style = pd.DataFrame(
                '',
                index=df_diff.index,
                columns=df_diff.columns,
                )

            df_diff_style.loc[:, cols_added] = f'background-color: {GREEN}'
            df_diff_style.loc[:, cols_removed] = f'background-color: {RED}'
            df_diff_style.loc[rows_added, :] = f'background-color: {GREEN}'
            df_diff_style.loc[rows_removed, :] = f'background-color: {RED}'

            if self.cols_retain is not None:
                df_diff = _add_cols_retain(df_diff, self.cols_retain)
            col_diff = ensure_unique_string('diff', df_diff.columns)
            df_diff.insert(0, col_diff, '')
            df_diff.loc[rows_added, col_diff] += 'row added'
            df_diff.loc[rows_removed, col_diff] += 'row removed'



        #highlight values in shared columns

        #replace "<" and ">" with html entities to prevent interpretation as html tags
        #doing this also impacts dtypes, which might be more problematic than the odd
        #html tag
        # if pd.__version__ >= '2.1.0':
        #     df_diff = df_diff.map(lambda x: _replace_gt_lt(x))
        # else:
        #     df_diff = df_diff.applymap(lambda x: _replace_gt_lt(x))

        df_old_isna = old.loc[rows_shared, cols_shared].isna()
        df_new_isna = new.loc[rows_shared, cols_shared].isna()
        df_new_equals_old = (
            new.loc[rows_shared, cols_shared]
            == old.loc[rows_shared, cols_shared]
            )

        #these comparisons can result in dtype "boolean" instead of "bool"
        #"boolean" masks cannot be used to set values as str
        df_added = (df_old_isna & ~df_new_isna).astype(bool)
        df_removed = (df_new_isna & ~df_old_isna).astype(bool)
        df_changed = (~df_new_isna & ~df_old_isna & ~df_new_equals_old).astype(bool)

        df_diff_style.loc[rows_shared, cols_shared] += (
            df_added
            .mask(df_added, f'background-color: {GREEN_LIGHT}')
            .where(df_added, '')
            )

        df_diff_style.loc[rows_shared, cols_shared] += (
            df_removed
            .mask(df_removed, f'background-color: {RED_LIGHT}')
            .where(df_removed, '')
            )

        df_diff_style.loc[rows_shared, cols_shared] += (
            df_changed
            .mask(df_changed, f'background-color: {ORANGE_LIGHT}')
            .where(df_changed, '')
            )


        #summarize changes in diff column
        sum_added = df_added.sum(axis=1)
        sum_removed = df_removed.sum(axis=1)
        sum_changed = df_changed.sum(axis=1)

        added = sum_added[sum_added > 0].index
        removed = sum_removed[sum_removed > 0].index
        changed = sum_changed[sum_changed > 0].index

        removed_and_changed = removed.intersection(changed)
        removed_or_changed = removed.union(changed)
        removed_or_changed_and_added = removed_or_changed.intersection(added)

        df_diff.loc[added, col_diff] += 'vals added: '
        df_diff.loc[added, col_diff] += sum_added[added].astype('string')
        df_diff.loc[removed_or_changed_and_added, col_diff] += linebreak

        df_diff.loc[removed, col_diff] += 'vals removed: '
        df_diff.loc[removed, col_diff] += sum_removed[removed].astype('string')
        df_diff.loc[removed_and_changed, col_diff] += linebreak

        df_diff.loc[changed, col_diff] += 'vals changed: '
        df_diff.loc[changed, col_diff] += sum_changed[changed].astype('string')


        if mode == 'new+':
            df_all_modifications = (df_added | df_removed | df_changed)
            df_old_changed = (
                old
                .loc[rows_shared, cols_shared]
                .where(df_all_modifications, pd.NA)
                .rename(columns=cols_shared_mapping)
                )
            df_diff.loc[rows_shared, cols_shared_mapping.values()] = df_old_changed


        if len(df_diff.columns) * len(df_diff.index) > 100_000:
            msg = (
                'warning: more than 100 000 cells are being formatted.'
                'while this might not cause performance issues for formatting,'
                'the result might be slow to render, especially in jupyter notebooks.'
                )
            log(msg, 'du.Diff', self.verbosity)

        diff_styled = (
            df_diff
            .style
            .apply(lambda x: df_diff_style, axis=None)
            .set_properties(white_space='pre-wrap')
            )
        msg = 'debug: created df with highlighted differences'
        log(msg, 'du.Diff', self.verbosity)
        return diff_styled


    def str(self):
        """
        String summary of differences between datasets.
        """
        string = f'Diff of {self.name!r}:\n'
        if self.old.empty and self.new.empty:
            string += '  both datasets are empty\n'
        elif self.old.empty:
            string += '  old dataset is empty\n'
        elif self.new.empty:
            string += '  new dataset is empty\n'
        elif self.old.equals(self.new):
            string += '  datasets are identical\n'
        else:
            details = self.details()
            cols_shared_str = _to_str(
                details.cols_shared_all,
                linebreak='\n  ',
                )
            cols_added_str = _to_str(
                details.cols_added_all,
                linebreak='\n  ',
                )
            cols_removed_str = _to_str(
                details.cols_removed_all,
                linebreak='\n  ',
                )
            rows_shared_str = _to_str(
                details.rows_shared_all,
                linebreak='\n  ',
                )
            rows_added_str = _to_str(
                details.rows_added_all,
                linebreak='\n  ',
                )
            rows_removed_str = _to_str(
                details.rows_removed_all,
                linebreak='\n  ',
                )
            dtypes_changed_str = _to_str(
                details.dtypes_changed_all,
                linebreak='\n  ',
                )
            string += (
                f' cols shared: {details.cols_shared}\n'
                f' cols added: {details.cols_added}\n'
                f' cols removed: {details.cols_removed}\n'
                f' rows shared: {details.rows_shared}\n'
                f' rows added: {details.rows_added}\n'
                f' rows removed: {details.rows_removed}\n'
                f' dtypes changed: {details.dtypes_changed}\n'
                f' all cols shared:\n  {cols_shared_str}\n'
                f' all cols added:\n  {cols_added_str}\n'
                f' all cols removed:\n  {cols_removed_str}\n'
                f' all rows shared:\n  {rows_shared_str}\n'
                f' all rows added:\n  {rows_added_str}\n'
                f' all rows removed:\n  {rows_removed_str}\n'
                f' all dtypes changed:\n  {dtypes_changed_str}\n'
                )
        return string

    def print(self):
        print(self.str())
        return self




def _rename_cols(
        old: pd.DataFrame,
        new: pd.DataFrame,
        cols_mapping: dict | None,
        ) -> tuple[pd.DataFrame, pd.DataFrame, dict, dict]:
    """
    Rename cols from both dfs before diffing
    """

    if cols_mapping is None:
        return old, new, {}, {}

    cols_mapping_old = {
        k: v
        for k, v
        in cols_mapping.items()
        if k in old.columns
        }

    cols_mapping_new = {
        k: v
        for k, v
        in cols_mapping.items()
        if k in new.columns
        }

    old = old.rename(columns=cols_mapping_old)
    new = new.rename(columns=cols_mapping_new)

    return old, new, cols_mapping_old, cols_mapping_new



def _retain_cols(
        old: pd.DataFrame,
        new: pd.DataFrame,
        cols: typing.Any,
        ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Remove cols from both dfs before diffing,
    then readd the ones from the old df to
    the diff result later.
    """

    if cols is None:
        return old, new, pd.DataFrame()

    cols_retain = _arg_to_list(cols)

    cols_retain_old = old.columns.intersection(cols_retain)
    cols_retain_new = new.columns.intersection(cols_retain)

    cols_retained = old[cols_retain_old].copy()

    old = old.drop(columns=cols_retain_old)
    new = new.drop(columns=cols_retain_new)

    return old, new, cols_retained



def _remove_cols(
        old: pd.DataFrame,
        new: pd.DataFrame,
        cols: typing.Any,
        ) -> tuple[pd.DataFrame, pd.DataFrame, list, list]:
    """
    Remove cols from both dfsbefore diffing.
    """
    if cols is None:
        return old, new, [], []

    cols_remove = _arg_to_list(cols)

    cols_remove_old = (
        old.columns.
        intersection(cols_remove)
        .to_list()
        )
    cols_remove_new = (
        new.columns
        .intersection(cols_remove)
        .to_list()
        )

    old = old.drop(columns=cols_remove_old)
    new = new.drop(columns=cols_remove_new)

    return old, new, cols_remove_old, cols_remove_new



def _remove_cols_by_suffix(
        old: pd.DataFrame,
        new: pd.DataFrame,
        suffix: str | None,
        ) -> tuple[pd.DataFrame, pd.DataFrame, list, list]:
    """
    Remove cols from both dfs ending with
    a specific suffix before diffing.
    """

    if suffix is None:
        return old, new, [], []

    cols_remove_old = [
        col
        for col
        in old.columns
        if str(col).endswith(suffix)
        ]
    old = old.drop(columns=cols_remove_old)

    cols_remove_new = [
        col
        for col
        in new.columns
        if str(col).endswith(suffix)
        ]
    new = new.drop(columns=cols_remove_new)

    return old, new, cols_remove_old, cols_remove_new



def _ignore_cols(
        old: pd.DataFrame,
        new: pd.DataFrame,
        cols: typing.Any,
        ) -> list:
    """
    Ignore columns for diffing,
    but keep them in both datasets.
    """

    if cols is None:
        return []

    cols_ignore = (
        old.columns
        .union(new.columns)
        .intersection(_arg_to_list(cols))
        .to_list()
        )

    return cols_ignore



def _set_uid(
        old: pd.DataFrame,
        new: pd.DataFrame,
        uid: typing.Any = None,
        name='data',
        verbosity=3,
        ) -> tuple[pd.DataFrame, pd.DataFrame, typing.Any]:
    """
    find suitable unique identifier (uid) column
    for comparing rows between old and new dfs.
    """

    if uid is False:
        msg = 'trace: using index as uid'
        log(msg, 'dk.diffing._set_uid', verbosity)
        uid = ''

    elif uid is None:
        msg = 'trace: searching for suitable uid column'
        log(msg, 'dk.diffing._set_uid', verbosity)
        uid = _find_uid(
            old,
            new,
            name,
            verbosity,
            )
        old.index = old[uid]
        new.index = new[uid]
        old.drop(columns=uid, inplace=True)
        new.drop(columns=uid, inplace=True)

    elif uid in old.columns and uid in new.columns:
        old.index = old[uid]
        new.index = new[uid]
        old.drop(columns=uid, inplace=True)
        new.drop(columns=uid, inplace=True)

    else:
        raise ValueError(f"UID column {uid!r} not found in both dataframes.")


    if not old.index.is_unique:
        old.index = deduplicate(
            old.index,
            name=f'{uid} in old df',
            verbosity=verbosity,
            )
    if not new.index.is_unique:
        new.index = deduplicate(
            new.index,
            name=f'{uid} in new df',
            verbosity=verbosity,
            )

    if not old.index.name:
        old.index.name = 'index'
    if not new.index.name:
        new.index.name = 'index'

    return old, new, uid



def _find_uid(
        old: pd.DataFrame,
        new: pd.DataFrame,
        name='data',
        verbosity=3,
        ) -> typing.Any:
    """
    Used if no suitable uid column was provided.
    """

    uids_potential = new.columns.intersection(old.columns)
    uids_by_uniqueness = {}

    for uid in uids_potential:
        unique_in_old = pd.Index(old[uid].dropna()).unique()
        unique_in_new = pd.Index(new[uid].dropna()).unique()
        unique_shared = unique_in_new.intersection(unique_in_old)
        uids_by_uniqueness[uid] = len(unique_shared)

    uids_by_uniqueness = sorted(
        uids_by_uniqueness.items(),
        key=lambda item: item[1],
        reverse=True,
        )

    if len(uids_by_uniqueness) > 0:
        uid = uids_by_uniqueness[0][0]
        msg = f'debug: found uid {uid!r} for {name!r}'
        log(msg, 'du.Diff', verbosity)
    else:
        uid = ''
        msg = f'debug: no uid found. using index for {name!r}'
        log(msg, 'du.Diff', verbosity)

    return uid




class Diffs:
    """
    Stores differences between (multiple) datasets.
    For more detailed documentation see diff().
    """

    def __init__(
            self,
            old: pd.DataFrame | str,
            new: pd.DataFrame | str,
            uid=None,
            ignore_cols=None,
            rename_cols=None,
            retain_cols=None,
            remove_cols=None,
            remove_cols_by_suffix=None,
            remove_sheets=None,
            verbosity=3,
            ):
        self.verbosity = verbosity
        self.all = self._get_Diffs(
            old=old,
            new=new,
            uid=uid,
            ignore_cols=ignore_cols,
            rename_cols=rename_cols,
            retain_cols=retain_cols,
            remove_cols=remove_cols,
            remove_cols_by_suffix=remove_cols_by_suffix,
            remove_sheets=remove_sheets,
            )
        self.cols_summary = [
            'uid',
            'in both datasets',
            'cols shared',
            'cols added',
            'cols removed',
            'rows shared',
            'rows added',
            'rows removed',
            'dtypes changed',
            ]


    def _get_Diffs(
            self,
            old,
            new,
            uid=None,
            ignore_cols=None,
            rename_cols=None,
            retain_cols=None,
            remove_cols=None,
            remove_cols_by_suffix=None,
            remove_sheets=None,
            ):
        """
        Loads dataframes from various sources (pd.DataFrame, CSV files, Excel files)
        and determines whether to compare single sheets or multiple Excel sheets.
        """
        msg = 'Debug: getting data for Diffs'
        log(msg, 'du.Diffs', self.verbosity)
        self.old = old
        self.new = new

        #when both inputs are excel files, they might
        #contain multiple sheets to be compared
        conditions_excel_comp = (
            isinstance(old, str)
            and isinstance(new, str)
            and old.endswith('.xlsx')
            and new.endswith('.xlsx')
            )
        if conditions_excel_comp:
            diffs = self._get_excel_Diffs(
                old=old,
                new=new,
                uid=uid,
                ignore_cols=ignore_cols,
                rename_cols=rename_cols,
                retain_cols=retain_cols,
                remove_cols=remove_cols,
                remove_cols_by_suffix=remove_cols_by_suffix,
                remove_sheets=remove_sheets,
                )
            return diffs


        #only 2 dfs need to be compared if input is
        #2 dfs, 2 csvs or 1 df and 1 csv/excel file
        else:
            if isinstance(old, str):
                if old.endswith('.csv'):
                    df_old = pd.read_csv(old)
                elif old.endswith('.xlsx'):
                    df_old = pd.read_excel(old, dtype_backend='numpy_nullable')
                else:
                    msg = f'error: unknown file extension: {old}'
                    log(msg, 'du.Diffs', self.verbosity)
                    raise ValueError(msg)
            elif isinstance(old, pd.DataFrame):
                df_old = old
            else:
                msg = 'error: incompatible type for old df'
                log(msg, 'du.Diffs', self.verbosity)
                raise ValueError(msg)

            if isinstance(new, str):
                if new.endswith('.csv'):
                    df_new = pd.read_csv(new)
                elif new.endswith('.xlsx'):
                    df_new = pd.read_excel(new, dtype_backend='numpy_nullable')
                else:
                    msg = f'error: unknown file extension: {new}'
                    log(msg, 'du.Diffs', self.verbosity)
            elif isinstance(new, pd.DataFrame):
                df_new = new

            else:
                msg = 'error: incompatible type for new df'
                log(msg, 'du.Diffs', self.verbosity)

            diff = Diff(
                old=df_old,
                new=df_new,
                uid=uid,
                ignore_cols=ignore_cols,
                rename_cols=rename_cols,
                retain_cols=retain_cols,
                remove_cols=remove_cols,
                remove_cols_by_suffix=remove_cols_by_suffix,
                verbosity=self.verbosity,
                )
            diff.sheet = ''
            diff.in_both_datasets = 'yes'
            diffs = [diff]
            return diffs


    def _get_excel_Diffs(
            self,
            old,
            new,
            uid=None,
            ignore_cols=None,
            rename_cols=None,
            retain_cols=None,
            remove_cols=None,
            remove_cols_by_suffix=None,
            remove_sheets=None,
            ):
        """
        Read all sheets from two Excel files.
        """

        diffs = []
        sheets_old = pd.ExcelFile(old).sheet_names
        sheets_new = pd.ExcelFile(new).sheet_names
        sheets_all = list(dict.fromkeys(sheets_new + sheets_old))  #preserves order
        sheets_remove = _arg_to_list(remove_sheets)

        for sheet in sheets_all:
            if sheet in sheets_remove:
                msg = f'trace: removing sheet {sheet!r} before diffing'
                log(msg, 'du.Diffs', self.verbosity)
                continue
            elif sheet in sheets_old and sheet in sheets_new:
                df_old = pd.read_excel(
                    old,
                    sheet_name=sheet,
                    dtype_backend='numpy_nullable',
                    )
                df_new = pd.read_excel(
                    new,
                    sheet_name=sheet,
                    dtype_backend='numpy_nullable',
                    )
                in_both_datasets = 'yes'
            elif sheet in sheets_new:
                df_old = pd.DataFrame()
                df_new = pd.read_excel(
                    new,
                    sheet_name=sheet,
                    dtype_backend='numpy_nullable',
                    )
                in_both_datasets = 'only in new'
            elif sheet in sheets_old:
                df_old = pd.read_excel(
                    old,
                    sheet_name=sheet,
                    dtype_backend='numpy_nullable',
                    )
                df_new = pd.DataFrame()
                in_both_datasets = 'only in old'

            if isinstance(uid, dict):
                uid_sheet = uid.get(sheet, None)
            else:
                uid_sheet = uid

            diff = Diff(
                old=df_old,
                new=df_new,
                uid=uid_sheet,
                ignore_cols=ignore_cols,
                rename_cols=rename_cols,
                retain_cols=retain_cols,
                remove_cols=remove_cols,
                remove_cols_by_suffix=remove_cols_by_suffix,
                name=sheet,
                verbosity=self.verbosity,
                )
            diff.sheet = sheet
            diff.in_both_datasets = in_both_datasets
            diffs.append(diff)

        msg = 'debug: created Diffs for 2 excel files'
        log(msg, 'du.Diffs', self.verbosity)
        return diffs


    def __getitem__(self, key):
        """
        Get a specific Diff by sheet name or index.
        """
        if isinstance(key, int):
            item = self.all[key]
        else:
            for diff in self.all:
                if diff.name == key:
                    item = diff
                    break
            else:
                msg = f'error: sheet "{key}" not found in diffs'
                log(msg, 'du.Diff', self.verbosity)
                return None
        return item


    def info(self):
        """
        Basic information about the datasets.
        """
        if isinstance(self.old, str):
            name_old = self.old
            size_old = os.path.getsize(self.old) / 1024
        else:
            name_old = type(self.old).__name__
            size_old = self.old.memory_usage(deep=True).sum() / 1024
        if isinstance(self.new, str):
            name_new = self.new
            size_new = os.path.getsize(self.new) / 1024
        else:
            name_new = type(self.new).__name__
            size_new = self.new.memory_usage(deep=True).sum() / 1024
        data = {
            'name': [name_old, name_new],
            'size (KB)': [size_old, size_new],
            }
        info = pd.DataFrame(
            data,
            index=['old dataset', 'new dataset'],
            )
        info.index.name = 'dataset'
        return info


    def details(
            self,
            separator=',',
            linebreak='\n',
            ):
        """
        Detailed information about differences between datasets.
        """

        datasets = [diff.name for diff in self.all]
        data = {
            'uid': [diff.uid for diff in self.all],
            'in both datasets': [diff.in_both_datasets for diff in self.all],
            }
        details = pd.DataFrame(data, index=datasets)
        details.index.name = 'dataset'

        cols = {
            #numerical summary
            'cols_shared': 'cols shared',
            'cols_added': 'cols added',
            'cols_removed': 'cols removed',
            'rows_shared': 'rows shared',
            'rows_added': 'rows added',
            'rows_removed': 'rows removed',
            'dtypes_changed': 'dtypes changed',
            #all changes
            'cols_shared_all': 'all cols shared',
            'cols_added_all': 'all cols added',
            'cols_removed_all': 'all cols removed',
            'rows_shared_all': 'all rows shared',
            'rows_added_all': 'all rows added',
            'rows_removed_all': 'all rows removed',
            'dtypes_changed_all': 'all dtypes changed',
            }

        for diff in self.all:
            diff_details = diff.details()
            for key, col in cols.items():
                string = _to_str(
                    diff_details[key],
                    separator,
                    linebreak,
                    )
                details.loc[diff.name, col] = string

        details = details.style.set_properties(**{
            # 'text-align': 'left',
            'white-space': 'pre-wrap',
            })
        return details


    def summary(
            self,
            separator=',',
            linebreak='\n',
            ):
        """
        Summary of differences between datasets.
        """
        details = self.details(separator, linebreak).data
        summary = details[self.cols_summary]
        summary = summary.style.set_properties(**{
            # 'text-align': 'left',
            'white-space': 'pre-wrap',
            })
        return summary


    def show(
            self,
            mode='mix',
            sheet=0,
            suffix_old=' *old',
            linebreak='\n',
            ):
        """
        Generate a styled DataFrame showing differences between datasets.
        Differences are highlighted with color-coded styles,
        supporting multiple visualization modes.

        Parameters
        ----------

        mode : str, default 'mix'
            Display mode for differences:
            * 'new': Show new DataFrame with added and changed elements highlighted
            * 'new+': Show new DataFrame with old values in additional (hidden) columns
            * 'old': Show old DataFrame with removed elements highlighted
            * 'mix': Combine both DataFrames showing all changes

        sheet : str | int, default 0
            Sheet name or index to show differences for (if there are multiple sheets)

        suffix_old : str, default ' *old'
            Suffix for columns showing old values (used in 'new+' mode)

        Returns
        -------
        pandas.io.formats.style.Styler
            Styled DataFrame with color-coded differences
        """
        diff = self[sheet]
        result = diff.show(
            mode,
            suffix_old,
            linebreak,
            )
        return result


    def to_excel(
            self,
            path,
            mode='new+',
            suffix_old=' *old',
            linebreak='\n',
            separator=',',
            index=True,
            apply_format=True,
            hide_info=True,
            hide_details=True,
            hide_summary=False,
            ):
        """
        Export diff results to an Excel file with formatting.

        Creates an Excel file containing a summary sheet and individual
        sheets for each comparison with highlighted differences. Applies
        Excel-specific formatting and hides columns with old values.


        Parameters
        ----------
        path : str
            File path for the output Excel file
        mode : str, default 'mix'
            Display mode for differences (see show() method for options)
        suffix_old : str, default ' *old'
            Suffix for columns showing old values (used in 'new+' mode)
        linebreak : str, default '\\n'
            String to use for line breaks in summary/details
        separator : str, default ','
            Separator string for lists in summary/details
        index : bool, default False
            Whether to include row indices in the Excel output
        hide_info : bool, default True
            Whether to hide the info sheet in the Excel file
        hide_details : bool, default True
            Whether to hide the details sheet in the Excel file
        hide_summary : bool, default False
            Whether to hide the summary sheet in the Excel file
        """

        log(f'debug: saving differences to "{path}"', 'du.Diff', self.verbosity)
        with pd.ExcelWriter(path) as writer:

            #metadata sheets: info, summary, details

            info = self.info()
            summary = self.summary(
                separator,
                linebreak,
                )
            details = self.details(
                separator,
                linebreak,
                )

            sheets = summary.index
            sheet_info = ensure_unique_string(
                'info',
                sheets,
                )
            sheet_summary = ensure_unique_string(
                'summary',
                sheets,
                )
            sheet_details = ensure_unique_string(
                'details',
                sheets,
                )

            info.to_excel(
                writer,
                sheet_name=sheet_info,
                index=True,
                )
            log('debug: info sheet saved', 'du.Diff', self.verbosity)

            summary.to_excel(
                writer,
                sheet_name=sheet_summary,
                index=True,
                )
            log('debug: summary sheet saved', 'du.Diff', self.verbosity)

            details.to_excel(
                writer,
                sheet_name=sheet_details,
                index=True,
                )
            log('debug: details sheet saved', 'du.Diff', self.verbosity)

            #diff sheets
            for diff in self.all:
                result = diff.show(
                    mode,
                    suffix_old,
                    linebreak,
                    )
                result.to_excel(
                    writer,
                    sheet_name=diff.name,
                    index=index,
                    )
                msg = f'debug: diff sheet saved: "{diff.name}"'
                log(msg, 'du.Diff', self.verbosity)


        #format excel file
        if apply_format:
            wb = openpyxl.load_workbook(path)

            #metadata sheets
            sheets_hide = []
            if hide_info:
                sheets_hide.append(sheet_info)
            if hide_summary:
                sheets_hide.append(sheet_summary)
            if hide_details:
                sheets_hide.append(sheet_details)
            format(
                path,
                sheet=[sheet_info, sheet_summary, sheet_details],
                hide_sheets=sheets_hide,
                freeze_panes='B2',
                openpyxl_workbook=wb,
                )
            msg = 'debug: info, summary, details sheets formatted'
            log(msg, 'du.Diff', self.verbosity)

            #diff sheets
            for diff in self.all:
                if index:
                    if diff.cols_retain is None:
                        freeze_panes = 'C2'
                    else:
                        freeze_panes = 'D2'
                else:
                    if diff.cols_retain is None:
                        freeze_panes = 'B2'
                    else:
                        freeze_panes = 'C2'
                if mode == 'new+':
                    cols_hide = list(diff.cols_shared_mapping.values())
                else:
                    cols_hide = None
                format(
                    path,
                    sheet=diff.name,
                    hide_cols=cols_hide,
                    freeze_panes=freeze_panes,
                    openpyxl_workbook=wb,
                    )
                msg = f'debug: diff sheet formatted: "{diff.name}"'
                log(msg, 'du.Diff', self.verbosity)

        log(f'info: differences saved to "{path}"', 'du.Diff', self.verbosity)


    def str(self):
        string = 'Diffs summary:'
        for diff in self.all:
            string += '\n  ' + diff.str().replace('\n', '\n  ')
        return string

    def print(self):
        print(self.str())
        return self

    def __iter__(self):
        for diff in self.all:
            yield diff


def _to_str(obj, separator=',', linebreak='\n'):

    if isinstance(obj, int):
        if obj == 0:
            string = ''
        else:
            string = str(obj)

    elif isinstance(obj, dict):
        if len(obj) == 0:
            string = ''
        else:
            strings = []
            for key, val in obj.items():
                val_old = val['old']
                val_new = val['new']
                strings.append(f'{key!r}: {val_old!r} -> {val_new!r}')
            string = f'{separator}{linebreak}'.join(strings)

    elif isinstance(obj, (list, set, tuple, pd.Index)):
        if len(obj) == 0:
            string = ''
        else:
            items = [f'{x!r}' for x in obj]
            string = f'{separator}{linebreak}'.join(items)

    else:
        string = str(obj)

    return string


def _add_cols_retain(df, cols_retain):
    idx_shared = df.index.intersection(cols_retain.index)
    df_retain = pd.DataFrame(
        '',
        index=df.index,
        columns=cols_retain.columns,
        )
    df_retain.loc[idx_shared, :] = cols_retain.loc[idx_shared, :]
    df_new = pd.concat([df_retain, df], axis=1)
    return df_new


def diff(
        old: pd.DataFrame | str,
        new: pd.DataFrame | str,
        uid=None,
        ignore_cols=None,
        rename_cols=None,
        retain_cols=None,
        remove_cols=None,
        remove_cols_by_suffix=None,
        remove_sheets=None,
        verbosity=3,
        ) -> Diffs:
    """
    Calculates differences between dataframes,
    csv or excel files and returns a Diffs object.


    Parameters
    ----------

    old, new : pd.DataFrame or filepath to CSV or Excel file

    uid : identifies corresponding rows in old and new data.
        * "COLNAME": use the specified column as unique identifier.
        * None: try to find a suitable column automatically.
        * False: use the index as unique identifier.
        * dict: when comparing multiple sheets from excel files, a dictionary
        with sheet names as keys and uid column names as values can be provided.
    ignore_cols : column(s) to ignore for comparison.
    rename_cols : dictionary to rename columns before comparison.
    retain_cols : column(s) to remove from both datasets, then readd to the result.
    remove_cols : column(s) to remove before comparison.
    remove_cols_by_suffix : remove columns that end with the specified suffix.
    remove_sheets : sheet name(s) to remove before comparison (only for excel files).


    Examples
    --------

    basic usage:

    >>> import dukit as du
    >>> diffs = du.diff('old.xlsx', 'new.xlsx')
    >>> diffs.info()  #df of compared datasets and their sizes
    >>> diffs.summary()  #df with summary stats
    >>> diffs.details()  #df with more detailed stats
    >>> diffs.show()   #df.style with highlighted differences
    >>> diffs.str()  #string version of summary stats
    >>> diffs.print()  #prints the string version
    >>> diffs.to_excel('diffs.xlsx')  #writes summary and dfs to file

    access individual sheet diffs:
    >>> diff_sheet1 = diffs[0]  #get diff for first sheet
    >>> diff_sheet1 = diffs['Sheet1']  #get by name
    >>> diff_sheet1.show()
    >>> diff_sheet1.rename_cols({'old_name': 'new_name'})
    """
    diffs = Diffs(
        old=old,
        new=new,
        uid=uid,
        ignore_cols=ignore_cols,
        rename_cols=rename_cols,
        retain_cols=retain_cols,
        remove_cols=remove_cols,
        remove_cols_by_suffix=remove_cols_by_suffix,
        remove_sheets=remove_sheets,
        verbosity=verbosity,
        )
    return diffs


def rediff(
        old: pd.DataFrame | str,
        new: pd.DataFrame | str,
        uid=None,
        ignore_cols=None,
        rename_cols=None,
        retain_cols='notes',
        remove_cols=('diff', 'uid.1'),
        remove_cols_by_suffix=' *old',
        remove_sheets=('info', 'summary', 'details'),
        verbosity=3,
        ) -> Diffs:
    """
    Same as diff(), but using defaults appropriate for
    when the old dataset is already a diff output.
    Can be imagined as diffing the data while managing
    metadata appropriately.
    """
    diffs = Diffs(
        old=old,
        new=new,
        uid=uid,
        ignore_cols=ignore_cols,
        rename_cols=rename_cols,
        retain_cols=retain_cols,
        remove_cols=remove_cols,
        remove_cols_by_suffix=remove_cols_by_suffix,
        remove_sheets=remove_sheets,
        verbosity=verbosity,
        )
    return diffs

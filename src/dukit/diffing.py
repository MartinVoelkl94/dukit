
import pandas as pd
import openpyxl
import typing
import os

from .pandas import deduplicate
from .excel import format
from .util import (
    log,
    _arg_to_list,
    ensure_unique_string,
    list_to_str,
    GREEN,
    RED,
    GREY_LIGHT,
    GREEN_LIGHT,
    ORANGE_LIGHT,
    RED_LIGHT,
    )


def diff(
        old: pd.DataFrame | str,
        new: pd.DataFrame | str,
        uid=None,
        mode='mix',
        rename_cols: dict = None,
        remove_cols: list | str = None,
        remove_cols_by_suffix='',
        retain_cols: list | str = None,
        ignore_cols: list | str = None,
        remove_sheets: list | str = None,
        name='data',
        linebreak='<br>',
        suffix_old=' *old',
        verbosity=3,
        ) -> Diffs:
    """
    Calculates differences between dfs,
    CSV or Excel files and returns a Diffs object.


    Parameters
    ----------

    old, new : pd.DataFrame or filepath to CSV or Excel file

    uid : identifies corresponding rows in old and new data.
        * "COLNAME": use the specified col as unique identifier.
        * None: try to find a suitable col automatically.
        * False: use the index as unique identifier.

    mode : how to display differences in the result.
        * "mix": show rows and cols from old and new df
        * "old": show only rows and cols from old df
        * "new": show only rows and cols from new df
        * "new+": also adds hidden columns with old values for comparison

    rename_cols : dictionary to rename cols before comparison.
    remove_cols : remove col(s) from both dfs.
    remove_cols_by_suffix : remove cols that end with the specified suffix.
    retain_cols : remove col(s) from both dfs, then readd to the result.
    ignore_cols : keep col(s) but ignore them for comparison.
    remove_sheets : remove sheets before comparison (only for excel files).


    Examples
    --------

    basic usage:

    >>> import dukit as dk
    >>> diffs = dk.diff('old.xlsx', 'new.xlsx')
    >>> diffs.show()   #highlighted additions/removals/changes
    >>> diffs.info()
    >>> diffs.summary()
    >>> diffs.details()
    >>> diffs.to_excel('diffs.xlsx')
    >>> diffs[0]  #get the first diff
    >>> diffs['Sheet1']  #get the diff for a specific sheet
    """

    diffs = Diffs(
        old=old,
        new=new,
        uid=uid,
        mode=mode,
        rename_cols=rename_cols,
        remove_cols=remove_cols,
        remove_cols_by_suffix=remove_cols_by_suffix,
        retain_cols=retain_cols,
        ignore_cols=ignore_cols,
        remove_sheets=remove_sheets,
        name=name,
        linebreak=linebreak,
        suffix_old=suffix_old,
        verbosity=verbosity,
        )
    return diffs




def rediff(
        old: pd.DataFrame | str,
        new: pd.DataFrame | str,
        uid=None,
        mode='new+',
        rename_cols: dict = None,
        remove_cols: list | str = 'diff',
        remove_cols_by_suffix=' *old',
        retain_cols: list | str = 'notes',
        ignore_cols: list | str = None,
        remove_sheets=['info', 'summary', 'details'],
        name='data',
        linebreak='\n',
        suffix_old=' *old',
        verbosity=3,
        ) -> Diffs:
    """
    Same as diff(), but using defaults appropriate for
    when the old data is already a diff output.
    Can be imagined as diffing the data
    while managing metadata appropriately.
    """
    diffs = Diffs(
        old=old,
        new=new,
        uid=uid,
        mode=mode,
        rename_cols=rename_cols,
        remove_cols=remove_cols,
        remove_cols_by_suffix=remove_cols_by_suffix,
        retain_cols=retain_cols,
        ignore_cols=ignore_cols,
        remove_sheets=remove_sheets,
        name=name,
        linebreak=linebreak,
        suffix_old=suffix_old,
        verbosity=verbosity,
        )
    return diffs




class Diffs:
    """
    Stores differences between (multiple) dfs.
    For more detailed documentation see diff().
    """

    def __init__(
            self,
            old: pd.DataFrame | str,
            new: pd.DataFrame | str,
            uid=None,
            mode='mix',
            rename_cols: dict = None,
            remove_cols: list | str = None,
            remove_cols_by_suffix='',
            retain_cols: list | str = None,
            ignore_cols: list | str = None,
            remove_sheets: list | str = None,
            name='data',
            linebreak='<br>',
            suffix_old=' *old',
            verbosity=3,
            ):

        self.linebreak = linebreak
        self.verbosity = verbosity

        if isinstance(old, pd.DataFrame) and isinstance(new, pd.DataFrame):
            self.old = {name: old}
            self.new = {name: new}
            self.old_name = 'old'
            self.new_name = 'new'
            self.old_size = old.memory_usage(deep=True).sum() / 1024
            self.new_size = new.memory_usage(deep=True).sum() / 1024

        elif isinstance(old, str) and isinstance(new, str):
            self.old, self.new = _get_data(
                old,
                new,
                remove_sheets,
                name,
                verbosity,
                )
            self.old_name = old
            self.new_name = new
            self.old_size = os.path.getsize(old) / 1024
            self.new_size = os.path.getsize(new) / 1024

        else:
            msg = (
                'ERROR: old and new must be 2 dfs,'
                ' 2 csv files or 2 excel files.'
                )
            log(msg, 'dk.diffing.Diffs.__init__', verbosity)
            raise ValueError(msg)


        self.diffs = _get_diffs(
            old=self.old,
            new=self.new,
            uid=uid,
            mode=mode,
            rename_cols=rename_cols,
            remove_cols=remove_cols,
            remove_cols_by_suffix=remove_cols_by_suffix,
            retain_cols=retain_cols,
            ignore_cols=ignore_cols,
            linebreak=linebreak,
            suffix_old=suffix_old,
            verbosity=verbosity,
            )


    def __getitem__(self, key):
        """
        Get a specific Diff by sheetname or index.
        """
        if isinstance(key, str):
            item = self.diffs[key]
        else:
            item = list(self.diffs.values())[key]
        return item


    def show(self, sheet=0):
        """
        Show a styled df with highlighted differences between dfs.
        """
        diff = self[sheet]
        return diff.result


    def info(self):
        """
        Basic information about the dfs.
        """
        data = {
            'data': [self.old_name, self.new_name],
            'size (KB)': [self.old_size, self.new_size],
            }
        info = pd.DataFrame(data)
        return info


    def summary(self) -> pd.DataFrame:
        """
        Summary of differences between dfs.
        """

        details = self.details()
        cols_remove = [
            'all cols added',
            'all cols removed',
            'all rows added',
            'all rows removed',
            ]
        cols = [
            col for col
            in details.columns
            if col not in cols_remove
            ]
        summary = details[cols]
        # summary = summary.style.set_properties(**{
        #     'text-align': 'left',
        #     'white-space': 'normal',
        #     })  #type:ignore

        return summary


    def details(self) -> pd.DataFrame:
        """
        Detailed information about differences between dfs.
        """

        names = [name for name in self.diffs.keys()]
        uids = [d.uid for d in self.diffs.values()]
        in_both = []
        for d in self.diffs.values():
            if d.old.empty and d.new.empty:
                in_both.append('not in old or new')
            elif d.old.empty:
                in_both.append('not in old')
            elif d.new.empty:
                in_both.append('not in new')
            else:
                in_both.append('yes')

        all_cols_shared = [d.cols_shared for d in self.diffs.values()]
        all_cols_added = [d.cols_added for d in self.diffs.values()]
        all_cols_removed = [d.cols_removed for d in self.diffs.values()]

        all_rows_shared = [d.rows_shared for d in self.diffs.values()]
        all_rows_added = [d.rows_added for d in self.diffs.values()]
        all_rows_removed = [d.rows_removed for d in self.diffs.values()]

        cols_added_str = [list_to_str(x) for x in all_cols_added]
        cols_removed_str = [list_to_str(x) for x in all_cols_removed]

        rows_added_str = [list_to_str(x) for x in all_rows_added]
        rows_removed_str = [list_to_str(x) for x in all_rows_removed]

        cols_shared = [len(x) for x in all_cols_shared]
        cols_added = [len(x) for x in all_cols_added]
        cols_removed = [len(x) for x in all_cols_removed]

        rows_shared = [len(x) for x in all_rows_shared]
        rows_added = [len(x) for x in all_rows_added]
        rows_removed = [len(x) for x in all_rows_removed]

        vals_added = [d.vals_added for d in self.diffs.values()]
        vals_removed = [d.vals_removed for d in self.diffs.values()]
        vals_changed = [d.vals_changed for d in self.diffs.values()]

        data = {
            'data': names,
            'uid': uids,
            'in both dfs': in_both,
            'cols shared': cols_shared,
            'cols added': cols_added,
            'cols removed': cols_removed,
            'rows shared': rows_shared,
            'rows added': rows_added,
            'rows removed': rows_removed,
            'vals added': vals_added,
            'vals removed': vals_removed,
            'vals changed': vals_changed,
            'all cols added': cols_added_str,
            'all cols removed': cols_removed_str,
            'all rows added': rows_added_str,
            'all rows removed': rows_removed_str,
            }
        details = (
            pd.DataFrame(data)
            .convert_dtypes()
            .astype('string')
            .fillna('')
            .replace('0', '')
            .replace('[]', '')
            .replace(r'{}', '')
            )
        # details = details.style.set_properties(**{
        #     'text-align': 'left',
        #     'white-space': 'normal',
        #     })  #type:ignore

        return details


    def to_excel(
            self,
            path,
            index=False,
            apply_format=True,
            freeze_panes='C2',
            hide_info=True,
            hide_details=True,
            hide_summary=False,
            ):
        """
        Export diff results to an Excel file with formatting.

        Creates an Excel file containing diff metadata and individual
        sheets for each comparison with highlighted differences. Applies
        Excel-specific formatting and hides columns with old values.


        Parameters
        ----------
        path : str
            File path for the output Excel file
        index : bool, default False
            Whether to include row indices in the Excel output
        apply_format : bool, default True
            Whether to apply formatting to the Excel file
        freeze_panes : str, default 'C2'
            Cell reference for freezing panes in the Excel file
        hide_info : bool, default True
            Whether to hide the info sheet in the Excel file
        hide_details : bool, default True
            Whether to hide the details sheet in the Excel file
        hide_summary : bool, default False
            Whether to hide the summary sheet in the Excel file
        """

        msg = f'DEBUG: saving differences to "{path}"'
        context = 'dk.diffing.Diffs.to_excel'
        log(msg, context, self.verbosity)

        with pd.ExcelWriter(path) as writer:

            info = self.info()
            summary = self.summary()
            details = self.details()

            sheets = self.diffs.keys()
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
                index=False,
                )
            log('DEBUG: info sheet saved', context, self.verbosity)

            summary.to_excel(
                writer,
                sheet_name=sheet_summary,
                index=False,
                )
            log('DEBUG: summary sheet saved', context, self.verbosity)

            details.to_excel(
                writer,
                sheet_name=sheet_details,
                index=False,
                )
            log('DEBUG: details sheet saved', context, self.verbosity)

            #diff sheets
            for sheet, diff in self.diffs.items():
                diff.result.to_excel(
                    writer,
                    sheet_name=sheet,
                    index=index,
                    )
                msg = f'DEBUG: diff sheet saved: "{sheet}"'
                log(msg, context, self.verbosity)


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
            msg = 'DEBUG: info, summary, details sheets formatted'
            log(msg, context, self.verbosity)

            #diff sheets
            for sheet, diff in self.diffs.items():
                if diff._metadata_col_mapping:
                    cols_hide = list(diff._metadata_col_mapping.values())
                else:
                    cols_hide = None
                format(
                    path,
                    sheet=diff.name,
                    hide_cols=cols_hide,
                    freeze_panes=freeze_panes,
                    openpyxl_workbook=wb,
                    )
                msg = f'DEBUG: diff sheet formatted: "{diff.name}"'
                log(msg, context, self.verbosity)

        log(f'INFO: differences saved to "{path}"', context, self.verbosity)


    def print(self):
        print(self.__str__())
        return self

    def __str__(self):
        string = 'Diff objects:'
        for diff in self.diffs.values():
            string += '\n  ' + str(diff).replace('\n', '\n  ')
        return string

    def __repr__(self) -> str:
        return self.__str__()

    def __iter__(self):
        for diff in self.diffs.values():
            yield diff




def _get_data(
        old: str,
        new: str,
        remove_sheets: list[str] | str = None,
        name='data',
        verbosity=3,
        ):

    both_csv = (
        isinstance(old, str)
        and isinstance(new, str)
        and old.endswith('.csv')
        and new.endswith('.csv')
        )
    both_xlsx = (
        isinstance(old, str)
        and isinstance(new, str)
        and old.endswith('.xlsx')
        and new.endswith('.xlsx')
        )

    if both_csv:
        data_old = {name: pd.read_csv(old)}
        data_new = {name: pd.read_csv(new)}

    elif both_xlsx:
        data_old, data_new = _read_excel(
            old,
            new,
            remove_sheets,
            verbosity,
            )

    else:
        msg = (
            'ERROR: old and new must be 2 dfs,'
            ' 2 csv files or 2 excel files.'
            )
        log(msg, 'dk.diffing._get_data', verbosity)
        raise ValueError(msg)

    return data_old, data_new



def _read_excel(
        old: str,
        new: str,
        remove_sheets: list[str] | str = None,
        verbosity=3,
        ) -> tuple[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:

    data_old = {}
    data_new = {}
    sheets_old = pd.ExcelFile(old).sheet_names
    sheets_new = pd.ExcelFile(new).sheet_names
    sheets_all = pd.Index(sheets_new).union(pd.Index(sheets_old), sort=False)
    sheets_ignore = _arg_to_list(remove_sheets)

    for sheet in sheets_all:
        if sheet in sheets_ignore:
            msg = f'TRACE: removing sheet {sheet!r} before diffing'
            log(msg, 'dk.diffing._read_excel', verbosity)
            continue
        if sheet in sheets_old:
            data_old[sheet] = pd.read_excel(old, sheet_name=sheet)
        if sheet in sheets_new:
            data_new[sheet] = pd.read_excel(new, sheet_name=sheet)

    return data_old, data_new




def _get_diffs(
        old: dict[str, pd.DataFrame],
        new: dict[str, pd.DataFrame],
        uid=None,
        mode='mix',
        rename_cols: dict = None,
        remove_cols: list | str = None,
        remove_cols_by_suffix='',
        retain_cols: list | str = None,
        ignore_cols: list | str = None,
        linebreak='<br>',
        suffix_old=' *old',
        verbosity=3,
        ) -> dict[str, Diff]:

    diffs = {}
    sheets_all = pd.Index(new.keys()).union(pd.Index(old.keys()), sort=False)

    for sheet in sheets_all:

        if sheet in new and sheet in old:
            d = _get_single_diff(
                old=old[sheet],
                new=new[sheet],
                uid=uid,
                mode=mode,
                rename_cols=rename_cols,
                retain_cols=retain_cols,
                remove_cols=remove_cols,
                remove_cols_by_suffix=remove_cols_by_suffix,
                ignore_cols=ignore_cols,
                name=sheet,
                linebreak=linebreak,
                suffix_old=suffix_old,
                verbosity=verbosity,
                )

        elif sheet in new:
            d = _get_single_diff(
                old=pd.DataFrame(),
                new=new[sheet],
                uid=uid,
                mode=mode,
                rename_cols=rename_cols,
                retain_cols=retain_cols,
                remove_cols=remove_cols,
                remove_cols_by_suffix=remove_cols_by_suffix,
                ignore_cols=ignore_cols,
                name=sheet,
                linebreak=linebreak,
                suffix_old=suffix_old,
                verbosity=verbosity,
                )

        elif sheet in old:
            d = _get_single_diff(
                old=old[sheet],
                new=pd.DataFrame(),
                uid=uid,
                mode=mode,
                rename_cols=rename_cols,
                retain_cols=retain_cols,
                remove_cols=remove_cols,
                remove_cols_by_suffix=remove_cols_by_suffix,
                ignore_cols=ignore_cols,
                name=sheet,
                linebreak=linebreak,
                suffix_old=suffix_old,
                verbosity=verbosity,
                )

        diffs[sheet] = d


    return diffs



def _get_single_diff(
        old: pd.DataFrame,
        new: pd.DataFrame,
        uid=None,
        mode='mix',
        rename_cols: dict = None,
        remove_cols: list | str = None,
        remove_cols_by_suffix='',
        retain_cols: list | str = None,
        ignore_cols: list | str = None,
        name='data',
        linebreak='<br>',
        suffix_old=' *old',
        verbosity=3,
        ) -> Diff:

    if mode not in ('mix', 'old', 'new', 'new+'):
        msg = f'ERROR: unknown mode "{mode}"'
        log(msg, 'dk.diffing._get_single_diff', verbosity)
        raise ValueError(f'Unknown mode "{mode}"')

    d = Diff(
        old=old,
        new=new,
        mode=mode,
        name=name,
        linebreak=linebreak,
        suffix_old=suffix_old,
        verbosity=verbosity,
        )

    if d.old.empty or d.new.empty:
        d = _handle_edgecases(d)
        return d

    d = _process_dfs(d)
    d = _rename_cols(d, rename_cols)
    d = _remove_cols(d, _arg_to_list(remove_cols))
    d = _remove_cols_by_suffix(d, remove_cols_by_suffix)
    d = _set_uid(d, uid)

    #_retain_cols() must be after _set_uid()
    #for correct row alignment when readding later
    d = _retain_cols(d, _arg_to_list(retain_cols))
    d = _ignore_cols(d, _arg_to_list(ignore_cols))

    d = _get_row_col_diffs(d)
    d = _align_dtypes(d)

    if mode == 'mix':
        d = _get_templates_mix(d)
    elif mode == 'old':
        d = _get_templates_old(d)
    elif mode in ('new', 'new+'):
        d = _get_templates_new(d)

    d = _get_val_diffs(d)

    if mode == 'new+':
        d = _process_metadata_cols(d)

    d = _apply_style(d)

    return d




class Diff:
    """
    Stores differences between 2 dfs.
    For more detailed documentation see diff().
    """

    def __init__(
            self,
            old: pd.DataFrame,
            new: pd.DataFrame,
            uid=None,
            mode='mix',
            name='data',
            linebreak='<br>',
            suffix_old=' *old',
            verbosity=3,
            ):

        self.old = old
        self.new = new
        self.uid = uid
        self.mode = mode
        self.name = name
        self.verbosity = verbosity

        self._linebreak = linebreak
        self._suffix_old = suffix_old
        self._df_retained = pd.DataFrame()
        self._cols_ignore: list = []
        self._col_summary = ''
        self._metadata_col_mapping = {}
        self._mask_added: pd.DataFrame
        self._mask_removed: pd.DataFrame
        self._mask_changed: pd.DataFrame

        self.cols_shared: pd.Index = pd.Index([], dtype='string')
        self.cols_added: pd.Index = pd.Index([], dtype='string')
        self.cols_removed: pd.Index = pd.Index([], dtype='string')

        self.rows_shared: pd.Index = pd.Index([], dtype='string')
        self.rows_added: pd.Index = pd.Index([], dtype='string')
        self.rows_removed: pd.Index = pd.Index([], dtype='string')

        self.vals_added: int | None = None
        self.vals_removed: int | None = None
        self.vals_changed: int | None = None

        self._values = pd.DataFrame()
        self._style = pd.DataFrame()
        self.result = pd.DataFrame().style



    def __str__(self):

        txt = (
            f'----------------Diff object [d]----------------\n'
            f'name: {self.name!r}\n'
            f'mode: {self.mode!r}\n'
            )
        if self.old.empty and self.new.empty:
            txt += 'both dfs are empty\n'
        elif self.old.empty:
            txt += 'old df is empty\n'
        elif self.new.empty:
            txt += 'new df is empty\n'
        elif self.old.equals(self.new):
            txt += 'dfs are identical\n'
        else:
            txt += (
                f'cols shared: {len(self.cols_shared)}\n'
                f'cols added: {len(self.cols_added)}\n'
                f'cols removed: {len(self.cols_removed)}\n'
                f'rows shared: {len(self.rows_shared)}\n'
                f'rows added: {len(self.rows_added)}\n'
                f'rows removed: {len(self.rows_removed)}\n'
                f'vals added: {self.vals_added}\n'
                f'vals removed: {self.vals_removed}\n'
                f'vals changed: {self.vals_changed}\n'
                )
        txt += (
            '>>>d.result\n'
            '>>>d.summary\n'
            '>>>d.details\n'
            )
        txt += '----------------Diff object end----------------\n'

        return txt


    def __repr__(self) -> str:
        return self.__str__()




def _handle_edgecases(d: Diff) -> Diff:
    """
    Handle edge cases where one or both dfs are empty.
    """

    if d.old.empty and d.new.empty:
        values = pd.DataFrame({'diff': ['empty dfs']})
        style = pd.DataFrame(
            f'background-color: {GREY_LIGHT}',
            index=values.index,
            columns=values.columns,
            )

    elif d.old.empty:
        values = d.new.copy()
        col_diff = ensure_unique_string('diff', values.columns)
        values.insert(0, col_diff, 'df added')
        style = pd.DataFrame(
            f'background-color: {GREEN}',
            index=values.index,
            columns=values.columns,
            )

    elif d.new.empty:
        values = d.old.copy()
        col_diff = ensure_unique_string('diff', values.columns)
        values.insert(0, col_diff, 'df removed')
        style = pd.DataFrame(
            f'background-color: {RED}',
            index=values.index,
            columns=values.columns,
            )

    result = values.style.apply(lambda x: style, axis=None)
    result = result.set_properties(white_space='normal')
    d.result = result
    d._values = values
    d._style = style

    return d



def _process_dfs(d: Diff) -> Diff:
    d.old = d.old.convert_dtypes()
    d.new = d.new.convert_dtypes()
    return d



def _rename_cols(d: Diff, cols_mapping: dict | None) -> Diff:

    if cols_mapping is None:
        return d

    cols_mapping_old = {
        k: v
        for k, v
        in cols_mapping.items()
        if k in d.old.columns
        }

    cols_mapping_new = {
        k: v
        for k, v
        in cols_mapping.items()
        if k in d.new.columns
        }

    d.old = d.old.rename(columns=cols_mapping_old)
    d.new = d.new.rename(columns=cols_mapping_new)

    return d



def _remove_cols(d: Diff, cols: list) -> Diff:

    if not cols:
        return d

    cols_remove_old = (
        d.old.columns.
        intersection(cols)
        .to_list()
        )
    cols_remove_new = (
        d.new.columns
        .intersection(cols)
        .to_list()
        )

    d.old = d.old.drop(columns=cols_remove_old)
    d.new = d.new.drop(columns=cols_remove_new)

    return d



def _remove_cols_by_suffix(d: Diff, suffix: str) -> Diff:
    """
    Remove cols from both dfs ending with
    a specific suffix before diffing.
    """

    if not suffix:
        return d

    cols_remove_old = [
        col
        for col
        in d.old.columns
        if str(col).endswith(suffix)
        ]
    d.old = d.old.drop(columns=cols_remove_old)

    cols_remove_new = [
        col
        for col
        in d.new.columns
        if str(col).endswith(suffix)
        ]
    d.new = d.new.drop(columns=cols_remove_new)

    return d



def _set_uid(d: Diff, uid: typing.Any) -> Diff:
    """
    set unique identifier (uid) column for
    comparing rows between old and new dfs.
    """

    if uid is False:
        msg = 'TRACE: using index as uid'
        log(msg, 'dk.diffing._set_uid', d.verbosity)
        cols_all = d.old.columns.union(d.new.columns)
        uid = ensure_unique_string('index', cols_all)
        d.uid = '<index>'

    elif uid is None:
        msg = 'TRACE: searching for suitable uid column'
        log(msg, 'dk.diffing._set_uid', d.verbosity)
        uid = _find_uid(
            d.old,
            d.new,
            d.name,
            d.verbosity,
            )
        d.uid = uid
        d.old.index = d.old[uid]
        d.new.index = d.new[uid]
        d.old.drop(columns=uid, inplace=True)
        d.new.drop(columns=uid, inplace=True)

    elif uid in d.old.columns and uid in d.new.columns:
        d.uid = uid
        d.old.index = d.old[uid]
        d.new.index = d.new[uid]
        d.old.drop(columns=uid, inplace=True)
        d.new.drop(columns=uid, inplace=True)

    else:
        raise ValueError(f"UID column {uid!r} not found in both dataframes.")


    if not d.old.index.is_unique:
        d.old.index = deduplicate(
            d.old.index,
            name=f'{uid} in old df',
            verbosity=d.verbosity,
            )
        d.new.index = d.new.index.astype(str)

    if not d.new.index.is_unique:
        d.new.index = deduplicate(
            d.new.index,
            name=f'{uid} in new df',
            verbosity=d.verbosity,
            )
        d.old.index = d.old.index.astype(str)

    d.old.insert(0, uid, d.old.index)
    d.new.insert(0, uid, d.new.index)
    d._cols_ignore.append(uid)

    return d



def _find_uid(
        old: pd.DataFrame,
        new: pd.DataFrame,
        name='data',
        verbosity=3,
        ) -> typing.Any:

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
        msg = f'DEBUG: found uid {uid!r} for {name!r}'
        log(msg, 'dukit.diffing._find_uid', verbosity)
    else:
        uid = ''
        msg = f'DEBUG: no uid found. using index for {name!r}'
        log(msg, 'dukit.diffing._find_uid', verbosity)

    return uid



def _retain_cols(d: Diff, cols: list) -> Diff:
    """
    Remove cols from both dfs before diffing,
    then readd the ones from the old df to
    the diff result later.
    """

    if not cols:
        return d

    cols_retain_old = d.old.columns.intersection(cols)
    cols_retain_new = d.new.columns.intersection(cols)

    df_retained = d.old[cols_retain_old].copy()

    d.old = d.old.drop(columns=cols_retain_old)
    d.new = d.new.drop(columns=cols_retain_new)
    d._df_retained = df_retained

    return d



def _ignore_cols(d: Diff, cols: list) -> Diff:
    """
    Ignore columns for diffing,
    but keep them in both dfs.
    """

    if not cols:
        return d

    d._cols_ignore = (
        d.old.columns
        .union(d.new.columns)
        .intersection(cols)
        .to_list()
        )

    return d


def _get_row_col_diffs(d: Diff) -> Diff:

    d.cols_shared = (
        d.new.columns
        .intersection(d.old.columns)
        .difference(d._cols_ignore)
        )
    d.cols_added = (
        d.new.columns
        .difference(d.old.columns)
        .difference(d._cols_ignore)
        )
    d.cols_removed = (
        d.old.columns
        .difference(d.new.columns)
        .difference(d._cols_ignore)
        )

    d.rows_shared = (
        d.new.index
        .intersection(d.old.index)
        )
    d.rows_added = (
        d.new.index
        .difference(d.old.index)
        )
    d.rows_removed = (
        d.old.index
        .difference(d.new.index)
        )

    return d



def _align_dtypes(d: Diff) -> Diff:
    """
    covers dtypes resulting from df.convert_dtypes():
        - string
        - boolean
        - Int64
        - Float64
        - datetime64
    """

    for col in d.cols_shared:
        dtype_old = str(d.old[col].dtype)
        dtype_new = str(d.new[col].dtype)

        if dtype_old == dtype_new:
            continue

        elif dtype_old.startswith('Int') and dtype_new.startswith('Float'):
            d.old[col] = d.old[col].astype('Float64')

        elif dtype_new.startswith('Int') and dtype_old.startswith('Float'):
            d.new[col] = d.new[col].astype('Float64')

        else:
            d.old[col] = d.old[col].astype('object')
            d.new[col] = d.new[col].astype('object')

    return d



def _get_templates_mix(d: Diff) -> Diff:

    rows_old_only = d.old.index.difference(d.new.index)
    cols_old_only = d.old.columns.difference(d.new.columns)

    values = pd.concat([d.new, d.old.loc[:, cols_old_only]], axis=1)
    values.loc[rows_old_only, :] = d.old.loc[rows_old_only, :]

    style = pd.DataFrame(
        '',
        index=values.index,
        columns=values.columns,
        )

    style.loc[:, d.cols_added] = f'background-color: {GREEN}'
    style.loc[:, d.cols_removed] = f'background-color: {RED}'
    style.loc[d.rows_added, :] = f'background-color: {GREEN}'
    style.loc[d.rows_removed, :] = f'background-color: {RED}'

    if not d._df_retained.empty:
        values = _add_df_retained(values, d._df_retained)

    colname = ensure_unique_string('diff', values.columns)
    col_diff = pd.Series(
        '',
        index=values.index,
        dtype='string',
        )
    col_diff[d.rows_added] += 'row added'
    col_diff[d.rows_removed] += 'row removed'
    values.insert(0, colname, col_diff)

    d._col_summary = colname
    d._values = values
    d._style = style

    return d



def _get_templates_old(d: Diff) -> Diff:

    values = d.old.copy()
    style = pd.DataFrame(
        '',
        index=values.index,
        columns=values.columns,
        )

    style.loc[:, d.cols_removed] = f'background-color: {RED}'
    style.loc[d.rows_removed, :] = f'background-color: {RED}'

    if not d._df_retained.empty:
        values = _add_df_retained(values, d._df_retained)

    colname = ensure_unique_string('diff', values.columns)
    col_diff = pd.Series(
        '',
        index=values.index,
        dtype='string',
        )
    col_diff[d.rows_removed] += 'row removed'
    values.insert(0, colname, col_diff)

    d._col_summary = colname
    d._values = values
    d._style = style

    return d



def _get_templates_new(d: Diff) -> Diff:

    values = d.new.copy()
    style = pd.DataFrame(
        '',
        index=values.index,
        columns=values.columns,
        dtype='string',
        )

    #add metadata columns
    if d.mode == 'new+':
        values, style, mapping = _add_cols_metadata(d, values, style)
        d._metadata_col_mapping = mapping

    style.loc[:, d.cols_added] = f'background-color: {GREEN}'
    style.loc[d.rows_added, :] = f'background-color: {GREEN}'

    if not d._df_retained.empty:
        values = _add_df_retained(values, d._df_retained)

    colname = ensure_unique_string('diff', values.columns)
    col_diff = pd.Series(
        '',
        index=values.index,
        dtype='string',
        )
    col_diff[d.rows_added] += 'row added'
    values.insert(0, colname, col_diff)

    d._col_summary = colname
    d._values = values
    d._style = style

    return d


def _add_df_retained(df, df_retained):
    idx_shared = df.index.intersection(df_retained.index)
    df_retained = df_retained.loc[idx_shared, :]
    df_new = pd.concat([df_retained, df], axis=1)
    return df_new



def _add_cols_metadata(
        d: Diff,
        values: pd.DataFrame,
        style: pd.DataFrame,
        ) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str]]:

    col_mapping = {}
    cols_reorder = []

    for col in values.columns:
        cols_reorder.append(col)
        if col != d.uid and col in d.cols_shared:
            colname_meta = ensure_unique_string(
                col + d._suffix_old,
                taken=values.columns,
                strategy=f'suffix={d._suffix_old}',
                )
            cols_reorder.append(colname_meta)
            col_mapping[col] = colname_meta

    df_meta = values.loc[:, col_mapping.keys()].copy()
    df_meta.loc[:, :] = pd.NA
    df_meta.rename(columns=col_mapping, inplace=True)

    data = {
        colname: ['font-style: italic'] * len(values.index)
        for colname in col_mapping.values()
        }
    df_meta_style = pd.DataFrame(
        data,
        index=values.index,
        dtype='string',
        )

    values = pd.concat(
        [values, df_meta],
        axis=1,
        )
    style = pd.concat(
        [style, df_meta_style],
        axis=1,
        )

    values = values[cols_reorder]
    style = style[cols_reorder]

    return values, style, col_mapping



def _get_val_diffs(d: Diff) -> Diff:

    old = d.old
    new = d.new
    values = d._values
    rows_shared = d.rows_shared
    cols_shared = d.cols_shared
    colname = d._col_summary
    linebreak = d._linebreak

    old_isna = old.loc[rows_shared, cols_shared].isna()
    new_isna = new.loc[rows_shared, cols_shared].isna()
    new_equals_old = (
        new.loc[rows_shared, cols_shared]
        == old.loc[rows_shared, cols_shared]
        )

    #these comparisons can result in dtype "boolean" instead of "bool"
    #"boolean" masks cannot be used to set values as str
    added = (old_isna & ~new_isna).astype(bool)
    removed = (new_isna & ~old_isna).astype(bool)
    changed = (~new_isna & ~old_isna & ~new_equals_old).astype(bool)

    blank = pd.DataFrame(
        '',
        index=rows_shared,
        columns=cols_shared,
        )

    add = (
        blank
        .copy()
        .mask(added, f'background-color: {GREEN_LIGHT};')
        )
    remove = (
        blank
        .copy()
        .mask(removed, f'background-color: {RED_LIGHT};')
        )
    change = (
        blank
        .copy()
        .mask(changed, f'background-color: {ORANGE_LIGHT};')
        )

    d._style.loc[rows_shared, cols_shared] += add
    d._style.loc[rows_shared, cols_shared] += remove
    d._style.loc[rows_shared, cols_shared] += change


    #summarize changes in diff column
    sum_added = added.sum(axis=1)
    sum_removed = removed.sum(axis=1)
    sum_changed = changed.sum(axis=1)

    rows_added = sum_added[sum_added > 0].index
    rows_removed = sum_removed[sum_removed > 0].index
    rows_changed = sum_changed[sum_changed > 0].index

    removed_and_changed = rows_removed.intersection(rows_changed)
    removed_or_changed = rows_removed.union(rows_changed)
    removed_or_changed_and_added = removed_or_changed.intersection(rows_added)

    values.loc[rows_added, colname] += 'vals added: '
    values.loc[rows_added, colname] += sum_added[rows_added].astype('string')
    values.loc[removed_or_changed_and_added, colname] += linebreak

    values.loc[rows_removed, colname] += 'vals removed: '
    values.loc[rows_removed, colname] += sum_removed[rows_removed].astype('string')
    values.loc[removed_and_changed, colname] += linebreak

    values.loc[rows_changed, colname] += 'vals changed: '
    values.loc[rows_changed, colname] += sum_changed[rows_changed].astype('string')

    d._values = values
    d._mask_added = added
    d._mask_removed = removed
    d._mask_changed = changed
    d.vals_added = sum_added.sum()
    d.vals_removed = sum_removed.sum()
    d.vals_changed = sum_changed.sum()

    return d



def _process_metadata_cols(d: Diff) -> Diff:

    all_modifications = (
        d._mask_added
        | d._mask_removed
        | d._mask_changed
        )

    old_changed = (
        d.old
        .loc[d.rows_shared, d.cols_shared]
        #.convert_dtypes() results in only nullable dtypes
        .where(all_modifications, pd.NA)  #type:ignore
        )

    for col, col_meta in d._metadata_col_mapping.items():
        d._values[col_meta] = old_changed[col]

    return d



def _apply_style(d: Diff) -> Diff:

    context = 'dk.diffing._apply_style'
    if len(d._values.columns) * len(d._values.index) > 100_000:
        msg = (
            'warning: more than 100 000 cells are being formatted.'
            'while this might not cause performance issues for formatting,'
            'the result might be slow to render, especially in jupyter notebooks.'
            )
        log(msg, context, d.verbosity)

    d.result = (
        d._values
        .style
        .apply(lambda x: d._style, axis=None)
        .set_properties(white_space='normal')
        )
    msg = 'DEBUG: created df with highlighted differences'
    log(msg, context, d.verbosity)

    return d

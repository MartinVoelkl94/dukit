
import os
import typing
import pandas as pd

from .pandas import deduplicate
from .excel import format
from .typing import list_, str_
from .utils import (
    log,
    ensure_unique_string,
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
    compare two dfs or pairs of CSV or Excel files.

    Parameters
    ----------
    old, new : pandas.DataFrame or str
        data sources to compare. Both arguments must be dfs, CSV
        paths, or Excel paths.
    uid : str, False, or None, default None
        col used to identify corresponding rows. If ``None``, a suitable
        shared col is selected automatically. If ``False``, the index is
        used.
    mode : {'mix', 'old', 'new', 'new+'}, default 'mix'
        controls the values included in each result.
        - 'mix': show rows and cols from old and new df.
        additions and deletions are highlighted.
        - 'old': show only rows and cols from the old df.
        deletions are highlighted.
        - 'new': show only rows and cols from the new df.
        additions are highlighted.
        - 'new+': also preserve changed old values in parallel metadata cols.
    rename_cols : dict, optional
        mapping of original col names to names used during comparison.
    remove_cols : list or str, optional
        cols removed from both inputs before comparison.
    remove_cols_by_suffix : str, default ''
        remove cols whose names end with this suffix.
    retain_cols : list or str, optional
        keep only the cols from the old df.
    ignore_cols : list or str, optional
        cols excluded from comparison.
    remove_sheets : list or str, optional
        excel sheet names excluded before comparison.
    name : str, default 'data'
        name used for df comparisons and single-sheet files.
    linebreak : str, default '<br>'
        text inserted between multiple diff descriptions.
    suffix_old : str, default ' *old'
        suffix used for metadata cols containing old values in ``'new+'`` mode.
    verbosity : int, default 3
        logging verbosity level.

    Returns
    -------
    Diffs
        object containing one :class:`Diff` per compared sheet.

    Raises
    ------
    ValueError
        if the inputs, mode, or UID are invalid.

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
    same as diff(), but using defaults appropriate for
    when the old data is already a diff output.
    can be imagined as diffing the data
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
    stores differences between (multiple) dfs.
    for more detailed documentation see diff().
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
        get a specific Diff by sheetname or index.
        """
        if isinstance(key, str):
            item = self.diffs[key]
        else:
            item = list(self.diffs.values())[key]
        return item


    def show(self, sheet=0):
        """
        return a styled df with highlighted differences.

        Parameters
        ----------
        sheet : str or int, default 0
            sheet name or zero-based position.

        Returns
        -------
        pandas.io.formats.style.Styler
            styled result for the selected sheet.
        """
        diff = self[sheet]
        return diff.result


    def info(self):
        """
        return a df with basic information
        about the compared data sources.

        Returns
        -------
        pandas.DataFrame
            source names and sizes in kilobytes.
        """
        data = {
            'data': [self.old_name, self.new_name],
            'size (KB)': [self.old_size, self.new_size],
            }
        info = pd.DataFrame(data)
        return info


    def summary(self) -> pd.DataFrame:
        """
        return a df with a compact summary
        of differences for each data source.

        Returns
        -------
        pandas.DataFrame
            counts of changed cols, rows, and values.
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
        return a df with detailed information
        on differences for each data source.

        Returns
        -------
        pandas.DataFrame
            counts and lists of added, removed, and changed items.
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

        cols_added_str = [str_(x) for x in all_cols_added]
        cols_removed_str = [str_(x) for x in all_cols_removed]

        rows_added_str = [str_(x) for x in all_rows_added]
        rows_removed_str = [str_(x) for x in all_rows_removed]

        cols_shared = [len(x) for x in all_cols_shared]
        cols_added = [len(x) for x in all_cols_added]
        cols_removed = [len(x) for x in all_cols_removed]

        rows_shared = [len(x) for x in all_rows_shared]
        rows_added = [len(x) for x in all_rows_added]
        rows_removed = [len(x) for x in all_rows_removed]

        vals_added = [sum(d.vals_added) for d in self.diffs.values()]
        vals_removed = [sum(d.vals_removed) for d in self.diffs.values()]
        vals_changed = [sum(d.vals_changed) for d in self.diffs.values()]

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
        export diff results to an Excel file with formatting.

        creates an Excel file containing diff metadata and individual
        sheets for each comparison with highlighted differences. applies
        excel-specific formatting and hides cols with old values.


        Parameters
        ----------
        path : str or os.PathLike
            destination workbook path.
        index : bool, default False
            whether to include row indices
        apply_format : bool, default True
            whether to apply worksheet formatting
        freeze_panes : str, default 'C2'
            cell reference for freezing panes
        hide_info : bool, default True
            whether to hide the info sheet
        hide_details : bool, default True
            whether to hide the details sheet
        hide_summary : bool, default False
            whether to hide the summary sheet.

        Returns
        -------
        None
            the workbook is written to ``path``.
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
    sheets_ignore = list_(remove_sheets)

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
    d = _remove_cols(d, list_(remove_cols))
    d = _remove_cols_by_suffix(d, remove_cols_by_suffix)

    d = _set_uid(d, uid)
    d = _retain_cols(d, list_(retain_cols))  #depends on _set_uid()
    d = _ignore_cols(d, list_(ignore_cols))

    d = _create_working_values(d)
    d = _create_diff_col(d)
    d = _create_style(d)

    d = _get_row_col_diffs(d)
    d = _create_meta_cols(d)  #depends on _get_row_col_diffs()
    d = _align_dtypes(d)  #depends on _get_row_col_diffs()
    d = _get_val_diffs(d)  #depends on _get_row_col_diffs() and _align_dtypes()

    d = _populate_row_col_styles(d)  #depends on _get_row_col_diffs()
    d = _populate_val_styles(d)  #depends on _get_val_diffs()
    d = _populate_meta_cols(d)  #depends on _get_row_col_diffs() and _get_val_diffs()
    d = _populate_diff_col(d)  #depends on _get_row_col_diffs() and _get_val_diffs()

    d = _add_retained_cols(d)
    d = _add_diff_col(d)
    d = _add_uid_col(d)
    d = _apply_style(d)

    return d




class Diff:
    """
    store differences between two dfs.

    a ``Diff`` is normally created internally by :func:`diff` and contains
    comparison statistics, difference masks, and a styled result for one
    sheet.
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
        self.linebreak = linebreak
        self.suffix_old = suffix_old

        #determined by _get_row_col_diffs()
        self.cols_shared: pd.Index = pd.Index([], dtype='string')
        self.cols_added: pd.Index = pd.Index([], dtype='string')
        self.cols_removed: pd.Index = pd.Index([], dtype='string')
        self.rows_shared: pd.Index = pd.Index([], dtype='string')
        self.rows_added: pd.Index = pd.Index([], dtype='string')
        self.rows_removed: pd.Index = pd.Index([], dtype='string')

        #determined by _get_val_diffs()
        self.vals_added: pd.Series = pd.Series(dtype='int')
        self.vals_removed: pd.Series = pd.Series(dtype='int')
        self.vals_changed: pd.Series = pd.Series(dtype='int')

        #helper attributes for internal use
        self._df_retained: pd.DataFrame
        self._cols_ignore: list[str]
        self._metadata_col_mapping: dict[str, str]
        self._mask_added: pd.DataFrame
        self._mask_removed: pd.DataFrame
        self._mask_changed: pd.DataFrame
        self._diff_col: pd.Series
        self._values: pd.DataFrame
        self._style: pd.DataFrame
        self.result: pd.io.formats.style.Styler



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
                f'vals added: {sum(self.vals_added)}\n'
                f'vals removed: {sum(self.vals_removed)}\n'
                f'vals changed: {sum(self.vals_changed)}\n'
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
    handle comparisons where one or both dfs are empty.

    the result is marked as empty, added, or removed
    and receives the corresponding worksheet styling.
    """

    if d.old.empty and d.new.empty:
        values = pd.DataFrame({'diff': ['empty dfs']})
        style = pd.DataFrame(
            f'background-color: {GREY_LIGHT};',
            index=values.index,
            columns=values.columns,
            )

    elif d.old.empty:
        values = d.new.copy()
        col_diff = ensure_unique_string('diff', values.columns)
        values.insert(0, col_diff, 'df added')
        style = pd.DataFrame(
            f'background-color: {GREEN};',
            index=values.index,
            columns=values.columns,
            )

    elif d.new.empty:
        values = d.old.copy()
        col_diff = ensure_unique_string('diff', values.columns)
        values.insert(0, col_diff, 'df removed')
        style = pd.DataFrame(
            f'background-color: {RED};',
            index=values.index,
            columns=values.columns,
            )

    d.result = values.style.apply(lambda x: style, axis=None)
    d.result = d.result.set_properties(white_space='normal')
    d._values = values
    d._style = style

    d._df_retained = pd.DataFrame()
    d._cols_ignore = []
    d._metadata_col_mapping = {}
    d._mask_added = pd.DataFrame(dtype='bool')
    d._mask_removed = pd.DataFrame(dtype='bool')
    d._mask_changed = pd.DataFrame(dtype='bool')
    d._diff_col = pd.Series(dtype='string')

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
    remove cols ending with ``suffix`` before comparison.
    """

    if not suffix:
        return d

    cols_remove_old = [
        col
        for col
        in d.old.columns
        if str(col).endswith(suffix)
        ]
    cols_remove_new = [
        col
        for col
        in d.new.columns
        if str(col).endswith(suffix)
        ]

    d.old = d.old.drop(columns=cols_remove_old)
    d.new = d.new.drop(columns=cols_remove_new)

    return d



def _set_uid(d: Diff, uid: typing.Any) -> Diff:
    """
    set the row identifier used to compare the two dfs.

    duplicate identifiers are made unique with :func:`deduplicate`.
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
        d.old.index = d.old[uid]
        d.new.index = d.new[uid]
        d.old.drop(columns=uid, inplace=True)
        d.new.drop(columns=uid, inplace=True)
        d.uid = uid

    elif uid in d.old.columns and uid in d.new.columns:
        d.old.index = d.old[uid]
        d.new.index = d.new[uid]
        d.old.drop(columns=uid, inplace=True)
        d.new.drop(columns=uid, inplace=True)
        d.uid = uid

    else:
        raise ValueError(f"UID column {uid!r} not found in both dfs.")


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
    remove cols from both dfs before diffing,
    then readd the ones from the old df to
    the diff result later.
    """

    if not cols:
        d._df_retained = pd.DataFrame()
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
    keep selected cols while excluding them from comparison.
    """

    if not cols:
        d._cols_ignore = []
        return d

    d._cols_ignore = (
        d.old.columns
        .union(d.new.columns)
        .intersection(cols)
        .to_list()
        )

    return d



def _create_working_values(d: Diff) -> Diff:

    if d.mode == 'mix':
        rows_old_only = d.old.index.difference(d.new.index)
        cols_old_only = d.old.columns.difference(d.new.columns)
        d._values = pd.concat([d.new, d.old.loc[:, cols_old_only]], axis=1)
        d._values.loc[rows_old_only, :] = d.old.loc[rows_old_only, :]

    elif d.mode == 'old':
        d._values = d.old.copy()

    elif d.mode in ('new', 'new+'):
        d._values = d.new.copy()

    return d



def _create_diff_col(d: Diff) -> Diff:
    d._diff_col = pd.Series(
        '',
        index=d._values.index,
        dtype='string',
        )
    return d



def _create_style(d: Diff) -> Diff:
    d._style = pd.DataFrame(
        '',
        index=d._values.index,
        columns=d._values.columns,
        dtype='string',
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



def _create_meta_cols(d: Diff) -> Diff:

    if d.mode != 'new+':
        d._metadata_col_mapping = {}
        return d

    values = d._values
    style = d._style

    col_mapping = {}
    cols_reorder = []

    for col in values.columns:
        cols_reorder.append(col)
        if col != d.uid and col in d.cols_shared:
            colname_meta = ensure_unique_string(
                col + d.suffix_old,
                taken=values.columns,
                strategy=f'suffix={d.suffix_old}',
                )
            cols_reorder.append(colname_meta)
            col_mapping[col] = colname_meta

    df_meta = values.loc[:, col_mapping.keys()].copy()
    df_meta.loc[:, :] = pd.NA
    df_meta.rename(columns=col_mapping, inplace=True)

    data = {
        colname: ['font-style: italic;'] * len(values.index)
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

    d._metadata_col_mapping = col_mapping
    d._values = values[cols_reorder]
    d._style = style[cols_reorder]

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



def _get_val_diffs(d: Diff) -> Diff:

    old = d.old
    new = d.new
    rows_shared = d.rows_shared
    cols_shared = d.cols_shared

    old_isna = old.loc[rows_shared, cols_shared].isna()
    new_isna = new.loc[rows_shared, cols_shared].isna()
    new_equals_old = (
        new.loc[rows_shared, cols_shared]
        == old.loc[rows_shared, cols_shared]
        )

    d._mask_added = (old_isna & ~new_isna)
    d._mask_removed = (new_isna & ~old_isna)
    d._mask_changed = (~new_isna & ~old_isna & ~new_equals_old)

    d.vals_added = d._mask_added.sum()
    d.vals_removed = d._mask_removed.sum()
    d.vals_changed = d._mask_changed.sum()

    return d



def _populate_row_col_styles(d: Diff) -> Diff:

    if d.mode == 'mix':
        d._style.loc[:, d.cols_added] += f'background-color: {GREEN};'
        d._style.loc[d.rows_added, :] += f'background-color: {GREEN};'
        d._style.loc[:, d.cols_removed] += f'background-color: {RED};'
        d._style.loc[d.rows_removed, :] += f'background-color: {RED};'
        d._diff_col[d.rows_added] += 'row added'
        d._diff_col[d.rows_removed] += 'row removed'

    elif d.mode == 'old':
        d._style.loc[:, d.cols_removed] += f'background-color: {RED};'
        d._style.loc[d.rows_removed, :] += f'background-color: {RED};'
        d._diff_col[d.rows_removed] += 'row removed'

    elif d.mode in ('new', 'new+'):
        d._style.loc[:, d.cols_added] += f'background-color: {GREEN};'
        d._style.loc[d.rows_added, :] += f'background-color: {GREEN};'
        d._diff_col[d.rows_added] += 'row added'

    return d



def _populate_val_styles(d: Diff) -> Diff:

    blank = pd.DataFrame(
        '',
        index=d.rows_shared,
        columns=d.cols_shared,
        )

    add = (
        blank
        .copy()
        .mask(d._mask_added, f'background-color: {GREEN_LIGHT};')
        )
    remove = (
        blank
        .copy()
        .mask(d._mask_removed, f'background-color: {RED_LIGHT};')
        )
    change = (
        blank
        .copy()
        .mask(d._mask_changed, f'background-color: {ORANGE_LIGHT};')
        )

    d._style.loc[d.rows_shared, d.cols_shared] += add
    d._style.loc[d.rows_shared, d.cols_shared] += remove
    d._style.loc[d.rows_shared, d.cols_shared] += change

    return d



def _populate_diff_col(d: Diff) -> Diff:

    sum_added = d._mask_added.sum(axis=1)
    sum_removed = d._mask_removed.sum(axis=1)
    sum_changed = d._mask_changed.sum(axis=1)

    rows_added = sum_added[sum_added > 0].index
    rows_removed = sum_removed[sum_removed > 0].index
    rows_changed = sum_changed[sum_changed > 0].index

    removed_and_changed = rows_removed.intersection(rows_changed)
    removed_or_changed = rows_removed.union(rows_changed)
    removed_or_changed_and_added = removed_or_changed.intersection(rows_added)

    d._diff_col[rows_added] += 'vals added: '
    d._diff_col[rows_added] += sum_added[rows_added].astype('string')
    d._diff_col[removed_or_changed_and_added] += d.linebreak

    d._diff_col[rows_removed] += 'vals removed: '
    d._diff_col[rows_removed] += sum_removed[rows_removed].astype('string')
    d._diff_col[removed_and_changed] += d.linebreak

    d._diff_col[rows_changed] += 'vals changed: '
    d._diff_col[rows_changed] += sum_changed[rows_changed].astype('string')

    return d



def _populate_meta_cols(d: Diff) -> Diff:

    if d.mode != 'new+':
        return d

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



def _add_retained_cols(d: Diff) -> Diff:

    if d._df_retained.empty:
        return d

    idx_shared = d._values.index.intersection(d._df_retained.index)
    df_retained = d._df_retained.loc[idx_shared, :]
    d._values = pd.concat([df_retained, d._values], axis=1)

    return d



def _add_diff_col(d: Diff) -> Diff:
    colname = ensure_unique_string('diff', d._values.columns)
    d._diff_col.name = colname
    d._values = pd.concat([d._diff_col, d._values], axis=1)
    return d



def _add_uid_col(d: Diff) -> Diff:

    colname_uid = ensure_unique_string(str(d.uid), d._values.columns)
    uid_col = pd.Series(
        d._values.index,
        index=d._values.index,
        name=colname_uid,
        )
    d._values = pd.concat([uid_col, d._values], axis=1)

    index_diff = d._values.index.difference(d._style.index)
    if index_diff.empty:
        d._values.reset_index(drop=True, inplace=True)
        d._style.reset_index(drop=True, inplace=True)
    else:
        msg = (
            'ERROR: index of values and style dfs do not match.'
            'This should never happen. Please report this issue.'
            f'Index difference: {index_diff}'
            )
        log(msg, 'dk.diffing._add_uid_col', d.verbosity)

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

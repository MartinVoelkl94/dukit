import openpyxl
import pandas as pd
from .util import (
    log,
    _arg_to_list,
    )


def format_excel(
        path,
        sheet=None,
        freeze_panes='B2',
        hide_sheets=None,
        hide_cols=None,
        col_width_max=70,
        col_width_padding=2,
        align_vertical='top',
        align_horizontal='left',
        wrap_text=True,
        openpyxl_workbook=None,
        verbosity=3,
        ):  #pragma: no cover (does not affect reading of xlsx files)
    """
    applies formatting to an Excel file:
    - adjust col width to max length of cell content (accounts for linebreaks)
    - set cell alignment to top-left and wrap text
    - hide specified columns
    """

    if openpyxl_workbook:
        wb = openpyxl_workbook
    else:
        wb = openpyxl.load_workbook(path)
    if sheet:
        sheetnames = _arg_to_list(sheet)
    else:
        sheetnames = [sheetname for sheetname in wb.sheetnames]
    sheets_hide = _arg_to_list(hide_sheets)
    cols_hide = _arg_to_list(hide_cols)


    for sheetname in sheetnames:

        data = pd.read_excel(path, sheet_name=sheetname)
        sheet = wb[sheetname]

        if sheetname in sheets_hide:
            sheet.sheet_state = 'hidden'

        if freeze_panes:
            sheet.freeze_panes = freeze_panes

        #adjust column widths, cell alignment and text wrapping
        for col in sheet.columns:
            colname = col[0].value
            col_letter = col[0].column_letter  #type:ignore

            if colname is None:
                text = (
                    'warning: skipping column with'
                    f' no header in sheet "{sheet.title}"'
                    )
                log(text, 'du.format_excel()', verbosity)
                continue

            if colname in cols_hide:
                sheet.column_dimensions[col_letter].hidden = True  #type:ignore


            #multiline cells are split by newline,
            #expanded into new rows,
            #and the maximum length is calculated
            #these changes are not applied to the actual data,
            #only the column width is adjusted
            max_length = (
                data[colname]  #type:ignore
                .apply(str)
                .apply(lambda x: x.split('\n'))
                .explode()
                .str
                .len()
                .max()
                )
            max_length = max(max_length, len(str(colname)))
            max_length = min(max_length, col_width_max) + col_width_padding

            sheet.column_dimensions[col_letter].width = max_length

            for cell in col:
                cell.alignment = openpyxl.styles.Alignment(  #type:ignore
                    vertical=align_vertical,
                    horizontal=align_horizontal,
                    wrap_text=wrap_text
                    )

    wb.save(path)
    wb.close()

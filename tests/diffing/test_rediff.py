
import openpyxl
import pandas as pd
import dukit as dk

from dukit._test_utils import _get_dfs



def test_rediff(tmpdir):

    df_old, df_new = _get_dfs()
    df_old.insert(1, 'notes', ['note1', 'note2', 'note3'])
    df_new.insert(1, 'notes', ['note3', 'note4', 'note5'])
    df_new1 = df_new.copy()
    df_new1.loc['y', 'b'] = 0
    df_new1.loc['y', 'a'] = pd.NA
    df_new1.loc['z', 'a'] = 1

    path_df_old = f'{tmpdir}/df_old.xlsx'
    path_df_new = f'{tmpdir}/df_new.xlsx'
    path_df_new1 = f'{tmpdir}/df_new1.xlsx'
    path_diff1 = f'{tmpdir}/diff1.xlsx'
    path_diff2 = f'{tmpdir}/diff2.xlsx'
    df_old.to_excel(path_df_old, index=False)
    df_new.to_excel(path_df_new, index=False)
    df_new1.to_excel(path_df_new1, index=False)

    dk.diff(
        path_df_old,
        path_df_new,
        uid='uid',
        mode='new+',
        ignore_cols='notes',
        ).to_excel(path_diff1)

    dk.rediff(
        path_diff1,
        path_df_new1,
        uid='uid',
        ).to_excel(path_diff2)


    sheets = openpyxl.load_workbook(path_diff2, read_only=True).sheetnames
    info = pd.read_excel(path_diff2, sheet_name='info')
    details = pd.read_excel(path_diff2, sheet_name='details').fillna('')

    assert sheets == ['info', 'summary', 'details', 'Sheet1']
    assert str(info.loc[0, 'data']).split('/')[-1] == 'diff1.xlsx'
    assert str(info.loc[1, 'data']).split('/')[-1] == 'df_new1.xlsx'

    col_val_mapping_details = {
        'in both dfs': 'yes',
        'cols shared': 3,
        'cols added': '',
        'cols removed': '',
        'rows shared': 3,
        'rows added': '',
        'rows removed': '',
        'vals added': 1,
        'vals removed': 1,
        'vals changed': 1,
        'all cols added': '',
        'all cols removed': '',
        'all rows added': '',
        'all rows removed': '',
        }
    for col, val in col_val_mapping_details.items():
        result = details.loc[0, col]
        expected = val
        assert result == expected

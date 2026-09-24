
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import get_dfs



def _get_expected_flatten():

    expected = pd.DataFrame()

    expected['id'] = [
        10002,
        20001,
        30001,
        ]
    expected['medication#1'] = [
        'Aspirin',
        'Ibuprofen',
        'Amoxicillin',
        ]
    expected['medication#2'] = [
        pd.NA,
        'Paracetamol',
        'Ciprofloxacin',
        ]
    expected['medication#3'] = [
        pd.NA,
        pd.NA,
        'Metformin',
        ]
    expected['dose#1'] = [
        100,
        200,
        250,
        ]
    expected['dose#2'] = [
        pd.NA,
        pd.NA,
        500,
        ]
    expected['dose#3'] = [
        pd.NA,
        pd.NA,
        1000,
        ]
    expected['unit#1'] = [
        'mg',
        'mg',
        'mg',
        ]
    expected['unit#2'] = [
        pd.NA,
        '',
        'ml',
        ]
    expected['unit#3'] = [
        pd.NA,
        pd.NA,
        'mg',
        ]
    expected = expected.convert_dtypes()

    return expected



def test_collapse():

    expected = pd.DataFrame()

    expected['id'] = [
        10002,
        20001,
        30001,
        ]
    expected.loc[0, 'medication'] = 'Aspirin'
    expected.loc[1, 'medication'] = (
        '#1: Ibuprofen\n'
        '#2: Paracetamol\n'
        )
    expected.loc[2, 'medication'] = (
        '#1: Amoxicillin\n'
        '#2: Ciprofloxacin\n'
        '#3: Metformin\n'
        )

    expected['dose'] = pd.Series(dtype='object')
    expected.loc[0, 'dose'] = 100
    expected.loc[1, 'dose'] = (
        '#1: 200\n'
        '#2: <NA>\n'
        )
    expected.loc[2, 'dose'] = (
        '#1: 250\n'
        '#2: 500\n'
        '#3: 1000\n'
        )

    expected.loc[0, 'unit'] = 'mg'
    expected.loc[1, 'unit'] = (
        '#1: mg\n'
        '#2: \n'
        )
    expected.loc[2, 'unit'] = (
        '#1: mg\n'
        '#2: ml\n'
        '#3: mg\n'
        )

    expected = expected.convert_dtypes()

    df1, df2 = get_dfs()
    result = df2.dk.collapse(
        on='id',
        template_col='{colname}',
        template_item='#{counter}: {item}\n',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_collapse_formatted():

    expected = pd.DataFrame()

    expected['id'] = [
        10002,
        20001,
        30001,
        ]
    expected.loc[0, 'medication_collapsed'] = 'Aspirin'
    expected.loc[1, 'medication_collapsed'] = (
        '(item1: Ibuprofen)'
        '(item2: Paracetamol)'
        )
    expected.loc[2, 'medication_collapsed'] = (
        '(item1: Amoxicillin)'
        '(item2: Ciprofloxacin)'
        '(item3: Metformin)'
        )

    expected['dose_collapsed'] = pd.Series(dtype='object')
    expected.loc[0, 'dose_collapsed'] = 100
    expected.loc[1, 'dose_collapsed'] = (
        '(item1: 200)'
        '(item2: <NA>)'
        )
    expected.loc[2, 'dose_collapsed'] = (
        '(item1: 250)'
        '(item2: 500)'
        '(item3: 1000)'
        )

    expected.loc[0, 'unit_collapsed'] = 'mg'
    expected.loc[1, 'unit_collapsed'] = (
        '(item1: mg)'
        '(item2: )'
        )
    expected.loc[2, 'unit_collapsed'] = (
        '(item1: mg)'
        '(item2: ml)'
        '(item3: mg)'
        )

    expected = expected.convert_dtypes()

    df1, df2 = get_dfs()
    result = df2.dk.collapse(
        on='id',
        template_col='{colname}_collapsed',
        template_item='(item{counter}: {item})',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_embed():

    spacer = '\u00A0'
    spacer_x7 = spacer * 7  #non-breaking space
    expected = pd.DataFrame()

    expected['id'] = [
        10002,
        20001,
        30001,
        ]
    expected.loc[0, 'medication #1'] = (
        f'medication:{spacer}Aspirin\n'
        f'dose:{spacer_x7}100\n'
        f'unit:{spacer_x7}mg\n'
        )
    expected.loc[1, 'medication #1'] = (
        f'medication:{spacer}Ibuprofen\n'
        f'dose:{spacer_x7}200\n'
        f'unit:{spacer_x7}mg\n'
        )
    expected.loc[2, 'medication #1'] = (
        f'medication:{spacer}Amoxicillin\n'
        f'dose:{spacer_x7}250\n'
        f'unit:{spacer_x7}mg\n'
        )

    expected.loc[0, 'medication #2'] = pd.NA
    expected.loc[1, 'medication #2'] = (
        f'medication:{spacer}Paracetamol\n'
        f'dose:{spacer_x7}<NA>\n'
        f'unit:{spacer_x7}\n'
        )
    expected.loc[2, 'medication #2'] = (
        f'medication:{spacer}Ciprofloxacin\n'
        f'dose:{spacer_x7}500\n'
        f'unit:{spacer_x7}ml\n'
        )

    expected.loc[0, 'medication #3'] = pd.NA
    expected.loc[1, 'medication #3'] = pd.NA
    expected.loc[2, 'medication #3'] = (
        f'medication:{spacer}Metformin\n'
        f'dose:{spacer_x7}1000\n'
        f'unit:{spacer_x7}mg\n'
        )
    expected = expected.convert_dtypes()

    df1, df2 = get_dfs()
    result = df2.dk.embed(
        on='id',
        colname='medication',
        template='{colname} #{counter}',
        line_start='',
        separator=':',
        spacer='\u00A0',  #non-breaking space
        line_stop='\n',
        ).convert_dtypes()

    assert_frame_equal(result, expected)







def test_embed_formatted():

    spacer = '-'
    spacer_x7 = spacer * 7  #non-breaking space
    expected = pd.DataFrame()

    expected['id'] = [
        10002,
        20001,
        30001,
        ]
    expected.loc[0, 'medication #1'] = (
        f'col(medication){spacer}Aspirin | '
        f'col(dose){spacer_x7}100 | '
        f'col(unit){spacer_x7}mg | '
        )
    expected.loc[1, 'medication #1'] = (
        f'col(medication){spacer}Ibuprofen | '
        f'col(dose){spacer_x7}200 | '
        f'col(unit){spacer_x7}mg | '
        )
    expected.loc[2, 'medication #1'] = (
        f'col(medication){spacer}Amoxicillin | '
        f'col(dose){spacer_x7}250 | '
        f'col(unit){spacer_x7}mg | '
        )

    expected.loc[0, 'medication #2'] = pd.NA
    expected.loc[1, 'medication #2'] = (
        f'col(medication){spacer}Paracetamol | '
        f'col(dose){spacer_x7}<NA> | '
        f'col(unit){spacer_x7} | '
        )
    expected.loc[2, 'medication #2'] = (
        f'col(medication){spacer}Ciprofloxacin | '
        f'col(dose){spacer_x7}500 | '
        f'col(unit){spacer_x7}ml | '
        )

    expected.loc[0, 'medication #3'] = pd.NA
    expected.loc[1, 'medication #3'] = pd.NA
    expected.loc[2, 'medication #3'] = (
        f'col(medication){spacer}Metformin | '
        f'col(dose){spacer_x7}1000 | '
        f'col(unit){spacer_x7}mg | '
        )
    expected = expected.convert_dtypes()

    df1, df2 = get_dfs()
    result = df2.dk.embed(
        on='id',
        colname='medication',
        template='{colname} #{counter}',
        line_start='col(',
        separator=')',
        spacer='-',  #non-breaking space
        line_stop=' | ',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_flatten():

    df1, df2 = get_dfs()
    expected = _get_expected_flatten()

    result = df2.dk.flatten(
        on='id',
        template='{colname}#{counter}',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_flatten_template():

    df1, df2 = get_dfs()
    temp = _get_expected_flatten()
    expected = temp[['id']]

    for col in temp.columns:
        if col == 'id':
            continue
        counter = col.split('#')[1]
        colname = col.split('#')[0]
        expected[f'#{counter}_{colname}'] = temp[col]

    result = df2.dk.flatten(
        on='id',
        template='#{counter}_{colname}',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_stagger():

    df1, df2 = get_dfs()
    expected = _get_expected_flatten()
    expected['#1'] = ''
    expected['#2'] = ''
    expected['#3'] = ''
    cols_reordered = [
        'id',
        '#1',
        'medication#1',
        'dose#1',
        'unit#1',
        '#2',
        'medication#2',
        'dose#2',
        'unit#2',
        '#3',
        'medication#3',
        'dose#3',
        'unit#3',
        ]
    expected = expected[cols_reordered].convert_dtypes()

    result = df2.dk.stagger(
        on='id',
        template='{colname}#{counter}',
        separator_col='#{counter}',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_stagger_no_separator_col():

    df1, df2 = get_dfs()
    expected = _get_expected_flatten()
    cols_reordered = [
        'id',
        'medication#1',
        'dose#1',
        'unit#1',
        'medication#2',
        'dose#2',
        'unit#2',
        'medication#3',
        'dose#3',
        'unit#3',
        ]
    expected = expected[cols_reordered].convert_dtypes()

    result = df2.dk.stagger(
        on='id',
        template='{colname}#{counter}',
        separator_col=None,
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_stagger_separator_col():

    df1, df2 = get_dfs()
    expected = _get_expected_flatten()
    expected['staggered_col1:'] = ''
    expected['staggered_col2:'] = ''
    expected['staggered_col3:'] = ''
    cols_reordered = [
        'id',
        'staggered_col1:',
        'medication#1',
        'dose#1',
        'unit#1',
        'staggered_col2:',
        'medication#2',
        'dose#2',
        'unit#2',
        'staggered_col3:',
        'medication#3',
        'dose#3',
        'unit#3',
        ]
    expected = expected[cols_reordered].convert_dtypes()

    result = df2.dk.stagger(
        on='id',
        template='{colname}#{counter}',
        separator_col='staggered_col{counter}:',
        ).convert_dtypes()

    assert_frame_equal(result, expected)



def test_stagger_template():

    df1, df2 = get_dfs()
    temp = _get_expected_flatten()
    expected = temp[['id']]

    for col in temp.columns:
        if col == 'id':
            continue
        counter = col.split('#')[1]
        colname = col.split('#')[0]
        expected[f'#{counter}_{colname}'] = temp[col]

    expected['#1'] = ''
    expected['#2'] = ''
    expected['#3'] = ''
    cols_reordered = [
        'id',
        '#1',
        '#1_medication',
        '#1_dose',
        '#1_unit',
        '#2',
        '#2_medication',
        '#2_dose',
        '#2_unit',
        '#3',
        '#3_medication',
        '#3_dose',
        '#3_unit',
        ]
    expected = expected[cols_reordered].convert_dtypes()

    result = df2.dk.stagger(
        on='id',
        template='#{counter}_{colname}',
        separator_col='#{counter}',
        ).convert_dtypes()

    assert_frame_equal(result, expected)

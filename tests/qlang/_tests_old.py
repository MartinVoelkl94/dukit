

# def test_diff_mix():
#     result = get_df().q(r'$new=a   $diff=mix').data
#     result = result.reindex(sorted(result.columns), axis=1)
#     expected = get_df()
#     expected.insert(0, 'diff', '')
#     expected.insert(1, 'new', ['a'] * 11)
#     expected = expected.reindex(sorted(expected.columns), axis=1)
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_diff_new():
#     result = get_df().q(r'$new=1   $diff=new').data
#     expected = pd.DataFrame({
#         'diff': [''] * 11,
#         'new': ['1'] * 11,
#         })
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_diff_new_plus():
#     df = pd.DataFrame({
#         'a': [1, 2, 3],
#         })
#     result = df.q(r'$vals=b   $diff=new+').data
#     expected = pd.DataFrame({
#         'diff': ['vals changed: 1', 'vals changed: 1', 'vals changed: 1'],
#         'a': ['b', 'b', 'b'],
#         'old: a': [1, 2, 3],
#         })
#     expected['old: a'] = expected['old: a'].astype('object')
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_diff_old():
#     result = get_df().q(r'$new=1   $diff=old').data
#     expected = get_df()
#     expected.insert(0, 'diff', '')
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_diff_exists():
#     df = get_df()
#     df.insert(0, 'diff', 'test')
#     result = df.q(r'id  /=diff $diff=new').data
#     expected = df.loc[:, ['diff', 'ID']]
#     expected.insert(0, 'diff1', [''] * 11)
#     assert result.equals(expected), ql.diff(result, expected).str()



# def test_modify_rows_vals():

#     result = get_df().q(
#         r"""
#         name  $vals a
#         is any;  %%is any;
#         """
#         )
#     expected = get_df()
#     expected['name'] = 'a'
#     text = (
#         'failed test0: set values\nDIFF:\n'
#         + ql.diff(result, expected).str()
#         )
#     assert result.equals(expected), text


#     result = get_df().q(
#         r"""
#         name %%is any; $ =a
#         is any; %%is any;
#         """
#         )
#     expected = get_df()
#     expected['name'] = 'a'
#     text = (
#         'failed test1: set values\nDIFF:\n'
#         + ql.diff(result, expected).str()
#         )
#     assert result.equals(expected), text


#     result = get_df().q(
#         r"""
#         name  %%%is any; $ a
#         gender $rows b
#         is any; %%is any;
#         """
#         )
#     expected = get_df()
#     expected['name'] = 'a'
#     expected['gender'] = 'b'
#     text = (
#         'failed test2: set values in multiple cols\nDIFF:\n'
#         + ql.diff(result, expected).str()
#         )
#     assert result.equals(expected), text


#     result = df.q(
#         r"""
#         name  $rows=a   %%%is any;  $+=a
#         is any; %%is any;
#         """
#         )
#     expected = get_df()
#     expected['name'] = 'aa'
#     text = (
#         'failed test3: appending to values\nDIFF:\n'
#         + ql.diff(result, expected).str()
#         )
#     assert result.equals(expected), text


#     result = df.q(r'name  %%%?j  $=@ID  %is any;')
#     expected = get_df()
#     expected['name'] = [
#         10001,
#         10002,
#         10003,
#         'Bob Brown',
#         'eva white',
#         'Frank miller',
#         'Grace TAYLOR',
#         'Harry Clark',
#         'IVY GREEN',
#         30004,
#         30005,
#         ]
#     text = (
#         'failed test: replace values with column content\nDIFF:\n'
#         + ql.diff(result, expected).str()
#         )
#     assert result.equals(expected), text


#     result = df.q(r'name  %%%?j  $+=@ID  %is any;')
#     expected = get_df()
#     expected['name'] = [
#         'John Doe10001',
#         'Jane Smith10002',
#         'Alice Johnson10003',
#         'Bob Brown',
#         'eva white',
#         'Frank miller',
#         'Grace TAYLOR',
#         'Harry Clark',
#         'IVY GREEN',
#         'JAck Williams30004',
#         'john Doe30005',
#         ]
#     text = (
#         'failed test: add column content to selected values\nDIFF:\n'
#         + ql.diff(result, expected).str()
#         )
#     assert result.equals(expected), text


#     result = get_df().q(
#         r"""
#         $new=___ERROR  $cols=error code
#             %%%is any;  $vals+=@ID

#         %age  /gender
#             %%idx>5  &&idx<=8
#                 %%%is na;
#                     $vals+=@error code
#                     $bg=orange

#         is any;  %%is any;
#         """
#         ).data
#     expected = get_df()
#     expected['error code'] = [
#         '___ERROR10001',
#         '___ERROR10002',
#         '___ERROR10003',
#         '___ERROR20001',
#         '___ERROR20002',
#         '___ERROR20003',
#         '___ERROR30001',
#         '___ERROR30002',
#         '___ERROR30003',
#         '___ERROR30004',
#         '___ERROR30005',
#         ]
#     expected.loc[6, 'age'] = 'nan___ERROR30001'
#     expected.loc[8, 'age'] = '___ERROR30003'
#     expected.loc[7, 'gender'] = 'NaN___ERROR30002'
#     expected.loc[8, 'gender'] = 'None___ERROR30003'
#     assert result.equals(expected), ql.diff(result, expected).str()




# def test_previous_bugs():
#     try:
#         df = get_df()
#         df.q(
#             r"""
#             %age ///!is num;
#             is any;
#             $bg=orange
#             """
#             )
#     except Exception as e:
#         assert False, f'failed test0: check if previous bug is fixed: {e}'


#     #from v0.7.5
#     result = get_df().q(r'%%%>0    &&&<50  %trim;  $bg=orange').data
#     expected = get_df().loc[:, ['age', 'height', 'bp systole', 'dose']]
#     assert result.equals(expected), ql.diff(result, expected).str()


#     #from v0.8.0 prototype
#     #inverting a selection was applied to all selected values,
#     #not just those in the current row/col selection
#     ql.qlang.APPLY_STYLE = False
#     df = get_df()
#     result = df.q(
#         r"""
#         %%%?j
#         %name   %%%invert;
#         %date of birth
#         $vals=replaced
#         is any;
#         """
#         )
#     expected = df
#     expected.loc[8, 'date of birth'] = 'replaced'
#     assert result.equals(expected), ql.diff(result, expected).str()
#     ql.qlang.APPLY_STYLE = True






# df = get_df()
# params = [
#     #saving col selections

#     (
#         r'id           $save1              %is any;    %load1',
#         df.loc[:, ['ID']],
#         None
#     ),
#     (
#         r'id /name     $save1              %is any;    %load1',
#         df.loc[:, ['ID', 'name']],
#         None
#     ),
#     (
#         r'id           $save1              %name       /load1',
#         df.loc[:, ['ID', 'name']],
#         None
#     ),
#     (
#         r'id           $cols save = 1      %is any;    %load1',
#         df.loc[:, ['ID']],
#         None
#     ),
#     (
#         r'id           $cols save = 1      %name       $save1       %is any;    %load1',
#         df.loc[:, ['name']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),
#     (
#         r'id           $cols save = 1      %name       $cols save1  %is any;    %load1',
#         df.loc[:, ['name']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),
#     (
#         r'id           $cols save = 1      %name       $rows save1  %is any;    %load1',
#         df.loc[:, ['ID']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),



#     #saving row selections

#     (
#         r'id   %%?1          $save1      %%is any;    %%load1',
#         df.loc[[0, 1, 2, 3, 6], ['ID']],
#         None
#     ),
#     (
#         r'id   %%?1          $save=1     %%is any;    %%load=1',
#         df.loc[[0, 1, 2, 3, 6], ['ID']],
#         None
#     ),
#     (
#         r'id   %%any?1       $save1      %%is any;    %%load1',
#         df.loc[[0, 1, 2, 3, 6], ['ID']],
#         None
#     ),
#     (
#         r'id   %%all?1       $save1      %%is any;    %%load1',
#         df.loc[[0, 1, 2, 3, 6], ['ID']],
#         None
#     ),
#     (
#         r'id   %%?1          $save1      %is any;     %%is any;   %id        %%load1',
#         df.loc[[0, 1, 2, 3, 6], ['ID']],
#         None
#     ),
#     (
#         r'id   %%?2          $save1      %%?1         $save1      %%is any;  %%load1',
#         df.loc[[0, 1, 2, 3, 6], ['ID']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),
#     (
#         r'id   %%%?1         $save1      %%is any;    %%load1',
#         df.loc[:, ['ID']],
#         None
#     ),

#     (
#         r"""
#         id      %%?1    $save1
#         %name           $save1
#         %%is any;
#         %%load1
#         """,
#         df.loc[[0, 1, 2, 3, 6], ['name']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),

#     (
#         r"""
#         id      %%?1    $save1
#         %name   %%?j    $save1
#         %%is any;
#         %%load1
#         """,
#         df.loc[[0, 1, 2, 9, 10], ['name']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),

#     (
#         r"""
#         id      %%?1    $save1
#         %name   %%?j    $cols save1
#         %%is any;
#         %%load1
#         """,
#         df.loc[[0, 1, 2, 3, 6], ['name']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),

#     (
#         r"""
#         id      %%?1    $save1
#         %name   %%?j    $rows save=1
#         %%is any;
#         %load1  %%load1
#         """,
#         df.loc[[0, 1, 2, 9, 10], ['ID']],
#         'WARNING: a selection was already saved as "1". overwriting it'
#     ),


#     (
#         r"""
#         id   %%?1       $save1
#         id   %%?2       $save2
#         id   %%load1    &&load2
#         """,
#         df.loc[[1, 3], ['ID']],
#         None
#     ),

#     (
#         r"""
#         id   %%?1   $save1
#         id   %%?2   $save2
#         id   %%load1   //load2
#         """,
#         df.loc[[0, 1, 2, 3, 4, 5, 6, 7], ['ID']],
#         None
#     ),

#     (
#         r"""
#         id   %%!?1   $save1
#         id   %%?2   $save2
#         id   %%load1   &&load2
#         """,
#         df.loc[[4, 5, 7], ['ID']],
#         None
#     ),

#     (
#         r"""
#         id   %%!?1      $rows save = 1
#         id   %%!?2      $save2
#         id   %%load1    &&load2
#         """,
#         df.loc[[8, 9, 10], ['ID']],
#         None
#     ),
#     ]
# @pytest.mark.parametrize('code, expected, message', params)
# def test_save_load(code, expected, message):
#     result = get_df().q(code)
#     assert result.equals(expected), ql.diff(result, expected).str()
#     if message:  #pragma: no cover
#         check_message(message)






# params = [
#     (
#         'id            $sort;      %is any;',
#         'ID'
#     ),
#     (
#         'name          $sort;      %is any;',
#         'name'
#     ),
#     (
#         'id /name      $sort;      %is any;',
#         ['ID', 'name']
#     ),
#     (
#         'name /id      $sort;      %is any;',
#         ['ID', 'name']
#     ),
#     (
#         'id            $!sort;     %is any;',
#         'ID'
#     ),
#     (
#         'name          $!sort;     %is any;',
#         'name'
#     ),
#     (
#         'id /name      $!sort;     %is any;',
#         ['ID', 'name']
#     ),
#     (
#         'name /id      $!sort;     %is any;',
#         ['ID', 'name']
#     ),
#     ]
# @pytest.mark.parametrize('code, expected_cols', params)
# def test_sort(code, expected_cols):
#     result = get_df().q(code)
#     if '$!sort;' in code:
#         expected = get_df().sort_values(by=expected_cols, ascending=False)
#     else:
#         expected = get_df().sort_values(by=expected_cols)
#         text = 'failed test: sort values\nDIFF:\n' + ql.diff(result, expected).str()
#     assert result.equals(expected), text


# def test_style():
#     result = get_df().q(r'$color=red')
#     assert isinstance(result, pd.io.formats.style.Styler)

#     #updating the style
#     result = df.q(
#         r"""
#         $color=red
#         $new=a
#         $color=blue
#         """
#         )
#     isinstance(result, pd.io.formats.style.Styler)
#     expected = pd.DataFrame('a', index=df.index, columns=['new'])
#     text = (
#         'failed test: updating style\nDIFF:\n'
#         + ql.diff(result.data, expected).str()
#         )
#     assert result.data.equals(expected), text


# def test_symbols():
#     sym1 = ql.qlang.OPERATORS['=']
#     sym1a = ql.qlang.OPERATORS.SET
#     sym1b = ql.qlang.OPERATORS['SET']
#     sym2 = ql.qlang.OPERATORS.TRIM
#     assert sym1 == sym1a, f'symbol {sym1} should be equal to {sym1a}'
#     assert sym1 == sym1b, f'symbol {sym1} should be equal to {sym1b}'
#     assert sym1 != sym2, f'symbol {sym1} should not be equal to {sym2}'
#     assert sym1 < sym2, f'symbol {sym1} should be less than {sym2}'

#     details = (
#         'symbol:\n'
#         '\tname: SET\n'
#         '\tsymbol: =\n'
#         '\tdescription: set values\n'
#         '\ttraits:\n'
#         '\t\tselect\n'
#         '\t\tselect_vals\n'
#         '\t\tselect_rows\n'
#         '\t\tselect_cols\n'
#         '\t\tmodify\n'
#         '\t\tsettings\n'
#         '\t\tmetadata\n'
#         '\t'
#         )
#     assert sym1.details() == details, f'symbol {sym1} should have details:\n{details}'

#     symbols_modify1 = ql.qlang.OPERATORS.modify
#     symbols_modify2 = ql.qlang.OPERATORS['modify']
#     text = f'symbols {symbols_modify1} should be equal to {symbols_modify2}'
#     assert symbols_modify1 == symbols_modify2, text
#     assert sym1 in symbols_modify1, f'symbol {sym1} should be in modification symbols'

#     assert ql.qlang.OPERATORS['x'] is None, 'should return None for unknown symbol'
#     check_message('ERROR: symbol "x" not found in "OPERATORS"')

#     connectors = ql.qlang.CONNECTORS.__str__()
#     expected = (
#         'CONNECTORS:\n'
#         '\t<"%%%": NEW_SELECT_VALS>\n'
#         '\t<"&&&": AND_SELECT_VALS>\n'
#         '\t<"///": OR_SELECT_VALS>\n'
#         '\t<"%%": NEW_SELECT_ROWS>\n'
#         '\t<"&&": AND_SELECT_ROWS>\n'
#         '\t<"//": OR_SELECT_ROWS>\n'
#         '\t<"%": NEW_SELECT_COLS>\n'
#         '\t<"&": AND_SELECT_COLS>\n'
#         '\t<"/": OR_SELECT_COLS>\n'
#         '\t<"$": MODIFY>'
#         )
#     assert connectors == expected, f'CONNECTORS should be:\n{expected}'


# def test_tagging():

#     result = get_df_simple_tagged()
#     expected = get_df_simple_tagged()
#     expected['meta'] = ['', '', '\n@a: 1']
#     result = result.q(r'=a  %%>0   $tag1   %is any;  %%is any;')
#     assert result.equals(expected), ql.diff(result, expected).str()

#     expected['meta'] = ['', '', '\n@a: 1\n@a: 1']
#     result = result.q(r'=a   %%>0  $tag1   %is any;  %%is any;')
#     assert result.equals(expected), ql.diff(result, expected).str()

#     expected['meta'] = ['', '', '\n@a: 1\n@a: 1\n@a: 1']
#     result = result.q(r'=a   %%>0  $tag+=1   %is any;  %%is any;')
#     assert result.equals(expected), ql.diff(result, expected).str()

#     expected['meta'] = ['', '', '\n@a: 1']
#     result = result.q(r'=a   %%>0  $tag=1   %is any;  %%is any;')
#     assert result.equals(expected), ql.diff(result, expected).str()

#     #no inplace modification should take place
#     expected['meta'] = ['', '', '\n@a: 1']
#     result = get_df_simple_tagged()
#     result = result.q(r'=a  %%>0   $tag1   %is any;  %%is any;')
#     assert result.equals(expected), ql.diff(result, expected).str()

#     expected['meta'] = ['', '', '\n@a@b: 1']
#     result = get_df_simple_tagged()
#     result = result.q(r'a /b  %%all>0  $tag1  %is any;  %%is any;')
#     assert result.equals(expected), ql.diff(result, expected).str()



# def test_to_int():
#     result = get_df().q('age $to int;')
#     expected = get_df()
#     expected['age'] = [
#         -25,
#         30,
#         None,
#         None,
#         40,
#         None,
#         None,
#         None,
#         None,
#         None,
#         35,
#         ]
#     expected['age'] = expected['age'].astype('Int64')
#     expected = expected.loc[:, ['age']]
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_float():
#     result = get_df().q('=age  $ to float;')
#     expected = get_df()
#     expected['age'] = [
#         -25.0,
#         30.0,
#         None,
#         None,
#         40.0,
#         None,
#         None,
#         None,
#         None,
#         None,
#         35.0,
#         ]
#     expected['age'] = expected['age'].astype('Float64')
#     expected = expected.loc[:, ['age']]
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_num():
#     result = get_df().q('=age   $ to num;')
#     expected = get_df()
#     expected['age'] = [
#         -25,
#         30,
#         np.nan,
#         np.nan,
#         40,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         np.nan,
#         35,
#         ]
#     expected['age'] = expected['age'].astype('object')
#     expected = expected.loc[:, ['age']].astype('object')
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_str():
#     result = get_df().q('=age   $ to str;')
#     expected = get_df()
#     expected['age'] = [
#         '-25',
#         '30',
#         'nan',
#         'None',
#         '40.0',
#         'forty-five',
#         'nan',
#         'unk',
#         '',
#         'unknown',
#         '35',
#         ]
#     expected['age'] = expected['age'].astype(str)
#     expected = expected.loc[:, ['age']]
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_date():
#     result = get_df().q('date of birth   $to date;')
#     expected = get_df()
#     expected['date of birth'] = [
#         pd.to_datetime('1995-01-02', dayfirst=False).date(),
#         pd.to_datetime('1990/09/14', dayfirst=False).date(),
#         pd.to_datetime('1985.08.23', dayfirst=False).date(),
#         pd.to_datetime('19800406', dayfirst=False).date(),
#         pd.to_datetime('05-11-2007', dayfirst=True).date(),
#         pd.to_datetime('06-30-1983', dayfirst=False).date(),
#         pd.to_datetime('28-05-1975', dayfirst=True).date(),
#         pd.to_datetime('1960 Mar 08', dayfirst=False).date(),
#         pd.to_datetime('1955-Jan-09', dayfirst=False).date(),
#         pd.to_datetime('1950 Sep 10', dayfirst=False).date(),
#         pd.to_datetime('1945 October 11', dayfirst=False).date(),
#         ]
#     expected['date of birth'] = (
#         pd
#         .to_datetime(expected['date of birth'])
#         .astype('datetime64[ns]')
#         )
#     expected = expected.loc[:, ['date of birth']]
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_na():
#     result = get_df().q('=age   $to na;')
#     expected = get_df()
#     expected['age'] = [
#         -25,
#         '30',
#         None,
#         None,
#         '40.0',
#         'forty-five',
#         None,
#         'unk',
#         None,
#         'unknown',
#         35,
#         ]
#     expected['age'] = expected['age'].astype('object')
#     expected = expected.loc[:, ['age']]
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_nk():
#     result = get_df().q('=age   $to nk;')
#     expected = get_df()
#     expected['age'] = [
#         -25,
#         '30',
#         np.nan,
#         None,
#         '40.0',
#         'forty-five',
#         'nan',
#         'unknown',
#         '',
#         'unknown',
#         35,
#         ]
#     expected['age'] = expected['age'].astype('object')
#     expected = expected.loc[:, ['age']]
#     assert result.equals(expected), ql.diff(result, expected).str()


# def test_to_yn():
#     result = get_df().q('=diabetes   $ to yn;')
#     expected = get_df()
#     expected['diabetes'] = [
#         'no',
#         'yes',
#         None,
#         'no',
#         'yes',
#         'yes',
#         'no',
#         None,
#         None,
#         'no',
#         'yes',
#         ]
#     expected['age'] = expected['age'].astype('object')
#     expected = expected.loc[:, ['diabetes']]
#     assert result.equals(expected), ql.diff(result, expected).str()



# params = [
#     (
#         r'%%%is na;  %trim;',
#         df.loc[:, [
#             'age',
#             'gender',
#             'height',
#             'weight',
#             'bp systole',
#             'bp diastole',
#             'cholesterol',
#             'diabetes',
#             'dose',
#             ]]
#     ),
#     (
#         r'%%%is na;  %%trim;',
#         df.loc[[1, 2, 3, 4, 6, 7, 8, 9, 10], :]
#     ),
#     (
#         r'%%%is na;  %trim;  %%trim;',
#         df.loc[[1, 2, 3, 4, 6, 7, 8, 9, 10], [
#             'age',
#             'gender',
#             'height',
#             'weight',
#             'bp systole',
#             'bp diastole',
#             'cholesterol',
#             'diabetes',
#             'dose',
#             ]]
#     ),
#     (
#         r'%%%is na;  %!trim;',
#         df.loc[:, ['ID', 'name', 'date of birth']]
#     ),
#     (
#         r'%%%is na;  %is any;  %trim;',
#         df.loc[:, [
#             'age',
#             'gender',
#             'height',
#             'weight',
#             'bp systole',
#             'bp diastole',
#             'cholesterol',
#             'diabetes',
#             'dose',
#             ]]
#     ),
#     (
#         r'%%%is na;  %is any;  %!trim;',
#         df.loc[:, ['ID', 'name', 'date of birth']]
#     ),
#     ]
# @pytest.mark.parametrize('code, expected', params)
# def test_trim(code, expected):
#     temp = get_df().q(code)
#     result = get_df().loc[temp.index, temp.columns]
#     assert result.equals(expected), ql.diff(result, expected).str()



# def test_type_inference():
#     df1 = pd.DataFrame({1: [1, 2, 3], 'a': [4, 5, 6]})
#     df2 = pd.DataFrame({'1': [1, 2, 3], 'a': [4, 5, 6]})
#     result1 = df1.q('1')
#     result2 = df2.q('1')
#     expected1 = df1.loc[:, [1]]
#     expected2 = df2.loc[:, ['1']]
#     assert result1.equals(expected1), ql.diff(result1, expected1).str()
#     assert result2.equals(expected2), ql.diff(result2, expected2).str()

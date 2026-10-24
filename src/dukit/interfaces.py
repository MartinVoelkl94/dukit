
import datetime
import pandas as pd

from .excel import save
from .qlang import (
    q,
    qr,
    qs,
    )
from .pandas import (
    date_delta,
    date_table,
    collapse,
    embed,
    stack,
    unstack,
    transpose,
    split_col,
    )



@pd.api.extensions.register_dataframe_accessor('dk')
class DukitAccessor():

    def __init__(
            self,
            df: pd.DataFrame,
            ):
        self.df = df


    def q(
            self,
            code='',
            verbosity=3,
            ):
        return q(self.df, code, verbosity)


    def qs(
            self,
            code='',
            verbosity=3,
            ):
        return qs(self.df, code, verbosity)


    def qr(
            self,
            code='',
            verbosity=3,
            ):
        return qr(self.df, code, verbosity)


    def date_delta(
            self,
            reference_date: str | datetime.date | pd.Timestamp = None,
            reference_col: str = None,
            linebreak: str = '<br>',
            verbosity: int = 3,
            ):
        return date_delta(
            self.df,
            reference_date=reference_date,
            reference_col=reference_col,
            linebreak=linebreak,
            verbosity=verbosity,
            )


    def date_table(
            self,
            reference_col: str = None,
            uid: str = None,
            upper: int = None,
            lower: int = None,
            start_at_day1: bool = True,
            schedule: dict[int, str] = None,
            filler: str = '.',
            linebreak: str = '<br>',
            verbosity: int = 3,
            ):
        return date_table(
            df=self.df,
            reference_col=reference_col,
            uid=uid,
            upper=upper,
            lower=lower,
            start_at_day1=start_at_day1,
            schedule=schedule,
            filler=filler,
            linebreak=linebreak,
            verbosity=verbosity,
            )


    def collapse(
            self,
            on: str,
            template_col='{colname}',
            template_item='#{counter}: {item}\n',
            ):
        df_new = collapse(
            self.df,
            on=on,
            template_col=template_col,
            template_item=template_item,
            )
        return df_new


    def embed(
            self,
            on: str,
            colname='',
            template='{colname}_#{counter}',
            line_start='',
            separator=':',
            spacer='\u00A0',  #non-breaking space
            line_stop='\n',
            ):
        df_new = embed(
            self.df,
            on=on,
            colname=colname,
            template=template,
            line_start=line_start,
            separator=separator,
            spacer=spacer,
            line_stop=line_stop,
            )
        return df_new


    def stack(
            self,
            uid: str,
            col_pattern: str = r'(?P<col>.+)_(?P<subid>.+)',
            uid_template: str = '{uid}_{subid}',
            cols_keep: list[str] | None = None,
            dropna: bool = True,
            sort: bool = True,
            verbosity: int = 3,
            ) -> pd.DataFrame:
        df_new = stack(
            self.df,
            uid=uid,
            col_pattern=col_pattern,
            uid_template=uid_template,
            cols_keep=cols_keep,
            dropna=dropna,
            sort=sort,
            verbosity=verbosity,
            )
        return df_new


    def unstack(
            self,
            uid: str,
            uid_pattern: str = r'(?P<uid>.+)_(?P<subid>.+)',
            col_template: str = '{col}_{subid}',
            cols_keep: list[str] | None = None,
            stagger: bool = True,
            verbosity: int = 3,
            ) -> pd.DataFrame:
        df_new = unstack(
            self.df,
            uid=uid,
            uid_pattern=uid_pattern,
            col_template=col_template,
            cols_keep=cols_keep,
            stagger=stagger,
            verbosity=verbosity
            )
        return df_new


    def transpose(
            self,
            header='uid',
            ) -> pd.DataFrame:
        df_new = transpose(
            self.df,
            header=header,
            )
        return df_new


    def split_col(
            self,
            col: str = 'uid',
            sep: str = '::\n',
            new1: str = None,
            new2: str = 'label',
            ):
        df_new = split_col(
            self.df,
            col=col,
            sep=sep,
            new1=new1,
            new2=new2,
            )
        return df_new


    def save(
            self,
            path: str,
            sheet_name='df',
            index=False,
            format_excel=True,
            freeze_panes='B2',
            hide_sheets=None,
            hide_cols=None,
            col_width_max=70,
            col_width_padding=2,
            align_vertical='top',
            align_horizontal='left',
            wrap_text=True,
            **kwargs,
            ):
        save(
            df=self.df,
            path=path,
            sheet_name=sheet_name,
            index=index,
            format_excel=format_excel,
            freeze_panes=freeze_panes,
            hide_sheets=hide_sheets,
            hide_cols=hide_cols,
            col_width_max=col_width_max,
            col_width_padding=col_width_padding,
            align_vertical=align_vertical,
            align_horizontal=align_horizontal,
            wrap_text=wrap_text,
            **kwargs,
            )
        return None


    def style(self):
        code = r"""
        .replace("\n", "<br>")
        .wrap(normal)
        .mono()
        .align(left)
        %.align(center)
        """
        df_styled = qs(self.df, code)
        return df_styled

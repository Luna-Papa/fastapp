from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from celery_app.tasks import single_sjxf, all_sbno_sjxf, chn_sjxf, all_table_sjxf, sjbf
import datetime


def sjbf_main():
    def button_click(f, *args):
        f.delay(*args)
        toast('请求已提交后台处理', duration=2, position='right', color='info')

    put_markdown('## 数据下发相关')
    put_tabs([
        {
            'title': '全量数据(单表单机构）',
            'content': [
                put_input('sbno1', type=TEXT, label='请输入机构序号（6位）', help_text='格式：340101')
                    .style('margin-top:30px'),
                put_input('table1', type=TEXT, label='请输入完整表名', help_text='格式：<表名>，如 NSOP_TMP_AMFM21')
                    .style('margin-bottom:40px'),
                put_markdown('---'),
                put_row([
                    put_button('单表单机构下发',
                               onclick=lambda: button_click(single_sjxf, pin.sbno1, pin.table1)),
                    put_button('为该机构下发所有表',
                               onclick=lambda: button_click(all_table_sjxf, pin.sbno1)),
                    put_button('为所有机构下发该表',
                               onclick=lambda: button_click(all_sbno_sjxf, pin.table1))
                ]),
            ]
        },
        {
            'title': '全量数据(单机构单渠道）',
            'content': [
                put_input('sbno2', type=TEXT, label='请输入机构序号（6位）', help_text='格式：340101')
                    .style('margin-top:30px'),
                put_input('chn2', type=TEXT, label='请输入渠道号，如SOP', help_text='格式：SOP')
                    .style('margin-bottom:40px'),
                put_markdown('---'),
                put_button('提交后台',
                           onclick=lambda: button_click(chn_sjxf, pin.sbno2, pin.chn2))
            ]
        },
        {
            'title': '增量包补发（七天内）',
            'content': [
                put_input('sbno3', type=TEXT, label='请输入机构序号（6位）', help_text='格式：340101')
                    .style('margin-top:30px'),
                # put_input('date1', type=TEXT, label='请输入需要补发的数据包日期', help_text='格式：20210101'),
                put_radio(label='请选择补发日期', name='date3', inline=True,
                          options=[(datetime.datetime.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
                                   for i in range(7, 0, -1)]).style('margin-bottom:40px'),
                put_markdown('---'),
                put_button('提交后台',
                           onclick=lambda: button_click(sjbf, pin.sbno3, pin.date3))
            ]
        }
    ]).style('margin-top:50px')

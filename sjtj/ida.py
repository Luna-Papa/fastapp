from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from .summary import zzqs, get_metric_date, get_ida_detail


def ida_main():
    put_markdown('## 自助取数平台统计')
    current_period, begin_date, end_date = get_metric_date('month')
    login_count, query_count, download_count = zzqs(begin_date, end_date)
    file_name = get_ida_detail(begin_date, end_date)
    put_table([
        ['数据周期', '登录次数', '查询次数', '下载次数'],
        [current_period, login_count, query_count, download_count],
        ['明细统计文件', span(put_file(file_name, open(f'static/{file_name}', 'rb').read()), col=3)]
    ]).style('text-align:center')
    # put_code(f"数据周期：{current_period}\n登录次数：{login_count}\n查询次数：{query_count}\n下载次数：{download_count}")
    put_markdown('#### 自定义查询').style('margin-top:30px')
    put_row([
        put_input('begin_date', type=DATE, label='请输入起始日期', value='').style('width:350px'),
        put_input('end_date', type=DATE, label='请输入终止日期', value='').style('width:350px')
    ])
    _begin_date = ''
    _end_date = ''
    while True:
        changed = pin_wait_change('begin_date', 'end_date')
        with use_scope('zzqs', clear=True):
            if changed['name'] == 'begin_date':
                _begin_date = changed['value']
            elif changed['name'] == 'end_date':
                _end_date = changed['value']
            put_code(f"查询起始日期：{_begin_date}\n查询终止日期：{_end_date}")
            if _begin_date == '' or _end_date == '':
                put_text('请输入完整日期！').style('color:red')
            elif _end_date > _begin_date:
                _login_count, _query_count, _download_count = zzqs(pin.begin_date, pin.end_date)
                put_table([
                    ['统计周期', '登录次数', '查询次数', '下载次数'],
                    [f' {pin.begin_date} 至 {pin.end_date} ', _login_count, _query_count, _download_count]
                ]).style('text-align:center')
                f = get_ida_detail(pin.begin_date, pin.end_date)
                put_button('下载明细',
                           onclick=lambda: put_download(f))
            else:
                put_text('终止日期小于起始日期！').style('color:red')


def put_download(f):
    with use_scope('download', clear=True):
        put_file(f, open(f'static/{f}', 'rb').read())


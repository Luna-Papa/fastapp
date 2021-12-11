from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from sfcx.query import sfcx, open_date_query, pos_query, xyk1_query, xyk2_query


def sfcx_main():
    def button_click(f, *args):
        f(*args)
        toast('请求已提交后台处理', duration=2, position='right', color='info')

    put_markdown('## 司法查询相关')
    put_tabs([
        {
            'title': '对手信息查询',
            'content': [
                put_input('account1', type=TEXT, label='请输入账号'),
                put_input('begin_date1', type=TEXT, label='请输入起始日期'),
                put_input('end_date1', type=TEXT, label='请输入终止日期'),
                put_button('提交后台',
                           onclick=lambda: button_click(sfcx, pin.account1, pin.begin_date1, pin.end_date1))
            ]
        },
        {
            'title': 'POS商户信息查询',
            'content': [
                put_input('account2', type=TEXT, label='请输入卡号'),
                put_input('date2', type=TEXT, label='请输入8位交易日期'),
                put_input('amt2', type=TEXT, label='请输入交易金额'),
                put_button('提交后台',
                           onclick=lambda: button_click(pos_query, pin.account2, pin.date2, pin.amt2))
            ]
        },
        {
            'title': '开户信息查询',
            'content': [
                put_input('id_no3', type=TEXT, label='请输入对私客户证件号码'),
                put_input('org_no3', type=TEXT, label='请输入组织机构代码或统一社会代码'),
                put_input('account3', type=TEXT, label='请输入23位账号或卡号'),
                put_input('name3', type=TEXT, label='请输入对公账户名称'),
                put_button('提交后台',
                           onclick=lambda: button_click(open_date_query, pin.id_no3, pin.org_no3, pin.account3, pin.name3))
            ]
        },
        {
            'title': '信用卡相关查询',
            'content': [
                put_row([
                    put_input('account4', type=TEXT, label='请输入卡号', value=''),
                ]),
                put_row([
                    put_button('查询账户信息',
                               onclick=lambda: button_click(xyk1_query, pin.account4)),
                    put_button('查询交易信息',
                               onclick=lambda: button_click(xyk2_query, pin.account4)),
                ])
            ]
        },
    ]).style('margin-top:60px')

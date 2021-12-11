from pywebio.output import *
from pywebio import start_server
from sjtj.ida import ida_main
from sjtj.sjxf import sjxf_main
from sjxf.index import sjbf_main
from sfcx.index import sfcx_main


def index():
    put_markdown('## 集中访问入口（运行支持部）').style('margin-bottom:20px')
    put_text('📢请点击【应用名称】跳转对应页面')
    put_table([
        ['序号', '应用名称', '功能简介'],
        [1, put_link('自助取数平台统计', app='ida_main'), '统计自助取数平台运行数据'],
        [2, put_link('数据下发平台统计', app='sjxf_main'), '统计数据下发平台运行数据'],
        [3, put_link('数据补发和全量下发', app='sjbf_main'), '为农商行补发近七日增量数据包和下发当日全量数据'],
        [4, put_link('司法查询小工具', app='sfcx_main'), '司法查询补对手信息等'],
    ]).style('margin-top:20px;text-align:center;')


start_server(
    [index, ida_main, sjxf_main, sjbf_main, sfcx_main],
    debug=True, port=8081, cdn=False
)

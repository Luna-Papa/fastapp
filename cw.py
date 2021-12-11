from pywebio.output import *
from duanka.find_clue import duanka
from disciplinary.find_clue import disciplinary
from pywebio import start_server


def index():

    put_markdown('## 集中访问入口（财务会计部）').style('margin-bottom:20px')
    put_text('📢请点击【应用名称】跳转对应页面')
    put_table([
        ['序号', '应用名称', '功能简介'],
        [1, put_link('断卡线索排查', app='duanka'), '导入断卡可疑线索，自动生成明细结果和汇总数据。'],
        [2, put_link('惩戒人员线索排查', app='disciplinary'), '导入惩戒人员信息，自动生成明细结果和汇总数据。'],
    ]).style('margin-top:20px;text-align:center;')


start_server([index, duanka, disciplinary], debug=True, port=8080, cdn=False)

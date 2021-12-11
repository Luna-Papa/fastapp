import time
from pywebio.input import *
from pywebio.output import *
from conf.settings import SSH
from .excute import insert_clue, get_summary, check_summary


def disciplinary():
    put_markdown('## 惩戒人员信息排查\n欢迎使用，您可以导入涉案人员线索数据，后台会自动处理，并向您展示汇总结果。\n')
    put_markdown('> #### 表格数据格式要求：\n'
                 '>   - 2列数据：第一列【身份证号码】第二列【手机号码】，顺序需要保持一致\n')\
        .style('margin-top:20px;margin-bottom:20px')
    info = input_group('文件导入⬇', [
        input("请输入年月，格式为：202101", name="period", type=TEXT, required=True),
        file_upload("请上传惩戒人员信息表",
                    accept=['application/vnd.ms-excel',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
                    name='file', required=True,
                    help_text='导入EXCEL表，第一列是身份证号码，第二列是手机号码。'),
    ])
    period = info['period']
    f = info['file']['content']
    insert_clue(f, period)
    # toast('🔔惩戒人员线索数据已导入，请等待后台处理', position='right', color='#2188ff', duration=0)
    # put_markdown('---')
    put_text('后台开始处理...')
    stdin, stdout, stderr = SSH.exec_command('sh /home/ares/eDataMover/script/chengjie.sh')
    with put_loading(shape='border', color='primary'):
        while True:
            time.sleep(60)
            result = check_summary(period)[0]
            if result == 1:
                summary = get_summary(period)
                break
    if summary:
        put_text('✅惩戒人员线索查询完成！')
        put_text('汇总结果如下表')
        put_table([
            ['期数', '手机卡', '银行卡', '信用卡'],
            [period, summary[0], summary[1], summary[2]],
        ])
        put_markdown('---')
        put_text('😸请通知农商银行在自助取数平台【模板取数-其它】目录进行查询，模板名如下：')
        put_table([
            ['序号', '模板名称'],
            [1, '惩戒人员信息_手机卡可疑线索'],
            [2, '惩戒人员信息_身份证可疑线索'],
            [3, '惩戒人员信息_信用卡可疑线索'],
        ])
        put_image(open('disciplinary/惩戒信息模板查询示意.png', 'rb').read())
    else:
        put_text('❌惩戒人员信息线索查询失败，请联系系统管理员。')

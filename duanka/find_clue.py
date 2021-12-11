import time
from pywebio.input import *
from pywebio.output import *
from conf.settings import SSH
from .excute import insert_clue, get_summary, check_summary


def duanka():
    put_markdown('## 断卡线索排查\n欢迎使用，您可以导入断卡线索数据，后台会自动处理，并向您展示汇总结果。\n')
    put_markdown('> #### 表格数据格式要求：\n'
                 '>   - 两个sheet页，第一个是手机卡线索，第二个是银行卡线索，sheet页里内容可以为空，但必须有两个sheet页。\n'
                 '>   - 手机卡线索sheet页字段顺序：【线索编号】【案件编号】【涉案号码】【开卡人】【证件号码】\n'
                 '>   - 银行卡线索sheet页字段顺序：【线索编号】【案件编号】【账号】【开卡人】【证件号码】\n')\
        .style('margin-top:20px;margin-bottom:20px')
    info = input_group('文件导入⬇', [
        input("断卡期数（请输入一个数字🔢）", name="period", type=NUMBER, required=True),
        file_upload("请上传断卡线索",
                    accept=['application/vnd.ms-excel',
                            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'],
                    name='file', required=True,
                    help_text='导入EXCEL表，第一页为手机卡数据，第二页为银行卡数据'),
    ])
    period = info['period']
    f = info['file']['content']
    insert_clue(f, period)
    # toast('🔔断卡线索数据已导入，请等待后台处理', position='right', color='#2188ff', duration=0)
    # put_markdown('---')
    put_text('后台开始处理...')
    stdin, stdout, stderr = SSH.exec_command('sh /home/ares/eDataMover/script/duanka.sh')
    with put_loading(shape='border', color='primary'):
        while True:
            time.sleep(60)
            result = check_summary(period)[0]
            if result == 1:
                summary = get_summary(period)
                break
    if summary:
        put_text('✅断卡线索查询完成！')
        put_text('汇总结果如下表')
        put_table([
            ['期数', '手机卡', '银行卡', '信用卡'],
            [period, summary[0], summary[1], summary[2]],
        ])
        put_markdown('---')
        put_text('😸请通知农商银行在自助取数平台【模板取数-其它】目录进行查询，模板名如下：')
        put_table([
            ['序号', '模板名称'],
            [1, '断卡行动_手机卡可疑线索'],
            [2, '断卡行动_银行卡可疑线索'],
            [3, '断卡行动_信用卡可疑线索'],
        ])
        put_image(open('duanka/断卡模板查询示意.png', 'rb').read())
    else:
        put_text('❌断卡线索查询失败，请联系系统管理员。')

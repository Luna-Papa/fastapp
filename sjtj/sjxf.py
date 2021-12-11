from pywebio.output import *
from sjtj.summary import sjxf, get_metric_date, get_sjxf_time


def sjxf_main():
    put_markdown('## 数据下发平台统计')
    current_period, begin_date, end_date = get_metric_date('month')
    nsh_count, czyh_count, sys_count, table_count = sjxf()
    put_table([
        ['数据周期', '农商行接入数', '村镇银行接入数', '系统数量', '下发表数'],
        [current_period, nsh_count, czyh_count, sys_count, table_count],
    ]).style('text-align:center')
    put_markdown('---')
    sjxf_lists = get_sjxf_time()
    put_table(tdata=sjxf_lists, header=["机构序号", "机构名称", "开通时间"]).style('text-align:center')

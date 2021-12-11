import datetime
from conf.settings import IDA_CONN, SJXF_CURR
import ibm_db
import pandas as pd


def get_metric_date(period_type):
    """
    根据当前日期计算统计周期需要的日期值
    :param str period_type: 日期类型，可允许值：day month year
    """
    current_period = ''  # 统计周期
    if period_type == 'day':
        current_period = \
            (datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')  # 获取昨天日期
    elif period_type == 'month':
        current_period = \
            (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).strftime('%Y-%m')  # 获取上个月月份
    elif period_type == 'year':
        current_period = (datetime.datetime.today().replace(month=1).replace(day=1) -
                          datetime.timedelta(days=1)).strftime('%Y')  # 获取去年年份
    end_date = (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    begin_date = (datetime.datetime.today().replace(day=1) - datetime.timedelta(days=1)) \
        .replace(day=1).strftime('%Y-%m-%d')
    return current_period, begin_date, end_date


def zzqs(begin_date, end_date):
    """
    自助取数平台业务量统计
    :param end_date: YYYY-MM-DD
    :param begin_date: YYYY-MM-DD
    """
    login_count_sql = f"select count(*) from ida_log_login where in_time >= to_date('{begin_date}', 'yyyy-MM-dd') " \
                      f"and in_time <= to_date('{end_date}', 'yyyy-mm-dd')"
    query_count_sql = f"select count(*) from ida_log_execute where start_time>=to_date('{begin_date}', 'yyyy-MM-dd') " \
                      f"and end_time< to_date('{end_date}', 'yyyy-MM-dd') and exec_type_id='7201'"
    download_count_sql = f"select count(*) from ida_log_execute where start_time>=to_date('{begin_date}', 'yyyy-MM-dd') " \
                         f"and end_time< to_date('{end_date}', 'yyyy-MM-dd') and exec_type_id='7204'"
    IDA_CONN.execute(login_count_sql)
    login_count = IDA_CONN.fetchall()[0][0]
    IDA_CONN.execute(query_count_sql)
    query_count = IDA_CONN.fetchall()[0][0]
    IDA_CONN.execute(download_count_sql)
    download_count = IDA_CONN.fetchall()[0][0]
    return login_count, query_count, download_count


def sjxf():
    """
    数据下发平台业务量统计
    """
    nsh_count_sql = "SELECT count(1) FROM ODMFDS.DATA_USER"
    czyh_count_sql = "SELECT count(DISTINCT a.CUSER_ID) FROM odmfds.DATA_SUB a, ods.nsop_mir_brfd01 b " \
                     "WHERE b.SUBBNKN = a.CUSER_ID AND b.brclvl = '3' AND b.brcattr = '0' AND b.ISCUBAK = '1'"
    sys_count_sql = "SELECT count(DISTINCT DS_ID)  FROM odmfds.BASETABLES a, odmfds.SCTJOB b " \
                    "WHERE b.JOBID = a.JOBID AND b.JOBVAL = '1' AND a.FLAG = '0'"
    table_count_sql = "SELECT count(1) FROM odmfds.BASETABLES a, odmfds.SCTJOB b WHERE b.JOBID = a.JOBID " \
                      "AND b.JOBVAL = '1' AND a.FLAG = '0'"
    stmt = ibm_db.exec_immediate(SJXF_CURR, nsh_count_sql)
    nsh_count = ibm_db.fetch_tuple(stmt)[0]
    stmt = ibm_db.exec_immediate(SJXF_CURR, czyh_count_sql)
    czyh_count = ibm_db.fetch_tuple(stmt)[0]
    stmt = ibm_db.exec_immediate(SJXF_CURR, sys_count_sql)
    sys_count = ibm_db.fetch_tuple(stmt)[0]
    stmt = ibm_db.exec_immediate(SJXF_CURR, table_count_sql)
    table_count = ibm_db.fetch_tuple(stmt)[0]
    return nsh_count, czyh_count, sys_count, table_count


def get_ida_detail(begin_date, end_date):
    """获取一段日期内各农商行自助取数平台的登录次数和查询次数"""
    sql = f"SELECT A.SBSSNO,A.SBSBNM,A.QUERY_NUM,B.DOWNLOAD_NUM FROM " \
          f"(select b.sbssno as SBSSNO,b.sbsbnm as SBSBNM,COALESCE(a.num,0) as QUERY_NUM from " \
          f"(select substr(user_id,1,6) as ssno,count(*) as num from ida_log_execute where user_id like '34%' and " \
          f"start_time>=to_date('{begin_date}', 'yyyy-MM-dd') and end_time< to_date('{end_date}', 'yyyy-MM-dd') and " \
          f"exec_type_id='7201' group by SUBSTR(user_id,1,6) order by SUBSTR(user_id,1,6)) a right join crsba b " \
          f"on a.ssno=b.sbssno  order by b.sbssno) A JOIN (select  b.sbssno as SBSSNO,b.sbsbnm as SBSBNM," \
          f"COALESCE(a.num,0) as DOWNLOAD_NUM from (select substr(user_id,1,6) as ssno,count(*) as num " \
          f"from ida_log_execute where user_id like '34%' and start_time>=to_date('{begin_date}', 'yyyy-MM-dd') and " \
          f"end_time< to_date('{end_date}', 'yyyy-MM-dd') and exec_type_id='7204' group by SUBSTR(user_id,1,6) " \
          f"order by SUBSTR(user_id,1,6)) a right join crsba b on a.ssno=b.sbssno order by b.sbssno)  B " \
          f"ON A.SBSSNO=b.SBSSNO"
    IDA_CONN.execute(sql)
    rel = IDA_CONN.fetchall()
    file_name = f"{begin_date}至{end_date}自助取数平台农商行使用数据统计" + '.xlsx'
    dret = pd.DataFrame.from_records(list(rel))
    dret.to_excel(f'static/{file_name}', index=False, header=('机构序号', '机构名称', '登录次数', '查询次数'))
    return file_name


def get_sjxf_time():
    sql = "select a.CUSER_ID, trim(b.brcname), min(a.CREATEDATE) FROM odmfds.DATA_SUB a, " \
          "ods.nsop_mir_brfd01 b WHERE b.SUBBNKN = a.cuser_id AND b.brclvl = '3' AND " \
          "b.brcattr = '0' GROUP BY a.CUSER_ID, b.brcname ORDER BY 3 DESC"
    stmt = ibm_db.exec_immediate(SJXF_CURR, sql)
    result = ibm_db.fetch_tuple(stmt)
    result_list = []
    while result:
        result_list.append(list(result))
        result = ibm_db.fetch_tuple(stmt)
    return result_list

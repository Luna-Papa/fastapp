from celery_app.celery import app
import ibm_db
from conf.settings import SJXF_CURR, SJXF_SSH


def check_table_name(table_name):
    sql1 = "SELECT ID,DS_ID FROM ODMFDS.BASETABLES WHERE tablename = '{}'".format(table_name.upper())  # 获取表和渠道编号
    stmt = ibm_db.exec_immediate(SJXF_CURR, sql1)
    result = ibm_db.fetch_tuple(stmt)
    if result:
        T_ID, DS_ID = result
        # TMP表替换为MIR表
        sql2 = "SELECT trim(CREATOR)||'.'||replace(trim(TABLENAME),'_TMP_','_MIR_') " \
               "FROM ODMFDS.BASETABLES WHERE ID='{T_ID}'".format(T_ID=T_ID)
        stmt = ibm_db.exec_immediate(SJXF_CURR, sql2)
        TBNAME_MIR = ibm_db.fetch_tuple(stmt)[0]
        return T_ID, DS_ID, TBNAME_MIR


@app.task
def single_sjxf(org_no, table_name):
    """单表单机构下发"""
    DUSER_ID = org_no
    T_ID, DS_ID, TBNAME_MIR = check_table_name(table_name)
    if TBNAME_MIR:
        stdin, stdout, stderr = SJXF_SSH.exec_command(
            '. /home/odmfds/.profile;'
            'sh /home/odmfds/eDataMover/script/erdd_mir_data.ksh {DS_ID} {DUSER_ID} {TBNAME_MIR} {T_ID}'
                .format(DS_ID=DS_ID, DUSER_ID=DUSER_ID, TBNAME_MIR=TBNAME_MIR, T_ID=T_ID))
        if stderr.read().decode() == "":
            print(org_no + '-' + table_name + "-下发完成！")


@app.task
def all_sbno_sjxf(table_name):
    """单张表下发所有机构"""
    T_ID, DS_ID, TBNAME_MIR = check_table_name(table_name)
    print(T_ID, DS_ID, TBNAME_MIR)
    if TBNAME_MIR:
        # 获取下发该表的所有机构号
        sql = "SELECT CUSER_ID FROM DATA_SUB WHERE T_ID = '{}' AND DUSER_ID <> 'MODEL'" \
              " group by CUSER_ID".format(T_ID)
        stmt = ibm_db.exec_immediate(SJXF_CURR, sql)
        result = ibm_db.fetch_tuple(stmt)
        result_list = []
        while result:
            result_list.append(list(result))
            result = ibm_db.fetch_tuple(stmt)
        # 循环读机构号，开始下发
        for i in range(len(result_list)):
            DUSER_ID = result_list[i][0]
            single_sjxf.delay(DUSER_ID, table_name)


@app.task
def all_table_sjxf(org_no):
    """单机构下发所有表"""
    DUSER_ID = org_no
    # 获取该机构该渠道下发的所有表编号
    sql1 = "SELECT T_ID FROM DATA_SUB WHERE CUSER_ID='{}'".format(DUSER_ID)
    stmt = ibm_db.exec_immediate(SJXF_CURR, sql1)
    result = ibm_db.fetch_tuple(stmt)
    result_list = []
    while result:
        result_list.append(list(result))
        result = ibm_db.fetch_tuple(stmt)
        for i in range(len(result_list)):
            T_ID = result_list[i][0]
            sql2 = "SELECT trim(TABLENAME) FROM ODMFDS.BASETABLES WHERE ID='{T_ID}'".format(T_ID=T_ID)
            tab_stmt = ibm_db.exec_immediate(SJXF_CURR, sql2)
            table_name = ibm_db.fetch_tuple(tab_stmt)[0]
            single_sjxf.delay(DUSER_ID, table_name)


@app.task
def chn_sjxf(org_no, chn):
    """单机构单渠道所有表下发"""
    DUSER_ID = org_no
    DS_ID = chn.upper()
    # 获取该机构该渠道下发的所有表编号
    sql1 = "SELECT T_ID FROM DATA_SUB WHERE DS_ID = '{}' AND CUSER_ID = '{}'".format(DS_ID, DUSER_ID)
    stmt = ibm_db.exec_immediate(SJXF_CURR, sql1)
    result = ibm_db.fetch_tuple(stmt)
    result_list = []
    while result:
        result_list.append(list(result))
        result = ibm_db.fetch_tuple(stmt)
        # 循环读机构号，开始下发
        for i in range(len(result_list)):
            T_ID = result_list[i][0]
            sql2 = "SELECT trim(TABLENAME) FROM ODMFDS.BASETABLES WHERE ID='{T_ID}'".format(T_ID=T_ID)
            tab_stmt = ibm_db.exec_immediate(SJXF_CURR, sql2)
            table_name = ibm_db.fetch_tuple(tab_stmt)[0]
            single_sjxf.delay(DUSER_ID, table_name)


@app.task
def sjbf(org_no, date):
    """补发增量包，限制7天内"""
    sql = "UPDATE ODMFDS.DD_LOG SET D_STATE='1' WHERE DUSER_ID='{}' AND " \
          "D_DATE='{}' AND D_STATE<>'6'".format(org_no, date)
    ibm_db.exec_immediate(SJXF_CURR, sql)
    print("已补发增量包")

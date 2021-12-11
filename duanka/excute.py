import pandas as pd
import ibm_db
from pywebio.output import *
from conf.settings import DB_CONN


def insert_clue(f, period):
    """ 解析前台上传的线索数据表，并插入后台登记表中

    :param f: 前台上传的excel文件对象
    :param int period: 断卡线索的期数
    """
    sql = f"truncate table dzyh.duanka_clue_phone immediate"
    ibm_db.exec_immediate(DB_CONN, sql)
    sql = f"truncate table dzyh.duanka_clue_card immediate"
    ibm_db.exec_immediate(DB_CONN, sql)
    print("清理中间表成功！")
    with pd.ExcelFile(f) as xls:
        try:
            with put_loading(shape='border', color='primary'):
                put_text('加载断卡线索-手机卡...')
                df1 = pd.read_excel(xls, sheet_name=0)  # 手机卡
                put_processbar('bar_phone', auto_close=True)
                for index in df1.index.values:
                    set_processbar('bar_phone', index / df1.index.values[-1])
                    clue_no, case_no, case_phone, name, id_no = \
                        df1.loc[index, ['线索编号', '案件编号', '涉案号码', '开卡人', '证件号码']]
                    sql = f"insert into dzyh.duanka_clue_phone values " \
                          f"({period}, '{clue_no}', '{case_no}', '{case_phone}', '{name}', '{id_no}')"
                    ibm_db.exec_immediate(DB_CONN, sql)
            # put_text(' ')
            put_text(f"✅第{period}期断卡-手机卡数据加载完成！")
            put_markdown('---')
        except Exception as e:
            print(e)
        try:
            with put_loading(shape='border', color='primary'):
                put_text('加载断卡线索-银行卡...')
                df2 = pd.read_excel(xls, sheet_name=1)  # 银行卡
                put_processbar('bar_card', auto_close=True)
                for index in df2.index.values:
                    set_processbar('bar_card', index / df2.index.values[-1])
                    clue_no, case_no, account, name, id_no = \
                        df2.loc[index, ['线索编号', '案件编号', '账号', '开卡人', '证件号码']]
                    sql = f"insert into dzyh.duanka_clue_card values " \
                          f"({period}, '{clue_no}', '{case_no}', '{account}', '{name}', '{id_no}')"
                    ibm_db.exec_immediate(DB_CONN, sql)
            put_text(f"✅第{period}期断卡-银行卡数据加载完成！")
        except Exception as e:
            print(e)


def get_summary(period):
    """
    根据断卡期数查询汇总查询结果
    :param int period: 断卡线索的期数
    """
    sql = f"select sjk_count, yhk_count, xyk_count from dzyh.dk_state where period={period}"
    summary = ()
    try:
        stmt = ibm_db.exec_immediate(DB_CONN, sql)
        summary = ibm_db.fetch_tuple(stmt)
    except Exception as e:
        print(e)
        summary = ()
    finally:
        return summary


def check_summary(period):
    """
    根据断卡期数查询汇总查询是否生成
    :param int period: 断卡线索的期数
    """
    sql = f"select count(*) from dzyh.dk_state where period={period}"
    try:
        stmt = ibm_db.exec_immediate(DB_CONN, sql)
        summary = ibm_db.fetch_tuple(stmt)
        return summary
    except Exception as e:
        print(e)



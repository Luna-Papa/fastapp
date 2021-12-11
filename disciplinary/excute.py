import pandas as pd
import ibm_db
from pywebio.output import *
from conf.settings import DB_CONN


def insert_clue(f, period):
    """ 解析前台上传的线索数据表，并插入后台登记表中

    :param f: 前台上传的excel文件对象
    :param int period: 断卡线索的期数
    """
    sql = f"truncate table dzyh.disciplinary_clue immediate"
    ibm_db.exec_immediate(DB_CONN, sql)
    print("清理中间表成功！")
    with pd.ExcelFile(f) as xls:
        try:
            with put_loading(shape='border', color='primary'):
                put_text('加载惩戒人员信息...')
                df = pd.read_excel(xls, sheet_name=0)
                put_processbar('bar', auto_close=True)
                for index in df.index.values:
                    set_processbar('bar', index / df.index.values[-1])
                    id_no, phone = df.loc[index]
                    sql = f"insert into dzyh.disciplinary_clue values ({period}, '{id_no}', '{phone}')"
                    ibm_db.exec_immediate(DB_CONN, sql)
            put_text(f"✅第{period}期惩戒人员信息数据加载完成！")
            put_markdown('---')
        except Exception as e:
            print(e)


def get_summary(period):
    """
    根据期数查询汇总查询结果
    :param int period: 惩戒人员信息表的期数
    """
    sql = f"select sjk_count, yhk_count, xyk_count from dzyh.chengjie_state where period={period}"
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
    sql = f"select count(*) from dzyh.chengjie_state where period={period}"
    try:
        stmt = ibm_db.exec_immediate(DB_CONN, sql)
        summary = ibm_db.fetch_tuple(stmt)
        return summary
    except Exception as e:
        print(e)



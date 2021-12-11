from pathlib import Path
import ibm_db
import psycopg2
import configparser
import paramiko

# 项目根目录
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# 后台SSH和数据库连接
BACKGROUND = 'hisdata'
IDA = "postgres"
SSH = ''
DB_CONN = ''
IDA_CONN = ''

cf = configparser.ConfigParser()
cf.read(BASE_DIR / 'conf' / 'cfg.ini')
try:
    ip = cf.get(BACKGROUND, "ip")
    ssh_port = 22
    db_port = cf.get(BACKGROUND, "port")
    user = cf.get(BACKGROUND, "user")
    password = cf.get(BACKGROUND, "passwd")
    SSH = paramiko.SSHClient()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SSH.connect(hostname=ip, port=ssh_port, username=user, password=password)
    conn_str = f"DATABASE={BACKGROUND};HOSTNAME={ip};PORT={db_port};PROTOCOL=TCPIP;UID={user};PWD={password};"
    DB_CONN = ibm_db.connect(conn_str, "", "")
except Exception as e:
    print(e)
try:
    ip = cf.get(IDA, "ip")
    db_port = cf.get(IDA, "port")
    user = cf.get(IDA, "user")
    password = cf.get(IDA, "passwd")
    conn = psycopg2.connect(database=IDA, user=user, password=password, host=ip, port=db_port)
    IDA_CONN = conn.cursor()
except Exception as e:
    print(e)
try:
    sjxf_ip = cf.get('sjxf', "ip")
    sjxf_ssh_port = 22
    sjxf_db_port = cf.get('sjxf', "port")
    sjxf_user = cf.get('sjxf', "user")
    sjxf_password = cf.get('sjxf', "passwd")
    sjxf_dbname = cf.get('sjxf', "dbname")
    SJXF_SSH = paramiko.SSHClient()
    SJXF_SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SJXF_SSH.connect(hostname=sjxf_ip, port=sjxf_ssh_port, username=sjxf_user, password=sjxf_password)
    sjxf_conn_str = f"DATABASE={sjxf_dbname};HOSTNAME={sjxf_ip};PORT={sjxf_db_port};PROTOCOL=TCPIP;UID={sjxf_user};PWD={sjxf_password};"
    SJXF_CURR = ibm_db.connect(sjxf_conn_str, "", "")
except Exception as e:
    print(e)

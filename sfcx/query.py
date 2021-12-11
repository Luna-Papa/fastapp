from conf.settings import DB_CONN, SSH
import ibm_db


def sfcx(account, begin_date, end_date=''):
    """司法查询刷交易对手"""
    print(account, begin_date, end_date)
    stdin, stdout, stderr = \
        SSH.exec_command(
            '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/cx.sh {account} {begin_date} {end_date}'
                .format(account=account, begin_date=begin_date, end_date=end_date))


def open_date_query(id_no='', org_no='', account='', name=''):
    if id_no:
        stdin, stdout, stderr = SSH.exec_command(
            '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/kh_zj_ds.sh {id_no}'
                .format(id_no=id_no))
    if org_no:
        stdin, stdout, stderr = SSH.exec_command(
            '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/kh_zj_dg.sh {org_no}'
                .format(org_no=org_no))
    if account:
        stdin, stdout, stderr = SSH.exec_command(
            '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/kh_zh.sh {account}'
                .format(account=account))
    if name:
        # ssh.connect(hostname='10.0.134.32', port=22, username='sysman', password='sysman')
        # stdin, stdout, stderr = ssh.exec_command('echo {name} > /mnt/nfsdata/dg_name.txt'.format(name=name))
        transport = paramiko.Transport(("10.0.134.110", 22))
        transport.connect(username='hisusr', password='hisusr')
        sftp = paramiko.SFTPClient.from_transport(transport)
        with open('c:/sfcx/dg_name.txt', 'w', encoding='gbk') as f:
            f.write(name)
        sftp.put('c:/sfcx/dg_name.txt', '/datatmp/sjm/YX_SFCX/dg_name.txt')
        sftp.close()
        # ssh.connect(hostname='10.0.134.110', port=22, username='hisusr', password='hisusr')
        stdin, stdout, stderr = SSH.exec_command(
            '. /dbhome/hisusr/.profile;'
            'sh /datatmp/sjm/YX_SFCX/kh_mc_dg.sh')


def pos_query(account, date, amt):
    stdin, stdout, stderr = SSH.exec_command(
        '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/pos.sh {account} {date} {amt}'
            .format(account=account, date=date, amt=amt))


def xyk1_query(account):
    """查询信用卡账户信息"""
    stdin, stdout, stderr = SSH.exec_command(
        '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/xyk_zhxx.sh {account}'
            .format(account=account))


def xyk2_query(account):
    """查询信用卡交易信息"""
    stdin, stdout, stderr = SSH.exec_command(
        '. /dbhome/hisusr/.profile;sh /datatmp/sjm/YX_SFCX/xyk_jyxx.sh {account}'
            .format(account=account))

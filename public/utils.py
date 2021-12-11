import paramiko
import ibm_db


class SSHConnection:
    def __init__(self, host, port, user, pwd):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

    def run_cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(command)
        res = stdout.read().decode()
        error = stderr.read().decode()
        if error.strip():
            return error
        else:
            return res

    # def connect(self):
    #     transport = paramiko.Transport((self.host, self.port))
    #     transport.connect(username=self.user, password=self.pwd)
    #     self.__transport = transport
    #
    # def close(self):
    #     self.__transport.close()

    def upload(self, local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path, confirm=True)
        # print(os.stat(local_path).st_mode)
        # 增加权限
        # sftp.chmod(target_path, os.stat(local_path).st_mode)
        sftp.chmod(target_path, 0o755)  # 注意这里的权限是八进制的，八进制需要使用0o作为前缀

    def download(self, target_path, local_path):
        # 连接，下载
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 下载至服务器 /tmp/test.py
        sftp.get(target_path, local_path)

    # def __del__(self):
    #     self.close()


class DBConnection:
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        conn_str = f"DATABASE={self.db};HOSTNAME={self.host};PORT={self.port};PROTOCOL=TCPIP;" \
                   f"UID={self.user};PWD={self.pwd};"
        self.db_conn = ibm_db.connect(conn_str, "", "")



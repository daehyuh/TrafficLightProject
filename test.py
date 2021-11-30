import paramiko
from scp import SCPClient, SCPException


class SSHManager:
    def __init__(self):
        self.ssh_client = None

    def create_ssh_client(self, hostname, username, password):
        """Create SSH client session to remote server"""
        if self.ssh_client is None:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname, username=username, password=password)
        else:
            print("SSH client session exist.")

    def close_ssh_client(self):
        """Close SSH client session"""
        self.ssh_client.close()

    def send_file(self, local_path, remote_path):
        """Send a single file to remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path, preserve_times=True)
        except SCPException:
            raise SCPException.message

    def get_file(self, remote_path, local_path):
        """Get a single file from remote path"""
        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.get(remote_path, local_path)
        except SCPException:
            raise SCPException.message

    def send_command(self, command):
        """Send a single command"""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        return stdout.readlines()


ssh_manager2 = SSHManager()  ##수신
ssh_manager2.create_ssh_client("192.168.1.6", "user", "user")


stop_check = False


def get_hex():
    ssh_manager2.get_file('/home/user/signal/signal', './signal_recieve')
    with open("signal_recieve", "r") as f2:
        item = f2.readline()
        # print("\r\r\r\r ------,", item)
    f2.close()
    print(item)
    return item


get_hex()
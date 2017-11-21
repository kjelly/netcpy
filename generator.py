import copy
import os
import templates
import utils


class Base(object):
    def __init__(self):
        self.local_tmp_dir = '/tmp/'
        self.remote_tmp_dir = '/tmp/'
        self.remote_dir = '/etc/sysconfig/network-scripts/'
        self.file_prefix = 'ifup-'

    def generate(self, data, template, device):
        data = copy.deepcopy(data)
        data['device'] = device
        file_path = os.path.join(self.local_tmp_dir, self.file_prefix + device)
        with open(file_path, 'w') as ftr:
            ftr.write(template.render(**data))
        return file_path

    def config(self, data):
        pass


class CentOSEth(Base):
    def config(self, data):
        device = data['ifnames'][0]
        local_file_path = self.generate(data, templates.centos_eth, device)
        file_name = self.file_prefix + device
        remote_tmp_path = os.path.join(self.remote_tmp_dir, file_name)
        utils.scp(data, local_file_path, remote_tmp_path, self.remote_dir)


class CentOSBond(Base):
    def generate_and_scp_bond(self, data, template, device):
        local_file_path = self.generate(data, template, device)
        file_name = self.file_prefix + device
        remote_file_path = os.path.join(self.local_tmp_dir, file_name)
        remote_tmp_path = os.path.join(self.remote_tmp_dir, file_name)
        utils.scp(data, local_file_path, remote_tmp_path, remote_file_path)

    def config(self, data):
        device = data['ifnames'][0]
        self.generate_and_scp_bond(data, templates.centos_bond_master, device)
        for device in data['ifnames'][1:]:
            self.generate_and_scp_bond(data, templates.centos_bond_eth, device)


class UbuntuEth(Base):
    def config(self, data):
        device = data['ifnames'][0]
        local_file_path = self.generate(data, templates.ubuntu_eth, device)
        file_name = self.file_prefix + device
        remote_tmp_path = os.path.join(self.remote_tmp_dir, file_name)
        remote_file_path = os.path.join(self.local_tmp_dir, file_name)
        utils.scp(data, local_file_path, remote_tmp_path, remote_file_path)

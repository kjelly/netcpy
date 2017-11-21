import copy
import os
from subprocess import check_output


def run_remote_command(data, cmd):
    data = copy.deepcopy(data)
    arg = ['ssh', '-i', data['key_path'], '-o',
           'UserKnownHostsFile=/dev/null', '-o',
           'StrictHostKeyChecking=no',
           '{user}@{target_ip}'.format(**data), cmd]
    output = check_output(arg)
    print(' '.join(arg))
    print(output)
    return output


def ifupdown(data):
    data = copy.deepcopy(data)
    data['device'] = data['ifnames'][0]
    run_remote_command(data, ('sudo ifdown {device};'
                              'sudo ifup {device}').format(**data))


def scp(data, src, remote_tmp_path, dest):
    data = copy.deepcopy(data)
    data['device'] = data['ifnames'][0]
    cmd = ('''scp -i {key_path} -o UserKnownHostsFile=/dev/null '''
           ''' -o StrictHostKeyChecking=no {src} '''
           '''{user}@{target_ip}:{remote_tmp_path} ''')

    print(cmd.format(src=src, remote_tmp_path=remote_tmp_path, **data))
    os.system(cmd.format(src=src, remote_tmp_path=remote_tmp_path, **data))
    cmd = ('sudo cp {remote_tmp_path} '
           '{dest}').format(remote_tmp_path=remote_tmp_path, dest=dest, **data)
    run_remote_command(data, cmd)

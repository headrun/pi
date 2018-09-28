#!/usr/bin/env python

import sys, os, traceback
import pexpect, time

VTV_SSH_PATTERN_LIST = [pexpect.EOF, pexpect.TIMEOUT,
                        'Are you sure you want to continue connecting .*\?', 'assword:', 
                        'Offending key']

VTV_SSH_MAX_INDEX = len(VTV_SSH_PATTERN_LIST)
VTV_SSH_EOF, VTV_SSH_TIMEOUT, VTV_SSH_CONNECT_PROMPT, VTV_SSH_PASSWORD, VTV_SSH_OFFENDING_KEY = range(VTV_SSH_MAX_INDEX)

VTV_SSH_LOCAL  = "local"
VTV_SSH_REMOTE = "remote"

VTV_SSH_TYPE_SSH = "ssh"
VTV_SSH_TYPE_SCP = "scp"

VTV_SSH_CONNECT_TIMEOUT = 10

VTV_SCP_COMMAND = "scp -o NumberOfPasswordPrompts=1 -o ConnectTimeout=%d" % VTV_SSH_CONNECT_TIMEOUT
VTV_SCP_DIR_COMMAND = "scp -r -o NumberOfPasswordPrompts=1 -o ConnectTimeout=%d" % VTV_SSH_CONNECT_TIMEOUT 
VTV_SSH_COMMAND = "ssh -t -o NumberOfPasswordPrompts=1 -o ConnectTimeout=%d" % VTV_SSH_CONNECT_TIMEOUT

VTV_SSH_CMD_TIMEOUT   = 300
VTV_SCP_CMD_TIMEOUT   = 1800
VTV_SSH_LOGIN_TIMEOUT = 30

VTV_DEFAULT_PROMPT = '#'


"""
ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/raman/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/raman/.ssh/id_rsa.
Your public key has been saved in /home/raman/.ssh/id_rsa.pub.
The key fingerprint is:
2c:f5:7f:41:2a:14:22:b4:27:ff:b8:47:2e:8b:3d:53 raman@kalyani
"""

def run_ssh_keygen_rsa():
    process = pexpect.spawn("ssh-keygen -t rsa")
    process.expect('Enter file in which to save the key .*:', 10)
    process.sendline('')
    index = process.expect(['Enter passphrase .*:', 'Overwrite .*\?']) 
    if index == 0:
        process.sendline('')
    elif index == 1:
        process.sendline('y')
        process.expect('Enter passphrase .*:') 
        process.sendline('')
    process.expect('Enter same passphrase again:')
    process.sendline('')
    process.expect('The key fingerprint is:')

    cwd = os.getcwd()
    home_dir = os.path.expanduser("~")
    os.chdir(home_dir)

    if not os.path.exists(".ssh"):
        print "Cannot find .ssh directory"
        sys.exit(1)
    
    if not os.path.exists(".ssh/id_rsa"):
        print "Cannot find id_rsa"
        sys.exit(1)
    
    if not os.path.exists(".ssh/id_rsa.pub"):
        print "Cannot find id_rsa.pub"
        sys.exit(1)
    
    os.chdir(cwd)


def ssh_login(process, user_pattern_list, type, local_or_remote, password, time_out = VTV_SSH_LOGIN_TIMEOUT, ssh_cmd = ""):
    pattern_list = VTV_SSH_PATTERN_LIST + user_pattern_list

    removed = False
    user_index = 0
    while True:
        index = process.expect(pattern_list, time_out)
        user_index = index - len(VTV_SSH_PATTERN_LIST)
        if index == VTV_SSH_EOF:
            return user_index, process
        elif index == VTV_SSH_TIMEOUT:
            return user_index, process
        elif index == VTV_SSH_CONNECT_PROMPT:
            process.sendline('yes')
            index = process.expect(pattern_list, time_out) 
            user_index = index - len(VTV_SSH_PATTERN_LIST)
            if index == VTV_SSH_PASSWORD:
                process.sendline(password)
            else:
                return user_index, process
        elif index == VTV_SSH_PASSWORD:
            process.sendline(password)
        elif index == VTV_SSH_OFFENDING_KEY:
            if removed:
                return user_index, process
            if local_or_remote == "local":
                try:
                    home_dir = os.path.expanduser("~")
                    if home_dir == '/':
                        ssh_key_file = "/root/.ssh/known_hosts"
                        if os.path.exists(ssh_key_file):
                            os.remove(ssh_key_file)
                    ssh_key_file = os.path.join(home_dir, ".ssh/known_hosts")
                    if os.path.exists(ssh_key_file):
                        os.remove(ssh_key_file)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception, e:
                    pass
                removed = True
                if type == VTV_SSH_TYPE_SSH:
                    process = pexpect.spawn(ssh_cmd)
            else:
                process.sendline("cd ~; rm -f .ssh/known_hosts")
            continue

        break

    return user_index, process


def ssh_ext(process, local_or_remote, ssh_cmd, host, user, password, cmd = None, prompt = VTV_DEFAULT_PROMPT, login_timeout = VTV_SSH_LOGIN_TIMEOUT, cmd_timeout = VTV_SSH_CMD_TIMEOUT):
    index, process = ssh_login(process, [prompt], VTV_SSH_TYPE_SSH, local_or_remote, password, login_timeout, ssh_cmd)

    if index < 0:
        if (index + VTV_SSH_MAX_INDEX) != VTV_SSH_PASSWORD:
             return None

    if index != 0 and index < VTV_SSH_MAX_INDEX:
        process.expect(prompt)

    if not cmd:
        return process

    process.sendline(cmd)
    process.expect(prompt, cmd_timeout)

    return process


def ssh(host, user, password, cmd = None, prompt = VTV_DEFAULT_PROMPT, login_timeout = VTV_SSH_LOGIN_TIMEOUT, cmd_timeout = VTV_SSH_CMD_TIMEOUT):
    ssh_cmd = "%s %s@%s" % (VTV_SSH_COMMAND, user, host)
    process = pexpect.spawn(ssh_cmd)
    process = ssh_ext(process, VTV_SSH_LOCAL, ssh_cmd, host, user, password, cmd, prompt, login_timeout, cmd_timeout)

    return process


def ssh_check_status(process, index, pattern_list, cmd_timeout = VTV_SSH_CMD_TIMEOUT):
    std_list = [pexpect.EOF, pexpect.TIMEOUT]
    need_list = std_list + pattern_list
    status = 1
    if index < 0:
        if (index + VTV_SSH_MAX_INDEX) == VTV_SSH_PASSWORD:
            index = process.expect(need_list, cmd_timeout)
            if not pattern_list and index == 0:
                status = 0
            elif index > VTV_SSH_TIMEOUT:
                status = 0
        elif (index + VTV_SSH_MAX_INDEX) == VTV_SSH_EOF:
            if not pattern_list:
                status = 0
    else:
        status = 0

    if pattern_list and status == 0:
        need_list = std_list 
        index = process.expect(need_list, cmd_timeout)
        if index > VTV_SSH_EOF:
            status = 2

    process.close()

    if status == 0:
        status = int(process.exitstatus)

    return status


def ssh_cmd_output(host, user, password, cmd, cmd_timeout = VTV_SSH_CMD_TIMEOUT):
    new_cmd = "%s %s@%s '%s'" % (VTV_SSH_COMMAND, user, host, cmd)
    pattern_list = []

    process = pexpect.spawn(new_cmd)
    index, process = ssh_login(process, pattern_list, VTV_SSH_TYPE_SSH, VTV_SSH_LOCAL, password, cmd_timeout, new_cmd)
    status = ssh_check_status(process, index, pattern_list, cmd_timeout)

    return status, process


def ssh_cmd(host, user, password, cmd, cmd_timeout = VTV_SSH_CMD_TIMEOUT):
    status, process = ssh_cmd_output(host, user, password, cmd, cmd_timeout)
    return status


def scp_ext(process, scp_cmd, password, copy_timeout = VTV_SCP_CMD_TIMEOUT):
    pattern_list = ["100%"]
    index, process = ssh_login(process, pattern_list, VTV_SSH_TYPE_SCP, VTV_SSH_LOCAL, password, copy_timeout)
    status = ssh_check_status(process, index, pattern_list, copy_timeout)
    return status

def scp_dir(password, src, dst, copy_timeout = VTV_SCP_CMD_TIMEOUT):
    scp_cmd = "%s %s %s" % (VTV_SCP_DIR_COMMAND, src, dst)
    process = pexpect.spawn(scp_cmd)
    status = scp_ext(process, scp_cmd, password, copy_timeout)

    return status 


def scp(password, src, dst, copy_timeout = VTV_SCP_CMD_TIMEOUT):
    scp_cmd = "%s %s %s" % (VTV_SCP_COMMAND, src, dst)
    process = pexpect.spawn(scp_cmd)
    status = scp_ext(process, scp_cmd, password, copy_timeout)

    return status 


def ssh_recursive_cmd(ssh_param_list, cmd):
    user, password, host, prompt = ssh_param_list[0]
    second_user, second_password, second_host, second_prompt = ssh_param_list[1]
    pattern_list = []

    process = ssh(host, user, password, None, prompt)
    second_ssh_cmd = "%s %s@%s '%s'" % (VTV_SSH_COMMAND, second_user, second_host, cmd)
    process.sendline(second_ssh_cmd)
    index, process = ssh_login(process, pattern_list, VTV_SSH_TYPE_SSH, VTV_SSH_REMOTE, second_password, VTV_SSH_LOGIN_TIMEOUT, second_ssh_cmd)
    process.expect(prompt)

    return process

def ssh_recursive(ssh_param_list):
    user, password, host, prompt = ssh_param_list[0]
    second_user, second_password, second_host, second_prompt = ssh_param_list[1]
    if prompt == '$':
        prompt = '\$'
    if second_prompt == '$':
        second_prompt = '\$'

    pattern_list = [second_prompt]

    process = ssh(host, user, password, None, prompt)
    second_ssh_cmd = "%s %s@%s" % (VTV_SSH_COMMAND, second_user, second_host)
    process.sendline(second_ssh_cmd)
    index, process = ssh_login(process, pattern_list, VTV_SSH_TYPE_SSH, VTV_SSH_REMOTE, second_password, VTV_SSH_LOGIN_TIMEOUT, second_ssh_cmd)

    process.sendline('stty -echo')
    process.expect(second_prompt)

    process.sendline('cd')
    process.expect(second_prompt)

    return process


def main():
    #run_ssh_keygen_rsa()

    if len(sys.argv) < 5:
        print "ssh_utils.py user password server prompt,..."
        sys.exit(0)

    prompt = '\$'
    prompt = '#'
    user, password, host, prompt = sys.argv[1:5]

    ssh_recursive([sys.argv[1:5], sys.argv[5:9]])
    return

    for server in host.split(','):
        print "\n\nTest: SCP Pass"
        status = scp(password, "%s@%s:/usr/include/syslog.h" % (user, server), "/tmp")
        print "%s scp pass: status: %s" % (server, status)

        print "\n\nTest: SCP Fail"
        status = scp(password, "%s@%s:/usr/include/syslogjunk.h" % (user, server), "/tmp")
        print "%s scp fail: status: %s" % (server, status)

        print "\n\nTest: SSH Command Pass"
        cmd = 'ls -l'
        status = ssh_cmd(server, user, password, cmd)
        print "%s ssh_cmd pass: status: %s" % (server, status)

        print "\n\nTest: SSH Command FAIL"
        cmd = 'iamfunny'
        status = ssh_cmd(server, user, password, cmd)
        print "%s ssh_cmd fail: status: %s" % (server, status)

        print "\n\nTest: SSH Command Output Pass"
        cmd = 'ls -l'
        status, process = ssh_cmd_output(server, user, password, cmd)
        print "%s ssh_cmd_output pass: status: %s before: %s after: %s" % (server, status, process.before, process.after)

        print "\n\nTest: SSH Command Output Fail"
        cmd = 'iamfunny'
        status, process = ssh_cmd_output(server, user, password, cmd)
        print "%s ssh_cmd_output fail: status: %s before: %s after: %s" % (server, status, process.before, process.after)

        print "\n\nTest: SSH Pass"
        cmd = 'ls -l'
        process = ssh(server, user, password, cmd)
        print "%s ssh with cmd pass: before: %s after: %s" % (server, process.before, process.after)

        print "\n\nTest: SSH Fail"
        cmd = 'iamfunny'
        process = ssh(server, user, password, cmd)
        print "%s ssh with cmd fail: before: %s after: %s" % (server, process.before, process.after)

        print "\n\nTest: SSH With No Command"
        process = ssh(server, user, password)
        print "%s ssh: before: %s after: %s" % (server, process.before, process.after)

        print "\n\nTest: SSH Recursive"
        cmd = 'ls /home/raman'
        second_user, second_password, second_host = sys.argv[1:4]
        second_prompt = '#'
        process = ssh_recursive_cmd([(user, password, host, prompt), (second_user, second_password, second_host, second_prompt)], cmd)
        print "%s recursive ssh: before: %s after: %s" % (server, process.before, process.after)


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print "exception: %s" % str(e)
        traceback.print_exc()
        sys.exit(1)

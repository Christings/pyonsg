# -*- coding:utf-8 -*-
from datetime import datetime
import pexpect
import re
import time
import threading


# 主方法
def ssh_command(user, host, password, command):
    ssh_new_key = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh -l %s %s %s' % (user, host, command))
    i = child.expect([pexpect.TIMEOUT, ssh_new_key, 'password: '])
    if i == 0:
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        return None
    if i == 1:
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:
            print('ERROR!')
            print('SSH could not login. Here is what SSH said:')
            print(child.before, child.after)
            return None
    child.sendline(password)
    return child

#gpu mem
def gpu_info():
    child = ssh_command("root", "10.153.51.60", "sogourank@2016", "nvidia-smi | grep 250W")
    child.expect(pexpect.EOF)
    gpuinfo = (child.before).decode('utf-8')
    gpu_lst = gpuinfo.strip().split('\r\n')
    print(gpuinfo)
    g_mem=gpu_lst[0].split()[8].split('MiB')[0]
    g_used=gpu_lst[0].split()[12].split('%')[0]
    timedata = datetime.now().strftime('[Date.UTC(%Y,%m,%d,%H,%M,%S)')
    print(timedata+","+g_mem+'],\n')
    print(timedata+","+g_used+'],\n')
#    with open(gpuMem,'a') as mem,open(gpuUsed,'a') as used:
#       print()
#       mem.write(timedata+","+g_mem+'],\n')
#       used.write(timedata+","+g_used+'],\n')
    #time.sleep(5)

# mem
def mem_info():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    child = ssh_command("root", "10.153.51.60", "sogourank@2016",  "cat /proc/meminfo")
    child.expect(pexpect.EOF)
    mem = child.before
    mem_values = re.findall(r"(\d+)\ kB", mem.decode('utf-8'))
    MemTotal = mem_values[0]
    MemFree = mem_values[1]
    Buffers = mem_values[2]
    Cached = mem_values[3]
    SwapTotal = mem_values[13]
    SwapFree = mem_values[14]
    if int(SwapTotal) == 0:
        print("交换内存总共为：0".encode('utf-8'))
    else:
        Rate_Swap = 100 - 100*int(SwapFree)/float(SwapTotal)
        print("交换内存利用率：".encode('utf-8'), Rate_Swap)
    Free_Mem = int(MemFree) + int(Buffers) + int(Cached)
    Used_Mem = int(MemTotal) - Free_Mem
    Rate_Mem = 100*Used_Mem/float(MemTotal)
    print("内存利用率：".encode('utf-8'), str("%.2f" % Rate_Mem), "%")


# io
def vm_stat_info():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    child = ssh_command("root","10.153.51.60", "sogourank@2016",  "vmstat 1 2 | tail -n 1")
    child.expect(pexpect.EOF)
    vmstat_info = child.before.strip().split()
    processes_waiting = vmstat_info[0]
    processes_sleep = vmstat_info[1]
    io_bi = vmstat_info[8]
    io_bo = vmstat_info[9]
    system_interrupt = vmstat_info[10]
    system_context_switch = vmstat_info[11]
    cpu_user = vmstat_info[12]
    cpu_sys = vmstat_info[13]
    cpu_idle = vmstat_info[14]
    cpu_wait = vmstat_info[15]
    print("processes_waiting:", processes_waiting)
    print("processes_sleep:", processes_sleep)
    print("io_bi:", io_bi)
    print("io_bo:", io_bo)
    print("system_interrupt:", system_interrupt)
    print("system_context_switch:", system_context_switch)
    print("cpu_user:", cpu_user)
    print("cpu_sys:", cpu_sys)
    print("cpu_idle:", cpu_idle)
    print("cpu_wait:", cpu_wait)


# cpu
def cpu_info():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    child = ssh_command("root", "10.153.51.60", "sogourank@2016", "cat /proc/cpuinfo")
    child.expect(pexpect.EOF)
    cpuinfo = child.before
    cpu_num = re.findall(r'processor.*?(\d+)', cpuinfo.decode('utf-8'))[-1]
    cpu_num = str(int(cpu_num) + 1)
    print("CPU数目：".encode('utf-8'), cpu_num)


if __name__ == '__main__':
    try:
        t1 = threading.Thread(target=gpu_info)
        t1.start()
    except Exception as e:
        print(str(e))

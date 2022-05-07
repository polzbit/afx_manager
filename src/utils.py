import os
from time import sleep
import subprocess


def _create_process(args):
    CLI_INFO = subprocess.STARTUPINFO()
    CLI_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    CLI_INFO.wShowWindow = subprocess.SW_HIDE
    return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW, startupinfo=CLI_INFO, shell = False)

def _start_process(args, output):
    ready_to_kill = False
    process = _create_process(args)
    for line in process.stdout:
        msg = line.decode('utf-8')
        print(msg)
        if not os.path.exists(output) and not ready_to_kill:
            ready_to_kill = True
        elif ready_to_kill and os.path.exists(output):
            sleep(1)
            _kill("aerender.exe")
            _kill("AfterFX.com")
            process.kill()

    f = open(output, "r")
    lines = f.readlines()
    f.close()
    return lines

def _kill(processName):
    args = r'taskkill /im "%s" /F' % (processName)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=subprocess.DETACHED_PROCESS, shell = False)
    for line in process.stdout:
        pass
    sleep(1)
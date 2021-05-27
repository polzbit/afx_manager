#!/usr/bin/env python3
####################################################################################
#   Adobe After Effects Manager
#   - extract image sequence from aep project using aerender.exe tool
#   - extract compositions names from aep file
####################################################################################
import os
from time import sleep
import subprocess

class ae_manager:
    def __init__(self, afx_path):
        self.AERENDER_PATH = afx_path + "\\Support Files\\aerender.exe"
        self.AFX_PATH = afx_path + "\\Support Files\\afterfx.com"
        self.JSX_SCRIPT =  ".\\get_comp_names.jsx"
        self.DATA_FILE = ".\\output.txt"
        self.ae_errors = ["Could not create the file", "Access was denied", "connection was forcibly closed", "Can't copy"]
    
    def start_img_sequence(self, proj_path, comp_name, start_frame=0, end_frame=0):
        error_raised = False
        # setting up start info for cli
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        # command arguments
        args = [self.AERENDER_PATH, '-project', proj_path, '-comp', comp_name , '-s', str(start_frame),'-e', str(end_frame),'-v', "ERRORS_AND_PROGRESS",  '-close', 'DO_NOT_CLOSE'] # clos_flag defualt is 'DO_NOT_SAVE_CHANGES'
        if end_frame == 0:
            args = [self.AERENDER_PATH, '-project', proj_path, '-comp', comp_name , '-v', "ERRORS_AND_PROGRESS",  '-close', 'DO_NOT_CLOSE'] 
        
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW, startupinfo=startupinfo, shell = False)
        # start getting data from aerender.exe
        for line in process.stdout:
            msg = line.decode('utf-8')
            for er in self.ae_errors:
                if er in msg:
                    error_raised = True
                    self.kill("aerender.exe")
                    self.kill("AfterFX.com")
                    process.kill()
                    break
            if error_raised:
                print("Error couldn't finish image sequence.")
                break
            print(msg)
        # end getting data from aerender.exe
        # check for errors
        if not error_raised:
            print("Success image sequence completed.")
        return error_raised

    def get_compositions(self, proj_path):
        content = [] 
        # setting info adobe ExtendScript 
        f = open(self.DATA_FILE, "w")
        f.write(proj_path)
        f.close()
        # setting up start info for cli
        info = subprocess.STARTUPINFO()
        info.dwFlags = 1
        info.wShowWindow = 0
        # lunch after effects at background and run jsx script 
        mycmd = r'"%s" -r -m -noui -s "%s"' % (self.AFX_PATH, self.JSX_SCRIPT) 
        # os.system(mycmd)
        process = subprocess.Popen(mycmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, startupinfo=info, creationflags=subprocess.CREATE_NO_WINDOW , shell = False)
        print("Extracting compositions data...")
        ready_to_kill = False
        for line in process.stdout:
            msg = line.decode('utf-8')
            print(msg)
            if not os.path.exists(self.DATA_FILE) and not ready_to_kill:
                ready_to_kill = True
            elif ready_to_kill and os.path.exists(self.DATA_FILE):
                sleep(1)
                self.kill("AfterFX.com")
                process.kill()
        
        f = open(self.DATA_FILE, "r")
        lines = f.readlines()
        f.close()
        # check if script extract compositions names from file
        if proj_path not in lines:
            for x in lines:
                data = x.strip().split("|")
                content.append(data)
        else:
            print("Failed to extract compositions names")
        return content             
        

    def kill(self, processName):
        com = r'taskkill /im "%s" /F' % (processName)
        process = subprocess.Popen(com, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=subprocess.DETACHED_PROCESS, shell = False)
        for line in process.stdout:
            pass
        sleep(1)

 

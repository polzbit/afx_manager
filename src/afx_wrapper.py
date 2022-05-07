#!/usr/bin/env python3
from time import sleep
from psutil import process_iter
from utils import _create_process, _start_process, _kill
import os
import sys

class afx_wrapper:
    def __init__(self, config):
        self.init(config)
        self.AERENDER_PATH = config['AFX_PATH'] + "\\Support Files\\aerender.exe"
        self.AFX_PATH = config['AFX_PATH']  + "\\Support Files\\afterfx.com"
        self.JSX_SCRIPTS =  {
            'GET_COMP_NAMES': config['JSX_PATH']  + "\\get_comp_names.jsx",
            'RENDER_IMG_SEQUENCE': config['JSX_PATH']  + "\\render_sequence.jsx",
            'RENDER_AUDIO': config['JSX_PATH']  + "\\render_audio.jsx",
            'RENDER_VID_FROM_SEQUENCE': config['JSX_PATH']  + "\\render_vid.jsx",
        }
        self.DATA_FILE = config['OUTPUT_FILE'] + "\\output.txt"
        self.ae_errors = ["Could not create the file", "Access was denied", "connection was forcibly closed", "Can't copy"]
    
    def init(self, config):
        if not os.path.exists(config['AFX_PATH']):
            sys.exit("[!] Cannot find Adobe After Effects.")
        if not os.path.exists(config['JSX_PATH']):
            sys.exit("[!] Cannot find jsx scripts.")

    def start_img_sequence(self, proj_path, comp_name, out_path, fps=30):
        error_raised = False
        f = open(self.DATA_FILE, "w")
        f.write(f'{proj_path};{comp_name};{fps};{out_path}')
        f.close() 
        args = [self.AFX_PATH, '-r', '-m', '-noui', '-s', self.JSX_SCRIPTS['RENDER_IMG_SEQUENCE']]
        process = _create_process(args)
        for line in process.stdout:
            msg = line.decode('utf-8')
            for er in self.ae_errors:
                if er in msg:
                    error_raised = True
                    _kill("aerender.exe")
                    _kill("AfterFX.com")
                    process.kill()
                    break
            if error_raised:
                print("Error couldn't finish image sequence.")
                break
            print(msg)
        # check for errors
        if not error_raised:
            print("Success image sequence completed.")
        return error_raised

    def get_compositions(self, proj_path):
        content = [] 
        f = open(self.DATA_FILE, "w")
        f.write(proj_path)
        f.close() 
        args = [self.AFX_PATH, '-r', '-m', '-noui', '-s', self.JSX_SCRIPTS['GET_COMP_NAMES']]
        print("Extracting compositions data...")
        data = _start_process(args, self.DATA_FILE)
        for x in data:
            info = x.strip().split("|")
            content.append({'name':info[0], 'duration':info[1], 'fps': info[2]})
   
        return content             
        
    def render_vid(self, first_psd_file, preset, duration, output_name, fps=30, audio_out='0'):
        f = open(self.DATA_FILE, "w")
        f.write(f'{first_psd_file};{preset};{fps};{audio_out};{output_name};{duration}')
        f.close()     
        # lunch after effects at background and run jsx script 
        args = [self.AFX_PATH, '-r', '-m', '-noui', '-s', self.JSX_SCRIPTS['RENDER_VID_FROM_SEQUENCE']]
        data = _start_process(args, self.DATA_FILE)

        while self.is_afx_running():
            sleep(2)
        if data != 'error': 
            print("[@ AFX ] Video generated: " + output_name)
        else:
            print("[@ AFX ] Failed to generate video: " + output_name)
        # remove cached audio
        if f'{os.environ["APPDATA"]}' in audio_out and os.path.exists(audio_out):
            os.remove(audio_out)
        
        return data != 'error'

    def render_audio(self, proj_path, comp, audio_out):
        f = open(self.DATA_FILE, "w")
        f.write(f'{proj_path};{comp};{audio_out}')
        f.close()     
        # lunch after effects at background and run jsx script 
        args = [self.AFX_PATH, '-r', '-m', '-noui', '-s', self.JSX_SCRIPTS['RENDER_AUDIO']]
        data = _start_process(args, self.DATA_FILE)

        while self.is_afx_running():
            sleep(2)

        if data != 'error': 
            print("[@ AFX ] Audio generated: " + audio_out)
        else:
            print("[@ AFX ] Failed to generate audio: " + audio_out)
        
        return data != 'error'
        
    def is_afx_running(self):
        return "AfterFx.com" in (p.name() for p in process_iter())


 

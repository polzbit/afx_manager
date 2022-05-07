from config import config
from afx_wrapper import afx_wrapper
import os

if __name__ == "__main__":
    project_path = 'project.aep'
    afx = afx_wrapper(config)
    # extract compositions info from render queue in aep file
    compositions = afx.get_compositions(project_path)
    # render audio for aep file (Note: make sure you WAV preset in your adobe after effects)
    audio_output = './audio/project.wav'
    afx.render_audio(project_path, compositions[0]['name'], audio_output)
    # render psd sequence
    sequence_output = './sequence'
    afx.start_img_sequence(project_path, compositions[0]['name'], sequence_output, compositions[0]['fps'])
    # render video from psd sequence
    frames = os.listdir(sequence_output)
    first_frame = sequence_output + '/' + frames[0]
    vid_output = './video/project.mov'
    afx.render_vid(first_frame, 'ProRes', compositions[0]['duration'],vid_output, compositions[0]['fps'], audio_output)
    


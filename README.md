# Adobe After Effects Wrapper

a wrapper for adobe after effects, it uses adobe ExtendScript to extract compositions info from render queue, extract psd sequence, render audio and render video from psd sequence. <br/>


## Usage
- set adobe after effects path in the config file. <br/>
- for audio rendering make sure you have the preset 'WAV' in your adobe after effects presets, if not just create it.<br/>
- for video rendering make sure you have the preset 'ProRes' in your adobe after effects presets, if not just create it.<br/>
- check start.py for example
## Future
currently the scripts only render .mov video files, i'll be adding ffmepg support to render the psd sequence in other formats.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

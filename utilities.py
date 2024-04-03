"""
NaStiPy.utilities (Naturalistic Stimuli in Python)
=====================
"""

__author__ = ["Billy Mitchell"]
__license__ = "MIT"

import warnings
import os
# import sounddevice as sd
# import lameenc
# import wave
from psychopy import data, gui, core, visual
import time

# ----- CREATE LOG -----
def make_log(experiment, subject, condition, date, path, psychopy_version):

    filename = _thisDir + os.sep + u'data/%s_%s_%s%s_%s' % (experiment, subject, 'Condition-', condition, date)
    
    return(data.ExperimentHandler(name=experiment, version='',
                                 extraInfo=subject, runtimeInfo=None,
                                 originPath=path,
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename))

# ----- UPDATE LOG -----
def update_log(log, Func = 'NA', Video = 'NA', CertRate = 'NA', CertStat = 'NA', Keys = 'NA', Text = 'NA', RespTime = 'NA', Onset = 'NA', Offset = 'NA', SystemTime_Start = 'NA', SystemTime_Stop = 'NA', FrameTimestamps = 'NA'):
    
    """
    update_log simplifies data logging of modular task components. It accepts a data.ExperimentHandler object and adds information for this task.
    
    Args:
        log: Accepts a pre-existing data.ExperimentHandler object to modify
        Func: Accepts any string, which would ideally be the name of the task
        Video: Accepts any string, which would ideally be the name of the stimulus
        CertRate: Accepts any data, which would ideally be data collected in this event
        CertStat: Accepts any data, which would ideally be data collected in this event 
        Keys: Accepts any string, which would ideally be the keys pressed during this event
        Text: Accepts any string, which would ideally be the text presented during this event
        RespTime: Accepts any data, which would ideally be the response time of key presses in this event
        Onset: Accepts any data, which would ideally be the relative time that this event started 
        Offset: Accepts any data, which would ideally be the relative time that this event ended 
        SystemTime_Start: Accepts any data, which would ideally be the global time that this event started
        SystemTime_Stop: Accepts any data, which would ideally be the global time that this event ended
        FrameTimestamps: Accepts any data, which would ideally be the frame rates of this event

    Returns:
        log: (data.ExperimentHandler) an updated data object

    """
    
    # Notes on Future Improvements:
    # + Video should be changed to stimulus
    # + Func should be changed to task
    # + CertRate should be changed to data
    # + I should double check what frame timestamps and cert stat capture 

    log.addData("Func", Func)
    log.addData("Video", Video)
    log.addData('CertRate', CertRate)
    log.addData("CertStat", CertStat)
    log.addData('Keys', Keys)
    log.addData('Text', Text)
    log.addData('RespTime', RespTime)
    log.addData('Onset', Onset)
    log.addData('Offset', Offset)
    log.addData('SystemTime_Start', SystemTime_Start)
    log.addData('SystemTime_Stop', SystemTime_Stop)
    log.addData('FrameTimestamps', FrameTimestamps)
    log.nextEntry()

    return(log)

# ----- KEY_OR_TIME ----
def key_or_time(win, duration, keyboard):

    """
    key_or_time simplifies the mechanism which determines when many task functions should end. It accepts either a key string or an integer and filters and changes how the task progresses depending upon the duration type. 
    
    Args:
        duration: Either an integer or the name of a key; for how long or until what 
        text: a PsychoPy.visual.TextStim() object
        keyboard: a PsychoPy.hardware.keyboard.keyboard() object

    Returns:

    """
        # If duration is an integer ...
    if isinstance(duration, int) or isinstance(duration, float):
        
        # Wait out the duration 
        start_time = time.time()

        while time.time() - start_time < duration:
        
            # If escape is pressed 
            if keyboard.getKeys(keyList=["escape"]):
                
                # End the experiment
                core.quit()

    # If duration is a string ...
    elif isinstance(duration, str):

        # Set a variable to track key presses
        key_pressed = False
        response = {'keys': None, 'rt': None}

        # ... and while that variable is false
        while not key_pressed:

            # Save any key presses that do occur
            keys = keyboard.getKeys(keyList=[duration])

            # If key presses have been registered
            if keys:

                # Change that tracking variable to true
                key_pressed = True

                # Save which keys were pressed
                response['keys'] = keys[-1].name

                # Save the response time of key presses
                response['rt'] = keys[-1].rt

            # However, if the escape key is pressed
            elif keyboard.getKeys(keyList=["escape"]):

                # End the experiment
                core.quit()

            # Otherwise ...
            else:

                # Flip the window
                win.flip()

        return response

# ----- DYNAMIC_SLIDER -----
# def dynamic_slider(win, label_R, label_L, image, scale_color):

# ----- WAV_TO_MP3 -----
# def wav_to_mp3(input, output, quality = 5):
  
#     """
#     wav_to_mp3 converts high-quality-but-bulky .wav formatted audio files to relatively smaller .mp3 audio files. Pydub is the most common means of doing this, but relies on ffmpeg being added to the psychopy path manually. As such, I've elected to instead rely on lameenc and wave because they do not depend upon external dependencies

#     Args:
#         input: The filepath, including the file name of the .wav you wish to input; should end in '.wav'
#         output: The filepath, including the file name of the .mp3 you wish to output; should end in '.mp3'
#         quality: An integer between 1 and 7 representing the quality of the subsequent .mp3; lower numbers represent higher quality 

#     Returns:

#     """

#     # Notes on Future Improvements:
#     # + Video should be changed to stimulus
#     # + Func should be changed to task
#     # + CertRate should be changed to data
#     # + I should double check what frame timestamps and cert stat capture 

#     # Open the WAV file
#     with wave.open(input, 'rb') as wav_file:
#         # Read the WAV file parameters
#         channels = wav_file.getnchannels()
#         frame_rate = wav_file.getframerate()
#         n_frames = wav_file.getnframes()
        
#         # Read the WAV file data
#         wav_data = wav_file.readframes(n_frames)

#     # Set up the MP3 encoder
#     encoder = lameenc.Encoder()
#     encoder.set_bit_rate(128)
#     encoder.set_in_sample_rate(frame_rate)
#     encoder.set_channels(channels)
#     encoder.set_quality(quality)  # 2=high, 5 = medium, 7=low

#     # Encode the WAV data to MP3
#     mp3_data = encoder.encode(wav_data)
#     mp3_data += encoder.flush()

#     # Save the MP3 data to a file
#     with open(output, 'wb') as mp3_file:
#         mp3_file.write(mp3_data)

#     print("Conversion complete!")

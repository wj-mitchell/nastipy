"""
NaStiPy.tasks (Naturalistic Stimuli in Python)
=====================
"""

__author__ = ["Billy Mitchell"]
__license__ = "MIT"

import warnings
import os
import sounddevice as sd
import numpy as np
import time
from psychopy import visual, core, event, prefs
prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound  # Import sound after setting preferences
from psychopy.hardware import keyboard
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from scipy.io import wavfile
import datetime
from nastipy import utilities

# + Create a task to accept ratings before active_view

# ----- TEXT_DISPLAY -----
def text_display(win, text, duration, log=None, text_color = 'white', text_height = 0.065, wrap_width = 1.45, task_name = 'instructions'):

    """
    text_display draws text on the window. If duration is an integer, it will appear for a number of seconds equal to that integer. If duration is the name of a recognized key, the fixation will appear until that key is pressed 
    
    Args:
        win: Defining the window to use
        log: An optional ExperimentHandler dataframe to record event-related details
        text: The text that you'd like to appear in your instructions
        duration: Either an integer or the name of a key; for how long or until what condition is met should the fixation be apparent 
        text_color: The color of the fixation
        text_height: The height of the fixation cross
        wrap_width: How long before text should break and wrap to the next line
        task_name: The name that appears on the log for this event
    Returns:

    """
    
    # Notes on Future Improvements:
    # + Add QAs and warnings

    # Start the clock
    ts_start = datetime.datetime.now()

    # Define our text object
    text = visual.TextStim(win=win, text=text, pos=[0,0], height=text_height, wrapWidth=wrap_width, color=text_color, autoDraw = True)
    
    # Flipping the window
    win.flip()

    # Initializing keyboard
    kb = keyboard.Keyboard()

    # If duration is an integer ...
    if isinstance(duration, int) or isinstance(duration, float):
        
        # Custom utility function to progress the event
        utilities.key_or_time(win = win, duration = duration, keyboard = kb)
    
    # If duration is a string ...
    elif isinstance(duration, str):
        
        # Custom utility function to progress the event
        response = utilities.key_or_time(win = win, duration = duration, keyboard = kb)

    # Stop drawing the text
    text.setAutoDraw(False)

    # Flip the window
    win.flip()

    # Stop the clock
    ts_end = datetime.datetime.now()

    # If a log was submitted
    if log is not None:

        # ... and this is a timed fixation, log it as such
        if isinstance(duration, int) or isinstance(duration, float):
            utilities.update_log(Func = task_name, Text = text,
                    Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    SystemTime_Start= ts_start, SystemTime_Stop=ts_end)
        
        # ... and this is not a timed fixation, log it as such
        elif isinstance(duration, str):
            utilities.update_log(Func = task_name, Keys= response["keys"],
                    Text = text, RespTime=response["rt"],
                    Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    SystemTime_Start= ts_start, SystemTime_Stop=ts_end)

# ----- FIXATION -----
def fixation(win, duration, log = None, text_color = 'white', text_height = 0.10):
   
    """
    fixation draws a fixation cross centered on the window. It can be used as an interstimulus or intertrial interval. If duration is an integer, it will appear for a number of seconds equal to that integer. If duration is the name of a recognized key, the fixation will appear until that key is pressed. 
    
    Args:
        win: Defining the window to use
        log: An optional ExperimentHandler dataframe to record event-related details
        duration: Either an integer or the name of a key; for how long or until what condition is met should the fixation be apparent 
        text_color: The color of the fixation
        text_height: The height of the fixation cross
        
    Returns:

    """
    
    # Notes on Future Improvements:
    # + Add QAs and warnings

    # Using the text_display command
    text_display(win = win, log = log,text = '+', duration = duration, text_color = text_color, text_height = text_height, wrap_width = 1.45, task_name = 'fixation')
  
# ----- MRI TRIGGER -----    
def trigger(win, log = None, text = 'The video will begin momentarily....', trigger_key = "equal", text_color = 'white', text_height = 0.1, wrap_width = 1.35):
    
    """
    trigger 
    
    Args:
        win: Defining the window to use
        log: An optional ExperimentHandler dataframe to record event-related details
        text: The text that you'd like to appear in your instructions
        
    Returns:

    """
    
    # Notes on Future Improvements:
    # + Add QAs and warnings

    # Using the text_display command
    text_display(win = win, log = log, text = text, duration = trigger_key, text_color = text_color, text_height = text_height, wrap_width = 1.45, task_name = 'trigger')

# ----- BACKGROUND INFORMATION -----
def backinfo(win, duration, text, character_name_L, character_role_L, character_image_L, log = None, text_color = 'white', text_height = 0.40, text_ypos = -0.05, wrap_width = 1.33, character_name_R = None, character_role_R = None, character_image_R = None, image_xpos = 0.35, image_ypos = 0.22, image_size = 0.44, task_name = 'backinfo'):

    
    """
    backinfo . If only one character needs to be presented, character_R details can be set to 'None'. 
    
    Args:
        
    Returns:

    """
    
    # Notes on Future Improvements:
    # + Allow image_size to be a vector for images that are not square shaped

    # Start the clock
    ts_start = datetime.datetime.now()

    # Define our text and image objects
    Information = visual.TextStim(win=win, text= text, pos=(0,-.30), height=text_height, wrapWidth=wrap_width, color=text_color, autoDraw = True);
    Image_L = visual.ImageStim(win=win, image=character_image_L, mask=None, ori=0.0, pos=(-(image_xpos), image_ypos), size=(image_size, image_size), color=[1,1,1], colorSpace='rgb', texRes=128.0, interpolate=True, depth=-4.0, autoDraw = True)
    Character_L = visual.TextStim(win=win, text=f"{character_role_L}:\n{character_name_L}",pos=(-(image_xpos), text_ypos), height=0.040, color='white', alignText='center', autoDraw = True);

    if character_image_R is not None:
        Image_R = visual.ImageStim(win=win, image=character_image_R, mask=None, ori=0.0, pos=(image_xpos, image_ypos), size=(image_size, image_size), color=[1,1,1], colorSpace='rgb', texRes=128.0, interpolate=True, depth=-4.0, autoDraw = True)
        Character_R = visual.TextStim(win=win, text=f"{character_role_R}:\n{character_name_R}",pos=(image_xpos, text_ypos), height=0.040, color='white', alignText='center', autoDraw = True);
    
    # Flipping the window
    win.flip()

    # Initializing keyboard
    kb = keyboard.Keyboard()
    kb.clearEvents()

    # If duration is an integer ...
    if isinstance(duration, int) or isinstance(duration, float):
        
        # Custom utility function to progress the event
        utilities.key_or_time(win = win, duration = duration, keyboard = kb)
    
    # If duration is a string ...
    elif isinstance(duration, str):
        
        # Custom utility function to progress the event
        response = utilities.key_or_time(win = win, duration = duration, keyboard = kb)

    # Stop drawing the text
    Information.setAutoDraw(False)
    Image_L.setAutoDraw(False)
    Character_L.setAutoDraw(False)
    
    if character_image_R is not None:
        Image_R.setAutoDraw(False)
        Character_R.setAutoDraw(False)

    # Flip the window
    win.flip()

    # Stop the clock
    ts_end = datetime.datetime.now()

    # If a log was submitted
    if log is not None:

        # ... and this is a timed fixation, log it as such
        if isinstance(duration, int) or isinstance(duration, float):
            utilities.update_log(Func = task_name, Text = text,
                    Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    SystemTime_Start= ts_start, SystemTime_Stop=ts_end)
        
        # ... and this is not a timed fixation, log it as such
        elif isinstance(duration, str):
            utilities.update_log(Func = task_name, Keys= response["keys"],
                    Text = text, RespTime= response["rt"],
                    Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                    SystemTime_Start= ts_start, SystemTime_Stop=ts_end)

# ----- PLAYING VIDEO -----
def passive_view(win, video, units ='height', video_name = None, log=None, mute_audio=False, size=0.075, ypos=0.045, task_name = 'passive_view'):

    """
    passive_view is a modular task component which, simply, plays a video.
    
    Args:
        
    Returns:

    """
    
    # Notes on Future Improvements:

    # Start the clock
    ts_start = datetime.datetime.now()

    # Initializing keyboard
    kb = keyboard.Keyboard()

    # Defining our video object
    Stimulus = visual.MovieStim(win=win, units = units, size=[(16*size), (9*size)], pos=(0, ypos), filename=video, name=video_name, loop=False, noAudio=mute_audio)

    # Start the stimulus
    Stimulus.play()

    # If the stimulus is still playing
    while Stimulus.status != visual.FINISHED:
        
        # Draw the current frame
        Stimulus.draw()

        # Flip the window
        win.flip()

        # and escape is pressed
        if kb.getKeys(keyList=["escape"]):

            # Quite the task
            core.quit()

    # Flip the window & Stop the video
    win.flip()
    Stimulus.stop()

    # Stop the clock
    ts_end = datetime.datetime.now()

    # If a log was submitted
    if log is not None:

        utilities.update_log(Func = task_name, Video = video_name,
                Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                SystemTime_Start= ts_start, SystemTime_Stop=ts_end)

# ----- RATING VIDEO -----
def pre_active(win, text, done_key, label_L, label_R, key_L, key_R, scale_color, text_height = 0.065, text_color = 'white', wrap_width = 1.33, log=None, increments = 5, task_name = 'pre_active'):

    """
    pre_active 
    
    Args:
        
    Returns:

    """
    
    # Notes on Future Improvements:

    # Start the clock
    ts_start = datetime.datetime.now()

    # Initializing keyboard
    kb = keyboard.Keyboard()

    # Defining our text and image objects
    Dynamic_Feedback = visual.TextStim(win=win, text='', pos=[0,-0.462], height=0.038, wrapWidth=1.55,color='white', autoDraw = True)
    PoleValue_L = visual.TextStim(win=win, text='100%', pos=(-0.483, -0.31), height=0.031, color='white', autoDraw = True)
    PoleValue_R = visual.TextStim(win=win, text='100%', pos=(0.497, -0.31), height=0.031, color='white', autoDraw = True)
    ScaleMidpoint = visual.TextStim(win=win, text="0%", pos=(0,-0.31), height=0.031, color="white", autoDraw = True)
    PoleLabel_R = visual.TextStim(win=win, text=label_R, pos=(0.615, -0.39), height=0.045, color='white', autoDraw = True)
    PoleLabel_L = visual.TextStim(win=win, text=label_L, pos=(-0.615, -0.39), height=0.045, color='white', autoDraw = True)

    # Defining our dynamic scale
    Increment = 0.001 * increments
    Current_Scale_Position = 0
    Current_Scale_Value = 0
    CertaintyRatings = visual.Slider(win=win, size=(0.995, 0.11), pos=(0,  -0.39), units=None, labels=None, ticks=[1,2,3], granularity=0.0, style='slider', styleTweaks=(), opacity=1.0, color='black', fillColor='darkblue', borderColor='White', colorSpace='rgb', font='Open Sans', labelHeight=0.05, flip=False, readOnly=False)
    innScale = visual.Rect(win=win, width=(Current_Scale_Position, 0.11)[0], height=(Current_Scale_Position, 0.18)[1], ori=0.0, pos=(0.6, 0),lineWidth=1.0,  colorSpace='rgb',  lineColor='darkGrey', fillColor= scale_color, opacity=0.75, depth=-6.0, interpolate=True, autoDraw = True)

    # Define our text object
    text = visual.TextStim(win=win, text=text, pos=[0,0], height=text_height, wrapWidth=wrap_width, color=text_color, autoDraw = True)
    
    # If the stimulus is still playing
    while True:
        
        # Capturing which keys have been pressed
        keys = kb.getKeys()

        # Extract key names
        key_names = [key.name for key in keys]

        # If the done_key is pressed, break the loop
        if done_key in key_names:
            break
        
        # Draw the current frame
        CertaintyRatings.draw()

        # Flip the window
        win.flip()

        # If the left key is pressed
        if len(kb.getKeys([key_L], waitRelease = True, clear = True)) == 1:

            # Change the value of Current_Scale_Position
            Current_Scale_Position -= round(Increment * 5, 3)

            # ... and clear the event log for kb
            kb.clearEvents()

        if len(kb.getKeys([key_R], waitRelease = True, clear = True)) == 1:

            # Change the value of Current_Scale_Position
            Current_Scale_Position += round(Increment * 5, 3)
            
            # ... and clear the event log for kb
            kb.clearEvents()

        # Keep Current_Scale_Position to only 3 digits
        Current_Scale_Position = round(Current_Scale_Position,3)

        # Convert the Current_Scale_Position position to an integer
        Current_Scale_Value = int(round(abs(Current_Scale_Position * 200), 0))

        # If that integer is greater than 100
        if Current_Scale_Value >= 100:

            # Make its value 100
            Current_Scale_Value = 100      

        # If Current_Scale_Position is 0     
        if Current_Scale_Position == 0:

            # Reset Current_Scale_Value to 0
            Current_Scale_Value = 0

        # If Current_Scale_Position reaches an increment which would be associated with a Current_Scale_Value value above 100
        if Current_Scale_Position >= Increment * 100:

            # Reset Current_Scale_Position and Current_Scale_Value
            Current_Scale_Position = Increment * 100
            Current_Scale_Value = 100 

         # If Current_Scale_Position reaches an increment which would be associated with a Current_Scale_Value value above 100
        if Current_Scale_Position <= -(Increment * 100):

             # Reset Current_Scale_Position and Current_Scale_Value
            Current_Scale_Position = -(Increment * 100)
            Current_Scale_Value = 100     

        if Current_Scale_Position>=0:
            Current_Scale_ValueStr = str(Current_Scale_Value)
            Dynamic_Feedback.setText(Current_Scale_ValueStr + "% Certain")

        elif Current_Scale_Position<0:
            Current_Scale_ValueStr = str(Current_Scale_Value)
            Dynamic_Feedback.setText(Current_Scale_ValueStr + "% Certain")

        innScale.setPos(((Current_Scale_Position/2), -0.39))
        innScale.setSize((Current_Scale_Position, 0.11))

        # and escape is pressed
        if kb.getKeys(keyList=["escape"]):

            # Quite the task
            core.quit()

    # Stop the video and related components
    components = [Dynamic_Feedback, PoleValue_L, PoleValue_R, ScaleMidpoint, PoleLabel_R, PoleLabel_L, CertaintyRatings, innScale, text]
    for COMPONENT in components:
        COMPONENT.setAutoDraw(False)
        
    # Flip the window & Stop the Video
    win.flip()

    # Stop the clock
    ts_end = datetime.datetime.now()

    # If a log was submitted
    if log is not None:

        utilities.update_log(Func = task_name, CertRate = Current_Scale_Position,
                   Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                   Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'), SystemTime_Start= ts_start, SystemTime_Stop=ts_end)
    
    return(Current_Scale_Position)

# ----- RATING VIDEO -----
def active_view(win, video, video_name, label_L, label_R, key_L, key_R, scale_color, starting_scale_position = 0, units ='height', log=None, mute_audio=False, size=0.075, ypos=0.045, increments = 5, image=None, framerate_sample_interval = 5, task_name = 'active_view'):

    """
    active_view 
    
    Args:
        
    Returns:

    """
    
    # Notes on Future Improvements:
    # + Make the scale a separate function
    # + Add a frame rate tracker
    # + Turn this into a class
    # + Add an argument to specify the starting scale position 
    # * Current increment set up would only work if the increments is set to 5. Correct that. 

    # Start the clock
    ts_start = datetime.datetime.now()

    # Initializing keyboard
    kb = keyboard.Keyboard()

    # Defining our text and image objects
    Dynamic_Feedback = visual.TextStim(win=win, text='', pos=[0,-0.462], height=0.038, wrapWidth=1.55,color='white', autoDraw = True)
    PoleValue_L = visual.TextStim(win=win, text='100%', pos=(-0.483, -0.31), height=0.031, color='white', autoDraw = True)
    PoleValue_R = visual.TextStim(win=win, text='100%', pos=(0.497, -0.31), height=0.031, color='white', autoDraw = True)
    ScaleMidpoint = visual.TextStim(win=win, text="0%", pos=(0,-0.31), height=0.031, color="white", autoDraw = True)
    PoleLabel_R = visual.TextStim(win=win, text=label_R, pos=(0.615, -0.39), height=0.045, color='white', autoDraw = True)
    PoleLabel_L = visual.TextStim(win=win, text=label_L, pos=(-0.615, -0.39), height=0.045, color='white', autoDraw = True)
    if image is not None:
        Static_Image = visual.ImageStim(win=win, image=image, pos=(0, 0.2), size=(0.3, 0.3), autoDraw = True)
        Static_Text = visual.TextStim(win=win, text='Target Image:', pos=(0, 0.35), height=0.03, color='white', autoDraw = True)

    # Defining our dynamic scale
    Increment = 0.001 * increments
    Current_Scale_Position = starting_scale_position
    Current_Scale_Value = int(round(abs(round(Current_Scale_Position * Increment * 5, 3) * 200), 0))
    CertaintyRatings = visual.Slider(win=win, size=(0.995, 0.11), pos=(0,  -0.39), units=None, labels=None, ticks=[1,2,3], granularity=0.0, style='slider', styleTweaks=(), opacity=1.0, color='black', fillColor='darkblue', borderColor='White', colorSpace='rgb', font='Open Sans', labelHeight=0.05, flip=False, readOnly=False)
    innScale = visual.Rect(win=win, width=(Current_Scale_Position, 0.11)[0], height=(Current_Scale_Position, 0.18)[1], ori=0.0, pos=(0.6, 0),lineWidth=1.0,  colorSpace='rgb',  lineColor='darkGrey', fillColor= scale_color, opacity=0.75, depth=-6.0, interpolate=True, autoDraw = True)
   
    # Creating arrays in which to store data
    Scale_Value = []
    Scale_Label = []
    Frame_Rate = []

    # # Create a clock to track time
    # clock = core.Clock()
    # clock.reset()

    # Defining our video object
    Stimulus = visual.MovieStim(win=win, units = units, size=[(16*size), (9*size)], pos=(0, ypos), filename=video, name = video_name, loop = False, noAudio=mute_audio)

    # If the stimulus is still playing
    while Stimulus.status != visual.FINISHED:

        # Draw the current frame
        Stimulus.draw()
        CertaintyRatings.draw()

        # Flip the window
        win.flip()

        #  # Check if it's time to sample the frame rate
        # if clock.getTime() >= framerate_sample_interval:
            
        #     # Sample the frame rate
        #     Current_Frame_Rate = win.getActualFrameRate()
        #     Frame_Rate.append(Current_Frame_Rate)

        #     # Reset the clock
        #     clock.reset()

        # If the left key is pressed
        if len(kb.getKeys([key_L], waitRelease = True, clear = True)) == 1:

            # Change the value of Current_Scale_Position
            Current_Scale_Position -= round(Increment * 5, 3)

            # ... and clear the event log for kb
            kb.clearEvents()

        if len(kb.getKeys([key_R], waitRelease = True, clear = True)) == 1:

            # Change the value of Current_Scale_Position
            Current_Scale_Position += round(Increment * 5, 3)
            
            # ... and clear the event log for kb
            kb.clearEvents()

        # Keep Current_Scale_Position to only 3 digits
        Current_Scale_Position = round(Current_Scale_Position,3)

        # Convert the Current_Scale_Position position to an integer
        Current_Scale_Value = int(round(abs(Current_Scale_Position * 200), 0))

        # If that integer is greater than 100
        if Current_Scale_Value >= 100:

            # Make its value 100
            Current_Scale_Value = 100      

        # If Current_Scale_Position is 0     
        if Current_Scale_Position == 0:

            # Reset Current_Scale_Value to 0
            Current_Scale_Value = 0

        # If Current_Scale_Position reaches an increment which would be associated with a Current_Scale_Value value above 100
        if Current_Scale_Position >= Increment * 100:

            # Reset Current_Scale_Position and Current_Scale_Value
            Current_Scale_Position = Increment * 100
            Current_Scale_Value = 100 

         # If Current_Scale_Position reaches an increment which would be associated with a Current_Scale_Value value above 100
        if Current_Scale_Position <= -(Increment * 100):

             # Reset Current_Scale_Position and Current_Scale_Value
            Current_Scale_Position = -(Increment * 100)
            Current_Scale_Value = 100     

        if Current_Scale_Position>=0:
            Scale_Label.append(label_R)
            Current_Scale_ValueStr = str(Current_Scale_Value)
            Scale_Value.append(Current_Scale_ValueStr)
            Dynamic_Feedback.setText(Current_Scale_ValueStr + "% Certain")

        elif Current_Scale_Position<0:
            Scale_Label.append(label_L)
            Current_Scale_ValueStr = str(Current_Scale_Value)
            Scale_Value.append("-" + Current_Scale_ValueStr)
            Dynamic_Feedback.setText(Current_Scale_ValueStr + "% Certain")

        innScale.setPos(((Current_Scale_Position/2), -0.39))
        innScale.setSize((Current_Scale_Position, 0.11))

        # and escape is pressed
        if kb.getKeys(keyList=["escape"]):

            # Quite the task
            core.quit()

    # Stop the video and related components
    if image is not None:
        components = [Dynamic_Feedback, PoleValue_L, PoleValue_R, ScaleMidpoint, PoleLabel_R, PoleLabel_L, Static_Image, Static_Text, CertaintyRatings, innScale, Stimulus]
    if image is None:
        components = [Dynamic_Feedback, PoleValue_L, PoleValue_R, ScaleMidpoint, PoleLabel_R, PoleLabel_L, CertaintyRatings, innScale, Stimulus]
    for COMPONENT in components:
        COMPONENT.setAutoDraw(False)
        
    # Flip the window & Stop the Video
    win.flip()
    Stimulus.stop()

    # Stop the clock
    ts_end = datetime.datetime.now()

    # If a log was submitted
    if log is not None:

        utilities.update_log(Func = task_name, Video = video_name, CertRate = Scale_Value,
                   CertStat = Scale_Label, Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                   Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'), SystemTime_Start= ts_start, SystemTime_Stop=ts_end)

# ----- FREE RECALL -----
def free_recall(win, log=None, device_info = sd.query_devices(None, 'input'), sample_rate = 'default_samplerate', output_file = 'recording', image='record.png', show_volume = True, target_volume = 50, volume_sensitivity = 150, volume_color = 'darkblue', trigger_text = "Waiting for scanner...", trigger_key = 'equal', end_key = 'space', task_name = 'free_recall'): 

    """
    free_recall is a modular task component which, upon receiving a trigger key, begins recording audio from the default microphone of the computer running it. It draws a live volume tracker to the right of the target image to give participants feedback regarding their speaking voices. It will recording indefinitely until the end key is pressed. Once completed, it will generate a .wav formatted output file.
    
    Required Args:
        win: Defining the window to use
        log: An optional ExperimentHandler dataframe to record event-related details
        device_info: A sounddevice object containing information regarding which microphone to use; will use the default microphone if not specified
        sample_rate: A string referring to the sample rate of the microphone
        output_file: Defining the name of the file that should be output to the current working directory
        output_format: The format of the output audio file ('.wav' or '.mp3'). 
        image: Defining which image to draw in the center of the window while free recall is being recorded
        show_volume: Boolean value; if false, no volume tracker will be shown
        target_volume: Accepts integers between 0 and 100; draws a horizontal red bar on tracker to highlight the volume above which participants should aim to speak 
        volume_sensitivity: Defining how sensitive the volume bar should be; larger numbers are less sensitive
        volume_color: Defining the color of the volume bar; accepts the standard fillColor options that PsychoPy visual objects do
        trigger_text: A string that appears before the task begins
        trigger_key: The key that will start the process
        end_key: The key that will end the process

    Returns:
        data: (np.dataframe) data regarding this task
        recording: (.wav or .mp3 file) an audio recording of what was said

    """

    # Notes on Future Improvements:
    # + Add an agrument and code to write data (using update_log)
    # + Recode the task to exit and generate data once end key is pressed; not escape
    # + Add a time limit
    # + Recode a return value
    # + Add warnings and QAs to the code 
    # + Add option to change the dimensions of the image
    # + Get .mp3 conversion to work (output_format = "wav")

    # Set the directory to where the script is located (or any other desired directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory where the script is located
    os.chdir(script_dir)  # Change the current working directory to the script directory
    print(f"Current working directory: {os.getcwd()}")  # Print the current working directory

    # Capturing the time
    ts_start = datetime.datetime.now()

    # Initialize shared variables
    recording_started = False
    recording_triggered = False
    
    # Create a text stimulus for the waiting message
    waiting_text = visual.TextStim(win, text = trigger_text, pos=(0, 0), height=0.1)

    # Set up the microphone
    samplerate = int(device_info[sample_rate])

    # If we want the volume tracker visualized
    if show_volume:
        
        # Initializing volume variable
        volume_norm = [0]

        # Position the volume bar to the right
        volume_bar = visual.Rect(win, width=0.15, height=0.5, fillColor=volume_color, pos=(0.8, 0))
        volume_tray = visual.Rect(win, width=0.18, height=1.5, fillColor='lightgrey', lineColor = 'black', lineWidth=10, pos=(0.8, 0)) 
        volume_target_high = visual.Rect(win, width=0.18, height=0.01, fillColor='red', pos=(0.8, target_volume * 0.0075))
        volume_target_low = visual.Rect(win, width=0.18, height=0.01, fillColor='red', pos=(0.8, -(target_volume * 0.0075)))
    
    # Modify the audio_callback function to update the first element of the list
    def audio_callback(indata, frames, time, status):
        if recording_started:
            volume_norm[0] = np.linalg.norm(indata) * 10
            output_data.extend(indata.copy())
    
    # Load and position the image in the center of the screen
    record_image = visual.ImageStim(win, image=image, pos=(0, 0), 
                                    size=(win.size[0]/(win.size[1] * 2.5), 
                                        win.size[1]/win.size[1]))

    # Prepare to record
    output_data = []

    # Start the audio stream
    stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate)
    stream.start()

    try:
        while True:
            keys = event.getKeys()

            if trigger_key in keys:
                recording_triggered = True  # Set the flag to indicate that recording has been triggered
            
            if recording_triggered:
                recording_started = True  # Start recording once triggered
                record_image.draw()  # Draw the image
                
                # If we want the volume tracker visualized
                if show_volume:
                    volume_bar.height = volume_norm[0] / volume_sensitivity  # Update the visual element with the latest volume level
                    volume_tray.draw()  # Draw the volume tray
                    volume_bar.draw()  # Draw the volume bar
                     
                    # If we entered a value for the target volume
                    if target_volume > 0: 
                        volume_target_high.draw() # Draw the target volume upper limit
                        volume_target_low.draw() # Draw the target volume lower limit
                
                if end_key in keys:     
                    recording_started = False
                    break

            else:
                waiting_text.draw()  # Draw the waiting text

            win.flip()

    finally:
        stream.stop()
        ts_end = datetime.datetime.now()
        
        # Check if there is any recorded data
        if len(output_data) > 0:  
            output_nparray = np.concatenate(output_data, axis=0).astype('float32')
            wavfile_path = os.path.join(script_dir, output_file)  # Ensure the path is where the script is
            wavfile.write(wavfile_path, samplerate, output_nparray)  # Save the recording to a WAV file
            print(f"Recording saved to: {wavfile_path}")  # Print the path to the saved recording
            
            # # If we want the file in .mp3 format
            # if output_format == 'mp3':
            #     mp3file_path = os.path.join(script_dir, f"{output_filename}.mp3")
            #     wav_to_mp3(input = wavfile_path, output = mp3file_path)
            #     print(f"Recording converted to: {mp3file_path}")
            #     os.remove(wavfile_path)
        
        else:
            print("No data was recorded.")
        
        if log is not None:
            utilities.update_log(log,
                       Func = task_name, Text = trigger_text,
                       Onset = ts_start.strftime('%Y-%m-%d %H:%M:%S.%f'),
                       Offset = ts_end.strftime('%Y-%m-%d %H:%M:%S.%f'),
                       SystemTime_Start= ts_start, SystemTime_Stop=ts_end)
        else:
            print("No log was updated.")
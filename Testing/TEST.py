from psychopy import visual
from nastipy import tasks
import sounddevice as sd

win = visual.Window(fullscr=True,  
                    winType='pyglet', 
                    allowGUI=True, 
                    allowStencil=False,
                    color=[0,0,0], 
                    colorSpace='rgb',
                    blendMode='avg', 
                    useFBO=True)

# tasks.text_display(win = win, text = "Here's what some instructions might say. Press 1 to continue.", duration = "1")

# tasks.text_display(win = win, text = "And these instructions are timed", duration = 5)

# tasks.trigger(win = win)

# tasks.fixation(win = win, duration = 5)

# start = tasks.pre_active(win = win, 
#                          text = "Update your rating as needed. Press 1 when finished", 
#                          done_key = "1",
#                          label_L = "Guilty", 
#                          label_R = "Innocent", 
#                          key_L = "2", 
#                          key_R = "3", 
#                          scale_color = "purple")

# tasks.active_view(win = win, video = 'practicestim.mp4', 
#                   video_name = "PracticeStim", 
#                   label_L = "Guilty", 
#                   label_R = "Innocent", 
#                   key_L = "2", 
#                   key_R = "3", 
#                   scale_color = "blue",
#                   starting_scale_position = start)

tasks.free_recall(win = win)
import csv
import os
import random
import codecs
from psychopy import visual, core, event, gui, sound
from datetime import datetime

import yaml
import atexit


conf = yaml.load(open('config.yaml', encoding='utf-8'), Loader=yaml.SafeLoader)
screen_res = conf['SCREEN_RES']
randomize_trials = conf['RANDOMIZE_TRIALS']
frame_rate = conf['FRAME_RATE']
bgcolor = conf['BGCOLOR']
full_screen = conf['FULL_SCREEN']
units = conf['UNITS']

part_ID = ""
part_Age = ""
part_Gend = ""

trialtype = "training"
datetime = datetime.now()

results = list()

@atexit.register
def SaveResults():
    date_time_str = datetime.strftime('%Y_%m_%d_%H_%M_%S')
    with open(f'results/{part_ID}_{part_Age}_{part_Gend}_{date_time_str}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row)

def check_exit(key = 'f7'):
    stop = event.getKeys(keyList=[key])
    if len(stop) > 0:
        SaveResults()
        exit(1)

def get_participant_info():
    participant_info = dict()

    participant_info['Participant ID'] = ""
    participant_info['Age'] = ""
    participant_info['Gender'] = ["Male", "Female", "Nonbinary"]

    dlg = gui.DlgFromDict(participant_info)

    if not dlg.OK:
        core.quit()
    return participant_info['Participant ID'], participant_info['Age'], participant_info['Gender']

def display_text(win, filename_txt):

    '''
    Function displays text from .txt file
    '''
    with open(filename_txt, 'r', encoding='utf-8') as file:
        text = file.read()
    
    text_stim = visual.TextStim(win, text=text, height=.7, units = units, wrapWidth=screen_res[1])

    while True:
        check_exit()
        stop = event.getKeys(keyList=['space'])
        text_stim.draw()
        win.flip()
        
        if len(stop) > 0:
            break

    event.clearEvents()

    return

def showFixation(fixation_cross, frames):
    for frame in range(frames):
        fixation_cross.draw()
        win.flip()

# Input from dialogue window
part_ID, part_Age, part_Gend = get_participant_info()

# Create window for procedure
win = visual.Window(screen_res, color = bgcolor, fullscr = full_screen, units = units, monitor = "testMonitor")

# import sentences from .csv file
# sentences should

def loadSentences(path='sentences.csv'):
    '''
    import sentences from .csv file and assign it into dict
    sentences.csv structure:
    sentence;answer
    '''
    with open(path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        sentences_dict = {sentence:answer for [sentence,answer] in [line for line in csv_reader]}

        return sentences_dict
    
sentences_dict = loadSentences(path='sentences.csv')
sentences_list = list(sentences_dict)

if randomize_trials:
    random.shuffle(sentences_list)

def executeTrial(fixation_cross,sentence):

    trial_type = 'training'

    showFixation(fixation_cross, 60+random.randint(0, 60))
    
    text_stim = visual.TextStim(win, text=sentence, height=.7, units = units, wrapWidth=screen_res[1])

    for frame in range(frame_rate*5):
        check_exit()
        keypressed = event.getKeys(keyList=['right', 'left'], timeStamped = True)
        text_stim.draw()
        win.flip()
        
        if len(keypressed) > 0:
            break
    
    if len(keypressed) > 0:
        answer = keypressed[0][0]
        if answer == 'left':
            answer = True
        elif answer == 'right':
            answer = False
        else:
            answer = "error"
    else:
        print("Oops timeout")
        answer = -1
        frame = -1

    event.clearEvents()

    return trial_type, sentence, frame, answer




fixation_cross = visual.TextStim(win, text = "+", height = 1, pos = [0, 0], units = units, color = "#FFFFFF")

mouse = event.Mouse(visible = False)

results.append(['trial_type', 'trial_number', 'sentence', 'rt', 'correct_answer' , 'answer', 'acc'])

display_text(win, 'messages/training1.txt')

for trial_number in range(0,len(sentences_list)):
    trial_type, sentence, rt, answer = executeTrial(fixation_cross, sentences_list[trial_number])
    correct_answer = sentences_dict[sentences_list[trial_number]]

    if str(answer) == str(correct_answer):
        acc = 1
    else:
        acc = 0

    results.append([trial_type, trial_number, sentence, rt, correct_answer, answer, acc])


    


# Zmiana czasu na odpowiedz (dluzej)
# Posprzatac - w jednym miejscu zadawac info ile blokow i zdan w bloku
# Instrukcja z czytaniem

import csv
import os
import random
import codecs
from psychopy import visual, core, event, gui
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
part_Group = ""

trialtype = "training"
datetime = datetime.now()

results = list()
results_recall = list()

@atexit.register
def SaveResults():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)
    date_time_str = datetime.strftime('%Y_%m_%d_%H_%M_%S')
    with open(f'results/beh_{part_ID}_{part_Age}_{part_Gend}_{date_time_str}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row)
    with open(f'results/recall_{part_ID}_{part_Age}_{part_Gend}_{date_time_str}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in results_recall:
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
    participant_info['Group'] = ["A", "B"]

    dlg = gui.DlgFromDict(participant_info)

    if not dlg.OK:
        core.quit()
    return participant_info['Participant ID'], participant_info['Age'], participant_info['Gender'], participant_info['Group']

def display_text(win, filename_txt):

    '''
    Function displays text from .txt file
    '''
    with open(filename_txt, 'r', encoding='UTF-8') as file:
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

# Input from dialogue window
part_ID, part_Age, part_Gend, part_Group = get_participant_info()

# Create window for procedure
win = visual.Window(screen_res, color = bgcolor, fullscr = full_screen, units = units, monitor = "testMonitor")

# import sentences from .csv file
# sentences should

def loadSentences(path='sentences3.csv'):
    '''
    import sentences from .csv file and assign it into dict
    sentences.csv structure:
    sentence;answer
    '''
    with open(path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        sentences_dict = {sentence:answer for [sentence,answer] in [line for line in csv_reader]}

        return sentences_dict
    
sentences_dict = loadSentences(path='sentences3.csv')
sentences_list = list(sentences_dict)

if randomize_trials:
    random.shuffle(sentences_list)

training1_list = sentences_list[:17]

recall_list = [sentences_list[i:i+88] for i in range(17, len(sentences_list), 88)]
task_list = [r[:44] for r in recall_list]

for l in recall_list:
    random.shuffle(l)

def executeTrial(sentences_list, trial_number, trial_type):

    sentence = sentences_list[trial_number]

    answer, answer_rt = -1, -1

    main_clock = core.Clock()
    win.callOnFlip(main_clock.reset)
    while main_clock.getTime() < random.uniform(1.2, 1.5):
        check_exit()
        fixation_cross.draw()
        win.flip()
    print(time_fix := main_clock.getTime())

    text_stim = visual.TextStim(win, text=sentence, height=.7, units = units, wrapWidth=screen_res[1])

    event.clearEvents()
    main_clock.reset()
    win.callOnFlip(main_clock.reset)
    while main_clock.getTime() < 4:
        check_exit()
        keypressed = event.getKeys(keyList=['right', 'left'], timeStamped = main_clock)
        text_stim.draw()
        win.flip()
        
        if len(keypressed) > 0:
            answer = keypressed[0][0]
            answer_rt = keypressed[0][1]
            break
    
    if trial_type.startswith('perc'):
        correct_answer = str("a" in sentence)
    elif trial_type.startswith('sema'):
        correct_answer = sentences_dict[sentence]

    if (answer == 'left' and correct_answer == 'True') or (answer == 'right' and correct_answer == 'False'):
        answer = 1
    else:
        answer = 0

    if trial_type.endswith('training'):
        if answer == 1:
            feedback = "DOBRZE"
        else:
            feedback = "BLAD"
        text_feedback = visual.TextStim(win, text=feedback, height=.7, units = units, wrapWidth=screen_res[1])

        main_clock.reset()
        while main_clock.getTime() < 1.5:
            check_exit()
            text_feedback.draw()
            win.flip()
    
    event.clearEvents()

    return trial_type, sentence, correct_answer, answer, answer_rt


def executeRecall(task_list, recall_list):

    results_recall = []

    for sentence in recall_list:
        text_stim = visual.TextStim(win, text=sentence, height=.7, units = units, wrapWidth=screen_res[1])
        in_task = sentence in task_list
        while True:
            check_exit()
            keypressed = event.getKeys(keyList=['right', 'left'])
            text_stim.draw()
            win.flip()
            if len(keypressed) > 0:
                if ((keypressed[0] == 'left') and in_task) or ((keypressed[0] == 'right') and not(in_task))  :
                    answer = 1
                else:
                    answer = 0
                break
        results_recall.append([sentence,in_task,answer])
    
    return results_recall
        
fixation_cross = visual.TextStim(win, text = "+", height = 1, pos = [0, 0], units = units, color = "#FFFFFF")

mouse = event.Mouse(visible = False)

results.append(['trial_type', 'trial_number', 'sentence', 'correct_answer', 'acc', 'answer_rt'])
results_recall.append(['sentence', 'in_task', 'acc'])

text_perceptual= visual.TextStim(win, text='Czy w zdaniu znajduje sie litera a?\n <- Tak     Nie ->', height=.7, units = units, wrapWidth=screen_res[1])
text_semantic = visual.TextStim(win, text='Czy zdanie jest prawdziwe?\n <- Tak     Nie ->', height=.7, units = units, wrapWidth=screen_res[1])

display_text(win, 'messages/training1.txt')
display_text(win, 'messages/perceptual_task.txt')

for trial_number in range(len(training1_list)):
    trial_type, sentence, correct_answer, answer, answer_rt = executeTrial(training1_list, trial_number, "perceptual_training")
    results.append([trial_type, trial_number ,sentence, correct_answer, answer, answer_rt])

display_text(win, 'messages/semantic_task.txt')

for trial_number in range(len(training1_list)):
    trial_type, sentence, correct_answer, answer, answer_rt = executeTrial(training1_list, trial_number, "semantic_training")
    results.append([trial_type, trial_number ,sentence, correct_answer, answer, answer_rt])

display_text(win, 'messages/main_task.txt')

for no_sublist in range(0, int(len(recall_list)), 2):
    if part_Group == "A":

        display_text(win, 'messages/semantic_task.txt')
        for trial_number in range(len(task_list[no_sublist])):
            trial_type, sentence, correct_answer, answer, answer_rt = executeTrial(task_list[no_sublist], trial_number, f"semantic_experiment{no_sublist}")
            results.append([trial_type, trial_number ,sentence, correct_answer, answer, answer_rt])

        display_text(win, 'messages/recall.txt')
        recall_output = executeRecall(task_list[no_sublist], recall_list[no_sublist])
        for line in recall_output:
            results_recall.append(line)

        
        display_text(win, 'messages/perceptual_task.txt')
        for trial_number in range(len(task_list[no_sublist+1])):
            trial_type, sentence, correct_answer, answer, answer_rt = executeTrial(task_list[no_sublist+1], trial_number, f"perceptual_experiment{no_sublist}")
            results.append([trial_type, trial_number ,sentence, correct_answer, answer, answer_rt])

        display_text(win, 'messages/recall.txt')
        recall_output = executeRecall(task_list[no_sublist+1], recall_list[no_sublist+1])
        for line in recall_output:
            results_recall.append(line)

    elif part_Group == "B":

        display_text(win, 'messages/perceptual_task.txt')
        for trial_number in range(len(task_list[no_sublist])):
            trial_type, sentence, correct_answer, answer, answer_rt = executeTrial(task_list[no_sublist], trial_number, f"perceptual_experiment{no_sublist}")
            results.append([trial_type, trial_number ,sentence, correct_answer, answer, answer_rt])

        display_text(win, 'messages/recall.txt')
        recall_output = executeRecall(task_list[no_sublist], recall_list[no_sublist])
        for line in recall_output:
            results_recall.append(line)

        display_text(win, 'messages/semantic_task.txt')
        for trial_number in range(len(task_list[no_sublist+1])):
            trial_type, sentence, correct_answer, answer, answer_rt = executeTrial(task_list[no_sublist+1], trial_number, f"semantic_experiment{no_sublist}")
            results.append([trial_type, trial_number ,sentence, correct_answer, answer, answer_rt])

        display_text(win, 'messages/recall.txt')
        recall_output = executeRecall(task_list[no_sublist+1], recall_list[no_sublist+1])
        for line in recall_output:
            results_recall.append(line)
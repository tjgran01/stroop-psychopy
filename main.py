from task_presentor import TaskPresentor

from stroop import StroopTask
from psychopy import gui
import sys

import pandas as pd

import time


def main(task_list):
    myDlg = gui.Dlg(title="Participant ID Entry Field")
    myDlg.addText('Please enter the Participant ID for this session:')
    myDlg.addField('Participant ID:', "XXXX")
    myDlg.addText('Please choose a presentation method.')
    myDlg.addField('Presentation Method', choices=["mri", "nirs"])
    myDlg.addText('What template will this participant be running through.')
    myDlg.addField('Task Template', choices=["A", "B"])
    myDlg.addText('Is this a test? (Answering Yes will not save output data.)')
    myDlg.addField('Testing?', choices=["Yes", "No"])


    sub_id = myDlg.show()  # show dialog and wait for OK or Cancel
    if not myDlg.OK:  # or if ok_data is not None
        sys.exit()

    if sub_id[1] == "nirs":
        task_list.insert(0, "resting_state")

    tp = TaskPresentor(sub_id[0], task_list=task_list, present_method=sub_id[1], task_template=sub_id[2])

if __name__ == "__main__":
    task_list = ["finger_tapping", "stroop", "affect_reading", "end"]
    # task_list = ["affect_reading", "end"]
    main(task_list)

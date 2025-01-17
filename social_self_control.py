from psychopy import visual, core, event
from psychopy_questions import QuestionFactory
from util.file_reader import FileReader
from input_handler import InputHandler

from pathlib import Path
import random
import time
from tqdm import tqdm


class SocialSelfControl(object):
    def __init__(self, subject_id, task_presentor, conditions=[], num_blocks=1, cue_time=15,
                 fixation_time=2, iti_time=6, num_trials=10, ibi_time=10, question_timeouts={},
                 stim_time=10, variable_isi=False, practice=False, is_non_social=False):
        self.task_name = "social_self_control"
        if is_non_social:
            self.task_name = "non_social_self_control"
        self.subject_id = subject_id
        self.task_presentor = task_presentor
        self.num_blocks = num_blocks
        self.cue_time = cue_time
        self.fixation_time = fixation_time
        self.iti_time = iti_time
        self.stim_time = stim_time
        self.num_trials = num_trials
        self.ibi_time = ibi_time
        self.question_timeouts = question_timeouts
        self.variable_isi = variable_isi
        self.is_non_social = is_non_social
        self.trials_presented = 0
        self.question_factory = QuestionFactory(self.task_presentor)

        if not practice:
            self.trial_fpath = Path(f"./resources/{self.task_name}_trials/")
        else:
            self.trial_fpath = Path(f"./resources/{self.task_name}_trials/practice/")
            self.num_trials=5
            self.num_blocks=1
        self.practice = practice

        self.instructions = self.task_presentor.read_instructions_from_file(self.task_name)
        self._block_num = 0

        self.stim_dictionary = self.create_stim_dictionary(shuffle=practice)

        self.trial_timer = core.CountdownTimer(self.stim_time)

        
    def create_stim_dictionary(self, shuffle=False):

        lines = FileReader(f"{self.trial_fpath}/{self.task_name}_trials.csv").return_rows()

        lines = lines[1:]

        if shuffle:
            random.shuffle(lines)

        stim_dictionary = {}
        for l in tqdm(lines[1:], desc="Loading Stims"):
            stim = visual.TextStim(self.task_presentor.window, l[1])
            cue_txt = "n"
            if l[2] == "0":
                cue_txt = "ü"
            cue = visual.TextStim(self.task_presentor.window, cue_txt)
            stim_dictionary[l[0]] = {"item": l[0], "scenario": l[1], "condition": l[2], "stim": stim, "cue": cue}

        return stim_dictionary

    def set_current_block_num(self, block_num):
        self._block_num = block_num

        
    def run_full_task(self, practice=False):

        self.task_presentor.display_experimenter_wait_screen("experimenter")
        self.task_presentor.display_instructions(self.instructions)
        self.task_presentor.draw_wait_for_scanner()
        self.scan_start = time.time()
        print("Wait for scanner run.")

        for block in range(self.num_blocks):
            self.set_current_block_num(block)
            self.run_block(block_num=block)
            if (self.num_blocks > 1 and not self.practice):
                self.task_presentor.run_ibi(self.ibi_time)


    def run_block(self, block_num=0):

        print(f"Running block {block_num} for {self.task_name}")

        if self.is_non_social:
            prefix = "Non_Social_Self_Control"
        else:
            prefix = "Social_Self_Control"

        self.task_presentor.trigger_handler.send_string_trigger(f"{prefix}_Block_Start")

        for trial, trial_data in self.stim_dictionary.items():
            if self.trials_presented < self.num_trials:
                self.run_single_trial(trial_data)
                self.task_presentor.run_isi(self.iti_time)
                self.trials_presented += 1
                print(self.trials_presented)
                print(self.num_trials)

        self.task_presentor.trigger_handler.send_string_trigger(f"{prefix}_Block_End")


    def run_single_trial(self, trial_data):

        cue_disp_time = time.time()
        self.task_presentor.display_stim(trial_data["cue"])
        core.wait(self.cue_time)
        stim_disp_time = time.time()
        self.task_presentor.display_stim(trial_data["stim"])
        self.trial_timer.reset()
        
        event.clearEvents()
        while not event.getKeys("1") and self.trial_timer.getTime() > 0:
            continue
        stim_removed_time = time.time()

        self.question_factory.create_question("nein_ja")
        self.question_factory.display_question_button_snap(core.CountdownTimer(self.question_timeouts["slider affect"]))
        q_data = self.question_factory.get_data_line(self.subject_id, 0)
        self.write_data(trial_data["item"], trial_data["scenario"], trial_data["condition"],
                        cue_disp_time, stim_disp_time, stim_removed_time, q_data)



    def write_data(self, item, scenario, condition, cue_disp_time, stim_disp_time, stim_removed_time,
                   q_data):


        data = [self.subject_id,
                time.time(),
                item,
                scenario,
                condition,
                q_data[-6],
                q_data[-3],
                q_data[-3] + q_data[-2],
                q_data[-1],
                cue_disp_time,
                stim_disp_time,
                stim_removed_time,
                self.scan_start
                ]

        self.task_presentor.logger.write_data_row(data)

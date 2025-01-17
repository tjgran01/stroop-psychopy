import pandas as pd

from stroop import StroopTask
from finger_tapping import FingerTappingTask
from affect_reading import AffectReadingTask
from emotional_anticipation import EmotionalAnticipationTask
from episodic_prospection import EpisodicProspectionTask
from social_self_control import SocialSelfControl

import pickle

class TaskFactory(object):
    def __init__(self, sub_id, task_presentor):
        self.sub_id = sub_id
        self.task_presentor = task_presentor


    def try_param_set_from_file(self, task_string):

        try:
            prefs = pd.read_csv(f"./preferences/task_preference_csvs/id_preference_table_{task_string}.csv", dtype={"sub_id": str})
            prefs.set_index("sub_id", inplace=True)
            prefs = prefs.loc[self.sub_id]
            return prefs
        except:
            print(f"WARNING: No preference file found (or preferences file is missing specified Subject ID: {self.sub_id}.)")
            print("Running with Default Arguments")
            return pd.Series()


    def create_task(self, task_string, practice=False):

        prefs = self.try_param_set_from_file(task_string)
        if prefs.empty:
            return self.create_default_task(task_string, practice=practice)

        if task_string == "stroop":

            task = StroopTask(self.sub_id,
                              self.task_presentor,
                              num_blocks=prefs["num_blocks"],
                              fixation_time=prefs["fixation_time"],
                              congruence_rate=prefs["congruence_rate"],
                              num_trials=prefs["num_trials"],
                              ibi_time=prefs["ibi_time"],
                              variable_isi=prefs["variable_isi"])
        elif task_string == "finger_tapping":

            task = FingerTappingTask(self.sub_id,
                                     self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     block_time=prefs["block_time"],
                                     ibi_time=prefs["ibi_time"],
                                     is_sound=prefs["is_sound"])
        elif task_string == "affect_reading":

            task = AffectReadingTask(self.sub_id,
                                     self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     block_time=prefs["block_time"],
                                     ibi_time=prefs["ibi_time"],
                                     is_sound=prefs["is_sound"])
        return task


    def create_default_task(self, task_string, practice=False):

        prefs = pickle.load(open(f"./preferences/saved_defaults/{task_string}_defaults.pkl", "rb"))

        if task_string == "stroop":

            return StroopTask(self.sub_id, self.task_presentor,
                              num_blocks=prefs["num_blocks"],
                              fixation_time=prefs["fixation_time"],
                              congruence_rate_congruent=prefs["congruence_rate_congruent"],
                              congruence_rate_incongruent=prefs["congruence_rate_incongruent"],
                              num_trials=prefs["num_trials"],
                              ibi_time=prefs["ibi_time"],
                              variable_isi=prefs["variable_isi"],
                              scoring_method=prefs["scoring_method"],
                              response_timeout=prefs["response_timeout"],
                              block_time=prefs["block_time"],
                              conditions=prefs["conditions"],
                              shuffle_conditions=prefs["shuffle_conditions"])
        elif task_string == "finger_tapping":
            return FingerTappingTask(self.sub_id, self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     block_time=prefs["block_time"],
                                     ibi_time=prefs["ibi_time"],
                                     is_sound=prefs["is_sound"],
                                     conditions=prefs["conditions"])
        elif task_string == "affect_reading":
            return AffectReadingTask(self.sub_id, self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     affect_order=prefs["affect_order"],
                                     max_reading_time=prefs["max_reading_time"],
                                     readings=prefs["readings"],
                                     mult_choice_question_num=prefs["mult_choice_question_num"],
                                     question_mode=prefs["question_mode"],
                                     snap_questions=prefs["snap_questions"],
                                     text_size_mult=prefs["text_size_mult"],
                                     randomize_question_presentation=prefs["randomize_question_presentation"],
                                     movie_size_mult=prefs["movie_size_mult"],
                                     affect_induction_time=prefs["affect_induction_time"],
                                     default_fixation_time=prefs["default_fixation_time"],
                                     question_timeouts=prefs["question_timeouts"],
                                     testing=prefs["testing"],
                                     use_padding=prefs["use_padding"],
                                     video_text_timer_prompt=prefs["video_text_timer_prompt"],
                                     reading_text_timer_prompt=prefs["reading_text_timer_prompt"])
        elif task_string == "emotional_anticipation":
            return EmotionalAnticipationTask(self.sub_id, self.task_presentor,
                                             num_blocks=prefs["num_blocks"],
                                             conditions=prefs["conditions"],
                                             fixation_time=prefs["fixation_time"],
                                             iti_time=prefs["iti_time"],
                                             cue_time=prefs["cue_time"],
                                             movie_time=prefs["movie_time"],
                                             num_trials=prefs["num_trials"],
                                             ibi_time=prefs["ibi_time"],
                                             variable_isi=prefs["variable_isi"],
                                             question_timeouts=prefs["question_timeouts"],
                                             practice=practice)
        elif task_string == "episodic_prospection":
            return EpisodicProspectionTask(self.sub_id, self.task_presentor,
                                             num_blocks=prefs["num_blocks"],
                                             conditions=prefs["conditions"],
                                             fixation_time=prefs["fixation_time"],
                                             iti_time=prefs["iti_time"],
                                             cue_time=prefs["cue_time"],
                                             num_trials=prefs["num_trials"],
                                             ibi_time=prefs["ibi_time"],
                                             variable_isi=prefs["variable_isi"],
                                             question_timeouts=prefs["question_timeouts"],
                                             practice=practice)
        elif task_string == "social_self_control":
            return SocialSelfControl(self.sub_id, self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     conditions=prefs["conditions"],
                                     fixation_time=prefs["fixation_time"],
                                     iti_time=prefs["iti_time"],
                                     cue_time=prefs["cue_time"],
                                     stim_time=prefs["stim_time"],
                                     num_trials=prefs["num_trials"],
                                     ibi_time=prefs["ibi_time"],
                                     variable_isi=prefs["variable_isi"],
                                     question_timeouts=prefs["question_timeouts"],
                                     practice=practice,
                                     is_non_social=False)
        elif task_string == "non_social_self_control":
            return SocialSelfControl(self.sub_id, self.task_presentor,
                                     num_blocks=prefs["num_blocks"],
                                     conditions=prefs["conditions"],
                                     fixation_time=prefs["fixation_time"],
                                     iti_time=prefs["iti_time"],
                                     cue_time=prefs["cue_time"],
                                     stim_time=prefs["stim_time"],
                                     num_trials=prefs["num_trials"],
                                     ibi_time=prefs["ibi_time"],
                                     variable_isi=prefs["variable_isi"],
                                     question_timeouts=prefs["question_timeouts"],
                                     practice=practice,
                                     is_non_social=True)

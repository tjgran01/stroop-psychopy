import pickle

#### EDIT THIS TO EDIT DEFAULT PARAMETERS.

stroop_defaults = {
                   "num_blocks": 6,
                   "fixation_time": 2, # How long between trials.
                   "conditions": ["congruent",
                                  "incongruent",
                                  "congruent",
                                  "incongruent",
                                  "congruent",
                                  "incongruent"],
                   "congruence_rate_congruent": 1,
                   "congruence_rate_incongruent": .33,
                   "num_trials": 20, # overridden if block_time != 0.
                   "ibi_time": 15,
                   "variable_isi": False, # Will use 'fixation_time as mean.'
                   "scoring_method": "congruence",
                   "response_timeout": 5,
                   "block_time": 30,
                   "shuffle_conditions": True,
                   "name": "stroop_defaults",
                   }


finger_tapping_defaults = {
                           "num_blocks": 6,
                           "block_time": 15, # In seconds
                           "ibi_time": 10, # In seconds
                           "is_sound": False,
                           "tap_window": .250, # in seconds.
                           "conditions": [[80, "right"],
                                          [80, "right"],
                                          [80, "right"],
                                          [80, "right"],
                                          [80, "right"],
                                          [80, "right"]],
                           "name": "finger_tapping_defaults",
                           }


affect_reading_defaults = {
                           "num_blocks": 2,
                           "affect_order": ["none", "sad"],
                           "max_reading_time": 150,
                           "readings": ["hypotheses", "causalclaims"],
                           "mult_choice_question_num": 3,
                           "question_mode": "likert",
                           "text_size_mult": 1,
                           "randomize_mult_choice_presentation": True,
                           "snap_questions": False,
                           "randomize_question_presentation": True,
                           "movie_size_mult": 2.5,
                           "affect_induction_time": 150, # in seconds.
                           "default_fixation_time": 2,
                           "question_timeouts": {"slider alert": 10,
                                                 "slider affect": 10,
                                                 "slider mind_wandering": 10,
                                                 "slider mult_choice": 22,
                                                 "slider practice_slider": 30,
                                                 "slider practice_mult_choice": 30},
                           "testing": False,
                           "use_padding": True,
                           "video_text_timer_prompt": 3,
                           "reading_text_timer_prompt": 3,
                           "name": "affect_reading_defaults"
                           }

defaults_dicts = [stroop_defaults, finger_tapping_defaults, affect_reading_defaults]

for defaults in defaults_dicts:
    fname = defaults.pop("name")
    pickle.dump(defaults, open(f"./preferences/saved_defaults/{fname}.pkl", "wb"))

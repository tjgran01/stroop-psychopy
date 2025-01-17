from psychopy import visual, event, hardware
import random

import time
import os

class QuestionFactory(object):
    def __init__(self, task_presentor, mode="likert", snap_for_all=True):
        self.task_presentor = task_presentor
        self.mode = mode
        self.mouse = event.Mouse()
        self.snap_for_all = snap_for_all
        self.image_path = None
        self.question_displayed_time = None


    def get_data_line(self, subject_id, block_num):

        if self.type == "mult_choice":
            score = self.score_mult_choice()
        else:
            score = -1

        if self.timeout:
            rt = None
            selection = self.selection
            score = -2
            selection_string = "TIMEOUT"
            duration = self._timeout_time

        else:
            rt = self.slider.getRT()
            selection = self.selection
            selection_string = self.m_labels[int(self.selection)-1]
            duration = rt


        return [subject_id,
                time.time(),
                rt,
                block_num,
                self.type_text,
                self._question_text,
                self.m_ticks,
                self.m_labels,
                selection,
                selection_string,
                score,
                self.question_displayed_time,
                duration,
                self.timeout]


    def score_mult_choice(self):

        if self.question_answers[int(self.selection) - 1] == self.mult_choice_data["CorrectAnswer"]:
            return 1
        else:
            return 0


    def create_question(self, type, mult_choice_data={}):

        self.m_question_text = ""
        self.mult_choice_data = mult_choice_data

        self.type = type

        if type == "alert":

            self.m_text = "How sleepy vs. alert are you at this moment?"
            self.m_ticks = [1, 2, 3]
            self.m_labels = ["Extremely Sleepy", "Neutral" ,"Extremely Alert"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_flip = False

            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5

        elif type == "affect":

            self.m_text = "How sad vs. happy are you at this moment?"
            self.m_ticks = [1, 2, 3]
            self.m_labels = ["Extremely Sad", "Neutral", "Extremely Happy"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_flip = False

            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5

        elif type == "mult_choice":

            self.m_text = mult_choice_data["InstructionText"]
            self.m_question_text = mult_choice_data["QuestionText"]
            self.m_ticks = [1,2,3,4]
            self.question_answers = [mult_choice_data["CorrectAnswer"],
                                     mult_choice_data["AnswerOption2"],
                                     mult_choice_data["AnswerOption3"],
                                     mult_choice_data["AnswerOption4"]]
            random.shuffle(self.question_answers)
            self.m_labels = self.question_answers
            self.m_style = "myRadio"
            self.m_size = [0.06, 0.6]
            self.m_pos = (-0.9, -0.5)
            self.m_flip = True
            self._question_text = self.m_question_text

            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5

        elif type == "mind_wandering":

            self.m_text = "How much were you 'zoning out' while reading the text?"
            self.m_ticks = [1, 2]
            self.m_labels = ["Not at all", "Most"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_flip = False
            self._question_text = self.m_question_text

            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5

        elif type == "practice_slider":

            self.m_text = "For the next task, you will see some questions that you will answer with the trackball in your hand. Scroll the trackball left and right to make your selection. Click the left button to make your selection and continue."
            self.m_ticks = [1, 2]
            self.m_labels = ["Left", "Right"]
            self.m_style = "triangleMarker"
            self.m_size = [1.0, 0.1]
            self.m_pos = (0.0, 0.0)
            self.m_text_pos = (0.0, 0.6)
            self.m_flip = False
            self._question_text = self.m_question_text

            self.m_text_pos = (0.0, 0.6)
            self.m_text_width = 1.5

        elif type == "practice_mult_choice":

            self.m_text = "You will sometimes see multiple choice questions in this task."
            self.m_question_text = "To respond, please move the trackball UP and DOWN in order to highlight your selection. Click the left button to submit your response."
            self.m_ticks = [1,2,3,4]
            self.question_answers = ["Answer Option 4",
                                     "Answer Option 3",
                                     "Answer Option 2",
                                     "Answer Option 1"]
            self.m_labels = self.question_answers
            self.m_style = "myRadio"
            self.m_size = [0.06, 0.6]
            self.m_pos = (-0.9, -0.5)
            self.m_flip = True
            self._question_text = self.m_question_text

            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5


        elif type == "emotional_SAM":

            self.m_text = "This is placeholder text."
            self.m_question_text = ""
            self.m_ticks = [1,2,3,4,5]
            self.question_answers = ["",
                                     "",
                                     "",
                                     ""]
            self.m_labels = self.question_answers
            self.m_style = "rating"
            self.m_size = [0.75, 0.1]
            self.m_pos = (0.0, -0.3)
            self.m_flip = False
            self._question_text = self.m_question_text
            self.image_path = f"{os.getcwd()}/resources/sam_images/sam_full.png"
            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5


        elif type == "wie_detalliert":

            self.m_text = "Wie detalliert?"
            self.m_ticks = [1, 2]
            self.m_question_text = ""
            self.question_answers = ["Nicht lebhaft",
                                     "Sehr lebhaft"]
            self.m_labels = self.question_answers
            self.m_style = "rating"
            self.m_size = [0.75, 0.1]
            self.m_pos = (0.0, -0.3)
            self.m_flip = False
            self._question_text = self.m_question_text
            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5
            self.m_style = "triangleMarker"


        elif type == "nein_ja":

            self.m_text = "?"
            self.m_ticks = [1, 2, 3, 4]
            self.m_question_text = ""
            self.question_answers = ["nein",
                                     "eher nein",
                                     "eher ja",
                                     "ja"]
            self.m_labels = self.question_answers
            self.m_style = "rating"
            self.m_size = [0.75, 0.1]
            self.m_pos = (0.0, -0.3)
            self.m_flip = False
            self._question_text = self.m_question_text
            self.m_text_pos = (0, .8)
            self.m_text_width = 1.5
            self.m_style = "triangleMarker"


        if self.mode == "likert":
            stims = self.create_likert_question(type, self.m_text, self.m_ticks, self.m_labels,
                                                self.m_style, self.m_size, self.m_pos, self.m_flip,
                                                m_question_text=self.m_question_text)

        return stims



    def create_vas_question(self, type, text, ticks, labels, style,
                            size, pos, flip, m_question_text=None):

        pass


    def create_likert_question(self, type, text, ticks, labels, style,
                               size, pos, flip, m_question_text=None):

        if type == "mult_choice":
            self.type_text = f"mult_choice_{self.mult_choice_data['Text']}_page_{self.mult_choice_data['PageNum']}"
        else:
            self.type_text = type
            self._question_text = text

        self.text_stim = visual.TextStim(win=self.task_presentor.window,
                                         text=text, pos=self.m_text_pos,
                                         color=self.task_presentor.globals.default_text_color,
                                         wrapWidth=self.m_text_width)
        self.slider = visual.Slider(win=self.task_presentor.window,
                                    ticks=ticks,
                                    labels=labels,
                                    style=style,
                                    size=size,
                                    pos=pos,
                                    flip=flip)

        if len(ticks) == 2:
            self.slider.setMarkerPos(random.choice([1.25, 1.5, 1.75]))
        elif len(ticks) == 5:
            self.slider.markerPos = random.choice([2, 3, 4])
        elif len(ticks) == 4:
            self.slider.markerPos = random.choice([1, 2, 3, 4])
        else:
            self.slider.markerPos = random.choice(ticks)

        if self.m_question_text:
            self.question_text_stim = visual.TextStim(win=self.task_presentor.window,
                                                      text=m_question_text, pos=(-0.2, .3),
                                                      color=self.task_presentor.globals.default_text_color)
            self.stims = [self.slider, self.question_text_stim, self.text_stim]
        else:
            self.stims = [self.slider, self.text_stim]


        # Adding images
        if self.image_path:
            self.image_stim = visual.ImageStim(win=self.task_presentor.window,
                                               image=self.image_path,
                                               pos=(0.0, 0.0),
                                               size=(0.9, 0.4))
            self.stims.append(self.image_stim)



    def display_question(self, question_timer):

        self.question_displayed_time = time.time()
        self._timeout_time = question_timer.getTime()

        self.mouse.setVisible(False)

        if self.type in ["mult_choice", "practice_mult_choice"]:
            mouse_indx = 1
            snapping = True
        else:
            mouse_indx = 0
            snapping = False

        # if self.snap_for_all:
        #     snapping = True

        self.task_presentor.display_stims(self.stims)

        while not self.slider.getRating() and question_timer.getTime() > 0:
            # See if mouse moved.
            y_change =  self.mouse.getRel()[mouse_indx]

            # If Mouse moved update the screen.
            if y_change != 0.0:
                if snapping:
                    self.slider.markerPos = round((self.mouse.getPos()[mouse_indx] + .5) * len(self.m_ticks))
                else:
                    self.slider.markerPos = (self.mouse.getPos()[mouse_indx] + .5) * len(self.m_ticks)
                # Update.
                self.task_presentor.display_stims(self.stims)

            # If They Submit answer.
            if self.mouse.getPressed()[0] == 1:
                self.timeout = False
                self.slider.recordRating(self.slider.markerPos)

                if snapping:
                    self.selection = self.slider.getRating()
                else:
                    # normalize between 0 - 1
                    self.selection = (self.slider.getRating() - 1) / (len(self.m_ticks) - 1)

                if type == "mult_choice":
                    self._question_text = m_question_text
                    self.type_text = f"mult_choice_{self.mult_choice_data['Text']}_page_{self.mult_choice_data['PageNum']}"
                else:
                    self.type_text = self.type
                    self.score = -1
                    self._question_text = self.m_text
                return

        self.timeout = True


    def display_question_button_slider(self, question_timer, speed_dampen=1.0):

        self.question_displayed_time = time.time()
        self._timeout_time = question_timer.getTime()

        self.mouse.setVisible(False)

        self.task_presentor.display_stims(self.stims)

        kb = hardware.keyboard.Keyboard()
        newPos = self.slider.markerPos
        while not self.slider.getRating() and question_timer.getTime() > 0:
            self.slider.markerPos = newPos
            self.task_presentor.display_stims(self.stims)
            keys = kb.getKeys(["1", "2", "4"], waitRelease=False, clear=False)
            if keys and not keys[-1].duration:
                key = keys[-1].name
                if key == "1" and newPos > 0.0:
                    newPos -= .05 * speed_dampen
                if key == "2" and newPos < 5.0:
                    newPos += .05 * speed_dampen
                if key == "4":
                    self.timeout = False
                    self.slider.recordRating(self.slider.markerPos)
                    self.selection = (self.slider.getRating() - 1) / (len(self.m_ticks) - 1)
                    self.type_text = self.type
                    self.score = -1
                    self._question_text = self.m_text
                    return

        self.slider.recordRating(self.slider.markerPos)
        self.selection = (self.slider.getRating() - 1) / (len(self.m_ticks) - 1)
        self.timeout = True


    def display_question_button_snap(self, question_timer):

        self.question_displayed_time = time.time()
        self._timeout_time = question_timer.getTime()

        self.mouse.setVisible(False)

        self.task_presentor.display_stims(self.stims)

        kb = hardware.keyboard.Keyboard()
        newPos = self.slider.markerPos
        while not self.slider.getRating() and question_timer.getTime() > 0:
            self.slider.markerPos = newPos
            self.task_presentor.display_stims(self.stims)
            keys = kb.getKeys(["1", "2", "4"], waitRelease=False, clear=True)
            if keys:
                key = keys[-1].name
                if key == "1" and newPos > 0.0:
                    newPos -= 1
                if key == "2" and newPos < 5.0:
                    newPos += 1
                if key == "4":
                    self.timeout = False
                    self.slider.recordRating(self.slider.markerPos)
                    self.selection = (self.slider.getRating() - 1) / (len(self.m_ticks) - 1)
                    self.type_text = self.type
                    self.score = -1
                    self._question_text = self.m_text
                    return

        self.slider.recordRating(self.slider.markerPos)
        self.selection = (self.slider.getRating() - 1) / (len(self.m_ticks) - 1)
        self.timeout = True

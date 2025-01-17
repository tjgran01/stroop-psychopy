from psychopy import core

from psychopy_questions import QuestionFactory
from task_presentor import TaskPresentor

def main():
    
    pres = TaskPresentor("0909", run_task_list=False)
    question = QuestionFactory(pres)
    question.create_question("nein_ja")
    question.display_question_button_snap(core.CountdownTimer(10))

if __name__ == "__main__":
    main()
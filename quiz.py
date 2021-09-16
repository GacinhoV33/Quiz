#!/usr/bin/python
# -*- coding: utf-8 -*-

import database2
import cv2 as cv
import cvzone

import time
from random import sample
import numpy as np
from settings import X_S, Y_S, Resolution, Res_center, ColorRect, DetectRectColor
from sources import Detector, Rect_list, Circle_list, Elipse, BallImage, BallRect, overlay_transparent
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

slow_now = False
pop_num = 0


class QuizQuestion:
    def __init__(self, text: str, position: tuple, qid=0, font=cv.FONT_HERSHEY_COMPLEX, fontscale=1.5, thickness=3, offset=15):
        self.text = text[:-1]
        self.offset = offset
        self.position = (position[0] - 2 * self.offset, position[1] - 2 * self.offset)
        self.qid = qid
        self.fontscale = fontscale
        self.font = font
        self.is_clicked = False
        self.size = None
        self.thickness = thickness
        (self.w, self.h), _ = cv.getTextSize(text, font, self.fontscale, self.thickness)
        self.w += self.offset
        self.h += self.offset

    def clicked(self, cursor):
        pass

    def upgrade(self, cursor):
        centerx, centery = self.position
        if centerx - self.w // 2 < cursor[0] < centerx + self.w // 2 and centery - self.h // 2 < cursor[1] < centery + self.h // 2:
            return True

    def show(self, frame):
        frame = cvzone.putTextRect(frame, str(self.text), self.position, self.fontscale, self.thickness, (255, 255, 255))


class QuizAnswer:
    def __init__(self, text: str, position: tuple, qid=0, font=cv.FONT_HERSHEY_COMPLEX, fontscale=2, thickness=2, offset=15):
        self.text = text[:-1]
        self.offset = offset
        self.position = (position[0] - self.offset, position[1] - self.offset)
        self.qid = qid
        self.font = font
        self.fontscale = fontscale
        self.thickness = thickness
        (self.w, self.h), _ = cv.getTextSize(text, font, self.fontscale, self.thickness)
        self.w += self.offset
        self.h += self.offset

    def upgrade(self, cursor):
        centerx, centery = self.position
        if centerx - self.w // 2 < cursor[0] < centerx + self.w // 2 and centery - self.h // 2 < cursor[1] < centery + self.h // 2:
            self.position = cursor

    def show(self, frame):
        cvzone.putTextRect(frame, self.text, self.position, self.fontscale, self.thickness, (255, 255, 255), (0, 255, 0), offset=25)


def AnswerQuestion(quest):
    AnsRoot = Toplevel()
    AnsRoot.title(quest.qid)
    randombutt = Button(AnsRoot, text="yo", command=AnsRoot.destroy)
    randombutt.place(x=0, y=0)
    AnsRoot.mainloop()


def get_distance(ans, quest):
    return (abs(ans.position[0]-quest.position[0])**2 + abs(ans.position[1]-quest.position[1])**2)**(1/2)


def Game(Root):
    try:
        Camera = cv.VideoCapture(0)
    except Exception as exc:
        try:
            Camera = cv.VideoCapture(1)
        except Exception as exc:
            messagebox.showerror("Error", "No Camera Found")
            Root.destroy()
            return 0

    Camera.set(3, Resolution[0])
    Camera.set(4, Resolution[1])

    GameQuestions, GameAnswers = make_question()
    for que, ans in zip(GameQuestions, GameAnswers):
        que.position = (que.position[0] + 190000//que.w, que.position[1])
        # ans.position = (ans.position[0] + 50000//ans.w, ans.position[1])
    while True:
        success, frame = Camera.read()
        if not success:
            break
        frame = cv.flip(frame, 1)
        hands = Detector.findHands(frame, flipType=False, draw=False)
        distances = [get_distance(Answer, Question) for Answer, Question in zip(GameAnswers, GameQuestions)]
        if hands:
            hand1 = hands[0]
            lmList = hand1['lmList']
            cursor = lmList[8]
            length, _ = Detector.findDistance(lmList[8], lmList[12])
            if length < 47:
                for Ans in GameAnswers:
                    Ans.upgrade(cursor)
                for num, el in enumerate(distances):
                    if el < 37:
                        cvzone.putTextRect(frame, 'CORRECT!', (800, 650), colorR=(0, 255, 0), colorT=(0, 0, 255))
                        # x, y = GameQuestions[num].position
                        # w, h = GameQuestions[num].w, GameQuestions[num].h
                        # cvzone.cornerRect(frame, (x, y, w//2, h//2), colorR=(0, 0, 255))

                        global slow_now, pop_num
                        slow_now = True
                        pop_num = num

        else:
            cv.rectangle(frame, (0, 0), (15, 15), DetectRectColor, cv.FILLED)

        for Q, A in zip(GameQuestions, GameAnswers):
           A.show(frame),  Q.show(frame)

        cv.imshow('FG', frame)
        cv.waitKey(1)
        if slow_now:
            time.sleep(0.5)
            GameQuestions.pop(pop_num)
            GameAnswers.pop(pop_num)
            slow_now = False


def Options():
    OptionsRoot = Toplevel()
    OptionsRoot.title("Options")
    OptionsRoot.geometry("300x500")


    OptionsRoot.mainloop()


def Questions():
    QueRoot = Toplevel()
    QueRoot.title("Questions")
    QueRoot.wm_attributes('-transparentcolor', '#ab23ff')
    logo_img = ImageTk.PhotoImage(file='images/redquest.png')
    QueRoot.tk.call('wm', 'iconphoto', QueRoot._w, logo_img)
    QueRoot.geometry(f'{int(Resolution[0]/2)}x{int(Resolution[1]/1.8)}+{Res_center[0]}+{Res_center[1]}')

    EnterQuestion = Text(QueRoot, width=40, height=10, bg='white', fg='red', borderwidth=5)
    EnterQuestion.insert(INSERT,"Enter your Question here:")
    EnterQuestion.place(x=int(Resolution[0]/8), y=int(Resolution[1]/20))

    EnterAnswer = Text(QueRoot, width=40, height=5, bg='white', fg='blue', borderwidth=5)
    EnterAnswer.insert(INSERT, "Enter your Answer here:")
    EnterAnswer.place(x=int(Resolution[0]/8), y=int(Resolution[1]/20 * 6))

    EnterCategory = Entry(QueRoot, width=40, bg='white', fg='red', borderwidth=5)
    EnterCategory.place(x=int(Resolution[0]/8), y=int(Resolution[1]/20 * 8.9))
    EnterCategory.insert(0, "Category:")

    EnterDiff = Entry(QueRoot, width=40, bg='white', fg='red', borderwidth=5)
    EnterDiff.place(x=int(Resolution[0] / 8), y=int(Resolution[1] / 20 * 10))
    EnterDiff.insert(0, "Difficulty(1-10):")

    AddQuestionButton = Button(QueRoot, text="Add Question", pady=5, padx=10,
                               command=lambda: Add_one(EnterQuestion.get("1.0", END), EnterAnswer.get("1.0", END), EnterCategory.get(), EnterDiff.get()))
    AddQuestionButton.place(x=int(Resolution[0] / 2.5), y=int(Resolution[1] / 20 * 10))

    QueRoot.mainloop()
    pass


def Add_one(question, answer, category, difficulty):
    try:
        database2.add_one(question, answer, category, difficulty)
        messagebox.showinfo(title="Question mark", message="Question added successfully!")
    except:
        messagebox.showerror("Error", "Adding question went wrong.")


def choose_questions(n=5):
    questions_answers = database2.select_all()
    rand_ints = sample(range(0, len(questions_answers)-1), n)
    quests = list()
    answers = list()
    category = list()
    difficulty = list()
    ids = list()
    for num in rand_ints:
        ids.append(questions_answers[num][0])
        quests.append(questions_answers[num][1])
        answers.append(questions_answers[num][2])
        category.append(questions_answers[num][3])
        difficulty.append(questions_answers[num][4])

    return ids, quests, answers


def make_question(n=5):
    ids, quests, answers = choose_questions(n)
    rand = sample(range(0, n), n)
    return [QuizQuestion(quests[i], (220, 150 + rand[i] * 100), qid=ids[i], fontscale=2) for i in range(n)], [QuizAnswer(answers[i], (100, 150 + i * 100), qid=ids[i], fontscale=2) for i in range(n)]


def show_questions():
    pass


if __name__ == '__main__':
    Root = Tk()
    Root.geometry(f'{Resolution[0]}x{Resolution[1]}+{Res_center[0]}+{Res_center[1]}')
    Root.title('Finger Game')
    Root.wm_attributes('-transparentcolor', '#ab23ff')
    logo_img = ImageTk.PhotoImage(file='images/intro.jpg')
    Root.tk.call('wm', 'iconphoto', Root._w, logo_img)

    canv = Canvas(Root, width=Resolution[0], height=Resolution[1], bg='white')
    canv.pack(fill="both", expand=True)
    startImg = ImageTk.PhotoImage((Image.open('images/intro.jpg')).resize((Resolution[0], Resolution[1])), Image.ANTIALIAS)
    canv.create_image(0, 0, anchor=NW, image=startImg)

    StartButton = Button(Root, text="Start", padx=int(X_S/15), pady=int(Y_S/22), font=("Helvetica", 23), command=lambda: Game(Root))
    StartButton.place(x=int(X_S/2 - 1.5 * X_S/15), y=int(Y_S/1.2 - 3 * Y_S/72))

    OptionButton = Button(Root, text="Options", padx=int(X_S/21.5), pady=int(Y_S/22), font=("Helvetica", 23), command=Options)
    OptionButton.place(x=int(X_S/2 - 6 * X_S/15), y=int(Y_S/1.2 - 3 * Y_S/72))

    QuestionButton = Button(Root, text="Questions", padx=int(X_S/22.5), pady=int(Y_S/22), font=("Helvetica", 23), command=Questions)
    QuestionButton.place(x=int(X_S/2 + 3 * X_S/15), y=int(Y_S/1.2 - 3 * Y_S/72))

    Root.mainloop()










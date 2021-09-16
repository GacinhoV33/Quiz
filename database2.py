#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
from datetime import date, datetime

# conn = sqlite3.connect('database2.db')
# c = conn.cursor()
# c.execute("""CREATE TABLE que_ans (
#             question text,
#             answer text,
#             category text,
#             difficulty INTEGER,
#             date text)""")


def show_all():
    conn = sqlite3.connect('database2.db')
    c = conn.cursor()
    c.execute("""SELECT rowid,* from que_ans
    """)
    for el in c.fetchall():
        print(el)
    conn.commit()
    conn.close()
    #TODO change to readable format


def add_one(question, answer, category, difficulty):
    now = datetime.now()
    date_str = now.strftime("%d/%m/%Y %H:%M:%S")
    conn = sqlite3.connect('database2.db')
    c = conn.cursor()
    c.execute("""INSERT INTO que_ans VALUES (?,?,?,?,?) 
    """, (question, answer, category, difficulty, date_str))
    conn.commit()
    conn.close()


def select_all():
    conn = sqlite3.connect('database2.db')
    c = conn.cursor()
    c.execute("SELECT rowid,* FROM que_ans ")
    return c.fetchall()

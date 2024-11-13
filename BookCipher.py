import json
import os
import random
import re

# GV's
LINE = 128
page = 64

keybook1 ="DrJekylArndMrHyde.txt"
keybook2 ='Shakespheare.txt'
keybook3 ='WarAndPeace.txt'

HOWMANYBOOKS = 3

line_number = 0
page_number = 0
characterwindow = []
linewindow = {}
Pages = {}


# Functions
def clean_line(line):
    return line.strip().replace('-', '') + ' '

def read_book(file):
    global characterwindow
    with open(file, 'r', encoding='utf-8-sig'):
        for line in file:
            line = clean_line(line)
            if line.strip():
                for c in line:
                    process_char(c)
    if len(characterwindow) > 0:
        add_line()
    if len(linewindow) > 0:
        add_page()


def process_char(char):
    global characterwindow
    characterwindow.append(char)
    if len(characterwindow) == LINE:
       add_line()

def add_line():
    global characterwindow, line_number
    line_number += 1
    process_page(''.join(characterwindow), line_number)
    characterwindow.clear()

def process_page(line, line_num):
    global linewindow, Pages, page_number
    linewindow[line_num] = line
    if len(linewindow) == page:
        add_page()

def add_page():
    global line_number, linewindow, Pages, page_number
    page_number += 1
    Pages[page_number] = dict( linewindow )
    linewindow.clear()
    line_number = 0

def process_books(*paths):
    for path in paths:
        read_book( path )

def generate_code_book():
    global Pages
    code_book = {}
    for Page, lines in Pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return code_book


def save(file_path, book):
    with open(file_path, 'w') as fp:
        # json.dump(book, fp, indent=4)
        json.dump(book, fp)


def load(file_path, *key_books, reverse=False):
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)
    else:
        process_books(*key_books)
        if reverse:
            save(file_path, Pages)
            return Pages
        else:
            code_book = generate_code_book()
            save(file_path, code_book)
            return code_book

def encrypt(code_book, message):
    cipher_text = []
    for char in message:
        index = random.randint(0, len(code_book[char]) - 1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)

def decrypt(rev_code_book, ciphertext):
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+', ciphertext):
        Page, line, char = cc.split('-')
        plaintext.append(
            rev_code_book[page][line][int(char)])
    return ''.join(plaintext)




read_book(keybook2)
print(Pages)
print(keybook3)


#book cipher

import os, json, re
from random import randint

HOW_MANY_BOOK = 2
LINE = 128
PAGE = 64
pages = {}
page_number = 0
line_window = {}
line_number = 0
char_window = []

#///////#

def clean_line(line):
    #cleans a line of whitespaces
    return line.strip().replace('-', ' ') + ' '  #adds space instead of newline

def process_books(*paths):
    #starts the process
    for path in paths:  #for paths provided
        # print(f'Reading {path}')
        read_book(path)     #read the text in the path
        print(f'{len(pages)}, {len(pages[1])}')     #print the length of the pages and the length of page 1

def read_book(file_path):
    #opens a file and takes apart each line for processing
    global char_window      #accesses global variable
    with open(file_path, 'r', encoding='utf-8-sig') as fp:      #with the text file and uhh encoding mumbo jumbo as a local variable
        for line in fp:     #for line in file var
            line = clean_line(line)     #clean the line
            if line.strip():        #if there is still something in the line after removing whitespace
                for c in line:      #for every character in the line
                    process_char(c)     #send it thru this function
    if len(char_window) > 0:        #if char_window is more than 0:
        add_line()          #do this
    if len(line_window) > 0:        #if line_window is more than 0:
        add_page()          #do this

def process_char(char):
    #processes each character
    global char_window      #accesses global variable
    char_window.append(char)    #append the character to char_window
    if len(char_window) == LINE:    #if the length of char_window is equal to LINE (length of a row of text characters above)
        add_line()      #go to the new line function

def add_line():
    #creates a new line
    global char_window, line_number #accesses global variables
    line_number += 1        #adds a line to the counter
    process_page( ''.join(char_window), line_number )   #calls page processor function
    char_window.clear()     #clears the char counter for new line

def process_page(line, line_num):
    #processes page
    global line_window, pages, page_number  #accesses global variables
    line_window[line_num] = line    #uses line_num to access a specific index in line_window, then assigns line to that spot
    if len(line_window) == PAGE:    #if the length of line_window is equal to PAGE (number of lines of text designated above)
        add_page()      #go to new page function

def add_page():
    #creates a new page
    global line_number, line_window, pages, page_number #accesses global variables
    page_number += 1    #adds a page to the counter
    pages[page_number] = dict(line_window)  #uses page_number to access a specific page in pages, then assigns line_window to that spot
    line_window.clear()     #clears the line window for new page
    line_number = 0     #restarts the line counter for new page

def generate_codebook():
    global pages        #accesses global variable
    code_book = {}      #creates new dictionary
    for page, lines in pages.items():   #for each key and value combo in pages (page level)
        for num, line in lines.items():     #for each key and value combo of lines (line level)
            for pos, char in enumerate(line):   #for each position and character in line (character level)
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')    #uhh??? makes a very specific pointer to each character, including page number, line number, and position in said line????
    return code_book    #return this beautiful, confusing mess

def save(file_path, book):
    #saves codebook to a json file
    with open(file_path, 'w') as fp: #with the file path designated above
        # json.dump(book, fp, indent=4)
        json.dump(book, fp)     #dump iiit

def load(file_path, *key_books, reverse=False):
    #loads codebook at specified destination
    if os.path.exists(file_path):   #if the path exists on your computer
        with open(file_path, 'r') as fp:    #with the file path designated above
            return json.load(fp)    #dump it into the var
    else:   #if the path doesn't exist
        process_books(*key_books)   #process the books
        if reverse:     #if reverse? if false?
            save(file_path, pages)  #save the file at that file path
            return pages    #return pages
        else:
            code_book = generate_codebook()     #runs codebook gen and assigns result to var
            save(file_path, code_book)      #then saves that result at the file path
            return code_book        #and returns said value

def encrypt(code_book, msg):
    #encrypts message with codebook
    ciphertext = []
    for char in msg:    #for each character in message
        index = randint(0, len(code_book[char]) - 1)     #pick a random instance of the same letter recorded in the codebook
        ciphertext.append(code_book[char].pop(index)) #append it to the ciphertext
    return '-'.join(ciphertext)     #return it

def decrypt(rev_code_book, ciphert):
    #decrypts message with codebook
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+', ciphert):   #for every 3-integer match it can find within the ciphertext sequence:
        page, line, char = cc.split('-')        #splits cc in 3 for page, line, and char numbers
        plaintext.append(rev_code_book[page][line][int(char)])      #appends it to decrypted var
    return ''.join(plaintext)       #returns plaintext

cb = load('./codebooks/book1.json', './books/gatsby.txt', reverse=False)
cbr = load('./codebooks/book1_r.json', './books/gatsby.txt', reverse=True)
ciphertext = '118-10-43-168-44-33-175-62-52-529-48-36'
message = 'abcd'

print(encrypt(cb, message))

print(decrypt(cbr, ciphertext))

#i cannot for the life of me to get this to work, and i don't have any more time today to work on this. im sorry.

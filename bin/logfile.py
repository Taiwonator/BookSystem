import os
import sys
import pprint
from datetime import date
import database as db

def log_checkout(book):
    if(book is not None):
        return ("%s (ID=%s) checkout out on %s" %(book["name"], book["id"], date.today().strftime("%d/%m/%Y")))

def log_return(book):
    if(book is not None):
        return ("%s (ID=%s) return on %s" %(book["name"], book["id"], date.today().strftime("%d/%m/%Y")))

#log_return(db.get_books()[0])

def write_to_log(input):
    if input:
        with open('logfile.txt', 'a') as f:
            f.write(input + "\n")

def get_log_file():
     with open('logfile.txt', 'r') as f:
            return f.readlines()

def book_occurances(book_name):
    count = 0
    log_file = get_log_file()
    for i in range(len(log_file)):
        if(book_name in log_file[i] and "checkout" in log_file[i]):
            count += 1
    return count

def format_occurances():
    checkout_num = {}
    books = db.get_books()
    for i in range(len(books)):
        if((books[i])["name"] not in [*checkout_num]):
            checkout_num[(books[i])["name"]] = book_occurances((books[i])["name"])
    #print (checkout_num)
    return checkout_num

#pprint.pprint(format_occurances())
    

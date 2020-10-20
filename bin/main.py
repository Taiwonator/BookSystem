"""
 this is main program for file operations
 by Firat
 date
"""
from filefunction import *

def menu():
    option=input("select your option"
                 +"\n a) add a record"
                 +"\n p) print the records"
                 +"\n s) save the records"
                 +"\n l) load the records"
                 +"\n q)quit\n:") 
    return option

def get_student_mark():
     s_name=input ("please enter a name")
     s_mark=int(input ("please enter the mark"))
     return [s_name,s_mark]


def main():
     while True:
          option=menu()
          if option=="a": 
               s_record=get_student_mark()
               add_mark(s_record[0],s_record[1])
          elif option=="q":
               print ("bye bye come back again")
               break
          elif option=="p":
               print (test_marks)
          elif option=="s":
               save_records()
          elif option=="l":
               load_records()
          else:
               print ("no such menu option")
# ------
# main program starts
# -------
main()



"""
this is a module for file operations
by Firat
date
"""


test_marks=[] # global list

def save_records():
     #print (test_marks)     
     f=open("testmarks.txt","w")
     for r in test_marks:
          s_name=r[0]
          s_mark=r[1]
          s_record=s_name+","+str(s_mark)+"\n"
          f.write(s_record)
     f.close()
     print ("all saved")

def load_records():
     f=open("testmarks.txt","r")
     for r in f:
          clean_record=r.strip()
          s_record=clean_record.split(",")
          s_name=s_record[0]
          s_mark= s_record[1]    
          add_mark(s_name,s_mark)
     f.close() 



def add_mark(s_name,s_mark):
     s_test_mark=[s_name,s_mark]
     test_marks.append(s_test_mark)

if __name__== "__main__":
     # testing load_records 
     load_records()
     print(test_marks)
     # many testing code could be written here
     

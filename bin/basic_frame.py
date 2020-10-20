import database as db
import booksearch as bs
from tkinter import *
import tkinter.messagebox

def raise_frame(frame):
    frame.tkraise()

def quitProgramme(r):
    answer = tkinter.messagebox.askquestion("Exit", "Are you sure")
    if answer == 'yes':
        r.destroy()

def return_entry(entry):
    return entry.get()

def display_in_box(books):
    search_listbox.delete(0,tkinter.END)
    if(isinstance(books, list)):
        for i in range(len(books)):
            search_listbox.insert(END, books[i])
    elif(isinstance(books, str)):
        search_listbox.insert(END, books)
    else:
        search_listbox.insert(END, books)

search_type = "name"
def change_search_type(type):
    global search_type
    search_type = type
    if(type in ["name", "author"]):
        search_title_var.set(("Search by " + type))
    elif type == "member_id":
        search_title_var.set("Search by member ID")
    elif type == "id":
        search_title_var.set("Search by book ID")
    else:
        search_title_var.set("Search by purchase year")
  
root = Tk()
root.title("Library Management System")
root.geometry('500x500')
search_title_var = tkinter.StringVar()
search_title_var.set("Search by name")

search_frame = Frame(root)
search_frame.place(x=0, y=0, width=500, height=500)
search_back = Button(search_frame, text="Back", command=lambda:raise_frame(main_menu)).place(relx=0.95, rely=0.95, anchor=SE)
search_title = Label(search_frame, textvariable=search_title_var, font=("Helvetica", 20)).pack()
search_button_name = Button(search_frame, text="Name", command=lambda:change_search_type("name")).pack(side="top", fill="x")
search_button_author = Button(search_frame, text="Author", command=lambda:change_search_type("author")).pack(side="top", fill="x")
search_button_year = Button(search_frame, text="Year", command=lambda:change_search_type("purchase_date")).pack(side="top", fill="x")
search_button_member_id = Button(search_frame, text="Member ID", command=lambda:change_search_type("member_id")).pack(side="top", fill="x")
search_button_id = Button(search_frame, text="Book ID", command=lambda:change_search_type("id")).pack(side="top", fill="x")
search_entry = Entry(search_frame, text="Search", width=50)
search_entry.place(relx=0.4, rely=0.4, anchor=CENTER)
search_button_all_books = Button(search_frame, text="Get All Books", command=lambda:display_in_box(db.get_books())).place(relx=0.5, rely=0.9, anchor=CENTER)
search_submit = Button(search_frame, text="SUBMIT", command=lambda:display_in_box(bs.search_for_book(return_entry(search_entry), search_type))).place(relx=0.8, rely=0.4, anchor=CENTER)
search_scrollbar = Scrollbar(search_frame)
search_scrollbar.pack(side=RIGHT, fill=Y)

search_listbox = Listbox(search_frame, width=75)
search_listbox.place(x=15, y=250)
search_listbox.config(yscrollcommand=search_scrollbar.set)
search_scrollbar.config(command=search_listbox.yview)

checkout_frame = Frame(root)
checkout_frame.place(x=0, y=0, width=500, height=500)
checkout_back = Button(checkout_frame, text="Back", command=lambda:raise_frame(main_menu)).place(relx=0.95, rely=0.95, anchor=SE)
checkout_title = Label(checkout_frame, text="Checkout book(s)", font=("Helvetica", 20)).pack()


main_menu = Frame(root)
main_menu.place(x=0, y=0, width=500, height=500)
main_menu_title = Label(main_menu, text="Library Management System", font=("Helvetica", 24)).pack(side="top", fill="x")
main_menu_search = Button(main_menu, text="Search for book", command=lambda:raise_frame(search_frame)).pack(expand=True, side="top", fill=BOTH)
main_menu_search = Button(main_menu, text="Checkout book", command=lambda:raise_frame(checkout_frame)).pack(expand=True, side="top", fill=BOTH)
main_menu_quit = Button(main_menu, text="Quit", command=lambda:quitProgramme(root)).pack(expand=True, side="top", fill=BOTH)

root.mainloop()



# Imports all other python files into menu
import database as db
import booksearch as bs
import bookcheckout as bc
import bookreturn as br
import booklist as bl

# Allows for the use of matplotlib and tkinter
from tkinter import *
import tkinter.messagebox
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# This shows a frame, passed as an argument, above the current one
def raise_frame(frame):
    frame.tkraise()

# This does what the function does above, but calls the embedded graph to be redrawn so it updates its data if new checkouts have been made
def raise_frame_bl(frame):
    frame.tkraise()
    bl.display_pie_chart_in(frame)

#This function simply closes the tkinter window
def quitProgramme(r):
    r.destroy()

# This function returns the input value of whatever is in an entry 
def return_entry(entry):
    return entry.get()

#This function is resposible for displaying the programmes responses. Whether it be a command to do something, or just a response to a query
def display_in_box(books, listbox, type):
    global checkout_type
    temp_book = {}
    # This clears the list box's contents on funtion call
    listbox.delete(0,tkinter.END)
    outputted_names = [] #So there is only one output of a single books checkout status
    # This is in the case where there is a list of list to be displayed, in the case of outputting the checkout and return info
    if(any(isinstance(el, list) for el in books)):
        # Because the list of lists outputted by the checkout module is slightly different than the one for the return, we have 2 different scenarios
        # They're almost identical however and only vary in the string which is produced to the user
        if(type == "checkout"):
            #This for loop iterates through the list of lists
            for i in range(len(books)):
                #This for loop iterates through each inidividual list in the list of lists
                for j in range(len(books[i])):
                    # Only allows the book to be printed if it hasn't been printed before
                    if((books[i])[j] not in outputted_names):
                        if(i == 0):
                            if(checkout_type == "id"):
                                temp_book = db.return_book_details((books[i])[j], "id")
                            else:
                                temp_book = db.return_book_details((books[i])[j], "name")
                            listbox.insert(END, (temp_book["name"] + " (ID: " + temp_book["id"] + ") was succesfully checked out"))
                        elif (i == 1):
                            if(checkout_type == "id"):
                                temp_book = db.return_book_details((books[i])[j], "id")
                            else:
                                temp_book = db.return_book_details((books[i])[j], "name")
                            listbox.insert(END, (temp_book["name"] + " (ID: " + temp_book["id"] + " is currently unavaliable"))
                        else:
                            listbox.insert(END, ("No book with ID: " + (books[i])[j] + ") exists in the library"))
                        #Here we keep track of all the books which have already displayed a msg incase the user inputs the same book twice
                        outputted_names.append((books[i])[j])
        elif(type == "return"):
            for i in range(len(books)):
                for j in range(len(books[i])):
                    if((books[i])[j] not in outputted_names):
                        if(i == 0):
                            listbox.insert(END, ((books[i])[j] + " was succesfully returned"))
                        elif (i == 1):
                            listbox.insert(END, ((books[i])[j] + " is currently avaliable in the library"))
                        else:
                            listbox.insert(END, ((books[i])[j] + " <- ID doesn't match any books in library"))
                        outputted_names.append((books[i])[j])
    # This more simply just adds all the elements of the b'ooks' list onto a new line in the listbox 
    elif(isinstance(books, list)):
        for i in range(len(books)):
            listbox.insert(END, books[i])
    # In the case where there is a string to be displayed, it will just display that string on the first line
    elif(isinstance(books, str)):
        listbox.insert(END, books)
    else:
        listbox.insert(END, books)

#This function will change the label in the search frame, depending on the search type the user decides
search_type = "name"
def change_search_type(type):
    display_in_box("", search_listbox, "none")
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

# This function changes the checkout type
checkout_type = "name"
def change_checkout_type(type):
    display_in_box("", checkout_listbox, "none")
    global checkout_type
    checkout_type = type
    if(type == "name"):
        checkout_title_var.set("Checkout by name")
    elif type == "id":
        checkout_title_var.set("Checkout by book ID")
    else:
        print(type)


# This returns a list of all the unvavliable books IDs
def get_unavaliable_book_IDs():
    books = db.get_unavaliable_books()
    if(len(books) > 0):        
        ids_string = (books[0])["id"]
        for i in range(1, len(books)):
            ids_string = ids_string + ", " + (books[i])["id"]
        return ids_string

# It was not suitable to have this all within a function because there were many variables I wanted to access within functions and it's much easier to do so this way
# -------------------
# main program starts
# -------------------

#Creates a tkinter window and sets its attributes such as title and size
root = Tk()
root.title("Library Management System")
root.geometry('500x500')

#This is what determins the value of the Label in the search_frame
search_title_var = tkinter.StringVar()
search_title_var.set("Search by name")

checkout_title_var = tkinter.StringVar()
checkout_title_var.set("Checkout by name")

#This creates a new frame which we will switch to, when the search button is clicked
search_frame = Frame(root)
search_frame.place(x=0, y=0, width=500, height=500)
# This button returns the user back to the main menu
search_back = Button(search_frame, text="Back", command=lambda:raise_frame(main_menu)).place(relx=0.95, rely=0.95, anchor=SE)
search_title = Label(search_frame, textvariable=search_title_var, font=("Helvetica", 20)).pack()
# This buttons change the search type (name, author, id ect..) as well as changing the title label to display this change
search_button_name = Button(search_frame, text="Name", command=lambda:change_search_type("name")).pack(side="top", fill="x")
search_button_author = Button(search_frame, text="Author", command=lambda:change_search_type("author")).pack(side="top", fill="x")
search_button_year = Button(search_frame, text="Year", command=lambda:change_search_type("purchase_date")).pack(side="top", fill="x")
search_button_member_id = Button(search_frame, text="Member ID", command=lambda:change_search_type("member_id")).pack(side="top", fill="x")
search_button_id = Button(search_frame, text="Book ID", command=lambda:change_search_type("id")).pack(side="top", fill="x")
# ------------------------------------------------------------------------------------------------------------------------
search_entry = Entry(search_frame, text="Search", width=50)
search_entry.place(relx=0.4, rely=0.4, anchor=CENTER)
#This button displays all the books
search_button_all_books = Button(search_frame, text="Get All Books", command=lambda:display_in_box(db.get_books(), search_listbox, "none")).place(relx=0.4, rely=0.9, anchor=CENTER)
#This button displays all the avaliable books
search_button_all_avaliable_books = Button(search_frame, text="Get Avaliable Books", command=lambda:display_in_box(db.get_avaliable_books(), search_listbox, "none")).place(relx=0.6, rely=0.9, anchor=CENTER)
#The command will run the search for book function with the user input, and return it in the display in box function so it can be read. This is the same concept used for all the submit buttons
search_submit = Button(search_frame, text="SUBMIT", command=lambda:display_in_box(bs.search_for_book(return_entry(search_entry), search_type), search_listbox, "none")).place(relx=0.8, rely=0.4, anchor=CENTER)
search_scrollbar = Scrollbar(search_frame)
search_scrollbar.pack(side=RIGHT, fill=Y)
search_listbox = Listbox(search_frame, width=75)
search_listbox.place(x=15, y=250)
search_listbox.config(yscrollcommand=search_scrollbar.set)
search_scrollbar.config(command=search_listbox.yview)

#This is the frame for the checkout screen
checkout_frame = Frame(root)
# This creates a container withtin the frame which allows all the content to be vertically centered align
checkout_frame_content = Frame(checkout_frame)
checkout_frame.place(x=0, y=0, width=500, height=500)
checkout_back = Button(checkout_frame, text="Back", command=lambda:raise_frame(main_menu)).place(relx=0.95, rely=0.95, anchor=SE)
checkout_title = Label(checkout_frame_content, text="Checkout book(s)", font=("Helvetica", 24)).pack()
checkout_button_name = Button(checkout_frame_content, text="Name", command=lambda:change_checkout_type("name")).pack(side="top", fill="x")
checkout_button_id = Button(checkout_frame_content, text="ID", command=lambda:change_checkout_type("id")).pack(side="top", fill="x")
checkout_subtitle = Label(checkout_frame_content, textvariable=checkout_title_var, font=("Helvetica", 12)).pack()
checkout_book_entry = Entry(checkout_frame_content, width=50)
checkout_book_entry.pack()
checkout_ID_label = Label(checkout_frame_content, text="Enter member ID", font=("Helvetica", 12)).pack()
checkout_book_label = Label(checkout_frame_content, text="Seperate inputs with ', ' (1, 2, 3, 4 ect)", font=("Helvetica", 8)).pack(pady=8)
checkout_ID_entry = Entry(checkout_frame_content, width=50)
checkout_ID_entry.pack()
# All the successful and unsuccessful checkouts are displayed, and the programme will of checkouted out all the books which were successful, this display_in_box just relays the information
checkout_submit = Button(checkout_frame_content, text="SUBMIT", command=lambda:display_in_box(bc.checkout_books(return_entry(checkout_book_entry), return_entry(checkout_ID_entry), checkout_type), checkout_listbox, "checkout")).pack(pady=10)
# Content within this frame is centerally aligned
checkout_frame_content.pack(expand=1)
checkout_scrollbar = Scrollbar(checkout_frame_content)
checkout_scrollbar.pack(side=RIGHT, fill=Y)
checkout_listbox = Listbox(checkout_frame_content, width=75, height=5)
checkout_listbox.pack()
checkout_listbox.config(yscrollcommand=checkout_scrollbar.set)
checkout_scrollbar.config(command=checkout_listbox.yview)

#This is the frame for the return screen
returnscreen_frame = Frame(root)
returnscreen_frame_content = Frame(returnscreen_frame)
returnscreen_frame.place(x=0, y=0, width=500, height=500)
returnscreen_frame_back = Button(returnscreen_frame, text="Back", command=lambda:raise_frame(main_menu)).place(relx=0.95, rely=0.95, anchor=SE)
returnscreen_frame_title = Label(returnscreen_frame_content, text="Return book(s)", font=("Helvetica", 24)).pack()
return_ID_label = Label(returnscreen_frame_content, text="Enter book ID(s)\n (seperated by a ', ' => 1, 3, 5 ect...)", font=("Helvetica", 12)).pack(pady=10)
return_ID_entry = Entry(returnscreen_frame_content, width=50)
return_ID_entry.pack()
# This button will return a list of outputs stating which books were successfully or non successfully returned 
return_submit = Button(returnscreen_frame_content, text="SUBMIT", command=lambda:display_in_box(br.return_multiple_books(return_entry(return_ID_entry)), returnscreen_listbox, "return")).pack(pady=10)
returnscreen_frame_content.pack(expand=1)
returnscreen_scrollbar = Scrollbar(returnscreen_frame_content)
returnscreen_scrollbar.pack(side=RIGHT, fill=Y)
returnscreen_listbox = Listbox(returnscreen_frame_content, width=75, height=5)
returnscreen_listbox.pack()
returnscreen_listbox.config(yscrollcommand=returnscreen_scrollbar.set)
returnscreen_scrollbar.config(command=returnscreen_listbox.yview)
# This button returns all the books which are on loan by having all the unavaliable_book_IDs as a paramater for the return multiple books function
return_all_books_button = Button(returnscreen_frame_content, text="Return all books", command=lambda:display_in_box(br.return_multiple_books(get_unavaliable_book_IDs()), returnscreen_listbox, "return")).pack(pady=10)

#This is the frame for the booklist screen
booklist_frame = Frame(root)
booklist_frame.place(x=0, y=0, width=500, height=500)
booklist_frame_title = Label(booklist_frame, text="Popularity of books", font=("Helvetica", 24)).pack()
booklist_frame_back = Button(booklist_frame, text="Back", command=lambda:raise_frame(main_menu)).pack(side=BOTTOM, fill=X)
#raise_frame_bl just runs bl function again, makes sure popularity is updated as before, the function only ran on load before

#Main menu frame and is the frame which dsplays first because it is defined below all the other frames
main_menu = Frame(root)
main_menu.place(x=0, y=0, width=500, height=500)
main_menu_title = Label(main_menu, text="Library Management System", font=("Helvetica", 24)).pack(side="top", fill="x")
main_menu_search = Button(main_menu, text="Search for book(s)", command=lambda:raise_frame(search_frame)).pack(expand=True, side="top", fill=BOTH)
main_menu_checkout = Button(main_menu, text="Checkout book(s)", command=lambda:raise_frame(checkout_frame)).pack(expand=True, side="top", fill=BOTH)
main_menu_return = Button(main_menu, text="Return book(s)", command=lambda:raise_frame(returnscreen_frame)).pack(expand=True, side="top", fill=BOTH)
#This raise_frame_bl differs slightly. All it does is recreate the graph with the most current data. What I think is happenning is that the graph is being drawn on top of the previous one, so visually essentially overwritting it
main_menu_booklist = Button(main_menu, text="View book popularity", command=lambda:raise_frame_bl(booklist_frame)).pack(expand=True, side="top", fill=BOTH)
#Closes down the programme
main_menu_quit = Button(main_menu, text="Quit", command=lambda:quitProgramme(root)).pack(expand=True, side="top", fill=BOTH)

#This keeps the window running 
root.mainloop()





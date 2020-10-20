# This date is used when writing into the logfile
from datetime import date
# This library makes printing dictionaries look more visually appealing. Only used for testing purposes
import pprint


# Used to imitate objects. This is an empty dictionary, which holds as a skeleton for book data to be stored within
book_dict = {
    "id":"",
    "name":"",
    "author":"",
    "purchase_date":"",
    "member_id":""
}

# This function simply returns the number of lines in a file. Passes a file name (including extension) as an argument
def file_length(file_name):
    if(isinstance(file_name, str)):
        try:
            with open(file_name, 'r') as f:
                return len(f.readlines())
        except:
            return file_name + " isn't a known file"
    else:
        return str(file_name) + " is not a string"
    
# -----------------------
#
# Book Retreival functions
#
# -----------------------

def get_books():
    '''
    OVERVIEW: This function searches through database file, and stores each line as a book within a dictionary and
              forms a list of dictionaries representing all the books in the library

    f_lines: This stores the database file as a list of strings, each string representing a line in the database
    
    The for loop starts from 1 as the first line in my database is header information to make it more legible
    
    line: This takes a line in the database, and removes the new line '\n'

    d_values: This stands for dictionary values and this removes the | between each piece of data, then turns it into
              a list based on the spaces

    new_book_dict: This takes the skeleton dictionary 'book_dict' defined above, then copies it so it can assign its values
                   just below

    The next lines assign the values to the dictionary, then add that complete dictionary to a list named 'books', which is
    then returned 
    '''
    with open('database.txt', 'r') as f:
        books = []
        f_lines = f.readlines()
        for i in range(1, file_length("database.txt")):
            # This try and accept just runs in the unlikely case f_lines is None 
            try:
                line = f_lines[i].rstrip()
            except Exception as e:
                return "Error " + str(e)
                break
            # This runs if the try was successful
            else:
                #d_values = (line.replace(" ", "")).split("|")
                d_values = (line.replace("|", "")).split()
                #print(d_values)
                new_book_dict = book_dict.copy()
                for j in range(0, len(d_values)):
                    new_book_dict[list(book_dict.keys())[j]] = d_values[j]
                    if j == (len(d_values) - 1):
                        books.append(new_book_dict)
        return books

# This function returns all the books which are avaliable to be checkouted out. If there are no books however, then a msg stating this is outputted.
def get_avaliable_books():
     avaliable_books = []
     empty = True
     books = get_books()
     for i in range(len(books)):
         if((books[i])["member_id"] == "0"):
             avaliable_books.append(books[i])
             empty = False
     if (not empty):
         return avaliable_books
     else:
         return "There are no avaliable books"

# This function does similar to the function above however instead, returns the books which are currently on load
# This is used in the function to return all books in the menu file
def get_unavaliable_books():
     unavaliable_books = []
     books = get_books()
     for i in range(len(books)):
         if(not((books[i])["member_id"] == "0")):
             unavaliable_books.append(books[i])
     return unavaliable_books

# -----------------------------

# This function returns the first book found satisfying the value (name) and key (type)
def return_book_details(name, type):
    books = get_books()
    with open('database.txt', 'r') as f:
        for i in range(0, len(books)):
            if(((books[i])[type]).lower() == name.lower()):
                return (books[i])
            
# This function returns a list of books found satisfying the value (name) and key (type)
def return_books_details(name, type):
    books = get_books()
    output = []
    with open('database.txt', 'r') as f:
        for i in range(0, len(books)):
            if(((books[i])[type]).lower() == name.lower()):
                output.append(books[i])
    return output 

# This function writes the argument books, into the database
# This function could also be named 'write_to_file', as when this function was initally made, it was also planned to write to the log file
def write_to_file(books):
    '''
    The if conditionals all just make sure that an empty list isn't being written to the database, as that would erase all
    content written before and leave us with an empty file.

    The list 'books' is then ran through a function which is responsible for reformatting in so reading the file will be the
    same process everytime
    '''
    if(books is not None and len(books) > 0):
        with open('database.txt', 'w') as f:
            f.write(format_books(books))

#This is the formatting function. It will format all the books so it can be written into the database.txt in a legible fashion
def format_books(books):
    '''
    We start with 5 empty lists, each soon to be containing the values of all the dictionaries in the list 'books'
    As long as each book has all details filled in, which they do, then the number of values for all the different type of
    data should equal the same number, the number of books

    The next part simply uses string formatting to store the data within a grid
    '''
    ids = []
    names = []
    authors = []
    dates = []
    member_ids = []
    output = []
    for i in range(len(books)):
        try:
            ids.append((books[i])["id"])
        except Exception as e:
            print("Error: " + str(e))
            break
        else:
            names.append((books[i])["name"])
            authors.append((books[i])["author"])
            dates.append((books[i])["purchase_date"])
            member_ids.append((books[i])["member_id"])
    for i in range(len(books)):
        if(len(ids) > 0):
            if(i == 0):
                output = "%5s| %20s| %15s| %15s| %12s\n" %("ID", "NAME", "AUTHOR", "PURCHASE DATE", "MEMBER_ID")
            if(i == len(books) - 1):
                output = str(output) + ("%5s| %20s| %15s| %15s| %12s" %(ids[i], names[i], authors[i], dates[i], member_ids[i]))
            else:
                output = str(output) + ("%5s| %20s| %15s| %15s| %12s\n" %(ids[i], names[i], authors[i], dates[i], member_ids[i]))
    return output

# As long as the IDs are in order in the database, then the ID will always be equal to the books line number - 1
# This is as the IDs start at 1, but the lines start at 0 index. This function simply overwrites a certain book depending on its ID
def swap_book_details(books, book, ID):
    # This makes sure the parameters cause a correct execution, otherwise None is returned
    try:
        books[ID-1] = book
        return books
    # None being returned means nothing is written into the file when this is run in the write_to_file function, which is what we want
    except Exception as e:
        print ("Error: " + str(e))
        return None

# This function takes in a list of books to be swapped, and runs the previous function until every book in the list books has been swapped
def swap_multiple_books(books):
    out_books = get_books()
    output = []
    for i in range(len(books)):
        output = swap_book_details(out_books, books[i], int((books[i])["id"]))
    return output

# This function returns a string which will format what to be written into the logfile.txt file
def log_checkout(book):
    if(book is not None):
        return ("%s (ID=%s) checkout out on %s by member %s" %(book["name"], book["id"], date.today().strftime("%d/%m/%Y"), book["member_id"]))

# This function is the same as the one above however is for returning a book instead of checking one out
def log_return(book):
    if(book is not None):
        return ("%s (ID=%s) return on %s" %(book["name"], book["id"], date.today().strftime("%d/%m/%Y")))

# This files open type is different. It is append. Instead of re-writting the whole file like with the database, it is easier just to add a new line
# Chcecks on whether input is empty or not is not required as this is checked when the function is called within the other functinos
def write_to_log(input):
    with open('logfile.txt', 'a') as f:
        f.write(input + "\n")

# This function returns the logfile as a list of strings where a string represents a line
def get_log_file():
     with open('logfile.txt', 'r') as f:
            return f.readlines()

# This function is used to see which book has been checkouted out the most, and serves as one of the metrics for popularity
def book_occurances(book_name):
    '''
    This function checks through each line for the string 'checkout', and the argument 'book_name', and returns the no.
    occurances of these 2 together.
    '''
    if(isinstance(book_name, str)):
        count = 0
        log_file = get_log_file()
        for i in range(len(log_file)):
            if(book_name in log_file[i] and "checkout" in log_file[i]):
                count += 1
        return count
    else:
        return "Enter a string"

# In short, this function returns a dictionary with keys representing every unique book title name, and values representing that book's no. checkouts
def format_occurances():
    '''
    A empty dictionary is made, and has its keys generated by every unique book title in the database. This means that even if a book
    hasn't been checkout out once, the key will still be added.

    Once that unique book title is found, it has serve as the argument for the 'book_occurances' function which takes in a book name.
    This nicely assigns the value of that unique book name to the number of times its shown up in the logfile.txt
    '''
    checkout_num = {}
    books = get_books()
    for i in range(len(books)):
        if((books[i])["name"] not in checkout_num):
            checkout_num[(books[i])["name"]] = book_occurances((books[i])["name"])
    #print (checkout_num)
    return checkout_num

# This function uses the same principle as the function above, however just sets each value to 0
def blank_book_titles():
    blank_list = {}
    books = get_books()
    for i in range(len(books)):
        if((books[i])["name"] not in blank_list):
            blank_list[(books[i])["name"]] = 0
    return blank_list

# This function uses the blank dictionary created using the function above, and returns the number of the same book the library has in stock
# It does this by iterating through the books, and incrementing the value of each key corresponding with a book name when it is spotted
def books_in_library():
    book_titles = blank_book_titles()
    books = get_books()
    for i in range(len(books)):
        book_titles[(books[i])["name"]] += 1
    return book_titles

# This function does the same as the one above however will only increment if that book is currently on loan
def books_in_library_checkouted():
    book_titles = blank_book_titles()
    books = get_books()
    for i in range(len(books)):
        if(not ((books[i])["member_id"] == "0")):
            book_titles[(books[i])["name"]] += 1
    return book_titles

# This function uses the results of the 2 previous functions to return a dictionary which keeps track of the percentage of loans for each similar book title
# This means if there are 2 of Book_1 in the libary, and 1 is on loan, then 50% of books are out.
def percentage_of_books_out():
    checkout_title_percentages = {}
    all_books = books_in_library()
    checkouted_out_books = books_in_library_checkouted()
    for i in range(len(all_books)):
        # This line takes elements x y in 'all_books' and 'checkout_out_books' respectively then returns a dictionary with values equal to y/x
        checkout_title_percentages[list(all_books.keys())[i]] = (list(checkouted_out_books.values())[i] / list(all_books.values())[i]) * 100
    return checkout_title_percentages
    

if __name__ == "__main__":
    # file_length function tests
    print("File length tests")
    print("Database number of lines:", file_length("database.txt"))
    print("Logfile number of lines:", file_length("logfile.txt"))
    print("file_length function (int):", file_length(2))
    print("file_length function (empty string):", file_length(""))
    print("file_length function (unknown string):", file_length("logfile.s"))

    # formatted books
    print("\nFormatted books")
    print(format_books(get_books()))
    print(format_books("1, 2, 3"))

    # formatted avaliable books
    print("\nFormatted avaliable books")
    print(format_books(get_avaliable_books()))

    # formatted unavaliable books
    print("\nFormatted avaliable books")
    print(format_books(get_unavaliable_books()))

    # blank list
    print("\nBlank book titles")
    print(blank_book_titles())

    # specific book title occurences
    print("\nspecific book title occurences")
    print("Book_1: " + str(book_occurances("Book_1")))
    print("Bosok: " + str(book_occurances("Bosok")))
    # These outputs would be a problem however the only parameters used will be correct book titles so they're not needed to be fixed
    print("1:  " + str(book_occurances("1")))
    print("Book:  " + str(book_occurances("Book")))
    # ----------------------------------------
    print("Empty:  " + str(book_occurances("")))
    print("Number input:  " + str(book_occurances(1)))

    # book title occurences
    print("\nbook title occurences")
    print(format_occurances())

    # Books titles in library 
    print("\nBooks titles in library")
    print(books_in_library())

    # Books titles in library checkouted
    print("\nBooks titles in library checkouted")
    print(books_in_library_checkouted())

    # Percentage of each book on loan
    print("\nPercentage of each book on loan")
    print(percentage_of_books_out())

    # String written to log file when a book is checkouted
    print("\nString written to log file when a book is checkouted")
    print(log_checkout(get_books()[0]))

    # Cannot test write to log and database files as that would cause issues. Those functions do work however

    
    
    






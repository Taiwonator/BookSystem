# database file imported 
import database as db
import pprint

# This function checks the arguments of the checkout_books
# This is done within a new function as it is quite long

def check_checkout_input(book_names_unsplit, member_id):
    # This makes sure that both the inputs are strings, as if they are not, then it'll cause errors in the checkout_books function
    if(isinstance(book_names_unsplit, str) and isinstance(member_id, str)):
        # This is if they entered an empty string for either argument, or if the member id isn't a digit
        if(not member_id.isdigit() or len(book_names_unsplit) == 0 or len(member_id) == 0):
            if(len(member_id) == 0):
                return "member ID empty"
            elif(len(book_names_unsplit) == 0):
                return "No book names inputed"
            else:
                return str(member_id) + " member ID is not a digit"
        else:
            # This checks if the memberID is truely a 4 digit number, and if so, then proced is returned. If this is returned, then the function below can run another section of code
            if(not (int(member_id) >= 1000 and int(member_id) <10000)):
                return str(member_id) + " not in range"
            else:
                return "proceed"
    else:
        print("At least one of %s or %s are not strings!" %(str(book_names_unsplit), str(member_id)))

# Stores book titles which are currently out on loan 
unavaliable_books = []
# Stores book titles which do not exist in the library
non_existent_books = []

# This function will checkout multitple books, and will return a list of lists, like in the return module. 
def checkout_books(book_names_unsplit, member_id, type):
    '''
    The first condition checks whether the inputs are valid, if not, then the appropriate error msg is returned. This function is used in the
    tkinter listbox so the error will be displayed to the user so they can change their input.

    If the first condition is met, then it resets the global variables. The book_names inputed are then split in the same way as in the return module

    book: This runs the function find_avaliable_book() which returns a book if there is a book with that title avaliable, however if not, then None is returned
          Using this information, the next condition checks if a book was found, and if so, adds it to a list of books which will be checkouted out later,
          as well as a list of all the successful books which will be displaeyed to the user.

    if(len(checkout_books) > 0): This line checks if there were any successfully checked out books. If not, then the list of lists will return 3 lists,
    with the successfully checkouted out list being empty. If the condition is true however, then the log file is written to, as well as the database being
    updated. Then the list of successfully checked out books can be added to the list of lists 'output', alongside the other 2 lists which will catch any of the
    non successful checkouts

    output = [[successful books], [unavaliable books], [non-existent books]]
    '''
    if(check_checkout_input(book_names_unsplit, member_id) == "proceed"):
        global unavaliable_books
        global non_existent_books
        unavaliable_books = []
        non_existent_books = []
        book_names = book_names_unsplit.split(', ')
        books = db.get_books()
        checkout_books = []
        checkout_books_names = []
        for i in range(len(book_names)):
            book = find_avaliable_book(books, book_names[i], type)
            if(book is not None):
                checkout_books.append(book)
                checkout_books_names.append(book[type])
        if(len(checkout_books) > 0):
            for i in range(len(checkout_books)):
                (checkout_books[i])["member_id"] = member_id
                db.write_to_log(db.log_checkout(checkout_books[i]))
            db.write_to_file(db.swap_multiple_books(checkout_books))
            output = []
            output.append(checkout_books_names)
            output.append(unavaliable_books)
            output.append(non_existent_books)
            #print(output)
            return output
        else:
            output = []
            output.append([])
            output.append(unavaliable_books)
            output.append(non_existent_books)
            #print(output)
            return output
    else:
        return check_checkout_input(book_names_unsplit, member_id)

# This function will return a book if there is a book with the name book_name in books which has a member_id of 0, meaning no one has taken it out yet
# If there is no find hoeverm then nothing is returned (None)
def find_avaliable_book(books, book_name, type):
    '''
    The boolean 'found' will be true if a book with the name book_name is found in books
    The boolean 'avaliable' requires a book to be found AND for that book to have a member_id of 0
    At the end of the function, these values are checked, and unless both of them are true, None was returned, and the book name was
    added to one of the lists.

    A key note in this function is that it will stop at the first instance of a book found with the required book_name. This means that
    the book with book_name with the smallest number ID will always be checkouted first. 
    '''
    avaliable = False
    found = False
    for i in range(len(books)):
        if((books[i])[type] == book_name):
            found = True
            if((books[i])["member_id"] == '0'):
                avaliable = True
                #print("%s is avaliable" %(book_name))
                return books[i]
                break

    if(not found):
        #print("%s doesn't exist in the library" %(book_name))
        non_existent_books.append(book_name)
    elif(found and not avaliable):
        #print("%s is not avaliable" %(book_name))
        unavaliable_books.append(book_name)


if __name__ == "__main__":
    print("Testing finding an avaliable book")
    print(find_avaliable_book(db.get_books(), 'Book_1'))
    print(find_avaliable_book(db.get_books(), 'Book_3'))
    print(find_avaliable_book(db.get_books(), 'asfaf'))

    print("\nTesing check_checkout_input function")
    print(check_checkout_input("Book_1, Book_2", "1000"))
    print(check_checkout_input("1, 2, 3, 4", "1000"))
    print(check_checkout_input("Book_1", "9999"))
    print(check_checkout_input("Bo", "9999"))
    print(check_checkout_input("Bo", "99"))
    print(check_checkout_input("Bo", 9999))
    print(check_checkout_input("", '9999'))
    print(check_checkout_input("Bo", ''))
    print(check_checkout_input("Bo", 's'))
    print(check_checkout_input("", 's'))
    print(check_checkout_input(1, 2))

    print("\nTesing checkout_books function")
    print(checkout_books("Book_1", '1000'))
    print(checkout_books("Book_1, Book_4, Book_3", '1000'))
    print(checkout_books("", 3))
    print(checkout_books("Book_1", '1000, 1202'))






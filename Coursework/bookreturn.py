# Imports the file database as an object named db
import database as db
import pprint

# This global list will contain all the books which are trying to be returned when they are already avaliable for checkout
avaliable_books = []
# This gloabl list will contain all the books entered by the user which don't exist
non_existent_books = []

# This function returns the book to be returned based on the ID inputed (take as a arguement)
def return_book(bookID):
    '''
    The function can only take string inputs, so it does a check first that the input is string, if not, then a msg will display.
    
    The function first checks if the string input is a digit. If not, then the appropriate message is relayed to the user.
    This is the same for if the user attempts to input a ID not in the range of possible IDs, which would be a number
    greater than the length of books ther are in the library

    If a book is to be returned, then the member_id must not equal 0, but if it is, then this is added to the avaliable_books
    list. The non_existent_books is also populated by books which either have IDs not in the range, or which have non digit IDs.

    For when a book is returnable however, the member_id value is switched to 0, and the function writes to the logfile saying
    that the return has been successful. At this point however, the book hasn't been stored in memory yet. It is added to a list
    which is defined in the next function
    '''
    global avaliable_books
    global non_existent_books
    books = db.get_books()
    if(isinstance(bookID, str)):
        if(bookID.isdigit()):
            if(int(bookID) > 0 and int(bookID) <= len(books)):
                if((books[int(bookID) - 1])["member_id"] != "0"):
                    (books[int(bookID) - 1])["member_id"] = "0"
                    db.write_to_log(db.log_return(books[int(bookID) - 1]))
                    print("%s was successfully returned" %(books[int(bookID)-1]))
                    return books[int(bookID) - 1]
                else:
                    print("Error, %s is already avaliable" %(books[int(bookID)-1]))
                    avaliable_books.append(  ((books[int(bookID) - 1])["name"]) + " (ID: " + bookID + ")"   )
            else:
                print("No book in database with ID", bookID)
                non_existent_books.append(bookID)
        else:
            print(bookID, "is not a natural number")
            non_existent_books.append(bookID)
    else:
        print(str(bookID) + " is not a string")
            

# Everytime this function is run, we want to blank the global variables values.
# This function will only run once on call. 
def return_multiple_books(ID_input):
    '''
    We again use these 2 global variables. Initally to clear them, but later to add them into another list and return a list of lists
    to be used in the menu file. A dictionary with list values would have been a cleaner way of doing this but that seemed like needless complication.

    ID_input: This will be a list of IDs which will allow the user to return mutliple items at once as long as they seperate each ID using a ', '.
              ID_input is checked to see if it is None for starters, as this would lead to an error when trying to apply the method split() to it.
              Considering this first condition is met, the string is split into a list of IDs. Each ID in that list is then run through the function above
              'return_book'. If the book ID is invalid, it'll be added into one of 2 lists, 'non_existent_books' or 'avaliable_books'. If the book ID is valid
              then the book is returned.

    The function with a valid book, will then add that to a list of books which will be successfully returned. And that book's name and ID is added into a list
    keeping track of the successful book returns.

    db.swap_multiple_books(returning_books): This function is explained in the database file. Essentially, this function will return all the books, but with
                                             the books in the list 'returning_books' having their info updated after their member_id has been changed back to 0
                                             in the return_books function. Then it is written using db.write_to_file()

    Finally, I wanted to output all of the lists to be used in the menu, so I added them all within a list to return a list of lists in the end

    output = [[successful books], [unavaliable books], [non-existent books]]
    '''
    global avaliable_books
    global non_existent_books
    avaliable_books = []
    non_existent_books = []
    # This variable below is used for outputting the names of the books which were successfully returned. It is used in the menu file
    returning_book_names = []
    returning_books = []
    if(ID_input is not None and isinstance(ID_input, str)):
        if(len(ID_input) > 0):
            book_IDs = ID_input.split(', ')
            for i in range(len(book_IDs)):
                #books = return_book(book_IDs[i])
                book = return_book(book_IDs[i])
                if(book is not None):
                    returning_book_names.append( (book["name"]) + " (ID: " + book["id"] + ")" )
                    returning_books.append(book) # Adds a book which needs to be returned to a list
        else:
            return "You have not entered any bookIDs"
    db.write_to_file(db.swap_multiple_books(returning_books))
    output = []
    output.append(returning_book_names)
    output.append(avaliable_books)
    output.append(non_existent_books)
    return output

if __name__ == "__main__":
    # Testing return book function
    print("Return a single book test")
    return_book('1')
    return_book('23ros')
    return_book('20')
    return_book(2)

    # Testing return books function
    print("\nReturn multiple books test")
    return_multiple_books("1, 2, 3")
    print("\n")
    return_multiple_books("s")
    print("\n")
    return_multiple_books("s, 6, w")
    print("\n")
    return_multiple_books(3)
    



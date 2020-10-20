#import the database file
import database as db
import pprint

# This is the default search type
search_type = "name"
# This is the list which contains all the successfully searched for books
displayed_books = []
# This variable helps with attempting to autocorrect the user's input
matching_letters = 0
# This list will hold the programmes attempt at guessing what the user meant to type in 
guesses = []

found = False
id_outputs = []
date_outputs = []
searching = False

# This function returns the number of matching characters in a and b
def num_matching_letters(a, b):
    count = 0
    for i in range(0, len(a)):
        if(a[i] in b):
            count += 1
    return count

#
def search_for_book(search, type):
    global found
    global guesses
    global matching_letters
    global id_outputs
    global date_outputs
    global displayed_books
    global searching
    
    # This essentially blanks all the lists everytime it searches for a book
    if(not searching):
        id_outputs = []
        date_outputs = []
        displayed_books = []
        guesses = []
        matching_letters = 0
        found = False
    searching = True
    books = db.get_books()
    search = search.lower()
    # This is if the input is nothing essentially
    if(search == "" or search.isspace()):
        return ("Please enter something")
    # If the function is searching based on the name of the book, or author, then the following statements run
    elif(type in ["name", "author"]):
        for i in range(0, len(books)):
            # This function will determine the value of found. If an exact match is found, the boolean found == True
            find_closest_word(((books[i])[type]).lower(), search, books[i])
        # This is ran if an exact match was not found
        if(not found):
            print(found, "DISAPLYED: " + str(displayed_books))
            if(len(guesses) > 0):
                searching = False
                # This returns the book the programme thinks it was trying to find
                # Returns every book with the book name guesses[len(guesses) - 1] 
                return db.return_books_details(guesses[len(guesses) - 1], type)
            else:
                # This is for when a guess was not able to be made
                searching = False
                return (search + " doesnt exist")
        else:
            # This is for when there is an exact match and the assured output will be displayed_books as it was checked in the find_closest_word function
            searching = False
            return displayed_books
    # This runs if the user is searching based on one of the ids.     
    elif(type in ["id", "member_id"]):
        for i in range(len(books)):
            # Checks if there is a book with the id the user searhed, and if so, adds it to a list which will later be returned
            if((books[i])[type] == str(search)):
                id_outputs.append(books[i])
            else:
                # This checks if the whole list has been checked and no finds have been made, then return a msg stating no books were found
                if(i == len(books) - 1 and len(id_outputs) == 0):
                    searching = False
                    return("Couldn't find book with " + type + " " + search)
                    break
        searching = False
        return id_outputs
    elif (type == "purchase_date"):
        for i in range(len(books)):
            #[5:9] takes the year part of a date so i can compare that with what the user searches
            if(((books[i])[type])[5:9] == search):
                date_outputs.append(books[i])
            else:
                if(i == len(books) - 1 and len(date_outputs) == 0):
                    searching = False
                    return("Couldn't find book with " + type + " " + search)
                    break
                    #search_for_book(type)
        searching = False
        return date_outputs
    else:
        return "type not valid"
            
# This function will take a string, and output all the (x in [2..x]) concecutive characters in word.
# EXAMPLE: get_word_parts("dog") ---> ['dog', 'do', 'og']
def get_word_parts(word):
    if(isinstance(word, str)):
        word_length = len(word)
        cls = []
        cl = word_length # this is the number of consecutive letters
        x = word_length -1 #
        while cl > 1: # runs until the length of the spliced word is equal to the word length (spliced = word)
            for j in range(0, word_length-x): # as when the spliced word size increases, the number of possible consecitve options reduce, it reduces by 1 everytime
                cls.append(word[slice(0+j, cl+j)])
            cl -= 1
            x -= 1
        return cls
    else:
        return "enter a string"

#
def find_closest_word(word, search, book):
    '''
    ARGUMENT word: A name of a book in the library
    ARGUMENT search: The name of a book the user is searching for
    ARGUMENT book: The book with the name 'word' in the library
    
    if (word == search): This is for when there is an exact match between the user input and a name in the library. What follows
    is as simple as adding this book to a list which will eventually display all the books, and setting the global var found to True.

    If however, the word != search, then a set of fairly complicated statements are run. The computer's guess is based on 2 factors
        1. The number of matching characters there are between both the book name and the user input
        2. If there are (x in [2..x]) consecutive characters which match (STRONG INDICATION OF A WORD MATCH)
    This meant that even if the user mispelt a couple characters wrong, or in a book name which had multiple words, misordered
    them, the programme would still easily find what they meant.

    As the user's input is run against every name in the library, then the matching_letters is a global variable which is set to 0
    initally but will change depending on the name and the search. If the same book name is searched, it'll have the same number of
    matching chars so the condition won't be met. The condition is only met when there is a book name with more matching chars then
    all that came before it. Once this is done, both 'word' and 'search' are split into all their consecutive chars, then compared
    against one another. If there is a find, then the new matching_letters is set, and the book name is added as a guess. Found will
    equal true yet however. Then the loop is broke.
    '''
    global matching_letters
    global guesses
    global found
    #guesses.clear()
    if (word == search):
        #print(word, "found")
        found = True
        displayed_books.append(book)
    else:
        if(num_matching_letters(word, search) > matching_letters):
            spliced_search = get_word_parts(search)
            for i in range(0, len(spliced_search)):        
                if (spliced_search[i] in get_word_parts(word)):
                    #print("Hope youre trying to spell", word)
                    guesses.append(word)
                    matching_letters = num_matching_letters(word, search)
                    found = False
                    break

if __name__ == "__main__":
    print("Testing get word_parts_function")
    print(get_word_parts("Hello"))
    print(get_word_parts("H"))
    print(get_word_parts("He"))
    print(get_word_parts("Hello Hello"))
    print(get_word_parts(""))
    print(get_word_parts(2))

    print("\nTesting search book")
    pprint.pprint(search_for_book("Book_1", "name"))
    print("\n")
    pprint.pprint(search_for_book("Baok_3", "name"))
    print("\n")
    pprint.pprint("Book_6: " + str(search_for_book("Book_6", "name")))
    print("\n")
    pprint.pprint("Lethal White: " + str(search_for_book("Lethal_White", "name")))
    print("\n")
    pprint.pprint(search_for_book("Author_2", "author"))
    print("\n")
    pprint.pprint(search_for_book("Auor_4", "author"))
    print("\n")
    pprint.pprint(search_for_book("1589", "member_id"))
    print("\n")
    pprint.pprint(search_for_book("5", "id"))
    print("\n")
    pprint.pprint(search_for_book("5", "i"))
    






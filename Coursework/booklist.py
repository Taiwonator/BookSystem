# Import the file database
import database as db

#These import matplotlib so I can plot the graph in tkinter
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def display_pie_chart_in(frame):
    # This simply creates a new figure, to this we can add a graph
    figure = matplotlib.figure.Figure()
    
    # Here we add a subplot. As we want 2 to display, the specifcations 121 and 122 place them side by side 
    sub = figure.add_subplot(121)
    sub2 = figure.add_subplot(122)
    
    # book_info contains the dictionary containing the checkout number info
    book_info = db.format_occurances()
    labels = tuple(book_info.keys())
    sizes = list(book_info.values())
    
    # This variable holds the data on percentages
    book_takeout_info = db.percentage_of_books_out()
    labels2 = tuple(book_takeout_info.keys())
    sizes2 = list(book_takeout_info.values())

    # A pie chart is used to display the data stored. This makes it much easier to compare the books with one another
    # The autopct uses string formatting so you can determine to what decimal place you want the values to show for example
    # In this case, it is displayed as a integer
    sub.pie(sizes, labels=labels, autopct='%1d%%', startangle=90)
    sub2.pie(sizes2, labels=labels2, autopct='%1d%%', startangle=90)
    # This sets the title of the whole figure
    figure.suptitle('Popularity of books', fontsize=12)
    # These set the individual plot titles
    sub.title.set_text('No. Checkouts')
    sub2.title.set_text('Percentage of books out')
    # This embeds the figure within the master frame, which is the function's arguement. This allows us in the menu to add it to any frame we want
    canvas = FigureCanvasTkAgg(figure, master=frame)
    # Place used so it will add on top, when pack used, it doesn't place on top of previous graph
    canvas.get_tk_widget().place(x=0, y=50, width=500, height=400)
    # This actually realises the graph
    canvas.draw()
    # Starts the event loop which displays the figure
    plt.show()


# This changes the font size, as it was too big and didn't look easy to read
plt.rcParams.update({'font.size': 8})
# This makes sure the text stays on the screen as it was cutting off at times
matplotlib.rcParams.update({'figure.autolayout': True})

#File cannot be tested within as it requires a frame which cannot be made here


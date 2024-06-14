'''This module contains the view of the program. 
It contains functions to interact with the user interface and is the main 
application that is run when the program is called. 
Written by Luyando Lisimba on 09/12/2021
'''

import tkinter as tk
import Controller.bookcheckout as bc
import Controller.bookreturn as br
import Controller.booksearch as bs
import Controller.bookrecommend as brec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


###### Global variables used ########
primarycolour = '#9fafca'
secondaryColour = "#0e387a"
##############################

######## Creating the tkinter app canvas to house the application ###########
window = tk.Tk()
window.state("zoomed") #makes the window fully enlarged
window.title("Library Management System")

canvas = tk.Canvas(window,height=1080, width=1920, bg=secondaryColour)
canvas.pack()

frame = tk.Frame(window, bg = primarycolour)
frame.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

################################ Controller ##################################
############################# Helper Functions ###############################
def gettext(textbox):
    '''Function used to get the text from a textbox in TKinter.

    Takes in the text box identifier as parameter and returns the text
    lower case and stripped down.
    '''
    txt = textbox.get()
    return(txt.strip().lower())

def checkoutbook(member_id_field,book_id_field,newframe):
    '''Helper funciton used to checkout a book.
    
    Called with the identifier of the member ID field (entry box), the book ID
    field (textbox) and the frame within which the returned message will be 
    displayed. Also returns a message with all books that a member has that 
    are overdue if any.
    '''
    member_id = bc.getmemberID(gettext(member_id_field))#returns the member ID
    book_id = gettext(book_id_field) #returns the bookID
    if len(bc.getmemberID(member_id)) == 4 and bc.getbookID(book_id):
        status = (bc.checkoutbook(member_id, book_id))#book checkout status               
    else:
        status = ("You have entered an invalid member ID or book ID. \
        Try again")
    status_display = tk.Text(newframe, bg=primarycolour,\
        font=("Times New Roman",10)) ##this displays status of the transaction
    status_display.place(relx=0.5,rely=0.35, relwidth=0.5, relheight=0.2,\
        anchor="n")
    status_display.insert(tk.END, status)

    status2 = bc.check_member_overdues(member_id)
    if status2[0] != []:
        overduelist = (status2[1]+" These are (separated by ||): ")
        for book in status2[0]:            
            overduelist+=("ID: %s Title: %s Author: %s || "\
                %(book[0][0],book[0][2],book[0][3]))

        status2_display = tk.Text(newframe, bg=primarycolour,\
            font=("Times New Roman",10))
        status2_display.place(relx=0.5,rely=0.45, relwidth=0.5,\
            relheight=0.2,anchor="n")
        status2_display.insert(tk.END, overduelist)

def returnbook(book_id_field,newframe):
    '''Helper function used to return a book.
    
    Called with the identifier of the book ID field (entry box) and the 
    frame within which the retured message will be displaeyd.
    '''
    book_id = gettext(book_id_field) #returns the bookID
    if bc.getbookID(book_id):
        status = br.returnbook(book_id) #status of return transaction
    else:
        status = "Invalid book ID entered. Try again."
    status_display = tk.Text(newframe, bg=primarycolour,\
    font=("Times New Roman",10))
    status_display.place(relx=0.5,rely=0.2, relwidth=0.5, relheight=0.2,\
    anchor="n")
    status_display.insert(tk.END, status)

def searchbook(book_title_field, newframe):
    '''Function used to display a book which a user searches for.
    
    The function takes in the book title field (entry box) identifier and 
    the frame in which the output will be displayed. Displays all books with
    the title being searched for. Also displays a list of all books that
    are overdue if any.
     '''
    book_title = gettext(book_title_field)
    books_with_title = bs.getbook(book_title)
    status = "Information about books with this title (separated by '||'): "
    if books_with_title != []:
        for book in books_with_title:
            status = (status+"ID: %s, Genre: %s, Title: %s, Author: %s,\
Purchase Date: %s,Currently with: %s || "%(book[0],book[1],book[2],book[3],\
    book[4],book[5]))
    else:
        status = "book does not exist in the database"
    status_display = tk.Text(newframe, bg=primarycolour,\
        font=("Times New Roman",10))
    status_display.place(relx=0.5,rely=0.2, relwidth=0.5,relheight=0.2,\
        anchor="n")
    status_display.insert(tk.END, status)
    
    ##this part checks for overdue books and gives a list of them if any 
    overduebooks = bs.morethan60()
    if len(overduebooks)>0:
        bookslist =""
        for book in overduebooks:
            bookslist = bookslist+("Book with id: "+str(book[0][0])+\
            " is overdue by "+str(book[1]-60)+" days || ")
        status_display2 = tk.Text(newframe, bg=primarycolour,\
            font=("Times New Roman",10))
        status_display2.place(relx=0.5,rely=0.3, relwidth=0.5, relheight=0.5,\
        anchor="n")
        status_display2.insert(tk.END, bookslist)

def recommendbook(memberField, newframe):
    '''Function used to display recommendations for a user.
    
    Called with the identifier of the member ID field (textbox) and the 
    frame within which the returned message will be displayed.
    '''
    member_id = gettext(memberField)
    if len(bc.getmemberID(member_id)) == 4: 
        member_id =bc.getmemberID(member_id)
        recommendations = brec.getRecommendations(member_id)
        if len(brec.checkFavouriteGenre(member_id)) <=1:
            toreturn = "%s has not read many books. Suggest the following: "\
            %(member_id)
        else:
            toreturn = "Recommend the following books for %s (separated by '||'): "%(member_id)
        for book in recommendations:
            toreturn+="Book ID: %s,Genre: %s Title: %s, Author: %s ||"\
            %(book[0],book[1], book[2], book[3])
    else:
        toreturn = "You have entered an invalid member ID. Please try again."
    status_display = tk.Text(newframe, bg=primarycolour,\
    font=("Times New Roman",10))
    status_display.place(relx=0.5,rely=0.2, relwidth=0.5, relheight=0.7,\
    anchor="n")
    status_display.insert(tk.END, toreturn)

def getMostPopular(newframe):
    '''Function to display grapgh of the most popular genres of books.

    The function is invoked by the push of a button on the book recommend
    menu. The result is displaying a bar graph of the most popular genres
    embedded in the tkinter frame.

    '''
    fig = plt.figure(figsize=(8,8),dpi=100)
    genres = brec.getMostPopularGenre() #gets dict with genre totals
    labelName = []
    totals = []
    for key in genres.keys():
        labelName.append(key)
        totals.append(genres[key])
    labels = (labelName[0],labelName[1],labelName[2],labelName[3],\
    labelName[4],labelName[5],labelName[6]) #Used for our x axis on the graph
    genretotals = totals

    ############## Designing of bar chart #############
    plt.bar(labelName, totals, align = 'center', alpha = 1.0)
    plt.xticks(labels)
    plt.ylabel('Totals')
    plt.xlabel('Genre')
    plt.tight_layout(pad=2.2,w_pad = 0.5,h_pad =0.1)
    plt.title('Most borrowed genres')
    plt.xticks(rotation = 30, horizontalalignment = "center")
    ####################################################

    canvasbar = FigureCanvasTkAgg(fig,master = newframe)
    canvasbar.draw()
    canvasbar.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

##############################################################################


################################### View #####################################
############################## checkout Menu #################################
def checkoutmenu():
    '''Function called to give the book Checkout Menu
    '''
    newframe = tk.Frame(frame)
    newframe.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

    label = tk.Label(newframe,\
    text = "Please enter the user's ID in the form of an email. \
eg coai@lboro.ac.uk (ID should be 4 letters long)",\
    font= ("Times New Roman", 10))
    label.place(relx=0.5,rely=0.05, anchor="n")

    memberField = tk.Entry(newframe,font=("Times New Roman",10))
    memberField.place(relx=0.5,rely=0.1, anchor="n")

    label2 = tk.Label(newframe, text = "Please enter the book ID",\
        font= ("Times New Roman", 10))
    label2.place(relx=0.5,rely=0.15, anchor="n")

    bookField = tk.Entry(newframe,font=("Times New Roman",10))
    bookField.place(relx=0.5,rely=0.2, anchor="n")

    button2 = tk.Button(newframe, text = "Submit",\
    font= ("Times New Roman", 10), command= lambda: checkoutbook(memberField,\
    bookField, newframe))
    #used lambda function so checkout book does not run until button clicked
    button2.place(relx=0.5,rely=0.25, anchor="n")

    homebutton = tk.Button(newframe,text="Back to Home", command=main)
    homebutton.pack(side=tk.BOTTOM)
##############################################################################

############################## Book Return Menu ##############################
def bookReturnMenu():
    '''Function to give the book return Menu
    '''
    newframe = tk.Frame(frame)
    newframe.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

    label = tk.Label(newframe, text = "Please enter the book ID being returned"\
    ,font= ("Times New Roman", 10))
    label.place(relx=0.5,rely=0.05, anchor="n")

    bookField = tk.Entry(newframe,font=("Times New Roman",10))
    bookField.place(relx=0.5,rely=0.10, anchor="n")

    button = tk.Button(newframe, text = "Submit",\
    font= ("Times New Roman", 10), command= lambda: returnbook(bookField,\
    newframe))
    button.place(relx=0.5,rely=0.15, anchor="n")

    homebutton = tk.Button(newframe,text="Back to Home", command=main)
    homebutton.pack(side=tk.BOTTOM)
##############################################################################

############################## Book Search Menu ##############################
def searchBookMenu():
    '''Function to give the book search Menu
    '''
    newframe = tk.Frame(frame)
    newframe.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

    label = tk.Label(newframe,\
    text = "Please enter the book title you are looking for",\
    font= ("Times New Roman", 10))
    label.place(relx=0.5,rely=0.05, anchor="n")

    memberField = tk.Entry(newframe,font=("Times New Roman",10))
    memberField.place(relx=0.5,rely=0.10, anchor="n")

    button = tk.Button(newframe, text = "Find Book",\
    font= ("Times New Roman", 10), command= lambda: searchbook(memberField,\
    newframe))
    button.place(relx=0.5,rely=0.15, anchor="n")

    homebutton = tk.Button(newframe,text="Back to Home", command=main)
    homebutton.pack(side=tk.BOTTOM)

##############################################################################

############################## Recommend Book Menu ###########################
def recommendBookMenu():
    '''Function to give the book recommendation Menu
    '''
    newframe = tk.Frame(frame)
    newframe.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

    label = tk.Label(newframe, text = "Please enter the member ID to get \
recommendations",font= ("Times New Roman", 10))
    label.place(relx=0.5,rely=0.05, anchor="n")

    memberField = tk.Entry(newframe,font=("Times New Roman",10))
    memberField.place(relx=0.5,rely=0.10, anchor="n")

    bookRecommendButton = tk.Button(newframe, text = "Get Recommendations",\
    font= ("Times New Roman", 10), command= lambda: recommendbook(memberField,\
    newframe))
    bookRecommendButton.place(relx=0.5,rely=0.15, anchor="n")

    popularGraphButton = tk.Button(newframe, text = "Show most borrowed genres",\
    font= ("Times New Roman", 10), command= lambda: getMostPopular(newframe))
    popularGraphButton.place(relx=0.5,rely=0.30, anchor="n")

    homebutton = tk.Button(newframe,text="Back to Home", command=main)
    homebutton.pack(side=tk.BOTTOM)

###############################################################################

############################## Main program starts here #######################
########################## GUI of the main program ############################

title = tk.Label(frame,text="University Library Management System",\
font=("Times New Roman",20), bg = primarycolour)
title.pack() 


################# Main function of the program ###############################
def main():
    '''Function called at the start of the program
    '''
    newframe = tk.Frame(frame, bg=primarycolour)
    newframe.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)
    title = tk.Label(frame,text="What would you like to do?",\
    font=("Times New Roman",15), bg = primarycolour)
    title.place(relx=0.5,rely=0.1,relheight=0.1,anchor="n")

    checkoutbutton = tk.Button(newframe,text="Checkout Book",\
    command=checkoutmenu, bg=primarycolour)
    checkoutbutton.place(relx=0.5,rely=0.2,relheight=0.1, relwidth=0.4,\
    anchor="n")

    returnbutton = tk.Button(newframe,text="Return Book",\
    command=bookReturnMenu, bg=primarycolour)
    returnbutton.place(relx=0.5,rely=0.4,relheight=0.1, relwidth=0.4,\
    anchor="n")

    searchBookButton = tk.Button(newframe,text="Search Book",\
    command=searchBookMenu,bg=primarycolour)
    searchBookButton.place(relx=0.5,rely=0.6,relheight=0.1, relwidth=0.4,\
    anchor="n")

    recommendBookButton = tk.Button(newframe,text="Book Recommendations",\
    command=recommendBookMenu, bg=primarycolour)
    recommendBookButton.place(relx=0.5,rely=0.8,relheight=0.1, relwidth=0.4,\
    anchor="n")

main()

window.mainloop()



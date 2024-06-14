'''
This module contains functions to allow a user to return a book. 
Contains functions to: check if a book exists; if a book is available or
loaned out; and check if a book is overdue. 
Written by Luyando Lisimba on 08/12/2021
'''

import Model.database as db 
from Controller.booksearch import morethan60, getBookByID

def checkid(bookID):
    '''A funciton used to check if a book exists in the database.

    The function takes in a bookID as a parameter and returns a boolean
    value; True if the book exists and False if teh book does not exist.
    '''
    booklist = db.getbooks()
    found = False 
    for book in booklist:
        if book[0] == str(bookID):
            found = True 
            break
    return found

def isAvailable(bookID):
    '''Checks if a book is currently in the library or has been loaned out
    It takes in a book ID as a parameter and returns a boolean value;
    True if book is available (in library), False if book is out on loan.
    '''
    booklist = db.getbooks()
    bookAvailable = True 
    for book in booklist:
        if (book[0] == str(bookID)) and (book[5] != '0'):
            bookAvailable = False 
            break
    return bookAvailable

def checkmorethan60(returningBook): 
    '''Checks if a returning book has been loaned out for more than 60 days
    
    A list containing the book information should be passed into the function
    and it then returns a boolean value; True if more than 60 and False if not
    '''
    overdueBooks = morethan60()
    for book in overdueBooks:
        if book[0][0] == returningBook[0]:  
            return [True,book[1]]
    return [False, ""]
  
def returnbook(bookID):
    '''Function to return a book into the library.
    
    Takes in the book ID as a parameter. If book is returned successfuly the
    transaction is written to the log file and the book database is updated.
    '''
    if checkid(bookID) and not isAvailable(bookID):
        returningBook = getBookByID(bookID)
        isOverdue = checkmorethan60(returningBook)
        returningBook[5] = "0"
        books = db.getbooks()
        for i in range(0, len(books)):
            if books[i][0] == returningBook[0]:
                books[i] = returningBook
                break
        if db.savebooks(books):
            db.log(returningBook)
            if isOverdue[0]:
                return("Book returned successfully. However, the book was \
overdue by %d days."%(isOverdue[1]-60))
            return("Book returned successfully")
        else:
            return("book return was not successful")
    else:
        return("the book is already available or does not exist.")

############ module tests ###########
assert checkid(1) == True, "should be True"
assert checkid("one") == False, "should be True"

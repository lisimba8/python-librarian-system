'''This is the Database access module

Every transaction that needs access to the database will make a call
to one of the functions in this module. It contains functions to: 
get a list of all books in the database; rewrite a list of books 
to the database; log transactions to log file; read from the log file.
Written by Luyando Lisimba on 06/12/2021
'''
from datetime import date 

def getbooks():
    ''' Function to get a list of all books in database.
    
    This function will be used to access the database of 
    books books. It will return a list of lists where the each list 
    within contains details about one book.
    '''
    booklist = []
    try:
        f = open ("database.txt", "r") #checks if database exists
    except OSError:  #if can not find the database file
        return booklist #returns an empty list rather than crashing
    else:
        for line in f:
            booklist.append(line.strip().split("|"))
        f.close()
        return booklist

def savebooks(books):
    '''
    This funciton will be used to update the database
    whenever a book has been checked out or returned
    '''
    try:
        f = open("database.txt", "w")
    except OSError:
        return False
    else:
        booklist = []
        for book in books:
            booklist.append("|".join(book))
        booklist = "\n".join(booklist)
        f.write(booklist)
        f.close()
        return True

def log(book):
    '''function used to write checkout or return logs to the log file
    
    It takes in a book that has just been checked out or returned as a list
    and then creates a string that can be written to the log file.
    '''
    newlog = preparelog(book)
    f = open("logfile.txt", "a")
    f.write(newlog + "\n")
    f.close()

def preparelog(book):
    '''function takes in a book parameter and returns a string 
    
    the book taken in must be in a list. A  date string is 
    produced as well and this is used to log to the file 
    '''
    today = date.today().strftime("%Y-%m-%d") #getting the current date in Y-m-d format
    book = "|".join(book)
    return "~".join([today,book])

def getlogs():
    '''gets logs out of log file and returns them as list of lists
    
    Each list contains the the date of log as first element and the book information
    as second element.
    '''
    booklist = []
    f = open("logfile.txt", "r")
    for line in f:
        line = line.strip().split("~")
        booklist.append(line)
    return booklist
    f.close()

############ module tests ###########
assert len(getlogs()) >0,\
"There should be some transactions already logged in the log file."
assert len(getbooks()) >0, "There should be more that one book in the database"









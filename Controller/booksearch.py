'''Module to search for books depending on requirements

It contains functions to help the user search for a book by giving the book
title or book ID. It also contains functions to allow user to search for books
that are overdue and a function to check how long a book has been out on loan
for.
Written by Luyando Lisimba on 08/12/2021 
'''
import Model.database as db
import datetime as dt

def getbook(title):
    ''' Function used to get book from the database using it's title.

    this function checks the database for any books with the title
    that has been passed in as a parameter. 
    '''
    booklist = []
    books = db.getbooks()
    for book in books:
        if book[2].lower() == title.strip().lower():
            booklist.append(book)
    return(booklist)

def getBookByID(bookID):
    '''Function used to get book from the database using it's title.

    This function checks the database for any books with the ID
    that the has been passed in as a parameter.
    '''
    booklist = db.getbooks()
    for book in booklist:
        if book[0] == str(bookID):
            return book 

def check_loan_days(log):
    '''checks how book has been loaned out for and returns days as integer
    
    it takes in a single log form the log file as a parameter and uses this
    to determine how long each book has been loaned out for. 
    '''
    olddate = dt.date.fromisoformat(log[0])#converts date to date class type
    delta = dt.date.today() - olddate #difference between checked out date and today 
    days_on_loan = delta.days
    return days_on_loan
    
def morethan60():
    '''Checks for all books that have been loaned out for more than 60 days

    it then returns a list of all books loaned out for more than 60 days
    that have not been returned.
    '''
    ##this part of function gets all logs that have been out for >60 days
    booklist = []
    logs = db.getlogs()
    for log in logs:
        book = log[1].split("|")
        days_on_loan = check_loan_days(log)
        if days_on_loan >60 and book[5] != "0":
            if [book,days_on_loan] not in booklist:
                booklist.append([book,days_on_loan])
                
    ##this part filters out all books that have been returned
    toreturn = []
    for book in booklist:
        # print(book)
        for i in range(len(logs)-1, -1, -1):
            log = logs[i][1].split("|")
            if book[0][0]==log[0] and log[5] =="0":
                break
            if book not in toreturn:
                toreturn.append(book)  
    return(toreturn)

# (morethan60()) #clear this before submission 

############ module tests ###########
if __name__ == "__main__":
    getbook("fault in our stars") 
    # Book ID for fault in our stars should be 2 therefore should return 2
    getBookByID("2")
    # should return "fault in our stars"
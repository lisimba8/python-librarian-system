'''this module is used to checkout a book from the library

the module contains fucntions that allow member to checkout a book 
and also allow for memebr to check for all books that they have borrowed
that are overdue. Also contains functions to get member ID and book ID
and perform validation on the two.
Written by Luyando Lisimba on 08/12/2021
'''
import Model.database as db
from Controller.booksearch import morethan60 

def getbookID(userInput):
    '''this function is used to get the ID of a book 

     It asks the user for an ID and performs a validaiton check
     to ensure that the input is indeed an integer.
     '''
    try:
        int(userInput)
    except ValueError:
        return False
    else:
        return True
    

def getmemberID(userinput):
    '''this function is used to get the ID of a member from email address 

     It takes an id in the form of an email address. It then 
     gets id from email and performs a validaiton check
     to ensure that the input is indeed a 4 letter ID. It returns
     the valid ID or an error meassage if not valid.
     '''
    valid = False
    id = userinput.split("@")[0] 
    for letter in id:
            try: #used to check if the member ID contains any integers
                int(letter)
            except ValueError: #integer would cause a value error 
                valid = True
            else:
                valid = False
                print("ID must be a combination of 4 letters")
                break
    if len(id)>4: #ensure that each id is 4 letters long
        valid = False
        print("ID must be a combination of 4 letters. Enter email\
            eg. coll@lboro.ac.uk")
    if valid:
        return id
    else:
        return "Id is invalid"

    
            
def checkoutbook(memberID, bookID):
    '''this function is used to checkout a book using it's ID

    It takes in the ID as a parameter. If the book has already been 
    borrowed, the book can not be checked out. Otherwise, the database 
    is updated if the book is available. 
    '''
    books = db.getbooks()
    book_exists = False #flag used to check if the book exists
    for i in range(0,len(books)):
        if books[i][0] == bookID and books[i][5] == "0":
            books[i][5] = memberID
            if db.savebooks(books): #if saving file was successful, show success message 
                db.log(books[i]) #logs the transaction onto the log file
                return("Booked was checked out successfully")
            else:
                return("Error when checking out book")
                
        elif books[i][0] == bookID and books[i][5] != "0":
            return("the book has already been borrowed")

    if book_exists == False: return("book not found")

def check_member_overdues(memberID):
    '''function to check if member has any books overdue
    
    this returns a list of all the books overdue by the member.
    The retrun value is a list of lists. Each list is a book's details. 
     '''
    total_overdue = 0
    overdue_list = []
    toreturn = [""] #needs at least one elemnt for first element comparison 
    books = morethan60() #list of books that are overdue 
    if books != []:
        for book in books:
            if book[0][5] == memberID:
                toreturn = book
                total_overdue+=1
                overdue_list.append(book)
            elif book[0][0] == toreturn[0] and book[5] == '0':#check if book reappears
                total_overdue -= 1  #remove the book from member's overdue books 
                overdue_list.remove(toreturn)
                toreturn = [""]
        if total_overdue>0:
            toreturn = ("%s has %d book(s) currently overdue"%(memberID,\
            total_overdue))

    return [overdue_list, toreturn]


    
################### module tests ##################
assert getbookID("123") == True, "Error, the book ID should be valid." 
assert getbookID("12s2") == False, "Error. Book ID should not be valid" 
assert getmemberID("luya@lboro.ac.uk") == "luya", "Should return only the\
user id when email is passed into the function"
if __name__ == "__main__":
    check_member_overdues("luya")
    # Should return a list containing a list as first element and a message
    # showing how many books a member has overdue if any as second element.
    getmemberID("coll@lboro.ac.uk")
    # Should return "coll"
    getmemberID("collchester@lboro.ac.uk")
    # Should print "ID must be a combination of 4 letters. Enter email 
    # eg. coll@lboro.ac.uk" to the console and return "Id is invalid"
    getmemberID("col3@lboro.ac.uk")
    # Should print "ID must be a combination of 4 letters" to
    # console and return "Id is invalid"


        
        
    

    
    



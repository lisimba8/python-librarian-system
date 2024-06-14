'''Contains functions that are used to recommend new books to members

It contains a function to check the favourite genres of a member. These 
genres can then be used to produce a list of recommended books. It aslo 
function to get the most read genre from teh logs which will be used to 
plot graph. 
Written by Luyando Lisimba on 08/12/2021
'''
import Model.database as db

def checkFavouriteGenre(memberID):
    '''Function to check favourite genre of a member.
    
    The function takes in a member's ID and then returns a list
    of all the genres that they have read so far.
     '''
    genreList = []
    logs = db.getlogs()
    for log in logs:
        book = log[1].split("|")
        if memberID.strip().lower() == book[5]:
            if book[1] not in genreList:
                genreList.append(book[1])
    return genreList
    
def getNewLogs():
    '''Function to get all logs without returnning logs in the list
    
    a list of all transactions without the returning transactions is produced;
    that is a list of all checkout transactions. This allows for clearer view 
    of which books have been loaned out more than others. 
    '''
    logs = db.getlogs()
    newlogs = []
    for log in logs:
        book = log[1].strip().split("|")
        if book[5] != "0":
            newlogs.append(book)
    return(newlogs)

def getRecommendations(memberID):
    '''Function to get a list of recommended books for the user.
    
    The function takes in a list of the user's favourite genres. It then 
    uses these to get more books of their favourite genres from the database.
    It also provides the functionality to recommend new books for users that
    have not not read as much (i.e. read 1 or less books) by recommending 
    similar genres.
    '''

    genrelist = checkFavouriteGenre(memberID)
    books = db.getbooks()
    logs = getNewLogs()
    recommendedBooks = []
    if len(genrelist)<=1: #recommend books to user even if not read much
        n=0 #counter makes sure recommended books < 10
        genres = {"horror":"thriller", "thriller":"sci-fi",\
            "sci-fi":"drama","drama":"romance", "romance":"comedy",\
            "comedy":"action", "action":"horror"}
        currentgenre = "horror"
        while n<10:
            for book in books:
                if book[1] == currentgenre:
                    recommendedBooks.append(book)
                    break
            books.remove(book)
            currentgenre = genres[currentgenre]
            n+=1
    else: #if member has read more than one book
        for log in logs:
            if log[1] in genrelist:
                recommendedBooks.append(log)
        totals = {}
        for genre in genrelist:
            totals[genre]= 0
        for book in recommendedBooks:
            totals[book[1]]+=1
        totals = dict(sorted(totals.items(), key=lambda item: item[1],\
        reverse = True))
        #above line of code is used to sort the dictionary using the values
        #rather than keys     
        total = 0
        for key in totals: 
            for log in logs:
                if key == log[1]:
                    if log not in recommendedBooks:
                        recommendedBooks.append(log)
                        total+=1
                    if total >= 10: break
            if total >= 10: break#num of recommended books should not be >10
    return(recommendedBooks[:10])#further ensures that recommended books <=10

def getMostPopularGenre():
    '''Function to get the list of the most borrowed genres in the library.
    
    It returns a dictionary with each genre as the key and the total number 
    of checkouts as the value.
    '''
    logs = getNewLogs()
    totals = {"sci-fi":0, "drama":0,"horror":0,"thriller":0,"comedy":0,\
    "action":0,"romance":0}
    for log in logs:
        if log[1].lower() in totals.keys():
            totals[log[1].lower()]+=1
    return(totals)    

########### module tests ###########
assert len(getRecommendations(" muna  ")) <= 10,\
"Should be less than 10 reccomended books"
assert len(getRecommendations(" luya  ")) <= 10,\
"Should be less than 10 reccomended books"
assert len(getRecommendations(" coll  ")) <= 10,\
"Should be less than 10 reccomended books"


# Python Librarian System

This program can be used by a librarian to manage the borrowing and returning of books in a library. It also provides functionality to recommend books to users (new or returning) and allows users to search for specific books in the database by name.

## Features

- **Borrow and Return Books**: Members can borrow and return books.
- **Book Recommendations**: Provides book recommendations for users.
- **Book Search**: Allows users to search for a specific book using its name.
- **Popular Genre Graph**: Displays the most popular genre graph.
- **Logs Transactions**: Keeps a log of all transactions that occur in the library.

## Program Structure

The program follows the Model-View-Controller (MVC) design pattern:

- **Model**: Manages the data of the application.
  - Includes modules that handle all transactions with the text files storing information 
  - `database.txt`: Contains data on each book.
  - `log.txt`: Contains logs of all transactions in the library.

- **Controller**: Handles the interactions and connects the Model and the View.
  - Includes modules that handle the logic for borrowing, returning, recommending, and searching books.

- **View**: Manages the display of information and user interaction.
  - `menu.py`: The main module of the program. This is the module to be called to start the application.

## Getting Started

1. **Clone the Repository**
    ```bash
    git clone https://github.com/lisimba8/python-librarian-system.git
    cd python-librarian-system
    ```

2. **Run the Application**
    ```bash
    python menu.py
    ```

## Usage

### Borrowing and Returning Books

- When a member borrows or returns a book, the system updates the `database.txt` file accordingly.
- The `log.txt` file records the transaction details.

### Book Recommendations

- The system can recommend books to users based on their borrowing history.
- New users can get a suggested list of books even if they have not checked out any books before.

### Searching for Books

- Users can search for a specific book by its name in the database.

### Popular Genre Graph

- The application displays the most popular genre graph, embedded within the program's interface.
##
#### Contributions are welcome! Feel free to fork this repository and submit pull requests or take it further as you wish :)

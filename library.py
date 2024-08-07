import difflib


def get_closest_match(word, possibilities):
    """
    Using a sequence matcher, it finds the closest match to a given word from a list of options.

    Args: word (str): Search for a close match.
        possibilities (list of str): A list of potential matches to compare to the provided word.

    Return: The closest matching string from the possibilities list if found; None otherwise.

    'difflib.get_close_matches' gets the closest matches depending on a specified cutoff.
    """

    #Get potential matches based on similarity
    matches = difflib.get_close_matches(word, possibilities, n=1, cutoff=0.0)

    # return the first match if found
    if matches:
        return matches[0]

    return None


class Book:
    """
    Represents a book in a library, with borrowing and returning options.

    Attributes:
        book_id (int): A unique identification for the book.
        name(str): The book's title.
        The availability str): field indicates if the book is available ("Free" or "Not Available").
        borrower(str): The borrower's username, which defaults to None.

    Methods:
        borrow_book: Allows a user to borrow a book that is available.
        return_book: Allows the user to return the book that they are presently borrowing.
    """

    def __init__(self, book_id, name, availability="Free", borrower=None):

        self.book_id = book_id
        self.name = name
        self.availability = availability
        self.borrower = borrower

    def borrow_book(self, username):
        # Allows a username to borrow a book.
        if self.borrower is not None:
            print("This book is already borrowed.")
        else:
            self.borrower = username
            self.availability = "Not Available"
            print(f"{username} has successfully borrowed {self.name}.")

    def return_book(self, username):
        # Allows a username to return a book.
        if self.borrower == username:
            self.borrower = None
            self.availability = "Free"
            print(f"{username} has successfully returned {self.name}.")
        else:
            print("This book was not borrowed by this user.")



class Library:
    """
    Represents a library's collection of books and provides ways for managing them.

    Attributes:
        library_books (dict): Stores book objects using their IDs as keys.

    Methods:
        display_available_books: Outputs a list of books that are presently available for borrowing.
        view_borrowed_books: Outputs a list of books borrowed by a certain user.
        Borrow_book: Manages the process of a user borrowing a book by name.
        Return_book: Manages the process of a user returning a book by name.
    """

    def __init__(self) -> None:
        #Initializes a Library object, storing books in a dictionary.

        self.library_books = {
            1:Book(1, "Foundation of Software engineering"),
            2:Book(2, "Mystery of the SCarred Schoolboys"),
            3:Book(3, "Sign of the artificial Pearls")
        }

    def add_books(self):
        while True:
            while True:
                user_book = input("Enter your book's name: ").strip()
                if is_alpha_numeric(user_book):  # Check if the book name is alphanumeric
                    user_book_lower = user_book.lower()
                    # Check if the book is already available in the library
                    if any(user_book_lower == book.name.lower() for book in library.library_books.values()):
                        print("This book is already in the library, please enter a unique name.")
                    else:
                        break
                else:
                    print("Please enter an alphanumeric name.")

            book_id_ = sorted(library.library_books.keys())[-1] + 1
            if book_id_ not in library.library_books:
                library.library_books[book_id_] = Book(book_id_, user_book)
                print(f"Book '{user_book}' added successfully with ID {book_id_}.")

            add_choice = input("Do you want to add another book? (y/n): ")
            if not y_or_n(add_choice):
                break

    def display_available_books(self):
        # Displays books with 'Free' availability.
        available_books = [ book for book in self.library_books.values()
                            if book.availability == "Free"]
        if available_books:
            sorted_books = sorted(available_books, key=lambda x: x.book_id)
            print("\nAvailable books: ")
            for book in sorted_books:
                print(f"{book.book_id}, Title: {book.name}")
        else:
            print("There are no available books")

    def view_borrowed_books(self, username):
        # Displays books currently borrowed by the user.
        print(f"\nBooks borrowed by {username}:")
        borrowed = [book for book in self.library_books.values() if book.borrower == username]
        if borrowed:
            for book in borrowed:
                print(f"- {book.name} (ID: {book.book_id})")
        else:
            print("You have no borrowed books.")

    def borrow_book(self, username):
        # User borrows a book
        self.display_available_books()
        while True:
            book_name = input("\nEnter the name of the book you want to borrow: ")
            if is_alpha_numeric(book_name):
                book_titles = [
                    book.name
                    for book in self.library_books.values()
                    if book.availability == "Free"
                    ]
                closest_match = get_closest_match(book_name, book_titles)
                break
            else:
                print("\nPlease enter an alphanumeric name.")

        if closest_match:
            # CLosest match to the book that is borrowed
            confirm = input(f"\nDid you mean '{closest_match}'? (y/n): ")
            if y_or_n(confirm):
                for book in self.library_books.values():
                    if book.name == closest_match and book.availability == "Free":
                        book.borrow_book(username)
                        return
            print("Book not found")

    def return_book(self, username):
        # User returns a book
        while True:
            book_name = input("Enter the title of the book you want to return: ")
            if is_alpha_numeric(book_name):
                # Checks if the name of the book is alphanumeric
                book_titles = [
                    book.name
                    for book in self.library_books.values()
                    if book.borrower == username
                    ]
                closest_match = get_closest_match(book_name, book_titles)
                break
            else:
                print("Please enter an alphanumeric name.")

        if closest_match:
            # CLosest match to the book that is borrowed
            confirm = input(f"Did you mean '{closest_match}'? (y/n): ")
            if y_or_n(confirm):
                for book in self.library_books.values():
                    if book.name == closest_match and book.borrower == username:
                        book.return_book(username)
                        return
        print("Book not found in your borrowed list.")

def is_alpha_numeric(username):
    """
    Checks if a given text is alphanumeric (may contain spaces).

    Arguments: Username (str): The string to be checked.

    Returns a bool: True if the string is alphanumeric (including spaces), False otherwise.

    It is used to check user input for names that do not contain any special characters.
    """
    if username:  # Check if username is not empty
        return all(char.isalnum() or char.isspace() for char in username)
    return False  # Return False if username is empty

def y_or_n(answer):
    while True:
        if answer.lower() == "y":
            return True
        elif answer.lower() == 'n':
            return False
        else:
            print("Enter either 'y' or 'n' (Yes/No)")

if __name__ == "__main__":
    # This block ensures the code within it only runs if the script is executed directly

    while True:
        current_user = input("Enter your username: ").strip()
        if is_alpha_numeric(current_user):
            break
        else:
            print("Please enter an alphanumeric username.")

    library = Library()

    while True:
        # Main loop providing the Library Menu. Continues until the user chooses to exit.
        print("\n============LIBRARY MENU============ ]")
        print("1. Add your own book")
        print("2. Borrow a Book")
        print("3. Return a Book")
        print("4. View Your Books")
        print("5. Display Available Books")
        print("6. Exit")

        while True:
            # Makes sure the user inputs a number between 1 to 5
            choice = input("Enter your choice: ")

            if choice.isnumeric():
                chint = int(choice)
                if 1 <= chint and chint <= 6:
                    break
                print("Enter a number between 1 to 6.")
            else:
                print("Enter a number between 1 to 6.")

        # Call the function that the user chose
        if choice == '1':
            library.add_books()
        elif choice == '2':
            library.borrow_book(current_user)
        elif choice == '3':
            library.return_book(current_user)
        elif choice == '4':
            library.view_borrowed_books(current_user)
        elif choice == '5':
            library.display_available_books()
        elif choice == '6':
            print("Exiting Library System...")
            break # Exit the main loop

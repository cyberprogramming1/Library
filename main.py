from database import DatabaseConnection
from admin import Admin
from user import User
from book import Book

def get_user_id():
    while True:
        try:
            user_id = int(input("Enter your user ID: "))
            if user_id <= 0:
                print("User ID must be a positive integer.")
            else:
                return user_id
        except ValueError:
            print("Invalid input. Please enter a valid integer for the user ID.")

def main():
    db_connection = DatabaseConnection()

    while True:
        role = input("Enter your role (admin/user) or type 'exit' to quit: ")
        if role.lower() == "exit":
            break
        elif role.lower() == "admin":
            admin = Admin(db_connection)
            while True:
                action = input("Enter action (add/update/delete/list/search/report) or type 'back' to go back: ")
                if action.lower() == "back":
                    break
                elif action.lower() == "add":
                    title = input("Enter book title: ")
                    author = input("Enter author name: ")
                    ISBN = input("Enter ISBN: ")
                    quantity = int(input("Enter quantity: "))
                    book = Book(title, author, ISBN, quantity)
                    admin.add_book(book)
                elif action.lower() == "update":
                    book_id = int(input("Enter book ID to update: "))
                    new_title = input("Enter new title: ")
                    new_author = input("Enter new author name: ")
                    new_ISBN = input("Enter new ISBN: ")
                    new_quantity = int(input("Enter new quantity: "))
                    admin.update_book(book_id, new_title, new_author, new_ISBN, new_quantity)
                elif action.lower() == "delete":
                    book_id = int(input("Enter book ID to delete: "))
                    admin.delete_book(book_id)
                elif action.lower() == "list":
                    admin.list_books()
                elif action.lower() == "search":
                    title = input("Enter book title: ")
                    admin.search_book(title)
                elif action.lower() == "report":
                    admin.generate_report()
                else:
                    print("Invalid action.")
        elif role.lower() == "user":
            user = User(db_connection)
            while True:
                action = input("Enter action (search/borrow/return/list_borrowed/register/update/view_history) or type 'back' to go back: ")
                if action.lower() == "back":
                    break
                elif action.lower() == "search":
                    title = input("Enter book title: ")
                    user.search_book(title)
                elif action.lower() == "borrow":
                    book_id = int(input("Enter book ID to borrow: "))
                    user_id = get_user_id()
                    user.borrow_book(user_id, book_id)
                elif action.lower() == "return":
                    book_id = int(input("Enter book ID to return: "))
                    user_id = get_user_id()
                    user.return_book(user_id, book_id)
                elif action.lower() == "list_borrowed":
                    user_id = get_user_id()
                    user.list_borrowed_books(user_id)
                elif action.lower() == "register":
                    name = input("Enter your name: ")
                    email = input("Enter your email: ")
                    user.register_user(name, email)
                elif action.lower() == "update":
                    user_id = get_user_id()
                    new_name = input("Enter new name: ")
                    new_email = input("Enter new email: ")
                    user.update_user(user_id, new_name, new_email)
                elif action.lower() == "view_history":
                    user_id = get_user_id()
                    user.view_borrowing_history(user_id)
                else:
                    print("Invalid action.")
        else:
            print("Invalid role.")

    # Close the database connection
    db_connection.close_connection()

if __name__ == "__main__":
    main()

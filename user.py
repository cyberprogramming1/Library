class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def user_exists(self, user_id):
        query = "SELECT COUNT(*) FROM Users WHERE ID = ?"
        self.db_connection.cursor.execute(query, (user_id,))
        return self.db_connection.cursor.fetchone()[0] > 0

    def search_book(self, title):
        query = "SELECT * FROM Books WHERE Title LIKE ?"
        values = ('%' + title + '%',)
        self.db_connection.cursor.execute(query, values)
        books = self.db_connection.cursor.fetchall()
        print("Search results:")
        for book in books:
            print(book)

    def borrow_book(self, user_id, book_id):
        if not self.user_exists(user_id):
            print(f"User ID {user_id} does not exist.")
            return

        # Check if the book is available
        query = "SELECT Quantity FROM Books WHERE ID=?"
        values = (book_id,)
        self.db_connection.cursor.execute(query, values)
        quantity = self.db_connection.cursor.fetchone()
        if not quantity:
            print(f"Book ID {book_id} does not exist.")
            return
        quantity = quantity[0]
        if quantity > 0:
            # Decrement the quantity of the book
            query = "UPDATE Books SET Quantity = Quantity - 1 WHERE ID = ?"
            self.db_connection.cursor.execute(query, (book_id,))
            # Record the borrowing transaction
            query = "INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate, DueDate) VALUES (?, ?, GETDATE(), DATEADD(day, 14, GETDATE()))"
            values = (user_id, book_id)
            self.db_connection.cursor.execute(query, values)
            self.db_connection.conn.commit()
            print("Book borrowed successfully.")
        else:
            print("Sorry, the book is not available.")

    def list_borrowed_books(self, user_id):
        query = "SELECT Books.Title, Books.Author, BorrowedBooks.BorrowDate, BorrowedBooks.DueDate \
                 FROM BorrowedBooks INNER JOIN Books ON BorrowedBooks.BookID = Books.ID \
                 WHERE BorrowedBooks.UserID = ? AND BorrowedBooks.ReturnDate IS NULL"
        self.db_connection.cursor.execute(query, (user_id,))
        borrowed_books = self.db_connection.cursor.fetchall()
        if borrowed_books:
            print("Borrowed Books:")
            for book in borrowed_books:
                print(book)
        else:
            print("You have not borrowed any books.")

    def return_book(self, user_id, book_id):
        # Check if the book is borrowed by the user
        query = "SELECT * FROM BorrowedBooks WHERE UserID=? AND BookID=? AND ReturnDate IS NULL"
        values = (user_id, book_id)
        self.db_connection.cursor.execute(query, values)
        borrowing_record = self.db_connection.cursor.fetchone()
        if borrowing_record:
            # Update the return date
            query = "UPDATE BorrowedBooks SET ReturnDate = GETDATE() WHERE UserID=? AND BookID=?"
            self.db_connection.cursor.execute(query, values)
            # Increment the quantity of the book
            query = "UPDATE Books SET Quantity = Quantity + 1 WHERE ID = ?"
            self.db_connection.cursor.execute(query, (book_id,))
            self.db_connection.conn.commit()
            print("Book returned successfully.")
        else:
            print("You haven't borrowed this book.")

    def register_user(self, name, email):
        query = "INSERT INTO Users (Name, Email) VALUES (?, ?)"
        values = (name, email)
        self.db_connection.cursor.execute(query, values)
        self.db_connection.conn.commit()
        print("User registered successfully.")

    def update_user(self, user_id, new_name, new_email):
        query = "UPDATE Users SET Name=?, Email=? WHERE ID=?"
        values = (new_name, new_email, user_id)
        self.db_connection.cursor.execute(query, values)
        self.db_connection.conn.commit()
        print("User information updated successfully.")

    def view_borrowing_history(self, user_id):
        query = "SELECT Books.Title, BorrowedBooks.BorrowDate, BorrowedBooks.DueDate \
                 FROM BorrowedBooks INNER JOIN Books ON BorrowedBooks.BookID = Books.ID \
                 WHERE BorrowedBooks.UserID = ? AND BorrowedBooks.ReturnDate IS NOT NULL"
        self.db_connection.cursor.execute(query, (user_id,))
        borrowing_history = self.db_connection.cursor.fetchall()
        if borrowing_history:
            print("Borrowing History:")
            for record in borrowing_history:
                print(record)
        else:
            print("No borrowing history found for this user.")

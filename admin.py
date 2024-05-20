class Admin:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_book(self, book):
        query = "INSERT INTO Books (Title, Author, ISBN, Quantity) VALUES (?, ?, ?, ?)"
        values = (book.title, book.author, book.ISBN, book.quantity)
        self.db_connection.cursor.execute(query, values)
        self.db_connection.conn.commit()
        print("Book added successfully.")

    def update_book(self, book_id, new_title, new_author, new_ISBN, new_quantity):
        query = "UPDATE Books SET Title=?, Author=?, ISBN=?, Quantity=? WHERE ID=?"
        values = (new_title, new_author, new_ISBN, new_quantity, book_id)
        self.db_connection.cursor.execute(query, values)
        self.db_connection.conn.commit()
        print("Book updated successfully.")

    def delete_book(self, book_id):
        query = "DELETE FROM Books WHERE ID=?"
        values = (book_id,)
        self.db_connection.cursor.execute(query, values)
        self.db_connection.conn.commit()
        print("Book deleted successfully.")

    def list_books(self):
        query = "SELECT * FROM Books"
        self.db_connection.cursor.execute(query)
        books = self.db_connection.cursor.fetchall()
        for book in books:
            print(book)

    def search_book(self, title):
        query = "SELECT * FROM Books WHERE Title LIKE ?"
        values = ('%' + title + '%',)
        self.db_connection.cursor.execute(query, values)
        books = self.db_connection.cursor.fetchall()
        for book in books:
            print(book)
    
    

    # def generate_report(self):
    #     # Total number of books
    #     query = "SELECT COUNT(*) FROM Books"
    #     self.db_connection.cursor.execute(query)
    #     total_books = self.db_connection.cursor.fetchone()[0]

    #     # Total number of users
    #     query = "SELECT COUNT(*) FROM Users"
    #     self.db_connection.cursor.execute(query)
    #     total_users = self.db_connection.cursor.fetchone()[0]

    #     # Total number of borrowed books
    #     query = "SELECT COUNT(*) FROM BorrowedBooks"
    #     self.db_connection.cursor.execute(query)
    #     total_borrowed_books = self.db_connection.cursor.fetchone()[0]

    #     # Most borrowed book
    #     query = "SELECT TOP 1 Title, COUNT(*) AS BorrowCount FROM BorrowedBooks GROUP BY Title ORDER BY BorrowCount DESC"
    #     self.db_connection.cursor.execute(query)
    #     most_borrowed_book = self.db_connection.cursor.fetchone()

    #     # Number of users with overdue books
    #     query = "SELECT COUNT(*) FROM BorrowedBooks WHERE ReturnDate IS NULL AND DueDate < GETDATE()"
    #     self.db_connection.cursor.execute(query)
    #     users_with_overdue_books = self.db_connection.cursor.fetchone()[0]

    #     print("Library Report:")
    #     print(f"Total Books: {total_books}")
    #     print(f"Total Users: {total_users}")
    #     print(f"Total Borrowed Books: {total_borrowed_books}")
    #     if most_borrowed_book:
    #         print(f"Most Borrowed Book: {most_borrowed_book[0]} (Borrow Count: {most_borrowed_book[1]})")
    #     else:
    #         print("Most Borrowed Book: None")
    #     print(f"Number of Users with Overdue Books: {users_with_overdue_books}")
    def generate_report(self):
        query = """
        SELECT Books.Title, Books.Author, Books.ISBN, COUNT(BorrowedBooks.BookID) AS BorrowCount
        FROM BorrowedBooks
        INNER JOIN Books ON BorrowedBooks.BookID = Books.ID
        GROUP BY Books.Title, Books.Author, Books.ISBN
        """
        self.db_connection.cursor.execute(query)
        report = self.db_connection.cursor.fetchall()
        print("Borrowing Report:")
        for record in report:
            print(record)

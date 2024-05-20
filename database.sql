create database Library;

-- Create the Books table
CREATE TABLE Books (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Title VARCHAR(100) NOT NULL,
    Author VARCHAR(100) NOT NULL,
    ISBN VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL
);

-- Create the Users table
CREATE TABLE Users (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL
);

-- Create the BorrowedBooks table to track borrowing history
CREATE TABLE BorrowedBooks (
    ID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT FOREIGN KEY REFERENCES Users(ID),
    BookID INT FOREIGN KEY REFERENCES Books(ID),
    BorrowDate DATETIME NOT NULL DEFAULT GETDATE(),
    DueDate DATETIME NOT NULL,
    ReturnDate DATETIME
);

insert into Users values 
('Raul', 'raul12@gmail.com')

select * from Books;
select * from Users;
select * from BorrowedBooks;

delete Books;
delete Users;
delete BorrowedBooks;

DBCC CHECKIDENT ('Books', RESEED, 0);
DBCC CHECKIDENT ('Users', RESEED, 0);
DBCC CHECKIDENT ('BorrowedBooks', RESEED, 0);




delete Books;
delete Users;
delete BorrowedBooks;


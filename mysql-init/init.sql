CREATE DATABASE IF NOT EXISTS librarydb;

USE librarydb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    usn VARCHAR(50),
    department VARCHAR(100),
    password VARCHAR(255),
    role VARCHAR(20) DEFAULT 'user'
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    author VARCHAR(255),
    category VARCHAR(100),
    quantity INT,
    available INT
);

CREATE TABLE borrow_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id INT,
    issue_date DATE,
    status VARCHAR(50)
);

INSERT INTO users
(name,email,phone,usn,department,password,role)

VALUES
(
'Admin',
'admin@gmail.com',
'9999999999',
'ADMIN001',
'Administration',
'admin123',
'admin'
);

INSERT INTO books
(title,author,category,quantity,available)

VALUES
('Java Programming','James Gosling','Programming',5,5),
('Operating Systems','Galvin','Operating Systems',3,3),
('Computer Networks','Andrew Tanenbaum','Networking',4,4);
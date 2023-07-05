-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 19, 2023 at 09:06 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity`
--

CREATE TABLE `activity` (
  `id` int(11) NOT NULL,
  `username` text DEFAULT NULL,
  `book_name` text DEFAULT NULL,
  `borrow_date` datetime DEFAULT NULL,
  `return_date` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `reg_date` datetime DEFAULT NULL,
  `logout` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity`
--

INSERT INTO `activity` (`id`, `username`, `book_name`, `borrow_date`, `return_date`, `last_login`, `reg_date`, `logout`) VALUES
(1, 'raunak', NULL, NULL, NULL, '2023-05-17 12:02:01', NULL, NULL),
(2, 'raunak', NULL, NULL, NULL, NULL, NULL, '2023-05-18 00:02:01'),
(3, 'sarvesh', 'The Great Gatsby', '2023-05-19 12:02:40', NULL, NULL, NULL, NULL),
(4, 'sarvesh', 'The Catcher in the Rye', '2023-05-19 12:02:40', NULL, NULL, NULL, NULL),
(5, 'sarvesh', 'The Hobbit', '2023-05-19 12:02:40', NULL, NULL, NULL, NULL),
(6, 'narendra', 'The Great Gatsby', '2023-05-19 12:02:50', NULL, NULL, NULL, NULL),
(7, 'narendra', 'To Kill a Mockingbird', '2023-05-19 12:02:50', NULL, NULL, NULL, NULL),
(8, 'rutwik', 'The Hobbit', '2023-05-19 12:03:04', NULL, NULL, NULL, NULL),
(9, 'rutwik', 'The Lord of the Rings', '2023-05-19 12:03:04', NULL, NULL, NULL, NULL),
(10, 'rutwik', 'Harry Potter and the Philosopher\'s Stone', '2023-05-21 10:03:04', NULL, NULL, NULL, NULL),
(11, 'mobin', 'The Great Gatsby', '2023-05-22 05:03:15', NULL, NULL, NULL, NULL),
(12, 'mobin', 'Pride and Prejudice', '2023-05-26 10:03:15', NULL, NULL, NULL, NULL),
(13, 'tejas', 'The Da Vinci Code', '2023-05-27 15:03:40', NULL, NULL, NULL, NULL),
(14, 'tejas', 'The Girl with the Dragon Tattoo', '2023-05-28 16:03:40', NULL, NULL, NULL, NULL),
(15, 'sarvesh', NULL, NULL, NULL, '2023-05-29 12:33:40', NULL, NULL),
(16, 'sarvesh', NULL, NULL, NULL, NULL, NULL, '2023-05-29 00:10:00'),
(17, 'rutwik', NULL, NULL, NULL, '2023-05-30 10:00:00', NULL, NULL),
(18, 'rutwik', NULL, NULL, NULL, NULL, NULL, '2023-05-30 12:33:53'),
(19, 'tejas', NULL, NULL, NULL, '2023-05-31 14:30:59', NULL, NULL),
(20, 'tejas', NULL, NULL, NULL, NULL, NULL, '2023-05-31 16:34:00');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `Username`, `Email`, `Password`) VALUES
(1, 'admin', 'admin@admin.com', '1');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `publisher` text NOT NULL,
  `book_id` int(11) NOT NULL,
  `category` varchar(255) NOT NULL,
  `author` text NOT NULL,
  `copies_available` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `status` varchar(255) NOT NULL,
  `added_on` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `name`, `publisher`, `book_id`, `category`, `author`, `copies_available`, `price`, `status`, `added_on`) VALUES
(1, 'The Great Gatsby', 'Penguin Books', 1234, 'Fiction', 'F. Scott Fitzgerald', 3, 499, 'available', '2023-04-01'),
(2, 'To Kill a Mockingbird', 'HarperCollins Publishers', 5678, 'Fiction', 'Harper Lee', 1, 399, 'available', '2023-05-02'),
(3, '1984', 'Penguin Books', 91011, 'Science Fiction', 'George Orwell', 6, 299, 'available', '2023-05-03'),
(4, 'The Catcher in the Rye', 'Little, Brown and Company', 121314, 'Fiction', 'J.D. Salinger', 0, 349, 'Unavailable', '2023-05-04'),
(5, 'Pride and Prejudice', 'Penguin Classics', 151617, 'Romance', 'Jane Austen', 2, 199, 'available', '2023-05-05'),
(6, 'The Hobbit', 'HarperCollins Publishers', 181920, 'Fantasy', 'J.R.R. Tolkien', 3, 299, 'available', '2023-05-06'),
(7, 'The Lord of the Rings', 'HarperCollins Publishers', 212223, 'Fantasy', 'J.R.R. Tolkien', 2, 499, 'available', '2023-05-07'),
(8, 'Harry Potter and the Philosopher\'s Stone', 'Bloomsbury Publishing', 242526, 'Fantasy', 'J.K. Rowling', 7, 599, 'available', '2023-05-08'),
(9, 'The Da Vinci Code', 'Transworld Publishers', 272829, 'Mystery', 'Dan Brown', 2, 449, 'available', '2023-05-14'),
(10, 'The Girl with the Dragon Tattoo', 'Vintage Books', 303132, 'Mystery', 'Stieg Larsson', 1, 399, 'available', '2023-05-22');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `FullName` text NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `reg_on` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `FullName`, `Username`, `Email`, `Password`, `reg_on`) VALUES
(1, 'Sarvesh Sutar', 'sarvesh', 'sarveshsutar1000@gmail.com', '1', '2023-04-19 12:52:04'),
(2, 'Raunak Sadhwani', 'raunak', 'raunak200308@gmail.com', '1', '2023-04-25 21:42:43'),
(3, 'Narendra Patil', 'narendra', 'narendrapatil2206@gmail.com', '1', '2023-04-29 13:53:35'),
(4, 'Tejas Parit', 'tejas', 'tejasparit1818@gmail.com', '1', '2023-05-01 07:24:02'),
(5, 'Rutwik Hanmant Patil', 'rutwik', 'rutwikpatil8329594516@gmail.com', '1', '2023-05-10 08:56:19'),
(6, 'Mobin Monachan George', 'mobin', 'mobinmgeorge@gmail.com', '1', '2023-05-19 11:56:21');

-- --------------------------------------------------------

--
-- Table structure for table `user_books`
--

CREATE TABLE `user_books` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `borrow_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `submitted_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_books`
--

INSERT INTO `user_books` (`id`, `user_id`, `book_id`, `borrow_date`, `return_date`, `submitted_date`) VALUES
(1, 1, 1234, '2023-05-19', '2023-05-26', NULL),
(2, 1, 121314, '2023-05-19', '2023-05-26', NULL),
(3, 1, 181920, '2023-05-19', '2023-05-26', NULL),
(4, 3, 1234, '2023-05-19', '2023-05-26', NULL),
(5, 3, 5678, '2023-05-19', '2023-05-26', NULL),
(6, 5, 181920, '2023-05-19', '2023-05-26', NULL),
(7, 5, 212223, '2023-05-19', '2023-05-26', NULL),
(8, 5, 242526, '2023-05-21', '2023-05-28', NULL),
(9, 6, 1234, '2023-05-22', '2023-05-29', NULL),
(10, 6, 151617, '2023-05-26', '2023-06-02', NULL),
(11, 4, 272829, '2023-05-27', '2023-06-03', NULL),
(12, 4, 303132, '2023-05-28', '2023-06-04', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity`
--
ALTER TABLE `activity`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `constraint_name` (`book_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_books`
--
ALTER TABLE `user_books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity`
--
ALTER TABLE `activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user_books`
--
ALTER TABLE `user_books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_books`
--
ALTER TABLE `user_books`
  ADD CONSTRAINT `user_books_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_books_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

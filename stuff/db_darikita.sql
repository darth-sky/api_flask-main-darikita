-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2025 at 01:23 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_darikita`
--

-- --------------------------------------------------------

--
-- Table structure for table `blood_donation_projects`
--

CREATE TABLE `blood_donation_projects` (
  `blood_project_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `target_amount` int(11) NOT NULL,
  `current_amount` int(100) NOT NULL DEFAULT 0,
  `project_photo` varchar(100) NOT NULL DEFAULT 'default.jpg',
  `user_id` int(11) NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `date_started` date NOT NULL DEFAULT current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `blood_donation_projects`
--

INSERT INTO `blood_donation_projects` (`blood_project_id`, `title`, `description`, `target_amount`, `current_amount`, `project_photo`, `user_id`, `status`, `date_started`, `created_at`) VALUES
(28, 'test donor', 'test donor', 10, 5, 'donor1.png', 28, 'approved', '2025-01-16', '2025-01-09 12:10:23'),
(29, 'testDonor', 'testDonorrr', 10, 0, 'donor1.png', 29, 'pending', '2025-01-29', '2025-01-09 15:56:11'),
(30, 'DONORRONRR', 'Didnidndinei', 2000, 2, 'donor1.png', 2, 'approved', '2025-01-28', '2025-01-10 04:55:30'),
(31, 'DONOR TSET', 'test', 20, 0, 'donor1.png', 32, 'pending', '2025-01-23', '2025-01-10 09:09:39'),
(32, 'DONOR etes', 'testr123', 19, 0, 'donor1.png', 32, 'approved', '2025-01-27', '2025-01-10 09:13:11');

-- --------------------------------------------------------

--
-- Table structure for table `blood_donors`
--

CREATE TABLE `blood_donors` (
  `donor_id` int(11) NOT NULL,
  `blood_project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `deskripsi` text NOT NULL,
  `golongan_darah` text NOT NULL DEFAULT 'O',
  `tgl_donor_terakhir` date NOT NULL DEFAULT current_timestamp(),
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `donation_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `blood_donors`
--

INSERT INTO `blood_donors` (`donor_id`, `blood_project_id`, `user_id`, `deskripsi`, `golongan_darah`, `tgl_donor_terakhir`, `status`, `donation_date`) VALUES
(36, 28, 2, 'Singaraja, 28 September 2004', 'B', '2026-12-11', 'approved', '2025-01-09 14:00:30'),
(42, 28, 26, 'singaraja', 'B', '2025-01-28', 'approved', '2025-01-10 04:12:30'),
(43, 30, 2, 'BALIIIII', 'B', '2025-01-30', 'approved', '2025-01-10 04:56:41'),
(44, 30, 30, 'BAAWLII', 'B', '2025-01-29', 'approved', '2025-01-10 04:58:38'),
(45, 28, 28, 'singadsaudasud', 'B', '2025-01-28', 'pending', '2025-01-10 05:00:02'),
(46, 28, 31, 'Singaraja, 1 Januari 2020', 'A', '2024-12-17', 'pending', '2025-01-10 06:48:54'),
(47, 28, 32, 'Singara,01 Januari 2020', 'B', '2024-11-12', 'approved', '2025-01-10 09:06:18');

--
-- Triggers `blood_donors`
--
DELIMITER $$
CREATE TRIGGER `update_blood_donation_total` AFTER INSERT ON `blood_donors` FOR EACH ROW BEGIN
    UPDATE blood_donation_projects
    SET current_amount = current_amount + 1
    WHERE blood_project_id = NEW.blood_project_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `donations`
--

CREATE TABLE `donations` (
  `donation_id` int(11) NOT NULL,
  `donation_project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `donated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donations`
--

INSERT INTO `donations` (`donation_id`, `donation_project_id`, `user_id`, `amount`, `donated_at`) VALUES
(23, 47, 30, 50000.00, '2025-01-10 04:54:03'),
(24, 43, 26, 10.00, '2025-01-10 05:44:51'),
(25, 43, 31, 10.00, '2025-01-10 06:47:29'),
(26, 43, 32, 10.00, '2025-01-10 09:05:20');

--
-- Triggers `donations`
--
DELIMITER $$
CREATE TRIGGER `update_donation_total` AFTER INSERT ON `donations` FOR EACH ROW BEGIN
    UPDATE donation_projects
    SET current_amount = current_amount + NEW.amount
    WHERE donation_project_id = NEW.donation_project_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `donation_categories`
--

CREATE TABLE `donation_categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donation_categories`
--

INSERT INTO `donation_categories` (`category_id`, `name`) VALUES
(1, 'Bencana Alam'),
(2, 'Sosial'),
(3, 'Pendidikan'),
(4, 'Kesehatan'),
(5, 'Infrastruktur');

-- --------------------------------------------------------

--
-- Table structure for table `donation_comments`
--

CREATE TABLE `donation_comments` (
  `comment_id` int(11) NOT NULL,
  `donation_project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` text NOT NULL,
  `commented_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donation_comments`
--

INSERT INTO `donation_comments` (`comment_id`, `donation_project_id`, `user_id`, `comment`, `commented_at`) VALUES
(1, 43, 28, 'asdasdasdads', '2025-01-09 12:44:51'),
(2, 43, 28, 'ha;oo', '2025-01-09 12:58:42'),
(3, 43, 28, 'pop', '2025-01-09 12:59:18'),
(4, 43, 26, 'test', '2025-01-10 05:46:04'),
(5, 43, 31, 'test', '2025-01-10 06:48:03'),
(6, 43, 32, 'test', '2025-01-10 09:05:40');

-- --------------------------------------------------------

--
-- Table structure for table `donation_projects`
--

CREATE TABLE `donation_projects` (
  `donation_project_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `target_amount` decimal(10,2) NOT NULL,
  `project_photo` varchar(100) NOT NULL DEFAULT 'default.jpg',
  `current_amount` decimal(10,2) NOT NULL DEFAULT 0.00,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `donation_projects`
--

INSERT INTO `donation_projects` (`donation_project_id`, `title`, `description`, `target_amount`, `project_photo`, `current_amount`, `category_id`, `user_id`, `status`, `created_at`) VALUES
(43, 'test donasi', 'test donasi', 100.00, 'volunteer.jpeg', 30.00, 1, 28, 'approved', '2025-01-09 12:09:57'),
(47, 'DONASI PERNIKAHAN', 'HAHAHAHAHAH', 500000.00, 'volunteer.jpeg', 50000.00, 5, 2, 'approved', '2025-01-10 04:52:49');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'test1name', 'test1@gmail.com', '$2b$12$RYxzM94xXDWcQJS40YtPk.ddzGISczBfRVwXbZdWlaVBOZysc3rKm', 'user', '2024-12-18 12:25:42'),
(2, 'changeme', 'changeme@gmail.com', '$2b$12$ovQUeN4IZFvmAFvOjAvmZOjnybTXf3Ugf9iUjAJEJPwCpz.PzSiiq', 'user', '2025-01-01 07:18:15'),
(3, 'changeme1', 'changeme1@gmail.com', '$2b$12$CRll/lPUGRaQJ7Jyso1Qkec3Z4RtVd6t82qAZUcsP9Iwylw79kZti', 'user', '2025-01-01 12:59:17'),
(4, 'changemeadmin', 'changemeadmin@gmail.com', '$2b$12$4Oc.Bm/zu832Omy0PIO7t.BAgGa1WvW6FS0u7SfV.5dLeev3cW0w6', 'admin', '2025-01-01 13:39:22'),
(5, 'tya', 'tya@gmail.com', '$2b$12$gnDW/jQpCea6VeDPN3NeQ.GPGPbTmteF6q3cW3DUfYnIQqfrnfH82', 'user', '2025-01-03 07:34:12'),
(6, 'tya1', 'tya1@gmail.com', '$2b$12$06bqhEGVABVh5l2Arqfg7uJDSy.b82KkcTsMyPL.5Gx2PHP0sQCeC', 'user', '2025-01-03 07:34:35'),
(7, 'tya2', 'tya2@gmail.com', '$2b$12$GyuZ5jyactxnkY8vld8qH.UHWcmHsn0HX0v3v1dX1i42zYur7Katy', 'user', '2025-01-03 07:35:12'),
(8, 'tya3', 'tya3@gmail.com', '$2b$12$kDTjoPUOMd89S/7WhjgL4Ogu7jJ0pMsBRQttKd6i87/eBCB4xmlUO', 'user', '2025-01-03 07:35:31'),
(9, 'testing', 'p@gmail.com', '$2b$12$BBpivPKNINIr4.erBYcFV.FQ2XSvjGqtOaXb9uVatVgd0Cp8QoI3m', 'user', '2025-01-03 07:39:53'),
(13, 'testing', 'ppppppp@gmail.com', '$2b$12$e2xPPO2eb9OzU7XweGG60eDK9U9Jo95YXlZLMLY6t/0rb2UY3trhS', 'user', '2025-01-03 07:40:41'),
(14, 'testing', 'pppppppppp@gmail.com', '$2b$12$GJ1kD/g00D7k3VdFUsNxyelIajsq83nvpVJiJS1ADzJ1cK1DjTRUW', 'user', '2025-01-03 07:41:19'),
(15, 'tya5', 'tya5@gmail.com', '$2b$12$eoV1eDjLElaidilzYqGpmeeyCjsW5A7fnXcYKjIHJudL9CjZOgC5K', 'user', '2025-01-03 07:43:21'),
(16, 'tya6', 'tya6@gmail.com', '$2b$12$4dRs2hxnWnhkHCy3jnIe0OjUuwA/Ue6eIpam6qv2BDJDECbDzF.se', 'user', '2025-01-03 07:43:53'),
(17, 'tya7', 'tya7@gmail.com', '$2b$12$eszn4WlkJ1wCKqDwOKgdGuPrzUI9PVPXeH9sYa1MRBg5IT/EAFnka', 'user', '2025-01-03 07:45:15'),
(18, 'tya9', 'tya9@gmail.com', '$2b$12$NymOokRJN6nvprcOQl.nYu/q4p4jjleYLXU9KhOW88ksSMBKlGxP2', 'user', '2025-01-03 07:46:45'),
(19, 'tya69', 'tya69@gmail.com', '$2b$12$3hUvdV2X9ZI10QAJxgkZA.6ryUi/eNrUPQ2OcESCEZsYo8v.X4MRm', 'user', '2025-01-08 02:59:46'),
(20, 'dennishehe', 'dennis@gmail.com', '$2b$12$o.rrmZf8l9BT3/2sAoxAUu3r5pRg6D/jfCiNDsqRFt2ph95dUzllK', 'user', '2025-01-08 09:45:57'),
(21, 'tya100', 'tya100', '$2b$12$3TBaDnQ6fTsNebusGhN3IupmkcV71uotoopJPyN5gY8r/ALS/HxAm', 'user', '2025-01-08 13:42:23'),
(22, 'tya129', 'tya129@gmail.com', '$2b$12$3KoZX5yiCRJz/bkUSOTAgONEtMlSDfsky23ZB6Lz0VFJ5h1UPGxPO', 'user', '2025-01-08 13:45:49'),
(23, '', 'tyat@gmail.com', '$2b$12$zgKqEFTupm4asiMqlW5BDu9fPdPe2oCyEfDBkpLpnEz.SlCoSZd/u', 'user', '2025-01-08 13:49:58'),
(24, 'gun', 'bbbb@gmail.com', '$2b$12$Gpgrt8rM3Ypxbfg0TgRQ/.MTIyhQp2GgYTr.HYzT9jUWQ5YZiABwK', 'user', '2025-01-09 04:42:03'),
(25, 'testing', 'testing@gmail.com', '$2b$12$Bz6WnFx1g45zWf0d5aA99eWz3yJ93k/flDGMnuP7IuWO97ZRxBmeO', 'user', '2025-01-09 08:18:53'),
(26, 'testingadit', 'testingadit@gmail.com', '$2b$12$u6908m1oTXR81tNhmmSaC.jBp.ZmTCmD.csmfxrXSkuHWjhCU4fEK', 'user', '2025-01-09 08:20:08'),
(27, 'testingtya', 'testingtya@gmail.com', '$2b$12$Iciw5uZunLJAKW7wqiZqtuA1frq5HRrmaJ252l/4dsf41NWhwEzdS', 'user', '2025-01-09 08:27:20'),
(28, 'kiky', 'sriayurejeki.id@gmail.com', '$2b$12$XtCtBt.HLL1QRVtpP0vUk.GBFePs2vvrIDDbXJJc2gEW0o093T6Bu', 'user', '2025-01-09 09:57:00'),
(29, 'halo123', 'halo123@gmail.com', '$2b$12$DcNH8OnMTUixIGNlyK9aBeZOUT8pchwMRi9MH1JdZT8LjNwuD2Ukm', 'user', '2025-01-09 15:16:11'),
(30, 'dennis', 'dennis123@gmail.com', '$2b$12$rTxrlEshyrSF5Szd5FyURuqU9xjkE2I5r4e2f8b2U4BQJ6uZNvkcu', 'user', '2025-01-10 04:42:38'),
(31, 'atheya', 'tyavinandita@gmail.com', '$2b$12$JcdcdRYY4Uv3lWdEprg/nOxkN01LUUm5.j4ubTnjHU5FKf3mL09na', 'user', '2025-01-10 06:46:18'),
(32, 'theya', 'theya@gmail.com', '$2b$12$vy9gtHsMykXeN.C/UPCZ9OWTmHwvk.Wl2DppxOpRhelEjycqEWEkC', 'user', '2025-01-10 09:03:55');

-- --------------------------------------------------------

--
-- Table structure for table `volunteers`
--

CREATE TABLE `volunteers` (
  `volunteer_id` int(11) NOT NULL,
  `volunteer_project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `deskripsi` text NOT NULL,
  `umur` text NOT NULL DEFAULT 'tidak diisi',
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `joined_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `volunteers`
--

INSERT INTO `volunteers` (`volunteer_id`, `volunteer_project_id`, `user_id`, `deskripsi`, `umur`, `status`, `joined_at`) VALUES
(19, 8, 2, 'pernah ikut volunteer sebelumnya', '20', 'pending', '2025-01-10 05:35:11'),
(20, 8, 31, 'mengikuti kegiatan bem', '20', 'approved', '2025-01-10 06:49:32'),
(21, 8, 32, '- mengikuti organisasi hmj', '20', 'pending', '2025-01-10 09:06:52');

--
-- Triggers `volunteers`
--
DELIMITER $$
CREATE TRIGGER `update_volunteer_total` AFTER INSERT ON `volunteers` FOR EACH ROW BEGIN
    UPDATE volunteer_projects
    SET current_amount = current_amount + 1
    WHERE volunteer_project_id = NEW.volunteer_project_id;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `volunteer_projects`
--

CREATE TABLE `volunteer_projects` (
  `volunteer_project_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `target_amount` int(11) NOT NULL,
  `current_amount` int(11) NOT NULL,
  `project_photo` varchar(100) NOT NULL DEFAULT 'default.jpg',
  `user_id` int(11) NOT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `date_started` date NOT NULL DEFAULT current_timestamp(),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `volunteer_projects`
--

INSERT INTO `volunteer_projects` (`volunteer_project_id`, `title`, `description`, `target_amount`, `current_amount`, `project_photo`, `user_id`, `status`, `date_started`, `created_at`) VALUES
(8, 'test volunteer', 'test volunteer', 100, 3, 'volunteer.jpeg', 28, 'approved', '2025-01-09', '2025-01-09 12:12:55'),
(9, 'test_volunteerrr', 'test_volunteerrr', 10, 0, 'volunteer.jpeg', 29, 'pending', '2025-01-22', '2025-01-09 15:57:02'),
(11, 'VOLUNTERR', 'test', 20, 0, 'volunteer.jpeg', 31, 'rejected', '2025-01-21', '2025-01-10 06:52:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blood_donation_projects`
--
ALTER TABLE `blood_donation_projects`
  ADD PRIMARY KEY (`blood_project_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `blood_donors`
--
ALTER TABLE `blood_donors`
  ADD PRIMARY KEY (`donor_id`),
  ADD KEY `blood_donors_ibfk_1` (`blood_project_id`),
  ADD KEY `blood_donors_ibfk_2` (`user_id`);

--
-- Indexes for table `donations`
--
ALTER TABLE `donations`
  ADD PRIMARY KEY (`donation_id`),
  ADD KEY `donations_ibfk_1` (`donation_project_id`),
  ADD KEY `donations_ibfk_2` (`user_id`);

--
-- Indexes for table `donation_categories`
--
ALTER TABLE `donation_categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `donation_comments`
--
ALTER TABLE `donation_comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `donation_project_id` (`donation_project_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `donation_projects`
--
ALTER TABLE `donation_projects`
  ADD PRIMARY KEY (`donation_project_id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `volunteers`
--
ALTER TABLE `volunteers`
  ADD PRIMARY KEY (`volunteer_id`),
  ADD KEY `volunteers_ibfk_1` (`volunteer_project_id`),
  ADD KEY `volunteers_ibfk_2` (`user_id`);

--
-- Indexes for table `volunteer_projects`
--
ALTER TABLE `volunteer_projects`
  ADD PRIMARY KEY (`volunteer_project_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blood_donation_projects`
--
ALTER TABLE `blood_donation_projects`
  MODIFY `blood_project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `blood_donors`
--
ALTER TABLE `blood_donors`
  MODIFY `donor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `donations`
--
ALTER TABLE `donations`
  MODIFY `donation_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `donation_categories`
--
ALTER TABLE `donation_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `donation_comments`
--
ALTER TABLE `donation_comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `donation_projects`
--
ALTER TABLE `donation_projects`
  MODIFY `donation_project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `volunteers`
--
ALTER TABLE `volunteers`
  MODIFY `volunteer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `volunteer_projects`
--
ALTER TABLE `volunteer_projects`
  MODIFY `volunteer_project_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `blood_donation_projects`
--
ALTER TABLE `blood_donation_projects`
  ADD CONSTRAINT `blood_donation_projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `blood_donors`
--
ALTER TABLE `blood_donors`
  ADD CONSTRAINT `blood_donors_ibfk_1` FOREIGN KEY (`blood_project_id`) REFERENCES `blood_donation_projects` (`blood_project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `blood_donors_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `donations`
--
ALTER TABLE `donations`
  ADD CONSTRAINT `donations_ibfk_1` FOREIGN KEY (`donation_project_id`) REFERENCES `donation_projects` (`donation_project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `donations_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `donation_comments`
--
ALTER TABLE `donation_comments`
  ADD CONSTRAINT `donation_comments_ibfk_1` FOREIGN KEY (`donation_project_id`) REFERENCES `donation_projects` (`donation_project_id`),
  ADD CONSTRAINT `donation_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `donation_projects`
--
ALTER TABLE `donation_projects`
  ADD CONSTRAINT `donation_projects_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `donation_categories` (`category_id`),
  ADD CONSTRAINT `donation_projects_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `volunteers`
--
ALTER TABLE `volunteers`
  ADD CONSTRAINT `volunteers_ibfk_1` FOREIGN KEY (`volunteer_project_id`) REFERENCES `volunteer_projects` (`volunteer_project_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `volunteers_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `volunteer_projects`
--
ALTER TABLE `volunteer_projects`
  ADD CONSTRAINT `volunteer_projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

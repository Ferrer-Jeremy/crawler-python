-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Apr 01, 2017 at 04:35 PM
-- Server version: 5.7.17
-- PHP Version: 7.0.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crawler`
--

-- --------------------------------------------------------

--
-- Table structure for table `movie`
--

CREATE TABLE `movie` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `id_imdb` int(7) UNSIGNED NOT NULL COMMENT 'prefix with tt',
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `year` int(4) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `movie__subtitle`
--

CREATE TABLE `movie__subtitle` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `id_movie` mediumint(8) UNSIGNED NOT NULL,
  `language` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `hash` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `movie__subtitle_name`
--

CREATE TABLE `movie__subtitle_name` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `id_subtitle` mediumint(8) UNSIGNED NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `movie__subtitle_path`
--

CREATE TABLE `movie__subtitle_path` (
  `id` mediumint(8) UNSIGNED NOT NULL,
  `id_subtitle` mediumint(8) UNSIGNED NOT NULL,
  `path` varchar(511) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movie`
--
ALTER TABLE `movie`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `imdb_id` (`id_imdb`),
  ADD KEY `imdb_id_2` (`id_imdb`);

--
-- Indexes for table `movie__subtitle`
--
ALTER TABLE `movie__subtitle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_movie` (`id_movie`);

--
-- Indexes for table `movie__subtitle_name`
--
ALTER TABLE `movie__subtitle_name`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_subtitle` (`id_subtitle`);

--
-- Indexes for table `movie__subtitle_path`
--
ALTER TABLE `movie__subtitle_path`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_subtitle` (`id_subtitle`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movie`
--
ALTER TABLE `movie`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `movie__subtitle`
--
ALTER TABLE `movie__subtitle`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `movie__subtitle_name`
--
ALTER TABLE `movie__subtitle_name`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `movie__subtitle_path`
--
ALTER TABLE `movie__subtitle_path`
  MODIFY `id` mediumint(8) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `movie__subtitle`
--
ALTER TABLE `movie__subtitle`
  ADD CONSTRAINT `movie__subtitle_ibfk_1` FOREIGN KEY (`id_movie`) REFERENCES `movie` (`id`);

--
-- Constraints for table `movie__subtitle_name`
--
ALTER TABLE `movie__subtitle_name`
  ADD CONSTRAINT `movie__subtitle_name_ibfk_1` FOREIGN KEY (`id_subtitle`) REFERENCES `movie__subtitle` (`id`);

--
-- Constraints for table `movie__subtitle_path`
--
ALTER TABLE `movie__subtitle_path`
  ADD CONSTRAINT `movie__subtitle_path_ibfk_1` FOREIGN KEY (`id_subtitle`) REFERENCES `movie__subtitle` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th1 19, 2025 lúc 07:06 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `qhc`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `device`
--

CREATE TABLE `device` (
  `id` int(11) NOT NULL,
  `device_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `device_code`
--

CREATE TABLE `device_code` (
  `id` int(11) NOT NULL,
  `code_id` int(11) NOT NULL,
  `code_type` varchar(10) NOT NULL,
  `device_id` int(11) NOT NULL,
  `get_code_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `get_qhca`
--

CREATE TABLE `get_qhca` (
  `id` int(11) NOT NULL,
  `code` varchar(6) NOT NULL,
  `wallet_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `get_qhcb`
--

CREATE TABLE `get_qhcb` (
  `id` int(11) NOT NULL,
  `code` varchar(6) NOT NULL,
  `wallet_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `get_qhcc`
--

CREATE TABLE `get_qhcc` (
  `id` int(11) NOT NULL,
  `code` varchar(6) NOT NULL,
  `wallet_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `get_qhcd`
--

CREATE TABLE `get_qhcd` (
  `id` int(11) NOT NULL,
  `code` varchar(6) NOT NULL,
  `wallet_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `ip_code`
--

CREATE TABLE `ip_code` (
  `id` int(11) NOT NULL,
  `code_id` int(11) NOT NULL,
  `code_type` varchar(10) NOT NULL,
  `ip_id` int(11) NOT NULL,
  `get_code_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qhc_a`
--

CREATE TABLE `qhc_a` (
  `id` int(11) NOT NULL,
  `unit` double NOT NULL DEFAULT 0.001,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `is_used` int(11) NOT NULL DEFAULT 0,
  `status` int(11) NOT NULL DEFAULT 1,
  `get_code_at` datetime DEFAULT NULL,
  `used_code_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qhc_b`
--

CREATE TABLE `qhc_b` (
  `id` int(11) NOT NULL,
  `unit` double NOT NULL DEFAULT 0.01,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `is_used` int(11) NOT NULL DEFAULT 0,
  `status` int(11) NOT NULL DEFAULT 1,
  `get_code_at` datetime DEFAULT NULL,
  `used_code_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qhc_c`
--

CREATE TABLE `qhc_c` (
  `id` int(11) NOT NULL,
  `unit` double NOT NULL DEFAULT 0.1,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `is_used` int(11) NOT NULL DEFAULT 0,
  `status` int(11) NOT NULL DEFAULT 1,
  `get_code_at` datetime DEFAULT NULL,
  `used_code_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qhc_d`
--

CREATE TABLE `qhc_d` (
  `id` int(11) NOT NULL,
  `unit` double NOT NULL DEFAULT 1,
  `code` varchar(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `is_used` int(11) NOT NULL DEFAULT 0,
  `status` int(11) NOT NULL DEFAULT 1,
  `get_code_at` datetime DEFAULT NULL,
  `used_code_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `transfers`
--

CREATE TABLE `transfers` (
  `id` int(11) NOT NULL,
  `main_wallet_address` varchar(50) NOT NULL,
  `wallet_id` double NOT NULL,
  `code` varchar(15) NOT NULL,
  `QHC` double NOT NULL,
  `Tx_hash` varchar(50) NOT NULL,
  `created_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `userip`
--

CREATE TABLE `userip` (
  `id` int(11) NOT NULL,
  `IP` varchar(25) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `wallets`
--

CREATE TABLE `wallets` (
  `id` int(11) NOT NULL,
  `wallet_address` varchar(255) NOT NULL,
  `POL` double NOT NULL DEFAULT 0,
  `QHC` float NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `wordpress`
--

CREATE TABLE `wordpress` (
  `id` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
  `user_agent` varchar(25) NOT NULL,
  `order_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `device`
--
ALTER TABLE `device`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `device_code`
--
ALTER TABLE `device_code`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `get_qhca`
--
ALTER TABLE `get_qhca`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `get_qhcb`
--
ALTER TABLE `get_qhcb`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `get_qhcc`
--
ALTER TABLE `get_qhcc`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `get_qhcd`
--
ALTER TABLE `get_qhcd`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `ip_code`
--
ALTER TABLE `ip_code`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qhc_a`
--
ALTER TABLE `qhc_a`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Chỉ mục cho bảng `qhc_b`
--
ALTER TABLE `qhc_b`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qhc_c`
--
ALTER TABLE `qhc_c`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qhc_d`
--
ALTER TABLE `qhc_d`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `transfers`
--
ALTER TABLE `transfers`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `userip`
--
ALTER TABLE `userip`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `wallets`
--
ALTER TABLE `wallets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `wallet_address` (`wallet_address`);

--
-- Chỉ mục cho bảng `wordpress`
--
ALTER TABLE `wordpress`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `device`
--
ALTER TABLE `device`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `device_code`
--
ALTER TABLE `device_code`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `get_qhca`
--
ALTER TABLE `get_qhca`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `get_qhcb`
--
ALTER TABLE `get_qhcb`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `get_qhcc`
--
ALTER TABLE `get_qhcc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `get_qhcd`
--
ALTER TABLE `get_qhcd`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `ip_code`
--
ALTER TABLE `ip_code`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `qhc_a`
--
ALTER TABLE `qhc_a`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `qhc_b`
--
ALTER TABLE `qhc_b`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `qhc_c`
--
ALTER TABLE `qhc_c`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `qhc_d`
--
ALTER TABLE `qhc_d`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `transfers`
--
ALTER TABLE `transfers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `userip`
--
ALTER TABLE `userip`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `wallets`
--
ALTER TABLE `wallets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `wordpress`
--
ALTER TABLE `wordpress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

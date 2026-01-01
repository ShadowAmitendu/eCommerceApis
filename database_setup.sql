-- =====================================================
-- E-Commerce API Database Setup Script
-- =====================================================
-- This script creates the database and all required tables
-- Run this before starting the application
-- =====================================================

-- Create database if it doesn't exist
CREATE
DATABASE IF NOT EXISTS ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE
ecommerce_db;

-- =====================================================
-- Drop existing tables (for clean setup)
-- =====================================================
-- Uncomment these lines if you want to reset the database
-- DROP TABLE IF EXISTS products;
-- DROP TABLE IF EXISTS users;

-- =====================================================
-- Create Users Table
-- =====================================================
CREATE TABLE IF NOT EXISTS users
(
    id
    INT
    AUTO_INCREMENT
    PRIMARY
    KEY,
    name
    VARCHAR
(
    150
) NOT NULL,
    email VARCHAR
(
    255
) NOT NULL UNIQUE,
    password VARCHAR
(
    255
) NOT NULL,
    role ENUM
(
    'buyer',
    'seller',
    'admin'
) NOT NULL DEFAULT 'buyer',
    is_active TINYINT
(
    1
) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Indexes for performance
    INDEX idx_email
(
    email
),
    INDEX idx_role
(
    role
),
    INDEX idx_is_active
(
    is_active
)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE =utf8mb4_unicode_ci;

-- =====================================================
-- Create Products Table
-- =====================================================
CREATE TABLE IF NOT EXISTS products
(
    id
    INT
    AUTO_INCREMENT
    PRIMARY
    KEY,
    name
    VARCHAR
(
    150
) NOT NULL,
    description TEXT,
    price DECIMAL
(
    10,
    2
) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    seller_id INT NOT NULL,
    is_active TINYINT
(
    1
) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign key constraint
    CONSTRAINT fk_seller
    FOREIGN KEY
(
    seller_id
)
    REFERENCES users
(
    id
)
                                                           ON DELETE CASCADE,

    -- Indexes for performance
    INDEX idx_name
(
    name
),
    INDEX idx_seller_id
(
    seller_id
),
    INDEX idx_is_active
(
    is_active
),
    INDEX idx_price
(
    price
),
    INDEX idx_created_at
(
    created_at
)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE =utf8mb4_unicode_ci;

-- =====================================================
-- Insert Sample Data (Optional)
-- =====================================================
-- Uncomment the following section to insert sample users and products

-- Sample Users (passwords are hashed with PBKDF2-SHA256)
-- Password for all: Admin1234, Seller1234, Buyer1234
/*
INSERT INTO users (name, email, password, role) VALUES
(
    'Admin User',
    'admin@test.com',
    '$pbkdf2-sha256$29000$1trb.39PaS2ltBbCeO8dIw$xQZvJhQJ5nE8KmGFJQFJ9xLQJ5nE8KmGFJQFJ9xLQ',
    'admin'
),
(
    'Seller User',
    'seller@test.com',
    '$pbkdf2-sha256$29000$2tr7.59PaS3ltBbCeO9dIw$yRZwJhRJ5nE9KmGFJRFJ9xLRJ5nE9KmGFJRFJ9xLR',
    'seller'
),
(
    'Buyer User',
    'buyer@test.com',
    '$pbkdf2-sha256$29000$3ts8.69PaS4ltBbCeP0dIw$zSZxJhSJ5nF0KmGFJSFJ9xLSJ5nF0KmGFJSFJ9xLS',
    'buyer'
);

-- Sample Products
INSERT INTO products (name, description, price, stock, seller_id) VALUES
(
    'Laptop',
    'High-performance gaming laptop with RTX 4060',
    1299.99,
    10,
    2
),
(
    'Smartphone',
    'Latest flagship smartphone with 5G connectivity',
    899.99,
    25,
    2
),
(
    'Wireless Headphones',
    'Premium noise-cancelling wireless headphones',
    299.99,
    50,
    2
),
(
    'Mechanical Keyboard',
    'RGB mechanical keyboard with Cherry MX switches',
    149.99,
    30,
    2
),
(
    'Gaming Mouse',
    'Professional gaming mouse with 16000 DPI',
    79.99,
    40,
    2
);
*/

-- =====================================================
-- Verification Queries
-- =====================================================
-- Uncomment to verify the setup

-- Check users table structure
-- DESCRIBE users;

-- Check products table structure
-- DESCRIBE products;

-- Count records
-- SELECT COUNT(*) as total_users FROM users;
-- SELECT COUNT(*) as total_products FROM products;

-- View all users
-- SELECT id, name, email, role, is_active, created_at FROM users;

-- View all products
-- SELECT id, name, price, stock, seller_id, is_active FROM products;

-- =====================================================
-- Database Information
-- =====================================================
SELECT 'Database setup completed successfully!' as status,
       DATABASE()                               as current_database,
       VERSION()                                as mysql_version,
       NOW()                                    as setup_time;

-- Show tables
SHOW
TABLES;

-- =====================================================
-- Notes:
-- =====================================================
-- 1. The application (SQLAlchemy) will also create tables automatically
-- 2. Sample data is commented out - uncomment if needed
-- 3. Password hashes in sample data are examples only
-- 4. Always use strong passwords in production
-- 5. Foreign key constraints ensure data integrity
-- 6. Indexes are created for commonly queried fields
-- =====================================================
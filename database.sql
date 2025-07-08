-- Create the database
CREATE DATABASE IF NOT EXISTS mental_health;
USE mental_health;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL
);

-- Create the history table
CREATE TABLE IF NOT EXISTS history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    input_data TEXT NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
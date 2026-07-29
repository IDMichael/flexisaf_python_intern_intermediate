# Student Database CRUD System

## Overview
This Python program manages student records using SQLite database operations and implements complete CRUD functionality with activity logging.

The program:
- Creates and manages a SQLite student database
- Stores student information such as name, age, and department
- Performs Create, Read, Update, and Delete (CRUD) operations
- Records database activities in a separate logs table
- Displays student records and activity history

## Features
- SQLite database connection handling
- Database table creation
- Student record insertion
- Student record retrieval
- Student department updates
- Student record deletion
- Activity logging system
- Input validation
- Error handling
- Automatic timestamp generation for logs

## Database Tables

### Students Table
Stores student information.

Columns:
- `id` - Automatically generated student ID
- `name` - Student name
- `age` - Student age
- `department` - Student department

### Logs Table
Stores database activity records.

Columns:
- `id` - Automatically generated log ID
- `action` - Type of database operation performed
- `description` - Details about the activity
- `created_at` - Timestamp of the activity

## Technologies Used
- Python 3
- SQLite3

## Required Libraries
No external libraries are required.

This program uses only Python built-in libraries:
- `sqlite3`

## How to Run the Program
### 1. Navigate into the folder
cd sqlite3_student_database

### 2. Run the Program
python main.py
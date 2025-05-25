-- E-School Database Setup Script

CREATE DATABASE IF NOT EXISTS `E-School`;
USE `E-School`;

-- Department table
CREATE TABLE IF NOT EXISTS Department (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

-- Student table
CREATE TABLE IF NOT EXISTS Student (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- Teacher table
CREATE TABLE IF NOT EXISTS Teacher (
    teacher_id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    office_hour VARCHAR(50),
    office_no VARCHAR(20)
);

-- Administrator table
CREATE TABLE IF NOT EXISTS Administrator (
    administrator_id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE
);

-- Lecture table
CREATE TABLE IF NOT EXISTS Lecture (
    lecture_id INT PRIMARY KEY AUTO_INCREMENT,
    lecture_name VARCHAR(100) NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- Warning table
CREATE TABLE IF NOT EXISTS Warning (
    warning_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    warning_text TEXT,
    administrator_id INT,
    FOREIGN KEY (administrator_id) REFERENCES Administrator(administrator_id)
);

-- Schedule table (düzeltilmiş spelling)
CREATE TABLE IF NOT EXISTS Schedule (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE NOT NULL,
    schedule_text TEXT,
    administrator_id INT,
    FOREIGN KEY (administrator_id) REFERENCES Administrator(administrator_id)
);

-- Take table (student-lecture relationship)
CREATE TABLE IF NOT EXISTS take (
    student_id INT,
    lecture_id INT,
    pass_grade DECIMAL(5,2),
    PRIMARY KEY (student_id, lecture_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (lecture_id) REFERENCES Lecture(lecture_id)
);

-- Teach table (teacher-lecture relationship)
CREATE TABLE IF NOT EXISTS teach (
    teacher_id INT,
    lecture_id INT,
    PRIMARY KEY (teacher_id, lecture_id),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id),
    FOREIGN KEY (lecture_id) REFERENCES Lecture(lecture_id)
);

-- Sample data insertion
INSERT INTO Department (dept_name) VALUES 
('Computer Science'),
('Mathematics'),
('Physics'),
('Chemistry');

INSERT INTO Administrator (username, password) VALUES 
('admin', 'admin123');

INSERT INTO Teacher (username, password, office_hour, office_no) VALUES 
('teacher1', 'teacher123', 'Mon-Wed 10:00-12:00', 'A101'),
('teacher2', 'teacher123', 'Tue-Thu 14:00-16:00', 'B202');

INSERT INTO Student (username, password, department_id) VALUES 
('student1', 'student123', 1),
('student2', 'student123', 2);

INSERT INTO Lecture (lecture_name, department_id) VALUES 
('Data Structures', 1),
('Calculus I', 2),
('Physics I', 3),
('General Chemistry', 4);

INSERT INTO teach (teacher_id, lecture_id) VALUES 
(1, 1),
(1, 2),
(2, 3),
(2, 4);

INSERT INTO take (student_id, lecture_id, pass_grade) VALUES 
(1, 1, 85.5),
(1, 2, 92.0),
(2, 2, 78.5),
(2, 3, 88.0);
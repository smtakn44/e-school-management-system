import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, List, Any

class Database:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'your_password_here',  # Replace with your actual password
            'host': 'localhost',
            'port': '3306',
            'database': 'E-School',
            'autocommit': True
        }
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None) -> Optional[List[Dict]]:
        if not self.connection or not self.connection.is_connected():
            self.connect()
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return None
                
        except Error as e:
            print(f"Query execution error: {e}")
            return None
    
    def execute_single(self, query: str, params: tuple = None) -> Optional[Dict]:
        result = self.execute_query(query, params)
        return result[0] if result else None

# Global database instance
db = Database()

# Authentication functions
def authenticate_user(username: str, password: str, user_type: str) -> Optional[Dict]:
    """Authenticate user and return user data if successful"""
    table_map = {
        'student': 'Student',
        'teacher': 'Teacher', 
        'admin': 'Administrator'
    }
    
    id_map = {
        'student': 'student_id',
        'teacher': 'teacher_id',
        'admin': 'administrator_id'
    }
    
    if user_type not in table_map:
        return None
    
    table = table_map[user_type]
    id_field = id_map[user_type]
    
    query = f"SELECT * FROM {table} WHERE username = %s AND password = %s"
    user = db.execute_single(query, (username, password))
    
    if user:
        user['user_type'] = user_type
        user['user_id'] = user[id_field]
    
    return user

# Student functions
def get_student_lectures(student_id: int) -> List[Dict]:
    """Get all lectures for a student with grades"""
    query = """
    SELECT l.lecture_id, l.lecture_name, d.dept_name, t.pass_grade,
           te.username as teacher_name
    FROM take t
    JOIN Lecture l ON t.lecture_id = l.lecture_id
    JOIN Department d ON l.department_id = d.department_id
    LEFT JOIN teach th ON l.lecture_id = th.lecture_id
    LEFT JOIN Teacher te ON th.teacher_id = te.teacher_id
    WHERE t.student_id = %s
    """
    return db.execute_query(query, (student_id,)) or []

def get_student_info(student_id: int) -> Optional[Dict]:
    """Get student information with department"""
    query = """
    SELECT s.*, d.dept_name
    FROM Student s
    LEFT JOIN Department d ON s.department_id = d.department_id
    WHERE s.student_id = %s
    """
    return db.execute_single(query, (student_id,))

# Teacher functions
def get_teacher_lectures(teacher_id: int) -> List[Dict]:
    """Get all lectures taught by a teacher"""
    query = """
    SELECT l.lecture_id, l.lecture_name, d.dept_name
    FROM teach t
    JOIN Lecture l ON t.lecture_id = l.lecture_id
    JOIN Department d ON l.department_id = d.department_id
    WHERE t.teacher_id = %s
    """
    return db.execute_query(query, (teacher_id,)) or []

def get_lecture_students(lecture_id: int) -> List[Dict]:
    """Get all students in a lecture with their grades"""
    query = """
    SELECT s.student_id, s.username, t.pass_grade, d.dept_name
    FROM take t
    JOIN Student s ON t.student_id = s.student_id
    LEFT JOIN Department d ON s.department_id = d.department_id
    WHERE t.lecture_id = %s
    """
    return db.execute_query(query, (lecture_id,)) or []

def update_student_grade(student_id: int, lecture_id: int, grade: float) -> bool:
    """Update student grade for a lecture"""
    query = "UPDATE take SET pass_grade = %s WHERE student_id = %s AND lecture_id = %s"
    result = db.execute_query(query, (grade, student_id, lecture_id))
    return result is not None

# Admin functions
def get_all_students() -> List[Dict]:
    """Get all students with department info"""
    query = """
    SELECT s.student_id, s.username, d.dept_name
    FROM Student s
    LEFT JOIN Department d ON s.department_id = d.department_id
    ORDER BY s.username
    """
    return db.execute_query(query) or []

def get_all_teachers() -> List[Dict]:
    """Get all teachers"""
    query = "SELECT teacher_id, username, office_hour, office_no FROM Teacher ORDER BY username"
    return db.execute_query(query) or []

def get_all_departments() -> List[Dict]:
    """Get all departments"""
    query = "SELECT * FROM Department ORDER BY dept_name"
    return db.execute_query(query) or []

def get_all_lectures() -> List[Dict]:
    """Get all lectures with department info"""
    query = """
    SELECT l.lecture_id, l.lecture_name, d.dept_name
    FROM Lecture l
    JOIN Department d ON l.department_id = d.department_id
    ORDER BY l.lecture_name
    """
    return db.execute_query(query) or []

def add_student(username: str, password: str, department_id: int) -> bool:
    """Add new student"""
    query = "INSERT INTO Student (username, password, department_id) VALUES (%s, %s, %s)"
    result = db.execute_query(query, (username, password, department_id))
    return result is not None

def add_teacher(username: str, password: str, office_hour: str, office_no: str) -> bool:
    """Add new teacher"""
    query = "INSERT INTO Teacher (username, password, office_hour, office_no) VALUES (%s, %s, %s, %s)"
    result = db.execute_query(query, (username, password, office_hour, office_no))
    return result is not None

def add_department(dept_name: str) -> bool:
    """Add new department"""
    query = "INSERT INTO Department (dept_name) VALUES (%s)"
    result = db.execute_query(query, (dept_name,))
    return result is not None

def delete_department(department_id: int) -> bool:
    """Delete a department by its ID"""
    query = "DELETE FROM Department WHERE department_id = %s"
    result = db.execute_query(query, (department_id,))
    return result is not None
# E-School Management System

A simple school management system built with FastAPI, MySQL, and Bootstrap for managing students, teachers, and administrators.

## Features

- **Student Portal**: View lectures, check grades, track academic progress
- **Teacher Portal**: Manage lectures, grade students, view class performance
- **Admin Portal**: Manage students, teachers, departments, and system operations
- **Responsive Design**: Bootstrap-based responsive interface
- **Session Management**: Simple session-based authentication

## Technology Stack

- **Backend**: FastAPI
- **Database**: MySQL
- **Frontend**: HTML, CSS, Bootstrap, jQuery
- **Styling**: Custom CSS with Bootstrap

## Prerequisites

- Python 3.12+
- MySQL Server
- MySQL Workbench (optional)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd E-School
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**
   - Create a database named `E-School`
   - Update database configuration in `app/database.py` if needed
   - Run the SQL script:
   ```bash
   mysql -u root -p E-School < database_setup.sql
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Open browser and go to `http://localhost:8000`

## Default Credentials

### Student
- Username: `student1`
- Password: `student123`

### Teacher
- Username: `teacher1`
- Password: `teacher123`

### Administrator
- Username: `admin`
- Password: `admin123`

## Database Configuration

Update the database configuration in `app/database.py`:

```python
self.config = {
    'user': 'root',
    'password': '#your_password_here',
    'host': 'localhost',
    'port': '3306',
    'database': 'E-School',
    'autocommit': True
}
```

## Project Structure

```
E-School/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection and queries
│   ├── models.py            # Pydantic models
│   ├── routes/              # API routes
│   │   ├── auth.py          # Authentication routes
│   │   ├── student.py       # Student routes
│   │   ├── teacher.py       # Teacher routes
│   │   ├── admin.py         # Admin routes
│   │   └── general.py       # General routes
│   └── utils/
│       └── helpers.py       # Helper functions
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── app.js           # JavaScript functionality
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── student/            # Student templates
│   ├── teacher/            # Teacher templates
│   └── admin/              # Admin templates
├── requirements.txt        # Python dependencies
├── database_setup.sql      # Database setup script
└── README.md              # This file
```

## Database Schema

### Tables
- **Department**: Academic departments
- **Student**: Student accounts and information
- **Teacher**: Teacher accounts and information
- **Administrator**: Admin accounts
- **Lecture**: Course/lecture information
- **Warning**: System warnings
- **Schedule**: System schedules
- **take**: Student-lecture enrollments with grades
- **teach**: Teacher-lecture assignments

## API Endpoints

### Authentication
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/logout` - Logout

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET /student/lectures` - Student lectures

### Teacher Routes
- `GET /teacher/dashboard` - Teacher dashboard
- `GET /teacher/lectures` - Teacher lectures
- `GET /teacher/lecture/{id}/students` - View students in lecture
- `POST /teacher/update_grade` - Update student grade

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/students` - Manage students
- `GET /admin/teachers` - Manage teachers
- `GET /admin/departments` - Manage departments
- `POST /admin/students/add` - Add new student
- `POST /admin/teachers/add` - Add new teacher
- `POST /admin/departments/add` - Add new department

## Development Notes

- No ORM used - direct MySQL queries
- No complex authentication - simple session-based auth
- Minimal external dependencies for simplicity
- Bootstrap for responsive design
- jQuery for client-side interactions

## Screenshots

### Login Page
Simple login interface with user type selection.

### Student Dashboard
View enrolled lectures, grades, and academic progress.

### Teacher Dashboard
Manage assigned lectures and grade students.

### Admin Dashboard
System overview with management options for students, teachers, and departments.

## Contributing

This is a demo project for learning purposes. Feel free to fork and modify as needed.

## License

This project is open source and available under the MIT License.

# Django Education Manager

A Django-based educational management system for managing students, teachers, courses, and grades.

## Features

- Student and teacher management with profile photos
- Course management
- Grade tracking
- Invitation code system for user registration
- Custom management commands for database operations

## Requirements

- Python 3.8+
- PostgreSQL 12+
- pip

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirments.txt
```

### 4. Set up PostgreSQL database

Create a PostgreSQL database and user:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE academy_db;
CREATE USER academy_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE academy_db TO academy_user;
\q
```

### 5. Configure environment variables

Create a `.env` file in the project root directory with the following configuration:

```env
DB_NAME=academy_db
DB_USER=academy_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DEBUG=True
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

## Management Commands

This project includes several custom Django management commands:

### Fill Database with Test Data

Populates the database with test students, teachers, courses, and grades. Students receive random duck photos, and teachers receive random fox photos.

```bash
python manage.py fill_db
```

Options:
- `--students N` - Number of students to create (default: 48)
- `--teachers N` - Number of teachers to create (default: 16)
- `--grades N` - Number of grades to create (default: 144)
- `--reset-ids` - Reset auto-increment IDs to 1

Example:
```bash
python manage.py fill_db --students 20 --teachers 5 --reset-ids
```

### Generate Invitation Code

Generates an invitation code for user registration.

```bash
python manage.py generate_invite_code <group>
```

Arguments:
- `group` - User group: `student`, `teacher`, `director`, or `admin`

Options:
- `--hours N` - Code validity period in hours (default: 1)
- `--profile-id N` - ID of the profile to associate with the code

Examples:
```bash
# Generate a student invitation code valid for 24 hours
python manage.py generate_invite_code student --hours 24

# Generate a teacher code associated with a specific profile
python manage.py generate_invite_code teacher --profile-id 5

# Generate an admin code valid for 2 hours
python manage.py generate_invite_code admin --hours 2
```

### Delete Expired Invitation Codes

Removes all invitation codes that have expired.

```bash
python manage.py delete_expired_codes
```

## Running the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Project Structure

```
.
├── main/                 # Main application
│   ├── management/       # Custom management commands
│   ├── migrations/       # Database migrations
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── forms.py          # Django forms
│   └── urls.py           # URL routing
├── settings/             # Django settings
│   ├── settings.py       # Main settings file
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── static/               # Static files
├── templates/            # HTML templates
├── manage.py             # Django management script
└── requirments.txt       # Python dependencies
```

## Models

- **Student** - Student profiles with personal information and enrolled courses
- **Teacher** - Teacher profiles with personal information and taught courses
- **Course** - Course information including name, description, and dates
- **Grade** - Student grades for courses
- **InvitationCode** - Time-limited invitation codes for user registration

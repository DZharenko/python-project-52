<div align="center">

  <h1>Hexlet project: Task Manager</h1>

  [A simple web application for managing team tasks](https://hexlet-code-zcyd.onrender.com/)


### Hexlet tests and linter status:
[![Actions Status](https://github.com/DZharenko/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DZharenko/python-project-52/actions)
[![Python CI](https://github.com/DZharenko/python-project-52/actions/workflows/pyci.yaml/badge.svg)](https://github.com/DZharenko/python-project-52/actions/workflows/pyci.yaml)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DZharenko_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DZharenko_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DZharenko_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=DZharenko_python-project-52)


</div>

---
### **Features**

- 👤 User registration and authentication
- 📝 Task creation, editing, and deletion
- 🏷️ Status and label management
- 🔍 Task filtering and search
- 📱 Responsive Bootstrap UI
- 🧪 Comprehensive test coverage
---
### **Tech Stack**
- Python 3.12
- Django 4+
- Bootstrap 5
- SQLite, PostgreSQL
- Rollbar
- Whitenoise
---
## Project Structure
```
task_manager/
├── users/         # User management
├── tasks/         # Task management
├── statuses/      # Task status management
├── labels/        # Task labels management
├── templates/     # HTML templates
├── locale/        # i18n translations
└── settings.py    # Project configuration
```
---
### **Setup and installation**
Clone the repository:
```
git clone https://github.com/INafanya/python-project-52.git
```
Install Python dependencies inside a virtual environment:
```
make install
```
Copy example environment and edit it if needed:
```
cp .env_template .env
```
Start the application:
```
make run
```
---
## **For development**
Install Python dependencies inside a virtual environment:
   ```
   make install
   ```
Runing test:
   ```
   make test
   ```
Checking for code style:
   ```
   make lint
   ```

## ⭐Star this repo if you found it useful! ⭐
### Hexlet tests and linter status:
[![Actions Status](https://github.com/DZharenko/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/DZharenko/python-project-52/actions)
[![Python CI](https://github.com/DZharenko/python-project-52/actions/workflows/pyci.yaml/badge.svg)](https://github.com/DZharenko/python-project-52/actions/workflows/pyci.yaml)

# Task manager
Web service on Django for create, track, and manage tasks with statuses and labels.

### [Task manager Demo](https://hexlet-code-zcyd.onrender.com)
---
### **Features**
- User authentication and authorization
- Task management (create, read, update, delete)
- Status management for tasks
- Label management for task categorization
- Filter tasks by status, executor, labels, and author
- Internationalization support (i18n)
- Responsive design
---
### **Tech Stack**
- Python 3.12
- Django 4+
- Bootstrap 5
- SQLite, PostgreSQL
---
### **Setup and installation**
Clone the repository:
```bash
git clone https://github.com/DZharenko/python-project-52.git
```
Install Python dependencies inside a virtual environment:
```bash
make install
---
## **For development**
Install Python dependencies inside a virtual environment:
   ```bash
   make install
   ```
Checking for code style:
   ```bash
   make lint
   ```
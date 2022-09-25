import sqlite3

# Establish connection to sqlite db/create database if does not exist
conn = sqlite3.connect("projects.db")
cursor = conn.cursor()

# statuses enum
class Statuses():
    active = 'active'
    completed = 'completed'
    planned = 'planned'

# Create tables
def createTables():
    cursor.execute(("""CREATE TABLE managers
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(25), last_name VARCHAR(25), email VARCHAR(64)) 
                """))
    cursor.execute("""CREATE TABLE projects
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50), description VARCHAR(500), status TEXT CHECK( status IN ('active', 'completed', 'planned')), manager_id INTEGER) 
                """)
    conn.commit()

# Insert project into db
def createProject(title, description, status, manager_id):
    query = "INSERT INTO projects (title, description, status, manager_id) VALUES (?,?,?,?)"
    cursor.execute(query, (title, description, status, manager_id))
    conn.commit()

# Read projects from db
def getProjects():
    query = "SELECT id, title, description, status, manager_id FROM projects"
    return cursor.execute(query).fetchall()

# Update project in db
def updateProject(project_id, title, description, status, manager_id):
    query = "UPDATE projects SET title=?, description=?, status=?, manager_id=? WHERE id=?"
    cursor.execute(query, (title, description, status, manager_id, project_id))
    conn.commit()

# Delete project from db
def deleteProject(project_id):
    query = "DELETE FROM projects WHERE id=?"
    cursor.execute(query, (project_id,))
    conn.commit()

# Read managers from db
def getManagers():
    query = "SELECT id, first_name, last_name, email FROM managers"
    return cursor.execute(query).fetchall()

# Fill tables with dummy data
def seedDB():
    managers = [('Fred', 'Smith', 'smith@gmail.com'), ('John', 'Doe', 'joe@gmail.com')]
    cursor.executemany("INSERT INTO managers (first_name, last_name, email) VALUES (?, ?, ?)", managers)

    projects = [('RadWorks Project', 'The overarching objective of the RadWorks project is to mature and demonstrate affordable, enabling solutions that mitigate radiation-related challenges of human exploration beyond Earth\'s orbit', 'active', 1),
    ('Advanced Modular Power Systems Project', 'AMPS prpoject is infusing new tech into power systems and components and proving their capabilities through exploration-based ground demonstrations.', 'planned', 1),
    ('Lunar Crater Radio Telescope', 'In Phase 1, we explored the fundamental physics and cosmoloy underlying the scientific objective of LCRT...', 'completed', 2)]
    cursor.executemany("INSERT INTO projects (title, description, status, manager_id) VALUES (?,?,?,?)", projects)
    conn.commit()

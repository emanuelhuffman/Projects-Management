import db

# db.createTables()
# db.seedDB()
# db.createProject("Hydrogen Car1", "It's a car that runs on Hydrogen", db.Statuses.active, 1)
# db.deleteProject(4)
# db.updateProject(4, "Hydrogen Car", "It's a car that runs on Hydrogen and it's a car", db.Statuses.completed, 2)
print(db.getProjects())
print(db.getManagers())
db.conn.close()
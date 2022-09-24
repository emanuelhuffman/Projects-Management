import db

# db.createTables()
# db.seedDB()
# db.createProject("Hydrogen Car", "It's a car that runs on Hydrogen", db.Statuses.active, 2)
db.updateProject(4, "Hydrogen Car", "It's a car that runs on Hydrogen", "completed", 2)
print(db.getProjects())
print(db.getManagers())
db.conn.close()

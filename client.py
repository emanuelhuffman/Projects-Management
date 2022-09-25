from tkinter import *
from tkinter import messagebox
from datetime import date
from os import walk
import db

# Grab projects and managers from db
projects = db.getProjects()
managers = db.getManagers()

#-----Core-----
ws = Tk()
ws.title('Project Manager')
ws.config(bg='#223441', padx=10, pady=10)
ws.resizable(width=False, height=False)

lbFrame = Frame(ws) #List Box
lbFrame.grid(row=0, column=0, pady=5, padx=5, columnspan=2)
lbFrame.config(bg='#223441')

lbDetailsFrame = Frame(ws)
lbDetailsFrame.grid(row=0, column=2, pady=5, padx=5, columnspan=2)
lbDetailsFrame.config(bg='#223441')

lb = Listbox(
    lbFrame,
    width=50,
    height=16,
    font=('Times', 12),
    bd=0,
    fg='#464646',
    highlightthickness=0,
    selectbackground='#a6a6a6',
    activestyle="none")
lb.pack(fill=None, expand=False, side=LEFT)

sb = Scrollbar(lbFrame)
sb.pack(side=LEFT, fill=BOTH)

lb.config(yscrollcommand=sb.set)
sb.config(command=lb.yview)

txt = Text(
    lbDetailsFrame,
    width=50,
    height=16,
    font=('Times', 12),
    bd=0,
    fg='#464646',
    highlightthickness=0,
    selectbackground='#a6a6a6',
    wrap=WORD)
txt.pack(fill=None, expand=False, side=RIGHT)

titleLabel = Label(ws ,text = "Title", fg='white', bg='#223441')
descriptionLabel = Label(ws ,text = "Description", fg='white', bg='#223441')
statusLabel = Label(ws ,text = "Status", fg='white', bg='#223441')
managerLabel = Label(ws ,text = "Manager", fg='white', bg='#223441')

title = Entry(
    ws,
    font=('times', 12),
    width=50
    )
title.insert(0, "Project Name")

description = Text(
    ws,
    font=('times', 12),
    width=50,
    height=5
    )
description.insert(END, "Project description")

statusOption = ''
managerOption = ''

def setStatusOption(selection):
    global statusOption
    statusOption = selection

def setManagerOption(selection):
    global managerOption
    managerOption = selection[0]

# Status options dropdown
statusOptions = StringVar(ws)
status = db.Statuses
statusOptions.set("Choose status") # default value
statusOM = OptionMenu(ws, statusOptions, status.active, status.completed, status.planned, command=setStatusOption)
statusOM.configure(width=60, padx=5, pady=5)

# Manager options dropdown
managerOptions = StringVar(ws)
managers = db.getManagers()
managersFullName = []
for man in managers:
    managersFullName.append(man[0:3])
managerOptions.set("Choose a manager") # default value
managerOM = OptionMenu(ws, managerOptions, *managersFullName, command=setManagerOption)
managerOM.configure(width=60, padx=5, pady=5)

# Add form components to grid
titleLabel.grid(row=1, column=0)
title.grid(row=1, column=1, padx=5, pady=5)
descriptionLabel.grid(row=2, column=0)
description.grid(row=2, column=1, padx=5, pady=5)
statusLabel.grid(row=3, column=0)
statusOM.grid(row=3, column=1)
managerLabel.grid(row=4, column=0)
managerOM.grid(row=4, column=1)

#-----functions-----
def displayProjects():
    lb.delete(0, END)
    for project in projects:
        lb.insert("end", project[1])

def showProjectDetails(event):
    w = event.widget
    index = w.curselection()
    if(len(index) != 0): # Check if tuple is not empty
        index = int(index[0])
        managers = db.getManagers()
        for man in managers: # Get manager of selected
            if(man[0] == projects[index][4]):
                manager = man
        managerFullName = manager[1] + " " + manager[2]
        managerEmail = manager[3]
        txt.delete(1.0, END)
        txt.insert(END, "STATUS: " + projects[index][3] + '\n')
        txt.insert(END, "MANAGER: " + managerFullName + " - " + managerEmail + '\n\n')
        txt.insert(END, "DESCRIPTION: " + projects[index][2] + '\n')
lb.bind('<<ListboxSelect>>', showProjectDetails) # List selection event listener

def createProject():
    global projects
    if(title.get() == '' or statusOption == '' or managerOption == ''):
        messagebox.showwarning("Error", "One or more fields are blank")
    else:
        db.createProject(title.get(), description.get('1.0', END), statusOption, managerOption)
        projects = db.getProjects()
        displayProjects()

def updateProject():
    pass

def deleteProject():
    global projects
    try:
        index = lb.curselection()[0]
        db.deleteProject(projects[index][0])
        projects = db.getProjects()
        displayProjects()
    except:
        messagebox.showwarning("Error", "No project selected")

# #-----buttons-----

addProject_btn = Button(
    ws,
    text='Add Project',
    font=('times 14'),
    bg='#c5f776',
    padx=75,
    command=createProject,
)
addProject_btn.grid(row=1, column=3)

updateProject_btn = Button(
    ws,
    text='Update Project',
    font=('times 14'),
    bg='green',
    padx=75,
    command=updateProject,
)
updateProject_btn.grid(row=2, column=3)

delProject_btn = Button(
    ws,
    text='Delete Project',
    font=('times 14'),
    bg='#ff8b61',
    padx=75,
    command=deleteProject
)
delProject_btn.grid(row=3, column=3)

# Display projects on panel
displayProjects()

#-----Main Loop-----
ws.mainloop()
# Todo Using Flet

A lightweight task management application built with **Python and Flet**, featuring local SQLite storage, task scheduling, automatic status tracking, priorities, deadline reminders, calendar-based task viewing, search, and productivity statistics.

The application is designed for personal task management and works with local data without requiring a remote backend or cloud database.

---

## 📱 Overview

**Todo Using Flet** is a desktop/mobile-oriented Todo application developed using Python and Flet.

The application allows users to:

- Create tasks
- Add task descriptions
- Set start date and time
- Set deadlines
- Assign task priorities
- Enable task notifications
- Search tasks
- Mark tasks as completed
- Delete tasks
- View tasks through a calendar
- Automatically track task status
- View productivity statistics
- Clear completed tasks
- Reset all tasks

The application stores task information locally using **SQLite**, making it suitable for offline personal use.

---

# ✨ Features

## 🏠 Home Dashboard

The Home section is the main task management area.

Users can:

- View existing tasks
- Search tasks
- View task status
- Mark tasks as completed
- Change task priority
- Enable or disable notifications
- Delete tasks
- Navigate through the calendar
- View tasks belonging to a selected date

---

## ➕ Add Task

Users can create a task by providing:

- Task Name
- Description
- Start Date
- Start Time
- Deadline Date
- Deadline Time

The task also supports:

- Priority
- Notifications

### Example

```text
Task Name:
Complete Machine Learning Assignment

Description:
Finish model evaluation and documentation.

Start:
10-Oct-2026 10:00

Deadline:
10-Oct-2026 13:00

Priority:
High

Notification:
Enabled

You can replace your entire README.md with this:
# Todo Using Flet

A lightweight task management application built with **Python and Flet**, featuring local SQLite storage, task scheduling, automatic status tracking, priorities, deadline reminders, calendar-based task viewing, search, and productivity statistics.

The application is designed for personal task management and works with local data without requiring a remote backend or cloud database.

---

## 📱 Overview

**Todo Using Flet** is a desktop/mobile-oriented Todo application developed using Python and Flet.

The application allows users to:

- Create tasks
- Add task descriptions
- Set start date and time
- Set deadlines
- Assign task priorities
- Enable task notifications
- Search tasks
- Mark tasks as completed
- Delete tasks
- View tasks through a calendar
- Automatically track task status
- View productivity statistics
- Clear completed tasks
- Reset all tasks

The application stores task information locally using **SQLite**, making it suitable for offline personal use.

---

# ✨ Features

## 🏠 Home Dashboard

The Home section is the main task management area.

Users can:

- View existing tasks
- Search tasks
- View task status
- Mark tasks as completed
- Change task priority
- Enable or disable notifications
- Delete tasks
- Navigate through the calendar
- View tasks belonging to a selected date

---

## ➕ Add Task

Users can create a task by providing:

- Task Name
- Description
- Start Date
- Start Time
- Deadline Date
- Deadline Time

The task also supports:

- Priority
- Notifications

### Example

```text
Task Name:
Complete Machine Learning Assignment

Description:
Finish model evaluation and documentation.

Start:
10-Oct-2026 10:00

Deadline:
10-Oct-2026 13:00

Priority:
High

Notification:
Enabled

⏱️ Automatic Task Status
Task status is automatically determined using the current time.
The application uses four task states:
Status	Meaning
NOT STARTED	The current time is before the task start time
ONGOING	The current time is between the start time and deadline
COMPLETED	The user has completed the task
MISSED	The deadline has passed before completion


The status values used internally are:
0 → NOT STARTED
1 → ONGOING
2 → COMPLETED
3 → MISSED

Status Flow
                 Current Time
                      │
          ┌───────────┴───────────┐
          │                       │
     Before Start            After Start
          │                       │
          ▼                 ┌─────┴─────┐
    NOT STARTED             │           │
                            ▼           ▼
                       Before       After
                       Deadline     Deadline
                            │           │
                            ▼           ▼
                         ONGOING      MISSED

User completes task at any point
                │
                ▼
           COMPLETED

A completed task remains completed and is not overwritten by the automatic status update process.
🔔 Deadline Notifications
The application supports local task notifications through the Plyer library.
When notifications are enabled and a task is approaching its deadline, the application checks the remaining time.
For a high-priority task, a reminder can be triggered when the deadline is within approximately 5 minutes.
Example notification:
Critical Task Reminder

Task 'Complete ML Assignment'
is due in less than 5 minutes!

The application also tracks whether the notification has already been sent so that the same reminder is not repeatedly triggered.
📅 Calendar
The Home page contains an integrated calendar.
Users can:
- Move to the previous month
- Move to the next month
- Return to today
- Select a specific date
- View tasks associated with that date
Calendar dates can visually indicate different task states.
For example:
ORANGE → NOT STARTED
CYAN   → ONGOING
GREEN  → COMPLETED
RED    → MISSED

Selecting a date displays the tasks associated with that date.
🔎 Search
The Home section provides task search functionality.
The user can search using the task name or description.
For example:
Search:
machine learning

The application checks the stored task information in SQLite and returns matching tasks.
The current search implementation supports:
- Task-name prefix matching
- Description text matching
✅ Complete a Task
Every task provides a Mark as Completed action.
When the user completes a task:
Task
 ↓
COMPLETED

The new status is stored in the SQLite database.
Completed tasks are visually distinguished in the interface.
🗑️ Delete Tasks
A user can delete an individual task.
Before deletion, the application displays a confirmation dialog.
Example:
Delete Task

Do you want to delete "Complete Assignment"?

[CANCEL]     [DELETE]

There is also a Settings option to remove all tasks.
🔴 Task Priority
Tasks support different priority levels.
Internally the application uses:
0 → LOW
1 → MEDIUM
2 → HIGH

The user interface allows a task's priority to be changed from the task card.
Priority also influences the visual presentation and reminder behavior.
📊 Statistics
The STATS page provides a productivity overview.
The application calculates:
- Total tasks
- Completed tasks
- Pending tasks
- Completion percentage
The completion percentage is calculated as:
Completed Tasks
----------------------- × 100
Total Tasks

This gives the user a quick overview of their task completion progress.
⚙️ Settings
The Settings section provides application management options.
Clear Completed Tasks
This option removes tasks whose current status is:
COMPLETED

The application reports how many completed tasks were removed.
Reset All Tasks
This option permanently removes all stored tasks.
Because this is a destructive operation, the application asks the user for confirmation before deleting everything.
About
The Settings page also contains information about the application and its implementation.
🔄 How the Application Works
The overall application flow is:
                USER
                  │
                  ▼
          FLET USER INTERFACE
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
       HOME      ADD       STATS
        │         │
        │         ▼
        │      VALIDATION
        │         │
        │         ▼
        │    operations.py
        │         │
        └─────────┤
                  ▼
             SQLite Database
                  │
                  ▼
         Automatic Status Check
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   NOT STARTED  ONGOING   MISSED
                  │
                  ▼
              COMPLETED

The Settings section provides additional database management operations.
🧩 Internal Architecture
The application is organized into three main Python files.
main.py
   │
   ├── User Interface
   ├── Navigation
   ├── Calendar
   ├── Task Cards
   ├── Search
   ├── Statistics
   ├── Notifications
   └── Status Processing
          │
          ▼
operations.py
   │
   ├── Add Task
   ├── Read Tasks
   ├── Search Tasks
   ├── Delete Task
   ├── Delete All Tasks
   ├── Update Status
   ├── Update Priority
   ├── Update Notification
   └── Update Notification State
          │
          ▼
db_config.py
   │
   ├── SQLite Connection
   └── Table Creation
          │
          ▼
      TasksDB.db

📂 Project Structure
The GitHub repository contains the source code required to recreate the application.
Todo_Using_flet/
│
├── main.py
├── operations.py
├── db_config.py
├── requirements.txt
├── README.md
└── .gitignore

Generated build files and local runtime data are intentionally excluded from Git.
🧠 main.py
main.py is the main application entry point.
It is responsible for:
- Initializing the Flet application
- Configuring the application window
- Creating the navigation bar
- Rendering the Home page
- Rendering the Add Task page
- Rendering the Statistics page
- Rendering the Settings page
- Rendering task cards
- Managing the calendar
- Searching tasks
- Completing tasks
- Deleting tasks
- Managing priority controls
- Managing notification controls
- Automatically updating task statuses
- Triggering deadline notifications
The application starts with:
if __name__ == "__main__":    ft.run(main)


🗃️ operations.py
operations.py separates database operations from the main user-interface logic.
The file contains functions for:
add_task()
get_tasks_list()
search_task_name()
remove_a_task()
delete_all_tasks()
update_status()
update_priority()
update_notify()
update_notified_sent()

This separation makes the application easier to manage by keeping most SQL/database operations outside the main UI file.
🗄️ db_config.py
db_config.py is responsible for creating and managing the SQLite database connection.
It contains:
create_connection()
create_table()

The application uses:
SQLite

and the database file is:
TasksDB.db

The database table is automatically created when the application starts if it does not already exist.
🗃️ Database Schema
The main table is:
tasks

The current schema contains:
Column	Description
task_no	Automatically generated task identifier
task_name	Name of the task
start	Task start date and time
deadline	Task deadline
status	Current task status
notify	Whether notification is enabled
priority	Task priority
description	Optional task description
notified_sent	Tracks whether the reminder was already sent


Database definition
Conceptually:
CREATE TABLE tasks (
    task_no INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    start TEXT NOT NULL,
    deadline TEXT NOT NULL,
    status INTEGER NOT NULL DEFAULT 0,
    notify INTEGER NOT NULL DEFAULT 0,
    priority INTEGER NOT NULL DEFAULT 0,
    description TEXT,
    notified_sent INTEGER NOT NULL DEFAULT 0
);

🔁 Background Status Processing
The application uses an asynchronous background task to periodically check task states.
The background process:
1. Reads the stored tasks.
2. Gets the current date/time.
3. Compares the current time with the task start time.
4. Compares the current time with the deadline.
5. Updates the status when required.
6. Updates the calendar.
7. Updates the selected-date task list.
8. Refreshes the Flet interface.
The automatic check runs approximately once every 60 seconds.
This allows task status to change automatically while the application remains open.
🔔 Notification Processing
The reminder flow is:
Task has notification enabled
          │
          ▼
Check task priority
          │
          ▼
Check remaining deadline time
          │
          ▼
Deadline ≤ 5 minutes
          │
          ▼
Show native notification
          │
          ▼
Mark notification as sent

The notification functionality uses:
from plyer import notification


🛠️ Technology Stack
Python
Python is the primary programming language.
It handles:
- Application logic
- Task processing
- Date/time processing
- Database operations
- Status calculation
- Notification logic
Why Python?
Python provides:
- Simple syntax
- Fast development
- Large ecosystem
- Easy database integration
- Strong support for automation and application logic
Flet
Flet is used to create the application's graphical user interface.
The interface is built entirely with Python rather than using a separate frontend language.
Examples of Flet components used in the project include:
Text
TextField
Container
Row
Column
Switch
IconButton
TextButton
AlertDialog
NavigationBar
DatePicker
TimePicker

Why Flet?
Flet makes it possible to build a modern UI using Python and provides a convenient route to mobile/desktop application packaging.
It is particularly useful for a project where the developer wants to keep the UI and application logic in the same Python ecosystem.
SQLite
SQLite is used for persistent local storage.
Why SQLite?
SQLite was selected because:
- It is lightweight
- It requires no database server
- It works locally
- It supports offline operation
- It is easy to distribute
- It is appropriate for a personal task-management application
Plyer
Plyer is used for local/platform notifications.
It allows the application to trigger native notifications when important deadlines are approaching.
asyncio
Python's asyncio functionality is used for background processing.
The application uses an asynchronous loop to periodically update task statuses without requiring the user to manually refresh the application.
📦 Dependencies
The project's current requirements.txt contains:
flet==0.86.5
plyer

Install them using:
pip install -r requirements.txt

💻 Local Installation
1. Clone the repository
git clone https://github.com/<YOUR_USERNAME>/Todo_Using_flet.git

Then:
cd Todo_Using_flet

2. Create a virtual environment
Windows:
python -m venv venv

Activate:
.\venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python main.py

The Flet application will start locally.
📱 Android APK
The application can be packaged as an Android APK using Flet's Android build process.
The generated build/ directory contains the packaged application and supporting files.
These generated build files are intentionally excluded from the Git repository.
The APK should instead be distributed through a GitHub Release.
📥 Download APK
After publishing a GitHub release, users can download the Android APK from:
https://github.com/<YOUR_USERNAME>/Todo_Using_flet/releases/latest

Example README link:
[📱 Download the latest APK](https://github.com/<YOUR_USERNAME>/Todo_Using_flet/releases/latest)

📦 Large Build ZIP
The generated build/package ZIP is intentionally not stored in the normal Git repository.
This is because generated builds can be extremely large and are not required to understand or recreate the source code.
The source repository contains the Python files and dependency definition required to rebuild the application.
🚫 Files Excluded From Git
The following are intentionally excluded:
build/
.flet/
__pycache__/
*.pyc
*.apk
*.aab
TasksDB.db
tasks.csv
venv/
.venv/
.vscode/
.idea/

These files are either:
- Generated automatically
- Local runtime data
- Local development files
- Large binary build artifacts
🎯 Why This Project?
The purpose of Todo Using Flet is to demonstrate how a complete task management application can be developed using Python while still providing:
- A graphical interface
- Persistent storage
- Automated time-based processing
- Notifications
- Calendar integration
- Productivity statistics
The project combines application development, database programming, UI design, asynchronous operations, and Android packaging in one application.
🚀 Future Improvements
Possible improvements include:
- Task editing
- Recurring tasks
- Task categories
- Tags
- Task sorting
- Drag-and-drop task ordering
- Dark/light theme settings
- Task history
- Undo delete
- Cloud synchronization
- User accounts
- Multi-device synchronization
- Data backup and restore
- CSV export/import
- Advanced productivity analytics
- Weekly productivity reports
- Monthly productivity reports
- More advanced notification scheduling
- Google Calendar integration
- Play Store distribution
📌 Current Status
Implemented
- [x] Task creation
- [x] Task descriptions
- [x] Start date and time
- [x] Deadline date and time
- [x] Automatic status tracking
- [x] Completed tasks
- [x] Missed tasks
- [x] Ongoing tasks
- [x] Task priorities
- [x] Notifications
- [x] Task search
- [x] Calendar view
- [x] Statistics
- [x] Delete task
- [x] Clear completed tasks
- [x] Reset all tasks
- [x] SQLite persistence
- [x] Flet-based interface
- [x] Android APK packaging
📸 Screenshots
Application screenshots can be added under a screenshots/ directory.
Example:
![Home Screen](screenshots/home.png)

Recommended screenshots:
screenshots/
├── home.png
├── add-task.png
├── statistics.png
└── settings.png

👨‍💻 Author
Utsadeep Kundu
B.Tech — Computer Science & Engineering
Artificial Intelligence & Machine Learning
📄 License
This project is intended for educational, academic, portfolio, and personal productivity purposes.

## 📱 Download APK

[⬇️ Download Todo Using Flet APK ]: (https://drive.google.com/file/d/1wx88VQ1kIU9svk12MyvCHKpMPLkjQ6g9/view)
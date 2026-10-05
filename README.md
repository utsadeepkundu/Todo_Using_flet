# TaskFlow — Flet Task Management Application

TaskFlow is a desktop/mobile-oriented task management application built with **Python and Flet**.

The application allows users to create tasks, assign start times and deadlines, mark tasks as completed, search for tasks, monitor task status, set high priority, enable reminders, view tasks through a calendar, and track productivity through statistics.

The application stores task information locally using **SQLite**, making it an offline-first task management application.

---

## 📱 Application Overview

TaskFlow is designed to provide a simple interface for managing daily tasks and deadlines.

Instead of depending on an online account or remote server, the application stores task information locally in a SQLite database.

The application provides four major sections:

- HOME
- ADD
- STATS
- SETTINGS

The overall workflow is:

```text
User
  │
  ▼
TaskFlow Flet Interface
  │
  ├── Add Task
  │      │
  │      ▼
  │   Validate Input
  │      │
  │      ▼
  │   SQLite Database
  │
  ├── Home
  │      │
  │      ├── Search
  │      ├── Calendar
  │      ├── Task Status
  │      └── Task Actions
  │
  ├── Statistics
  │      │
  │      └── Productivity Summary
  │
  └── Settings
         │
         ├── Clear Completed Tasks
         ├── Reset All Tasks
         └── About

  ✨ Main Features
1. Task Creation
Users can create a new task by providing:
- Task name
- Description
- Start date
- Start time
- Deadline date
- Deadline time
- High priority option
- Reminder option
The application validates the required information before saving the task.
A task cannot be saved when:
- Task name is empty
- Start date/time is missing
- Deadline date/time is missing
- Deadline is before the start time
- Deadline is exactly the same as the start time
2. Automatic Task Status
TaskFlow automatically determines the current status of a task based on the current time.
The application uses four states:
Status	Meaning
NOT STARTED	Current time is before the task start time
ONGOING	Current time is between the start and deadline
COMPLETED	User manually completed the task
MISSED	Current time has passed the deadline


The status is automatically updated while the application is running.
Status logic
Current Time
     │
     ├── Before Start
     │       ↓
     │   NOT STARTED
     │
     ├── Start → Deadline
     │       ↓
     │    ONGOING
     │
     ├── Deadline Passed
     │       ↓
     │     MISSED
     │
     └── User completes task
             ↓
         COMPLETED

Completed tasks are not automatically changed back to another state.
📝 How the User Uses the Application
Step 1 — Open TaskFlow
When the application starts, the user is taken to the main TaskFlow interface.
The application uses a mobile-style layout designed around a fixed 400 × 800 interface.
The main navigation contains:
HOME
ADD
STATS
SETTINGS

➕ Step 2 — Create a Task
The user opens the ADD section.
The form allows the user to enter the task information.
Example:
Task Name:
Complete ML Assignment

Description:
Finish model evaluation and prepare the report.

Start:
10-Oct-26 10:00

Deadline:
10-Oct-26 13:00

High Priority:
ON

Reminder:
ON

The user then saves the task.
✅ Step 3 — Validation
Before storing the task, TaskFlow checks the input.
For example:
Start:
10-Oct-26 15:00

Deadline:
10-Oct-26 14:00

This is invalid because the deadline occurs before the task starts.
The application displays:
Deadline must be after the start time.

Only valid tasks are stored.
💾 Step 4 — Save to SQLite
Once the task passes validation, the task is stored locally in the SQLite database.
The database used by the application is:
TasksDB.db

The main table is:
tasks

The table contains:
task_no
task_name
start
deadline
status
notify
priority
description
notified_sent

🏠 Step 5 — Home Dashboard
The HOME section acts as the main task management area.
The user can:
- View tasks
- Search tasks
- Mark tasks as completed
- Delete individual tasks
- Change task priority
- Enable/disable reminders
- View the task calendar
- See task statuses
🔎 Searching Tasks
The Home section provides a search field.
A user can search using the task name or description.
For example:
Search:
machine learning

TaskFlow searches the SQLite database for matching task information.
The search implementation supports:
Task name prefix matching
OR
Description text matching

✅ Completing a Task
Each task provides an action to mark it as completed.
When the user completes a task:
Task
 ↓
COMPLETED

The completed state is stored in SQLite.
Once a task is marked as completed, the automatic status updater does not overwrite it.
🗑️ Deleting a Task
A user can delete an individual task.
TaskFlow asks for confirmation before permanently deleting the task.
The database record is then removed.
🔴 Priority
Tasks have a priority value.
The application uses:
LOW
MEDIUM
HIGH

The task creation interface specifically allows the user to enable:
High Priority

A high-priority task is internally represented by a higher priority value.
Priority also affects the visual appearance of tasks and the reminder behavior.
🔔 Reminder / Notification System
TaskFlow can generate a native notification using the Plyer library.
The user can enable:
Reminder

for a task.
For high-priority tasks, TaskFlow checks how close the task is to its deadline.
When:
Deadline - Current Time <= 5 minutes

the application can display:
Critical Task Reminder

Task "<task name>" is due in less than 5 minutes!

The application also records that the notification has already been sent so that the same reminder is not repeatedly triggered during the same task state.
📅 Calendar
The Home section contains a calendar interface.
The calendar allows the user to:
- Navigate to the previous month
- Navigate to the next month
- Return to the current date
- Select a specific date
- View tasks associated with the selected date
Calendar cells can visually indicate task status.
Possible task states represented through the calendar include:
NOT STARTED
ONGOING
COMPLETED
MISSED

Selecting a date displays the tasks associated with that date.
📊 Statistics
TaskFlow contains a STATS page that provides a productivity overview.
The statistics section calculates:
Total Tasks
Completed Tasks
Pending Tasks
Completion Percentage

The completion percentage is calculated as:
Completed Tasks
---------------------- × 100
Total Tasks

This allows the user to get a quick overview of their task completion performance.
⚙️ Settings
The SETTINGS page provides application management options.
Clear Completed Tasks
Removes only tasks that are already marked:
COMPLETED

The application also reports how many completed tasks were removed.
Reset All Tasks
This option permanently removes all stored tasks.
Because this is destructive, TaskFlow displays a confirmation dialog before performing the operation.
The user can choose:
CANCEL

or:
DELETE ALL

About
The About section describes TaskFlow as:
An offline task management application
built with Flet and SQLite.

🧠 How the Application Works Internally
The application consists of three main Python source files.
main.py
   │
   ▼
Flet User Interface
   │
   ▼
operations.py
   │
   ▼
db_config.py
   │
   ▼
SQLite Database

📂 Project Structure
Recommended source repository structure:
TaskFlow/
│
├── main.py
├── operations.py
├── db_config.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── assets/
    └── ...

Generated files should not be committed.
🧩 Source Code Responsibilities
main.py
main.py contains the main TaskFlow application.
It is responsible for:
- Creating the Flet interface
- Navigation
- Home page
- Add Task page
- Statistics page
- Settings page
- Calendar
- Search
- Task actions
- Task status updates
- Reminder handling
- User interaction
- UI refresh
It is the main entry point of the application.
operations.py
operations.py contains the database operations related to tasks.
It provides functions for:
add_task()
get_tasks_list()
search_task_name()
remove_a_task()
delete_all_tasks()
update_status()
update_priority()
update_notify()
update_notified_sent()

This keeps database operations separate from most of the UI implementation.
db_config.py
db_config.py manages the SQLite connection and table creation.
It provides:
create_connection()
create_table()

The application automatically creates the tasks table if it does not already exist.
🗄️ Database Architecture
TaskFlow uses SQLite for local data persistence.
The main database is:
TasksDB.db

The main table is:
tasks

Schema:
task_no
task_name
start
deadline
status
notify
priority
description
notified_sent

Column explanation
Column	Purpose
task_no	Unique task identifier
task_name	Name of the task
start	Task start date and time
deadline	Task deadline
status	Current task state
notify	Whether reminder is enabled
priority	Task priority
description	Additional task information
notified_sent	Tracks reminder delivery state


🔄 Complete Functional Workflow
The complete TaskFlow workflow can be represented as:
                 USER
                   │
                   ▼
             FLET INTERFACE
                   │
          ┌────────┼────────┐
          │        │        │
          ▼        ▼        ▼
        ADD      HOME      STATS
          │        │
          │        ├── Search
          │        ├── Complete
          │        ├── Delete
          │        ├── Priority
          │        ├── Reminder
          │        └── Calendar
          │
          ▼
       VALIDATION
          │
          ▼
     operations.py
          │
          ▼
      db_config.py
          │
          ▼
     SQLite Database
          │
          ▼
  Automatic Status Update
          │
          ├── NOT STARTED
          ├── ONGOING
          ├── MISSED
          └── COMPLETED
          │
          ▼
      FLET UI REFRESH

🔁 Automatic Background Processing
TaskFlow uses asynchronous/background processing to periodically update task statuses.
The application runs an automatic status update process using:
page.run_task(...)


The background process checks the current time against:
Task Start Time
Task Deadline

and updates the SQLite database accordingly.
This allows the interface to reflect the current state of tasks without requiring the user to manually refresh every task.
🛠️ Technology Stack
Python
Python is the main programming language used for:
- Application logic
- Database operations
- Date/time processing
- Status calculation
- Notifications
- User interaction logic
Flet
Flet is used to create the graphical user interface.
It allows the project to create the application interface using Python instead of writing the UI separately in a traditional mobile framework.
Flet provides components used throughout TaskFlow such as:
Text
TextField
Button
Container
Row
Column
Switch
Dialog
NavigationBar
Calendar-related UI

SQLite
SQLite is used as the local database.
The main reasons for using SQLite are:
- Lightweight
- No separate database server
- Local storage
- Easy deployment
- Good fit for a single-user task management application
- Works well for offline applications
Plyer
Plyer is used for platform-level notifications.
TaskFlow uses it to generate native reminder notifications for high-priority tasks approaching their deadlines.
asyncio
Python's asynchronous capabilities are used for background task-status processing.
This helps the application periodically check and update task states while the UI remains active.
📦 Python Dependencies
The project currently uses:
flet==0.86.5
plyer

Install them with:
pip install -r requirements.txt

💻 Running the Application Locally
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd TaskFlow

2. Create a virtual environment
Windows:
python -m venv venv

Activate it:
.\venv\Scripts\Activate.ps1

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python main.py

Flet will start the application using the configured interface.
📱 Android APK
The project has been packaged into an Android APK using Flet's build system.
The generated build directory contains packaged Flutter and Python components.
The APK should not be committed directly to the normal Git repository because Android APK files are large binary artifacts.
Instead, the APK should be uploaded as a GitHub Release asset.
Example release:
v1.0.0

with:
TaskFlow.apk

attached.
📥 APK Download
After creating a GitHub Release, this section can be updated with the release URL:
https://github.com/<YOUR_USERNAME>/TaskFlow/releases/latest

A user can open the release page and download the APK.
🔒 Files Excluded From Git
The repository intentionally excludes generated and local files such as:
build/
.flet/
__pycache__/
*.apk
*.aab
TasksDB.db
tasks.csv

The source repository should contain the Python application code and configuration required to recreate the application.
🎯 Design Approach
TaskFlow follows an offline-first design.
The user does not need:
- A web server
- Cloud database
- Login system
- Internet connection for normal task management
The task data is stored locally using SQLite.
The result is a lightweight application designed for personal productivity.
🚀 Future Improvements
Possible future improvements include:
- Task editing functionality
- Recurring tasks
- Categories
- Tags
- Drag-and-drop task ordering
- Dark/light theme switching
- Cloud synchronization
- User accounts
- Multi-device synchronization
- Backup and restore
- Export/import
- Push notifications
- Richer productivity analytics
- Weekly and monthly productivity reports
- Search filters
- Task sorting
- Task history
- Android Play Store distribution
📌 Current Application Flow
Launch TaskFlow
      ↓
HOME
      ↓
Create / Search / Manage Tasks
      ↓
Task stored in SQLite
      ↓
Automatic time-based status calculation
      ↓
Reminder when applicable
      ↓
Task completion
      ↓
Statistics update

📸 Screenshots
Add application screenshots here after uploading them to the repository.
Example:
![TaskFlow Home](screenshots/home.png)
![Add Task](screenshots/add-task.png)
![Statistics](screenshots/statistics.png)
![Settings](screenshots/settings.png)


B.Tech — Computer Science & Engineering
Artificial Intelligence & Machine Learning
📄 License
This project is intended for educational, academic, portfolio, and personal productivity purposes.

## One important correction from the earlier setup

Since I inspected your real source code, I recommend keeping:

```text
TasksDB.db
tasks.csv

out of GitHub. Your application creates/opens TasksDB.db locally, and the source code does not require the existing database file to be distributed. The tasks.csv file is also not part of the core database workflow.
Your repository should therefore be:
to_do_app/
├── main.py
├── operations.py
├── db_config.py
├── requirements.txt
├── README.md
└── .gitignore
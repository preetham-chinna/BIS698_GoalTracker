import PySimpleGUI as sg
from datetime import datetime
import sqlite3
import register_login
# Function to create a new goal
def create_goal(conn, cursor):
    goal_title = values['goal_title']
    goal_info = values['goal_info']
    goal_due_date = values['goal_due_date']

    if goal_title and goal_info and goal_due_date:
        # Insert the goal data into the database
        cursor.execute("INSERT INTO goals (title, info, due_date) VALUES (?, ?, ?)",
                       (goal_title, goal_info, goal_due_date))
        conn.commit()
        sg.popup('Goal created successfully!')
    else:
        sg.popup('Please fill in all the fields.')

# Function to update the progress of a goal
def update_progress(conn, cursor):
    goal_progress = values['goal_progress']

    if goal_progress:
        # Update the progress in the database
        cursor.execute("UPDATE goals SET progress = ? WHERE id = ?", (goal_progress, selected_goal_id))
        conn.commit()
        sg.popup('Progress updated successfully!')
    else:
        sg.popup('Please enter a valid progress value.')

# Function to view the progress report of a goal
def view_progress_report(conn, cursor):
    cursor.execute("SELECT progress FROM goals WHERE id = ?", (selected_goal_id,))
    result = cursor.fetchone()
    if result:
        sg.popup('Progress report: ' + str(result[0]) + '%')
    else:
        sg.popup('Goal not found.')

# Create or connect to the SQLite database
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

# Create a goals table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                  id INTEGER PRIMARY KEY,
                  title TEXT,
                  info TEXT,
                  due_date TEXT,
                  progress INTEGER DEFAULT 0)''')
conn.commit()

# Layout for the main window
layout = [
    [sg.Text('Goal Title:'), sg.Input(key='goal_title')],
    [sg.Text('Goal Information:'), sg.Input(key='goal_info')],
    [sg.Text('Goal Due Date:'), sg.Input(key='goal_due_date', enable_events=True), sg.CalendarButton('Choose Date', key='goal_due_date_button')],
    #[sg.Button('Create Goal', bind_return_key=True), sg.Button('Update Progress', bind_return_key=True), sg.Button('View Progress Report', bind_return_key=True)],
    [sg.Text('Goal Progress (%):'), sg.Input(key='goal_progress')],
    [sg.Button('Create Goal', bind_return_key=True), sg.Button('Update Progress', bind_return_key=True),
     sg.Button('View Progress Report', bind_return_key=True)]
]

# Create the main window
window = sg.Window('Academic Goal Setting', layout)

selected_goal_id = None  # To store the currently selected goal ID

# Event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'goal_due_date_button':
        window['goal_due_date'].update(values['goal_due_date_button'])

    if event == 'Create Goal':
        create_goal(conn, cursor)

    if event == 'Update Progress':
        if selected_goal_id is not None:
            update_progress(conn, cursor)
        else:
            sg.popup('Please select a goal first.')

    if event == 'View Progress Report':
        selected_goal_id = sg.popup_get_text('Enter Goal ID to view progress:', title='Enter Goal ID')
        if selected_goal_id:
            view_progress_report(conn, cursor)

# Close the main window
window.close()

# Close the database connection
conn.close()

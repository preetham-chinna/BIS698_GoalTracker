import PySimpleGUI as sg
import sqlite3

# Create a SQLite database and a users table
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()
conn.close()

# Function to handle user registration
def register(username, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Function to handle user login
def login(username, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    user_id = result[0]
    if result:
        conn.close()
        return user_id#True check
    else:
        conn.close()
        return None #False check

# Layout for the main window
layout = [
    [sg.Text('Username:'), sg.Input(key='username')],
    [sg.Text('Password:'), sg.Input(key='password', password_char='*')],
    [sg.Button('Register'), sg.Button('Login')]
]

# Create the main window
window = sg.Window('User Registration and Login', layout)

# Event loop for registration and login
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == 'Register':
        username = values['username']
        password = values['password']
        if username and password:
            if register(username, password):
                sg.popup('Registration successful!')
            else:
                sg.popup('Username already exists.')
        else:
            sg.popup('Please fill in all the fields.')

    if event == 'Login':
        username = values['username']
        password = values['password']
        if username and password:
            if login(username, password):
                sg.popup('Login successful!')
                break  # Break out of the login loop and proceed to goal setting
            else:
                sg.popup('Invalid username or password.')
        else:
            sg.popup('Please fill in all the fields.')

window.close()



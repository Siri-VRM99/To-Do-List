import mysql.connector 
import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SIRI_99",
    database="todo_db"
)
cursor = conn.cursor()

# Function to Add a Task
def add_task(cursor, connection):
    while True:
        ID = input('Enter id: ')
        Title = input('Enter title: ')
        Description = input('Enter description: ')
        Due_Date_str = input("Enter due date (YYYY-MM-DD): ")
        Completed = str(input('Enter completed (yes/no): '))

        # convert date string to date object
        
        Due_Date_str = Due_Date_str.replace(' ', '-')
        Due_Date = datetime.datetime.strptime(Due_Date_str, "%Y-%m-%d").date()


        # SQL query
        sql = 'INSERT INTO tasks (ID, Title, Description, Due_Date, Completed) VALUES (%s, %s, %s, %s, %s)' 
        values = (ID, Title, Description, Due_Date, Completed)

        try:
            cursor.execute(sql, values)
            connection.commit()
            print("Task inserted successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()

        ch = input('Want to add more (y/n): ')
        if ch.lower() == 'n':
            break

# Function to List Tasks
def list_tasks():
    sql = "SELECT * FROM tasks"
    cursor.execute(sql)
    tasks = cursor.fetchall()
    if not tasks:
        print("No tasks found.")
    else:
        print("\nAll Tasks:")
        for task in tasks:
            print(f"Task {task[0]} - Title: {task[1]}, Description: {task[2]}, Due Date: {task[3]}, Completed: {task[4]}")

# Function to Set a Reminder
def set_reminder(task_id):
    current_time = datetime.datetime.now().date()
    sql = "SELECT Title, Due_Date FROM tasks WHERE ID = %s"
    cursor.execute(sql, (task_id,))
    task = cursor.fetchone()
    if task:
        task_title, due_date = task
        if due_date > current_time:
            print(f"Reminder: Task '{task_title}' is due on {due_date}.")
        else:
            print(f"Task '{task_title}' is overdue!")
    else:
        print(f"No task found with ID {task_id}.")

# ---- Run code ----
add_task(cursor, conn)
list_tasks()

task_id = input("Enter task ID to set reminder: ")
set_reminder(task_id)

cursor.close()
conn.close()

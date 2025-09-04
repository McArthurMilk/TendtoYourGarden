import tkinter as tk #desktop GUI
from tkinter import messagebox #showing pop up messages like errors
import sqlite3 #lightweight database to save info

# ---------- Database Setup ----------
conn = sqlite3.connect("habits.db") #opens database file called habits.db
cursor = conn.cursor() #cursor allows us to execute SQL commands

#creates table named habits with id, name, and streak
cursor.execute("""
CREATE TABLE IF NOT EXISTS habits ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    streak INTEGER DEFAULT 0
)
""")
conn.commit() #saves changes to database


# ---------- Functions ----------
def add_habit():
    habit_name = habit_entry.get().strip() #gets text from input box and strips extra spaces
    if not habit_name: #no text in text box
        messagebox.showwarning("Warning", "Please enter a habit to track.")
        return

    try:
        cursor.execute("INSERT INTO habits (name) VALUES (?)", (habit_name,))
        conn.commit() #saves changes
        habit_entry.delete(0, tk.END) #clears textbox after adding
        load_habits() #refreshes habit list with new habit
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"Habit '{habit_name}' already exists!")

def remove_habit(habit_id):

    try:
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
        habit_entry.delete(0, tk.END)  # clears textbox after adding
        load_habits()  # refreshes habit list with new habit
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"Habit '{habit_name}' does not exist!")

def increment_streak(habit_id):
    cursor.execute("UPDATE habits SET streak = streak + 1 WHERE id=?", (habit_id,))
    conn.commit()
    load_habits()


def reset_streak(habit_id):
    cursor.execute("UPDATE habits SET streak = 0 WHERE id=?", (habit_id,))
    conn.commit()
    load_habits()


def load_habits():
    for widget in habit_frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT id, name, streak FROM habits")
    habits = cursor.fetchall()

    for habit_id, name, streak in habits:
        frame = tk.Frame(habit_frame, pady=5)
        frame.pack(fill="x")

        tk.Label(frame, text=f"{name} (Streak: {streak})", font=("Arial", 12)).pack(side="left", padx=5)

        tk.Button(frame, text="Done ✅", command=lambda h=habit_id: increment_streak(h)).pack(side="left", padx=5)
        tk.Button(frame, text="Reset ♻️", command=lambda h=habit_id: reset_streak(h)).pack(side="left", padx=5)
        tk.Button(frame, text="Delete ", command=lambda h=habit_id: remove_habit(h)).pack(side="left", padx=5)


# ---------- UI Setup ----------
root = tk.Tk()
root.title("Habit Tracker")

# Input section
input_frame = tk.Frame(root, pady=10)
input_frame.pack()

habit_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
habit_entry.pack(side="left", padx=5)

add_button = tk.Button(input_frame, text="Add Habit", command=add_habit)
add_button.pack(side="left")


# Habit list section
habit_frame = tk.Frame(root, pady=10)
habit_frame.pack()

load_habits()

root.mainloop()

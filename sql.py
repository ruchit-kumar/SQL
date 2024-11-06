import sqlite3
from tkinter import *
from tkinter import messagebox

# Create or connect to a SQLite database
def connect():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)")
    conn.commit()
    conn.close()

def insert(title, author, year, isbn):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO book VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, title, author, year, isbn):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    conn.commit()
    conn.close()

# Function for handling selected row
def get_selected_row(event):
    global selected_tuple
    index = list1.curselection()[0]
    selected_tuple = list1.get(index)
    entry_title.delete(0, END)
    entry_title.insert(END, selected_tuple[1])
    entry_author.delete(0, END)
    entry_author.insert(END, selected_tuple[2])
    entry_year.delete(0, END)
    entry_year.insert(END, selected_tuple[3])
    entry_isbn.delete(0, END)
    entry_isbn.insert(END, selected_tuple[4])

# Function for view command
def view_command():
    list1.delete(0, END)
    for row in view():
        list1.insert(END, row)

# Function for search command
def search_command():
    list1.delete(0, END)
    for row in search(title_text.get(), author_text.get(), year_text.get(), isbn_text.get()):
        list1.insert(END, row)

# Function for add command
def add_command():
    insert(title_text.get(), author_text.get(), year_text.get(), isbn_text.get())
    list1.delete(0, END)
    list1.insert(END, (title_text.get(), author_text.get(), year_text.get(), isbn_text.get()))

# Function for delete command
def delete_command():
    delete(selected_tuple[0])

# Function for update command
def update_command():
    update(selected_tuple[0], title_text.get(), author_text.get(), year_text.get(), isbn_text.get())

# Tkinter GUI setup
window = Tk()
window.title("Online Bookstore")

# Labels
Label(window, text="Title").grid(row=0, column=0)
Label(window, text="Author").grid(row=0, column=2)
Label(window, text="Year").grid(row=1, column=0)
Label(window, text="ISBN").grid(row=1, column=2)

# Entry fields
title_text = StringVar()
entry_title = Entry(window, textvariable=title_text)
entry_title.grid(row=0, column=1)

author_text = StringVar()
entry_author = Entry(window, textvariable=author_text)
entry_author.grid(row=0, column=3)

year_text = StringVar()
entry_year = Entry(window, textvariable=year_text)
entry_year.grid(row=1, column=1)

isbn_text = StringVar()
entry_isbn = Entry(window, textvariable=isbn_text)
entry_isbn.grid(row=1, column=3)

# Listbox and scrollbar
list1 = Listbox(window, height=8, width=50)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)
list1.bind('<<ListboxSelect>>', get_selected_row)

scrollbar = Scrollbar(window)
scrollbar.grid(row=2, column=2, rowspan=6)
list1.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=list1.yview)

# Buttons
Button(window, text="View All", width=12, command=view_command).grid(row=2, column=3)
Button(window, text="Search Entry", width=12, command=search_command).grid(row=3, column=3)
Button(window, text="Add Entry", width=12, command=add_command).grid(row=4, column=3)
Button(window, text="Update Selected", width=12, command=update_command).grid(row=5, column=3)
Button(window, text="Delete Selected", width=12, command=delete_command).grid(row=6, column=3)
Button(window, text="Close", width=12, command=window.destroy).grid(row=7, column=3)

# Initialize the database
connect()

window.mainloop()

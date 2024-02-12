from tkinter import *
from tkinter import messagebox, simpledialog
from random import choice, randint, shuffle
import pyperclip
import json

def request_password():
    password = simpledialog.askstring("Password", "Enter your password:", show='*')
    if password != "Tere12345":  # Asendage see teie eelistatud salasõnaga
        messagebox.showwarning("Wrong Password", "The password you entered is incorrect.")
        window.destroy()  # Sulgeb akna, kui salasõna on vale

def generate_password():
    letters = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]
    numbers = [str(i) for i in range(10)]
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_chars = [choice(letters) for _ in range(randint(8, 10))] + \
                     [choice(symbols) for _ in range(randint(2, 4))] + \
                     [choice(numbers) for _ in range(randint(2, 4))]
    shuffle(password_chars)

    password = "".join(password_chars)
    password_entry.insert(0, password)
    pyperclip.copy(password)

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
        return

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)

    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# UI seadistamine
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")  # Veenduge, et logo.png asub teie skripti kaustas
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Sildid ja sisestusväljad
labels_texts = ["Website:", "Email/Username:", "Password:"]
entries = []

for i, text in enumerate(labels_texts):
    Label(text=text).grid(row=i+1, column=0)
    entry = Entry(width=35 if i > 0 else 21)
    entry.grid(row=i+1, column=1, columnspan=2 if i > 0 else 1)
    entries.append(entry)

website_entry, email_entry, password_entry = entries
website_entry.focus()
email_entry.insert(0, "")

# Nupud
Button(text="Search", width=13, command=find_password).grid(row=1, column=2)
Button(text="Generate Password", command=generate_password).grid(row=3, column=2)
Button(text="Add", width=36, command=save).grid(row=4, column=1, columnspan=2)

# Salasõna küsimine enne GUI kuvamist
window.after(100, request_password)

window.mainloop()

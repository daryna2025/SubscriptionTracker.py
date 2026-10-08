from tkinter import *
import sqlite3

#Luodaan tietokanta
connection = sqlite3.connect("subscriptions.db")

#Luodaan taulukko
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    payment_day INTEGER,
    category TEXT
)
""")

connection.commit()
connection.close()


def add_subscription():
    name = name_entry.get()
    price = price_entry.get()
    payment_day = data_entry.get()
    category = category_entry.get()

    connection = sqlite3.connect("subscriptions.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO subscriptions (name, price, payment_day, category) VALUES (?, ?, ?, ?)",
        (name, price, payment_day, category)
    )

    connection.commit()
    connection.close()
    show_subscriptions()

    name_entry.delete(0, END)
    price_entry.delete(0, END)
    data_entry.delete(0, END)
    category_entry.delete(0, END)


def show_subscriptions():
    connection = sqlite3.connect("subscriptions.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM subscriptions ORDER BY payment_day")
    subscriptions = cursor.fetchall()

    total = len(subscriptions)
    suma = sum(subscription[2] for subscription in subscriptions)

    total_label.config(text=f"Subscriptions: {total}    Total: {suma:.2f} €")

    connection.close()

    subscription_list.delete(0, END)

    for subscription in subscriptions:
        subscription_list.insert(
            END,
            f"{subscription[1]} | {subscription[2]} € | day {subscription[3]} | {subscription[4]}"
        )


def delete_subscription():
    selected = subscription_list.curselection()

    if selected:
        index = selected[0]

        connection = sqlite3.connect("subscriptions.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM subscriptions ORDER BY payment_day")
        subscriptions = cursor.fetchall()

        subscription_id = subscriptions[index][0]

        cursor.execute(
            "DELETE FROM subscriptions WHERE id = ?",
            (subscription_id,)
        )

        connection.commit()
        connection.close()

        show_subscriptions()

        name_entry.delete(0, END)
        price_entry.delete(0, END)
        data_entry.delete(0, END)
        category_entry.delete(0, END)


def edit_subscription():
    selected = subscription_list.curselection()

    if selected:
        index = selected[0]

        connection = sqlite3.connect("subscriptions.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM subscriptions ORDER BY payment_day")
        subscriptions = cursor.fetchall()

        subscription_id = subscriptions[index][0]

        cursor.execute(
            "UPDATE subscriptions SET name=?, price=?, payment_day=?, category=? WHERE id=?",
            (
                name_entry.get(),
                price_entry.get(),
                data_entry.get(),
                category_entry.get(),
                subscription_id
            )
        )

        connection.commit()
        connection.close()

        show_subscriptions()

        name_entry.delete(0, END)
        price_entry.delete(0, END)
        data_entry.delete(0, END)
        category_entry.delete(0, END)


def select_subscription(event):
    selected = subscription_list.curselection()

    if selected:
        connection = sqlite3.connect("subscriptions.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM subscriptions ORDER BY payment_day")
        subscriptions = cursor.fetchall()

        connection.close()

        subscription = subscriptions[selected[0]]

        name_entry.delete(0, END)
        name_entry.insert(0, subscription[1])

        price_entry.delete(0, END)
        price_entry.insert(0, subscription[2])

        data_entry.delete(0, END)
        data_entry.insert(0, subscription[3])

        category_entry.delete(0, END)
        category_entry.insert(0, subscription[4])


#Luodaan ikkuna
window = Tk()

window.title("Subscription Tracker")
window.geometry("600x500")

main_frame = Frame(window)
main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

#Luodaan otsikko
title = Label(main_frame, text="MONTHLY SUBSCRIPTION TRACKER")
title.grid(column=0, row=0, columnspan=2, pady=10)


#Luodaan nimi-teksti ja nimi-kenttä
name_label = Label(main_frame, text="Name")
name_label.grid(column=0, row=1)

name_entry = Entry(main_frame)
name_entry.grid(column=1, row=1)


#Luodaan nimi-teksti ja nimi-kenttä
price_label = Label(main_frame, text="Price")
price_label.grid(column=0, row=2)

price_entry = Entry(main_frame)
price_entry.grid(column=1, row=2)


#Luodaan nimi-teksti ja nimi-kenttä
data_label = Label(main_frame, text="Payment day")
data_label.grid(column=0, row=3)

data_entry = Entry(main_frame)
data_entry.grid(column=1, row=3)


#Luodaan nimi-teksti ja nimi-kenttä
category_label = Label(main_frame, text="Category")
category_label.grid(column=0, row=4)

category_entry = Entry(main_frame)
category_entry.grid(column=1, row=4)


#Luodaan lista
subscription_list = Listbox(main_frame, width=60, height=8)
subscription_list.grid(column=0, row=5, columnspan=2, pady=10)

subscription_list.bind("<<ListboxSelect>>", select_subscription)


#Luodaan kokonaismäärä
total_label = Label(main_frame, text="")
total_label.grid(column=0, row=6, columnspan=2)


#Luodaan painikkeet
button_frame = Frame(main_frame)
button_frame.grid(column=0, row=7, columnspan=2)

add_button = Button(button_frame, text="Add", command=add_subscription, fg="white", bg="green")
add_button.grid(column=0, row=0)

edit_button = Button(button_frame, text="Edit", command=edit_subscription, fg="black", bg="yellow")
edit_button.grid(column=1, row=0)

delete_button = Button(button_frame, text="Delete", command=delete_subscription, fg="white", bg="red")
delete_button.grid(column=2, row=0)
show_subscriptions()


#Käynnistetään ohjelma
window.mainloop()
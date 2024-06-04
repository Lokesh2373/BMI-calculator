import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt

def calculate_bmi():
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
        if height <= 0:
            messagebox.showerror('Error', 'Height must be greater than 0!')
            return None
        bmi = weight / (height ** 2)
        result_label.config(text="Your BMI is {:.1f}".format(bmi))
        return bmi
    except ValueError:
        messagebox.showerror('Error', 'Enter a valid number')
        return None

def determine_category(bmi):
    if bmi < 18.5:
        stage = "Underweight"
    elif 18.5 <= bmi < 25:
        stage = "Normal weight"
    elif 25 <= bmi < 30:
        stage = "Overweight"
    else:
        stage = "Obese"
    category_label.config(text="Category: {}".format(stage))
    return stage

def on_calculate():
    bmi = calculate_bmi()
    if bmi is not None:
        category = determine_category(bmi)
        save_to_db(height_entry.get(), weight_entry.get(), bmi, category)

def save_to_db(height, weight, bmi, category):
    conn = sqlite3.connect('bmi_calc.db')
    c = conn.cursor()
    c.execute("INSERT INTO bmi_records (height, weight, bmi, category) VALUES (?, ?, ?, ?)",
              (height, weight, bmi, category))
    conn.commit()
    conn.close()
    messagebox.showinfo('Success', 'Record saved to database')

def fetch_data():
    conn = sqlite3.connect('bmi_calc.db')
    c = conn.cursor()
    c.execute("SELECT height, weight, bmi, category FROM bmi_records")
    data = c.fetchall()
    conn.close()
    return data

def plot_data():
    data = fetch_data()
    if not data:
        messagebox.showinfo('No Data', 'No data available to plot')
        return

    heights, weights, bmis, categories = zip(*data)
    category_mapping = {'Underweight': 1, 'Normal weight': 2, 'Overweight': 3, 'Obese': 4}
    category_values = [category_mapping[cat] for cat in categories]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(heights, weights, 'b-', label='Height vs Weight')
    plt.xlabel('Height (m)')
    plt.ylabel('Weight (kg)')
    plt.title('Height vs Weight')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(bmis, category_values, 'r-', label='BMI vs Category')
    plt.xlabel('BMI')
    plt.ylabel('Category')
    plt.yticks(ticks=[1, 2, 3, 4], labels=['Underweight', 'Normal weight', 'Overweight', 'Obese'])
    plt.title('BMI vs Category')
    plt.legend()

    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("BMI Calculator")
root.geometry('400x350')
root.configure(background='#f5f5f5')

style = ttk.Style()
style.configure("TLabel", background='#f5f5f5', foreground='#333', font=('Helvetica', 12))
style.configure("TButton", background='#f5f5f5', foreground='#333', font=('Helvetica', 10, 'bold'), padding=6)
style.map("TButton",
          background=[('active', '#cce7ff'), ('pressed', '#99ceff')],
          foreground=[('active', '#000'), ('pressed', '#000')])

title_frame = ttk.Frame(root, padding="10")
title_frame.pack(fill='x')

input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill='x')

result_frame = ttk.Frame(root, padding="10")
result_frame.pack(fill='x')


title_label = ttk.Label(title_frame, text="BMI Calculator", font=('Helvetica', 16, 'bold'))
title_label.pack()


height_label = ttk.Label(input_frame, text="Height (m):")
height_label.grid(row=0, column=0, pady=5)

height_entry = ttk.Entry(input_frame, width=10)
height_entry.grid(row=0, column=1, pady=5)

weight_label = ttk.Label(input_frame, text="Weight (kg):")
weight_label.grid(row=1, column=0, pady=5)

weight_entry = ttk.Entry(input_frame, width=10)
weight_entry.grid(row=1, column=1, pady=5)

calculate_button = ttk.Button(input_frame, text="Calculate", command=on_calculate)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)


result_label = ttk.Label(result_frame, text="")
result_label.pack()

category_label = ttk.Label(result_frame, text="")
category_label.pack()

graph_button = ttk.Button(result_frame, text='View Graph', command=plot_data)
graph_button.pack(pady=10)

root.mainloop()
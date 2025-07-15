import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


CURRENCIES = [
    "USD", "EUR", "GBP", "PKR", "INR", "AUD", "CAD", "CNY", "JPY", "SAR", "AED", "ZAR", "TRY", "BDT"
]


def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_cur = from_combo.get()
        to_cur = to_combo.get()

        if from_cur == "" or to_cur == "":
            raise ValueError("Currency not selected.")

        API_KEY = "47050d2a226ffdd78becf2b90db50a7e"        
        url = f"https://api.exchangeratesapi.io/v1/convert?from={from_cur}&to={to_cur}&amount={amount}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["success"]:
            result = data["result"]
            time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_label.config(text=f"{amount} {from_cur} = {result:.2f} {to_cur} \n({time_stamp})", fg="green")

           
            with open("conversion_log.txt", "a") as log:
                log.write(f"{time_stamp} | {amount} {from_cur} => {result:.2f} {to_cur}\n")
        else:
            raise ValueError("API response error.")

    except ValueError as ve:
        result_label.config(text=f"❌ {ve}", fg="red")
    except requests.exceptions.RequestException:
        result_label.config(text="❌ Network Error. Check internet connection.", fg="red")


def clear_fields():
    amount_entry.delete(0, tk.END)
    from_combo.set("PKR")
    to_combo.set("USD")
    result_label.config(text="")


def on_enter(e): e.widget.config(bg="#cceeff")
def on_leave(e): e.widget.config(bg="#e6f7ff")


root = tk.Tk()
root.title("🌐 Real-Time Currency Converter")
root.geometry("420x400")
root.resizable(False, False)
root.configure(bg="#f9f9f9")


tk.Label(root, text="Currency Converter", font=("Arial", 18, "bold"), bg="#f9f9f9", fg="#333").pack(pady=10)


tk.Label(root, text="Amount:", bg="#f9f9f9").pack()
amount_entry = tk.Entry(root, font=("Arial", 12), width=30)
amount_entry.pack(pady=5)


tk.Label(root, text="From Currency:", bg="#f9f9f9").pack()
from_combo = ttk.Combobox(root, values=CURRENCIES, state="readonly")
from_combo.set("PKR")
from_combo.pack(pady=5)


tk.Label(root, text="To Currency:", bg="#f9f9f9").pack()
to_combo = ttk.Combobox(root, values=CURRENCIES, state="readonly")
to_combo.set("USD")
to_combo.pack(pady=5)


convert_btn = tk.Button(root, text="Convert", command=convert_currency, bg="#e6f7ff", font=("Arial", 11), width=20)
convert_btn.pack(pady=10)
convert_btn.bind("<Enter>", on_enter)
convert_btn.bind("<Leave>", on_leave)


clear_btn = tk.Button(root, text="Clear", command=clear_fields, bg="#ffe6e6", font=("Arial", 11), width=20)
clear_btn.pack()
clear_btn.bind("<Enter>", on_enter)
clear_btn.bind("<Leave>", on_leave)


result_label = tk.Label(root, text="", font=("Arial", 12), bg="#f9f9f9", fg="blue", wraplength=350)
result_label.pack(pady=20)

root.mainloop()

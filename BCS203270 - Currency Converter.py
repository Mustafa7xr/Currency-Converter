import tkinter as tk
import requests

# Load currency data from API
response = requests.get('https://openexchangerates.org/api/currencies.json')
currencies = response.json()

# Create GUI window
window = tk.Tk()
window.title('Currency Converter')

# Set up GUI widgets
selected_currency = tk.StringVar()
currency_menu = tk.OptionMenu(window, selected_currency, *currencies.keys())
currency_menu.pack(pady=10)
amount_label = tk.Label(window, text='Amount:')
amount_label.pack()
amount_entry = tk.Entry(window)
amount_entry.pack(pady=5)
result_label = tk.Label(window, text='')
result_label.pack(pady=10)

# Define conversion function
def convert_currency():
    try:
        amount = float(amount_entry.get())
    except ValueError:
        result_label.config(text='Error: Enter a valid number')
        return

    base_currency = selected_currency.get()
    target_currency = 'EUR'
    api_url = f'https://openexchangerates.org/api/latest.json?app_id=c49e0a9b7dbb45a388eedd7acd587390&base={base_currency}&symbols={target_currency}'

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        if 'error' in data:
            result_label.config(text=f'Error: {data["description"]}')
        else:
            exchange_rate = data['rates'][target_currency]
            converted_amount = amount * exchange_rate
            result_label.config(text=f'{converted_amount:.2f} {target_currency}')
    else:
        result_label.config(text='Error: API request failed')

# Set up GUI button for conversion
convert_button = tk.Button(window, text='Convert', command=convert_currency)
convert_button.pack(pady=5)

# Set up GUI button to reset form
def reset_form():
    amount_entry.delete(0, tk.END)
    selected_currency.set('USD')
    result_label.config(text='')

reset_button = tk.Button(window, text='Reset', command=reset_form)
reset_button.pack(pady=5)

# Run the GUI
window.mainloop()

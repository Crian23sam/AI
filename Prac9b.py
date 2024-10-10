import tkinter as tk
from tkinter import messagebox

class DistributiveLawApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Distributive Law Demonstration")

        self.label1 = tk.Label(master, text="Enter a number (a):")
        self.label1.grid(row=0, column=0, padx=5, pady=5)

        self.a_entry = tk.Entry(master)
        self.a_entry.grid(row=0, column=1, padx=5, pady=5)

        self.label2 = tk.Label(master, text="Enter an expression (b + c):")
        self.label2.grid(row=1, column=0, padx=5, pady=5)

        self.expression_entry = tk.Entry(master)
        self.expression_entry.grid(row=1, column=1, padx=5, pady=5)

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(master, text="", fg="blue")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=5)

    def calculate(self):
        try:
            a = float(self.a_entry.get())
            expression = self.expression_entry.get()

            # Split the expression into parts and evaluate them
            b, c = map(float, expression.split('+'))

            # Apply the Distributive Law
            result = a * (b + c)
            distributed_result = (a * b) + (a * c)

            self.result_label.config(text=f"{a}({b} + {c}) = {result}\n"
                                           f"Applying Distributive Law: {a}*{b} + {a}*{c} = {distributed_result}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in both fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DistributiveLawApp(root)
    root.mainloop()

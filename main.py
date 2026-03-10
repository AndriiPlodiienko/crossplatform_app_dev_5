import tkinter as tk


class ModelApp:
    def __init__(self):
        self.state = {}

    def set_value(self, key, val):
        self.state[key] = val
        self.notify()

    def clear(self):
        self.state = {}
        self.notify()

    def get_state(self):
        return self.state.copy()


class WaterEntry(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Кількість склянок води (лише числа)")

        self.entry = tk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.vcmd), "%P"),
            invalidcommand=self.register(self.invcmd)
        )
        self.entry.pack(fill="x")

        self.button = tk.Button(self, text="OK", command=self.handle_press)
        self.button.pack(fill="x")

    def vcmd(self, proposed):
        return proposed.isdecimal() or proposed == ""

    def invcmd(self):
        self.bell()

    def handle_press(self):
        self.on_press(self.entry.get())

    def clear(self):
        self.entry.delete(0, tk.END)


class FoodEntry(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Назва страви (повинна містити 'а')")

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")

        self.entry.bind("<KeyRelease>", self.on_release)

        self.button = tk.Button(self, text="OK", command=self.handle_press)
        self.button.pack(fill="x")

    def on_release(self, e):
        val = self.entry.get().lower()
        valid = "а" in val

        self.entry.config(bg="white" if valid or val == "" else "red")
        self.button.config(state="normal" if valid else "disabled")

    def handle_press(self):
        self.on_press(self.entry.get())

    def clear(self):
        self.entry.delete(0, tk.END)
        self.entry.config(bg="white")
        self.button.config(state="normal")


class MealEntry(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Кількість прийомів їжі (1–6)")

        self.var = tk.StringVar()
        self.var.trace_add("write", self.on_trace)

        self.entry = tk.Entry(self, textvariable=self.var)
        self.entry.pack(fill="x")

        self.button = tk.Button(self, text="OK", command=self.handle_press)
        self.button.pack(fill="x")

    def on_trace(self, *args):
        val = self.var.get()

        if val.isdecimal():
            num = int(val)
            valid = 1 <= num <= 6
        else:
            valid = False

        if val == "":
            valid = True

        self.entry.config(bg="white" if valid else "red")
        self.button.config(state="normal" if valid else "disabled")

    def handle_press(self):
        self.on_press(self.var.get())

    def clear(self):
        self.var.set("")
        self.entry.config(bg="white")
        self.button.config(state="normal")


class ViewApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="x")

        self.widgets = {
            "water": WaterEntry(self),
            "food": FoodEntry(self),
            "meals": MealEntry(self)
        }

        for w in self.widgets.values():
            w.pack(fill="x", pady=5)

        self.clear_btn = tk.Button(self, text="Очистити")
        self.clear_btn.pack(fill="x")

        self.label = tk.Label(self, bg="white", justify="left")
        self.label.pack(fill="x")

    def set_label(self, text):
        self.label.config(text=text)

    def clear_fields(self):
        for w in self.widgets.values():
            w.clear()


class ControllerApp:
    def __init__(self, root):
        self.model = ModelApp()
        self.view = ViewApp(root)

        self.model.notify = self.update_view

        for key, widget in self.view.widgets.items():
            widget.on_press = lambda v, k=key: self.on_press(k, v)

        self.view.clear_btn.config(command=self.clear)

    def on_press(self, key, val):
        self.model.set_value(key, val)

    def clear(self):
        self.model.clear()
        self.view.clear_fields()

    def update_view(self):
        self.view.set_label(str(self.model.get_state()))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Опитувальник: Харчові звички - variant - 5")

    app = ControllerApp(root)

    root.mainloop()
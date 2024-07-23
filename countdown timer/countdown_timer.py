import tkinter as tk
from tkinter import messagebox
import time
import threading

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        
        self.label = tk.Label(root, text="Enter time in seconds:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Helvetica", 14))
        self.entry.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Timer", command=self.start_timer, font=("Helvetica", 14))
        self.start_button.pack(pady=10)
        
        self.time_display = tk.Label(root, text="", font=("Helvetica", 20))
        self.time_display.pack(pady=20)

        self.stop_event = threading.Event()

    def start_timer(self):
        try:
            self.seconds = int(self.entry.get())
            self.time_display.config(text=self.format_time(self.seconds))
            self.stop_event.clear()
            threading.Thread(target=self.countdown).start()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number of seconds.")

    def countdown(self):
        while self.seconds > 0 and not self.stop_event.is_set():
            self.seconds -= 1
            self.time_display.config(text=self.format_time(self.seconds))
            time.sleep(1)

        if self.seconds == 0:
            messagebox.showinfo("Time's up", "The countdown has finished!")

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"

    def stop(self):
        self.stop_event.set()

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()

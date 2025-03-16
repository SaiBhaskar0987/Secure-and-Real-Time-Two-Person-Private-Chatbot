import socket
import threading
import tkinter as tk
from tkinter import ttk

# Function to handle sending messages
def send_message():
    user_input = entry.get().strip()
    if user_input:
        s.send(user_input.encode())
        display_message(user_input, "right")
        entry.delete(0, tk.END)

# Function to display messages in the chat window
def display_message(message, alignment):
    if alignment == "right":
        bg_color = "#DCF8C6"
        anchor = "e"
    else:
        bg_color = "#ECECEC"
        anchor = "w"
    message_frame = tk.Frame(chat_frame, bg="lightgray")
    message_frame.pack(anchor=anchor, pady=5, padx=10)

    message_label = tk.Label(
        message_frame,
        text=message,
        bg=bg_color,
        fg="black",
        padx=10,
        pady=5,
        wraplength=250,
        justify="left",
        font=("Arial", 10)
    )
    message_label.pack()
    chat_canvas.update_idletasks()
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
    chat_canvas.yview_moveto(1.0)

def receive_messages():
    while True:
        try:
            message = s.recv(1024).decode()
            if message:
                display_message(message, "left")
        except:
            print("Connection closed")
            break

def on_closing():
    s.close()
    root.destroy()

def insert_emoji(emoji):
    entry.insert(tk.END, emoji)

root = tk.Tk()
root.title("Client Chat")
root.geometry("500x600")

main_frame = tk.Frame(root, bg="lightgray")
main_frame.pack(fill=tk.BOTH, expand=True)

chat_canvas = tk.Canvas(main_frame, bg="lightgray")
chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=chat_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_canvas.configure(yscrollcommand=scrollbar.set)
chat_canvas.bind(
    "<Configure>",
    lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))
)

chat_frame = tk.Frame(chat_canvas, bg="lightgray")
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
entry_frame = tk.Frame(root, bg="white")
entry_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(entry_frame, width=30, font=("Arial", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

emoji_button = tk.Button(entry_frame, text="😊", command=lambda: insert_emoji("😊"))
emoji_button.pack(side=tk.LEFT, padx=5, pady=5)

send_button = tk.Button(entry_frame, text="Send", command=send_message, bg="#25D366", fg="white", font=("Arial", 12))
send_button.pack(side=tk.RIGHT, padx=5, pady=5)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12345))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
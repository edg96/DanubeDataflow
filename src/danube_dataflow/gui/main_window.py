import tkinter as tk

from ..models.Deputy import save_deputies_to_postgres
from ..models.Senators import save_senators_to_postgres


def run_both_functions():
    """Execute both save functions"""
    print("Starting to save deputies...")
    save_deputies_to_postgres()
    print("Deputies saved!")

    print("Starting to save senators...")
    save_senators_to_postgres()
    print("Senators saved!")


root = tk.Tk()
root.title("Danube Dataflow GUI")
root.geometry("800x600")

label = tk.Label(root, text="Welcome to Danube Dataflow GUI", font=("Arial", 16))
label.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

deputy_button = tk.Button(
    button_frame,
    text="Save Deputies Only",
    command=save_deputies_to_postgres,
    width=20,
    height=2,
)
deputy_button.pack(pady=10)

senator_button = tk.Button(
    button_frame,
    text="Save Senators Only",
    command=save_senators_to_postgres,
    width=20,
    height=2,
)
senator_button.pack(pady=10)

both_button = tk.Button(
    button_frame,
    text="Save Both",
    command=run_both_functions,
    width=20,
    height=2,
    bg="green",
    fg="white",
)
both_button.pack(pady=10)

root.mainloop()

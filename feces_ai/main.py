import tkinter as tk
import sys
import time
import os
import random
import platform
import pygame
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

system_name = platform.system()
default_motivation="Every night, I lay down my feces, ready to rise again."
motivation=default_motivation
death=int(os.getenv("STAMP_OF_DEATH"))
wrap_length = 740
fontbase = 20
btnsize = 100
# Store the last updated date
last_date = time.strftime("%d.%m.%Y")
refresh = False
temperature = 1.0
windowed = len(sys.argv) > 1 and sys.argv[1] == "windowed"
words = "\"feces\",\"turd\",\"fecal matter\",\"sludge\",\"excrement\""
questionIndex = 0

def get_motivation():
    global temperature
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        sys_instruct="You are an AI that generates creative, spicy, hilarious, thought-provoking, and inspiring quotes. The quotes might even rhyme occasionally. You respond with the quote only"
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            config=types.GenerateContentConfig(system_instruction=sys_instruct,max_output_tokens=100,temperature=temperature),
            contents="Give me a feces themed quote, avoid using the word \"toilet\""
        )
        answer = response.text.replace('"', '').replace('\n', '')
        return answer
    except Exception as e:
        print("Error: " + str(e))
        return default_motivation

def refresh_motivation():
    global refresh
    refresh = True


def save_motivation():
    global temperature
    """Save the current motivation to a local file and disable the button."""
    with open("saved_motivation.txt", "a") as file:
        file.write(motivation+":"+str(round(temperature, 2))+"\n")
    save_button.config(state="disabled", bg='dim gray')  # Disable button after saving
    pygame.mixer.init()
    index = int(random.uniform(0,18.99))
    pygame.mixer.Sound("sounds/long_fart-"+str(index)+".mp3").play()

def update_time():
    global last_date, motivation, refresh, temperature, fontbase
    current_date = time.strftime("%d.%m.%Y")
    current_time = time.strftime("%H:%M:%S")
    days_left = int((death - int(time.time())) / 86400)

    date_label.config(text=current_date)
    time_label.config(text=current_time)
    days_label.config(text=str(days_left) + "💀")
    # Check if the day has changed
    if (current_date != last_date) or refresh:
        last_date = current_date
        motivation = get_motivation()
        temperature = random.uniform(0.8, 1.5)
        #questionIndex = int(random.uniform(0, len(questions)));
        size = fontbase*2
        if len(motivation) > 60:
            size = int(fontbase*3/2)
        elif len(motivation) > 100:
            size = fontbase
        print("temp:"+str(temperature))
        motivation_label.config(text=motivation, font=("Arial", size))
        save_button.config(state="active", bg='linen')
        refresh = False
    root.after(1000, update_time)  # Update every second

# Initialize the main window
root = tk.Tk()
root.title("Text Changer App")
# Check for windowed mode argument
print("system:"+system_name)
if windowed:
    root.geometry("1600x960")
    wrap_length = wrap_length*2
else:
    root.attributes('-fullscreen', True)

if system_name == "Darwin":
    fontbase = 30
    wrap_length = 1000

root.configure(bg='black')

# Create a frame to hold date and days labels side by side
top_frame = tk.Frame(root, bg='black')
top_frame.pack(fill="x", padx=fontbase*2, pady=fontbase)  # Expand across width

# Create and pack the date label inside the frame
date_label = tk.Label(top_frame, font=("Arial", fontbase*2), bg='black', fg='white')
date_label.pack(side="left")

# Create and pack the days left label inside the frame
days_label = tk.Label(top_frame, font=("Arial", fontbase*2), bg='black', fg='white')
days_label.pack(side="right")

# Create and pack the time label
time_label = tk.Label(root, font=("Arial", fontbase*4), bg='black', fg='white')
time_label.pack()

# Motivation frame to hold text and buttons
motivation_frame = tk.Frame(root, bg='black')
# Configure grid layout
motivation_frame.grid_columnconfigure(0, weight=1)  # Left side expands
motivation_frame.grid_columnconfigure(1, weight=0)  # Right side fixed
motivation_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
motivation_frame.pack(fill="x", expand=True)  # Expand to fill window

motivation_label = tk.Label(motivation_frame, font=("Arial", fontbase*2), bg='black', fg='white', wraplength=wrap_length, justify="center")
motivation_label.config(text=motivation)
motivation_label.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
update_time()

motivation_frame_buttons = tk.Frame(motivation_frame, bg='black', width=btnsize)
motivation_frame_buttons.grid(row=0, column=1, sticky="ns", padx=(5, 10), pady=10)
motivation_frame_buttons.grid_propagate(False)  # Prevent frame from resizing

refresh_button = tk.Button(motivation_frame_buttons, text="🔄", font=("Arial", fontbase*2), command=refresh_motivation,  bg='linen', fg='white')
refresh_button.pack(fill="x", pady=20, padx=20)

save_button = tk.Button(motivation_frame_buttons, text="👍🏾", font=("Arial", fontbase*2), command=save_motivation,  bg='linen', fg='white')
save_button.pack(fill="x", pady=20, padx=20)
# Close app when Escape key is pressed
root.bind("<Escape>", lambda event: root.destroy())
# Run the application
root.mainloop()
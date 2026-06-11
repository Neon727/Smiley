import tkinter as tk
import pyttsx3
import threading
import os
import time

# 4 days converted to seconds (4 days * 24 hours * 60 mins * 60 secs)
FOUR_DAYS_IN_SECONDS = 345600
TIMESTAMP_FILE = "start_time.txt"
      

class DesktopCompanion:
    def __init__(self, root):
        self.root = root
        self.name = "Smiley"
        
        # Configure the window to be borderless and always on top
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Make the background transparent (works on Windows)
        self.root.config(bg='gray')
        self.root.attributes("-transparentcolor", 'gray')
        
        # Set window size and initial position on screen
        self.width = 200
        self.height = 200
        self.root.geometry(f"{self.width}x{self.height}+500+300")
        
        # Initialize the offline Text-to-Speech engine
        self.tts_engine = pyttsx3.init()
        
        # Create a visual placeholder for Smiley (a simple canvas)
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='gray', highlightthickness=0)
        self.canvas.pack()
        
        # Draw a basic face placeholder (Replace this later with a photo/GIF)
        self.canvas.create_oval(50, 50, 150, 150, fill="yellow", outline="black", width=3)
        self.canvas.create_oval(75, 80, 90, 95, fill="black")
        self.canvas.create_oval(110, 80, 125, 95, fill="black")
        self.canvas.create_arc(75, 100, 125, 130, start=0, extent=-180, style=tk.ARC, width=3)
        
        # Make the window draggable with the mouse
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        
        # Bind a double-click to trigger a greeting voice line
        self.canvas.bind("<Double-Button-1>", lambda event: self.speak_async("Hello. I am Smiley."))

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def speak_async(self, text):
        # Run TTS in a background thread so the window doesn't freeze while speaking
        def target():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        threading.Thread(target=target, daemon=True).start()
   
    def four_days():
      if not os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "w") as f:
          f.write(str(time.time()))
    
    
# Step 2: If it does exist, check if 4 days have passed
      else:
        with open(TIMESTAMP_FILE, "r") as f:
          start_time = float(f.read())
        
          current_time = time.time()
    
      if current_time - start_time >= FOUR_DAYS_IN_SECONDS:
        speak_async("It is time.")
        # INSERT YOUR DELAYED CODE HERE
        
        # Clean up the file so it can reset next time
        os.remove(TIMESTAMP_FILE)
      else:
        remaining_seconds = FOUR_DAYS_IN_SECONDS - (current_time - start_time)
        remaining_days = remaining_seconds / 86400

  if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopCompanion(root)
    root.mainloop()

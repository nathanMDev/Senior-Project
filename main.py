import tools.cleanup as cleanup, tools.process as process, tools.transcribe_local as transcribe_local, gui.gui as gui
import json, tkinter as tk

def transcribe_audio(model_size, folder):
    for i in range(0, 6):
        filename = f"./data/videos/{folder}/{i}.m4a"
        print(f"~~~~~~~~~~\n Transcribing {filename}...\n")
        result = transcribe_local.transcribe(filename, model_size)
        process.write_to_file(f"./data/processed/{folder}/{i}.json", json.dumps(result))
        print(f"Transcription result: {json.dumps(result['text'])[:100]} \n~~~~~~~~~~ \nEND\n~~~~~~~~~~~")

def main():
    """
    Main function.
    """
    # Transcribe audio from 1-5.mp3
    #transcribe_audio("medium", "kyle")
    # Extract messages
    #messages = cleanup.save_messages_csv(cleanup.extract_messages_csv("./data/preprocessed/goobahahhgoobah.csv"))
    # Print messages
    #for username, text in messages:
    #    if cleanup.filter_profanity(text) and cleanup.filter_unnecessary_content(text):
    #        text = f"{username}: {text}\n"
    #        write_to_file("./data/processed/messages.txt", text)
    
    # create GUI instance
    root = tk.Tk()
    chatroom = gui.ChatroomGUI(root)
    root.mainloop()
        
if __name__ == "__main__":
    main()

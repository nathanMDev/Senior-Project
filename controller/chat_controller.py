# ./controller/chat_controller.py
from .base_controller import BaseController
import json
import os

class ChatController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.chat_gui.set_controller(self)
        self.token_count = 0

    def send_message(self, user, bot, message):
        if message.strip() == "":
            return

        message = message.replace('\n', ' ')

        #Chat History from the gui
        chat_history = self.chat_gui.get_chat_history()

        # Pass the selected_classes from the GUI to the get_bot_response method
        response = self.get_bot_response(bot, chat_history)

        self.append_response_to_json_file(message = message, is_assistant= 0, file_path="./model/history/nathan_history.json")
        return response

    def get_bot_response(self, bot, chat_history):

        agent = self.model.agents.get(bot.lower())
        
        if bot == "All":
            response, chat_history = self.get_response_all(chat_history)
        
        response, tokens = self.model.get_response(agent, chat_history)
        self.token_count = self.token_count + tokens[0]
        chat_history.append({'role': 'assistant', 'content': f"{response}"})

        self.append_response_to_json_file(message =response, is_assistant= 1, file_path = './model/history/nathan_history.json')

        return response

    def append_response_to_json_file(self, message, is_assistant, file_path):
        is_assistant = bool(is_assistant)
        if is_assistant == 0:
            entry = {
                "role": "user",
                "content": message
            }
        else:
            entry = {
                "role": "assistant",
                "content": message
            }

        # Check if the file exists and create it if it doesn't
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('[\n')

        # Read the existing content of the file
        with open(file_path, 'r') as f:
            data = f.readlines()

        # If there is already content in the file, add a comma after the last JSON object
        if len(data) > 1:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'r+') as f:
                f.seek(file_size - 2)
                f.write(',\n')

        # Append the entry as a JSON string followed by a newline character
        with open(file_path, 'a') as f:
            json_entry = json.dumps(entry, indent=2)
            f.write(json_entry + "\n]")

    #TODO
    def get_response_all(self,history):
        """
            Get Responses from all agents and formats them into a chat history list
            
            *args:
            history: list of chat history
            
            *returns:
            updated history in this format {'role':'user', 'content':f"{user}: {message}"}
        """
        user_list = ['nathan', 'ali', 'jett', 'kate', 'robby', 'cat'] #add more users here
        responses = []
        #Get responses from all agents
        for user in user_list:
            response, tokens = self.model.get_response(user, history)
            self.token_count += tokens # type: ignore
            history.append({'role':'assistant', 'content':f"{user}: {response}"})
            
        #Update history
        history = [*history, *responses]
        
        # Clean up responses for display
        for response in responses:
            response['content'] = response['content'].replace('{user}:', '')
        
        return responses, history

    def close_app(self):
        #called from the gui
        #self.model.save_history()
        self.on_exit()

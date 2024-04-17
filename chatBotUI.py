import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
import chatbot
import json

class ChatUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot UI")

        # Create channel list
        self.channel_list = tk.Listbox(master, width=20)
        self.channel_list.pack(side=tk.LEFT, fill=tk.Y)

        # Create message display area
        self.message_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.message_display.pack(expand=True, fill=tk.BOTH)

        # Create message input field
        self.message_input = tk.Entry(self.master)
        self.message_input.pack(side=tk.BOTTOM, fill=tk.X)
        self.message_input.bind("<Return>", self.send_message)

        # Variable to store the selected chat's name
        self.selected_chat = 'new chat'


        self.loadChats()

    def loadChats(self):
        # Clear existing chats from the Listbox
        self.channel_list.delete(0, tk.END)

        # Add some sample channels
        file = open('chatCodes.txt', 'r')
        lines = file.readlines()  # Read all lines from the file
        file.close()  # Close the file after reading

        # Split each line whenever there's a newline character
        self.channels = ['new chat']
        for line in lines:
            parts = [part for part in line.split('\n') if part.strip()]
            for part in parts:
                self.channels.append(part)
            
        for channel in self.channels:
            self.channel_list.insert(tk.END, channel)

        # Bind right-click event to channel list
        self.channel_list.bind("<Button-3>", self.popup_menu)

    
        # Bind selection event to channel list
        self.channel_list.bind("<Button-1>", self.select_chat)

    def loadChatInfo(self, chatKey):
        file_path = "chatHistory\\" + chatKey + ".txt"
        file = open(file_path, 'r')
        lines = file.readlines()  # Read all lines from the file
        file.close()

        for line in lines:
            lineInfo = line.split('|')
            message = lineInfo[1].strip()
            self.display_message(lineInfo[0], message)
        

    def clear_chat_display(self):
        self.message_display.configure(state=tk.NORMAL)
        self.message_display.delete('1.0', tk.END)
        self.message_display.configure(state=tk.DISABLED)
    
    def send_message(self, event):
        message = self.message_input.get()
            
        self.display_message("You", message)
        # For demo purposes, let's simulate a bot response
        if(self.selected_chat == "new chat"):
            response = chatbot.newChat(message)
            self.display_message("Connor Bot", response[0])
            self.message_input.delete(0, tk.END)
            self.selected_chat = response[1]
            self.loadChats()
            
            file_name = "chatHistory\\" + response[1] + '.txt'
            file = open(file_name, 'a')
            file.close()
            file = open(file_name, 'w')
            file.write("You|"+message+"\n")
            file.write("Connor Bot|"+response[0])
            file.close()
        else:
            response = chatbot.continueChat(self.selected_chat, message)
            chatKey = response[1]
            self.display_message("Connor Bot", response[0])
            self.message_input.delete(0, tk.END)
            


            file_name = "chatHistory\\" + chatKey + '.txt'
            with open(file_name, 'r') as file:
                lines = file.readlines()
            with open(file_name, 'w') as file:
                # Iterate over each line
                for line in lines:
                        file.write(line)
                file.write("You|"+message+"\n")
                file.write("Connor Bot|"+response[0])
            file.close()

            
        

    def display_message(self, sender, message):
        color = None
        if(sender == "Connor Bot"):
            color = "blue"
        else:
            color = "green"
        self.message_display.configure(state=tk.NORMAL)
        self.message_display.insert(tk.END, f"{sender}: {message}\n", color)
        self.message_display.configure(state=tk.DISABLED)
        self.message_display.see(tk.END)

    def popup_menu(self, event):
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="Delete", command=self.delete_chat)
        menu.post(event.x_root, event.y_root)

    def delete_chat(self):        
        selected_index = self.channel_list.curselection()
        if selected_index:
            # Get the text from the selected item
            selected_text = self.channel_list.get(selected_index)
            if selected_text != "new chat":
                chatbot.deleteChat(selected_text)
                # Delete the selected item from the listbox
                self.channel_list.delete(selected_index)
                # Store the selected chat's name
                self.selected_chat = selected_text

    def select_chat(self, event):
        # Get the index of the selected item
        index = self.channel_list.nearest(event.y)
        # Get the text of the selected item
        self.selected_chat = self.channels[index]
        self.clear_chat_display()
        if(self.selected_chat != "new chat"):
            self.loadChatInfo(self.selected_chat)

    

if __name__ == "__main__":
    root = tk.Tk()
    chat_ui = ChatUI(root)
    root.mainloop()

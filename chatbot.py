import cohere
import os

co = cohere.Client('wzDHE5Qd32AeLEVPuu38piTWBKIstAK83IuHfF9q')

file = open('chatCodes.txt', 'a')
file.close()
if not os.path.exists('chatHistory'):
    os.makedirs('chatHistory')


def deleteChat(chatKey):
    # Open the file in read mode
    with open('chatCodes.txt', 'r') as file:
        lines = file.readlines()  # Read all lines from the file

    # Open the file in write mode to overwrite it
    with open('chatCodes.txt', 'w') as file:
        # Iterate over each line
        for line in lines:
            # Check if the line contains 'chatKey'
            if chatKey not in line:
                # If it does not contain 'chatKey', write it back to the file
                file.write(line)
    file.close()

def continueChat(chatKey, message):
    #ChatBot
    response = co.chat(
        conversation_id= chatKey,
        message=message,
        # perform web search before answering the question. You can also use your own custom connector.
        connectors=[{"id": "web-search"}],
    )
    return(response.text, chatKey)

def newChat(message):
    response = co.chat(
        message=message,
        # perform web search before answering the question. You can also use your own custom connector.
        connectors=[{"id": "web-search"}],
    )
    file = open('chatCodes.txt', 'a')
    file.write(response.generation_id+"\n")  # Write the new line of text
    file.close()  # Close the file when you're done

    #print(response.chat_history)
    return(response.text, response.generation_id)



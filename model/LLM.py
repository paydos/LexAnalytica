from langchain.schema import AIMessage, HumanMessage
from langchain.vectorstores import Pinecone
from langchain_openai import ChatOpenAI


class ExpertAgent:
    def __init__(self, api_key, model_name) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.chat_history = None
        self.chat_instance = None
        
        # Creates an instance of the ChatOpenAI class
        self._chat_instance()
            
    
    def _chat_instance(self):
        if not self.chat_instance:
            self.chat_instance = ChatOpenAI(api_key=self.api_key, model=self.model_name)
            
    def _chat_history(self, human: HumanMessage = None, gpt: AIMessage = None):
        if self.chat_history is None:
            self.chat_history = []
        if human is not None:
            if human.content == "exit":
                exit("User exited the chat")
            self.chat_history.append(human)
        if gpt is not None:
            self.chat_history.append(gpt)
    def chat(self, message):
        # Create a human message
        human_msg = HumanMessage(content=message)
        self._chat_history(human_msg)
        
        ai_message_content = self.chat_instance.invoke(self.chat_history)
        ai_message = AIMessage(content=ai_message_content.content)

        self._chat_history(ai_message)

        # Print out the conversation
        print(f"AI: {ai_message.content}")

from langchain.schema import AIMessage, HumanMessage
from langchain.vectorstores import Pinecone
from langchain_openai import ChatOpenAI


class ExpertAgent:
    def __init__(
        self,
        api_key: str = None,
        model_name: str = "gpt-4-turbo-preview",
        agent_description: str = " ",
        temperature: float = 0.7,
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.chat_history = None
        self.chat_instance = None
        self.agent_description = agent_description
        self.temperature = temperature

        # Creates an instance of the ChatOpenAI class
        self._chat_instance()

    def _chat_instance(self):
        """
        Creates an instance of ChatOpenAI and provides it with personality.
        """
        if not self.chat_instance:
            self.chat_instance = ChatOpenAI(
                api_key=self.api_key,
                model=self.model_name,
                temperature=self.temperature,
            )
            self._agent_description()

    def _chat_history(self, human: HumanMessage = None, gpt: AIMessage = None):
        if self.chat_history is None:
            self.chat_history = []
        if human is not None:
            if human.content == "exit":
                exit("User exited the chat")
            self.chat_history.append(human)
        if gpt is not None:
            self.chat_history.append(gpt)

    def _agent_description(self):
        """
        Sends a message to the bot upon instantiation to give it personality.
        Includes:
        - Description of the bot
        """

        agent_description = f"""
        {self.agent_description} 
        """

        if self.chat_instance:
            self.chat(agent_description)
        else:
            raise "The chat_instance had an error"

    def chat(self, message):
        # Create a human message
        human_msg = HumanMessage(content=message)
        self._chat_history(human_msg)

        ai_message_content = self.chat_instance.invoke(self.chat_history)
        ai_message = AIMessage(content=ai_message_content.content)

        self.ai_message = ai_message

        self._chat_history(ai_message)

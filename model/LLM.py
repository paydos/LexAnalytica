from typing import List

from langchain.schema import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from nltk import word_tokenize

from model import FusionRAG


class ExpertAgent:
    """Represents an expert agent that interacts with users and generates responses using a language model."""

    def __init__(
        self,
        fusion_rag: FusionRAG = None,
        api_key: str = None,
        model_name: str = "gpt-4-turbo",
        agent_description: str = " ",
        temperature: float = 0.7,
    ) -> None:
        """Initializes the expert agent with the given parameters.

        Args:
            fusion_rag (FusionRAG, optional): The FusionRAG model instance. Defaults to None.
            api_key (str, optional): The API key for accessing the language model. Defaults to None.
            model_name (str, optional): The name of the language model. Defaults to "gpt-4-turbo".
            agent_description (str, optional): A description of the agent's personality. Defaults to " ".
            temperature (float, optional): The temperature for generating responses. Defaults to 0.7.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.chat_history = None
        self.enhanced_chat_history = None
        self.chat_instance = None
        self.agent_description = agent_description
        self.temperature = temperature
        self.fusion_rag = fusion_rag
        self.status = ""
        self._chat_instance()

    def _chat_instance(self):
        """Creates an instance of ChatOpenAI and initializes it with the agent's personality."""
        if not self.chat_instance:
            self.chat_instance = ChatOpenAI(
                api_key=self.api_key,
                model=self.model_name,
                temperature=self.temperature,
            )
            self._agent_description()

    def _enhanced_chat_history(self, human: HumanMessage = None, gpt: AIMessage = None):
        """Updates the enhanced chat history with messages from the human user and the AI.

        Args:
            human (HumanMessage, optional): The message from the human user. Defaults to None.
            gpt (AIMessage, optional): The message from the AI. Defaults to None.
        """
        if self.enhanced_chat_history is None:
            self.enhanced_chat_history = []

        if human is not None:
            if human.content == "exit":
                exit("User exited the chat")
            self.enhanced_chat_history.append(human)

        if gpt is not None:
            self.enhanced_chat_history.append(gpt)

    def _chat_history(self, human: HumanMessage = None, gpt: AIMessage = None):
        """Updates the chat history with messages from the human user and the AI.

        Args:
            human (HumanMessage, optional): The message from the human user. Defaults to None.
            gpt (AIMessage, optional): The message from the AI. Defaults to None.
        """
        if self.chat_history is None:
            self.chat_history = []
        if human is not None:
            if human.content == "exit":
                exit("User exited the chat")
            self.chat_history.append(human)

        if gpt is not None:
            self.chat_history.append(gpt)

    def _agent_description(self):
        """Sends a message to the chat instance to define the agent's personality."""
        agent_description = f"{self.agent_description}"

        if self.chat_instance:
            self.chat(agent_description, rag=False, status=None)
        else:
            raise Exception("The chat_instance had an error")

    def _augment_prompt(self, status, human_msg: str):
        """Augments the prompt with additional context from the FusionRAG model.

        Args:
            status: The current status of the operation.
            human_msg (str): The message from the human user.

        Returns:
            str: The augmented prompt.
        """
        documents = self.fusion_rag.fusion_rag(self.chat_instance, human_msg, status)
        documents_processed = "\n".join([x.page_content for x in documents])

        augmented_prompt = f"""
        Instruciones del asistente de inteligencia artificial: {self.agent_description}.
        Pregunta:{human_msg}.

        Contexto:
        {documents_processed}
        """
        return augmented_prompt

    def chat(
        self,
        message,
        status,
        count=0,
        total_count=0,
        rag: bool = True,
    ):
        """Processes a chat message, generates a response, and updates the chat history.

        Args:
            message: The message to process.
            status: The current status of the operation.
            count (int, optional): The current count of processed messages. Defaults to 0.
            total_count (int, optional): The total count of messages to process. Defaults to 0.
            rag (bool, optional): Whether to use RAG for generating responses. Defaults to True.
        """
        if rag:
            if hasattr(status, "update"):
                status.update(
                    label=f"Generando ramas de conocimiento para la pregunta {count+1} de {total_count} ",
                    state="running",
                    expanded=True,
                )
            augmented_message = self._augment_prompt(status=status, human_msg=message)
            augmented_message = HumanMessage(content=augmented_message)

            message = HumanMessage(content=message)

            self._enhanced_chat_history(augmented_message)
            self._chat_history(message)
        else:
            message = HumanMessage(content=message)
            self._chat_history(message)
            self._enhanced_chat_history(message)
        if hasattr(status, "update"):
            status.update(
                label=f"Generando respuesta para la pregunta {count+1} de {total_count}",
                state="running",
                expanded=False,
            )

        ai_message_content = self.chat_instance.invoke(self.enhanced_chat_history)
        ai_message = AIMessage(content=ai_message_content.content)

        self.ai_message = ai_message
        if rag:
            if hasattr(status, "update"):
                status.update(
                    label="Respuesta generada",
                    state="complete",
                    expanded=True,
                )

        self._chat_history(ai_message)
        self._enhanced_chat_history(ai_message)
        self._controlTokenUsage()

    def _controlTokenUsage(self):
        """Controls the token usage by truncating the chat history when it exceeds a certain length."""
        chat_history_text = " ".join(
            [message.content for message in self.enhanced_chat_history]
        )
        tokens = len(word_tokenize(text=chat_history_text, language="spanish"))
        print(f"WINDOW LENGTH: {(tokens)}")
        if tokens > 70000:
            print(f"LENGTH EXCEEDED. TOTAL LENGTH: {tokens}")
            self.enhanced_chat_history = []
            self.enhanced_chat_history.append(
                HumanMessage(content=self.agent_description)
            )
            self.enhanced_chat_history.append(AIMessage(content=" "))

            new_chat_history_text = " ".join(
                [message.content for message in self.enhanced_chat_history]
            )

            print(
                f"LENGTH RESET. NEW LENGTH: {len(word_tokenize(text=new_chat_history_text, language='spanish'))}"
            )

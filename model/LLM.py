from typing import List

from langchain.schema import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from model import FusionRAG


class ExpertAgent:
    def __init__(
        self,
        fusion_rag: FusionRAG = None,
        api_key: str = None,
        model_name: str = "gpt-4-turbo-preview",
        agent_description: str = " ",
        temperature: float = 0.7,
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.chat_history = None
        self.enhanced_chat_history = None
        self.chat_instance = None
        self.agent_description = agent_description
        self.temperature = temperature
        self.fusion_rag = fusion_rag
        self.status = ""
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

    def _enhanced_chat_history(self, human: HumanMessage = None, gpt: AIMessage = None):
        if self.enhanced_chat_history is None:
            self.enhanced_chat_history = []

        if human is not None:
            if human.content == "exit":
                exit("User exited the chat")
            self.enhanced_chat_history.append(human)

        if gpt is not None:
            self.enhanced_chat_history.append(gpt)

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
            self.chat(agent_description, rag=False, status=None)
        else:
            raise "The chat_instance had an error"

    def _augment_prompt(self, human_msg: str):
        documents = self.fusion_rag.fusion_rag(self.chat_instance, human_msg)
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
        # Create a human message
        if rag:
            if hasattr(status, "update"):
                status.update(
                    label=f"Generando ramas de conocimeinto para la pregunta {count+1} de {total_count} ",
                    state="running",
                    expanded=False,
                )
            augmented_message = self._augment_prompt(message)
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
                    expanded=False,
                )

        self._chat_history(ai_message)
        self._enhanced_chat_history(ai_message)

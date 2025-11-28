"""Simple LLM Chatbot Implementation"""

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Load environment variables from examples/.env
load_dotenv(".env")


class SimpleChatbot:
    """Simple chatbot using LangChain"""

    def __init__(self, model: str = "gpt-4.1-mini", temperature: float = 0.7):
        """
        Initialize chatbot

        Args:
            model: OpenAI model to use
            temperature: Response randomness (0.0-1.0)
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.chat_history: list = []

        # Set system message
        system_message = SystemMessage(
            content=(
                "あなたは親切で友好的なAIアシスタントです。"
                "明確で正確、かつ簡潔な回答を提供してください。"
                "質問に答える際は、情報量がありながらも会話的な口調を心がけてください。"
                "不確かなことがある場合は、正直にそう伝えてください。"
            )
        )
        self.chat_history.append(system_message)

    def chat(self, user_input: str) -> str:
        """
        Respond to user input

        Args:
            user_input: Message from user

        Returns:
            AI response
        """
        # Add user message to history
        self.chat_history.append(HumanMessage(content=user_input))

        # Send to LLM and get response
        response = self.llm.invoke(self.chat_history)

        # Add AI response to history
        self.chat_history.append(AIMessage(content=response.content))

        return response.content

    def reset(self):
        """Reset chat history"""
        system_message = SystemMessage(
            content=(
                "あなたは親切で友好的なAIアシスタントです。"
                "明確で正確、かつ簡潔な回答を提供してください。"
                "質問に答える際は、情報量がありながらも会話的な口調を心がけてください。"
                "不確かなことがある場合は、正直にそう伝えてください。"
            )
        )
        self.chat_history = [system_message]

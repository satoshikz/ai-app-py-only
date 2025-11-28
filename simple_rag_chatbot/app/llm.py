"""Simple RAG Chatbot Implementation"""

from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv(".env")


class SimpleRAGChatbot:
    """Simple RAG chatbot using LangChain and ChromaDB"""

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.7,
        data_dir: str = "simple_rag_chatbot/data",
        persist_directory: str = "simple_rag_chatbot/.chroma_db",
    ):
        """
        Initialize RAG chatbot

        Args:
            model: OpenAI model to use
            temperature: Response randomness (0.0-1.0)
            data_dir: Directory containing HTML documents
            persist_directory: Directory to persist vector database
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.embeddings = OpenAIEmbeddings()
        self.chat_history: list = []

        # Initialize or load vector store
        self.vector_store = self._initialize_vector_store(data_dir, persist_directory)

        # Set system message
        system_message = SystemMessage(
            content=(
                "あなたは親切で知識豊富なAIアシスタントです。"
                "提供された文脈情報を使用して、正確で詳細な回答を提供してください。"
                "文脈に情報がない場合は、その旨を正直に伝えてください。"
                "回答は明確で簡潔にまとめてください。"
            )
        )
        self.chat_history.append(system_message)

    def _initialize_vector_store(self, data_dir: str, persist_directory: str) -> Chroma:
        """
        Initialize vector store from HTML documents

        Args:
            data_dir: Directory containing HTML documents
            persist_directory: Directory to persist vector database

        Returns:
            Chroma vector store
        """
        persist_path = Path(persist_directory)

        # Load existing vector store if available
        if persist_path.exists() and any(persist_path.iterdir()):
            return Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings,
            )

        # Create new vector store from documents
        documents = []
        data_path = Path(data_dir)

        # Load all HTML files
        for html_file in data_path.glob("*.html"):
            loader = UnstructuredHTMLLoader(str(html_file))
            documents.extend(loader.load())

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        splits = text_splitter.split_documents(documents)

        # Create and persist vector store
        vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=persist_directory,
        )

        return vector_store

    def _get_relevant_context(self, query: str, k: int = 3) -> str:
        """
        Retrieve relevant context from vector store

        Args:
            query: User query
            k: Number of documents to retrieve

        Returns:
            Concatenated relevant context
        """
        docs = self.vector_store.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    def chat(self, user_input: str) -> str:
        """
        Respond to user input using RAG

        Args:
            user_input: Message from user

        Returns:
            AI response
        """
        # Get relevant context
        context = self._get_relevant_context(user_input)

        # Create prompt with context
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "以下の文脈情報を使用して質問に答えてください:\n\n{context}",
                ),
                ("human", "{question}"),
            ]
        )

        # Format prompt
        formatted_prompt = prompt.format_messages(context=context, question=user_input)

        # Add to chat history
        self.chat_history.append(HumanMessage(content=user_input))

        # Get response
        response = self.llm.invoke(self.chat_history[:-1] + formatted_prompt)

        # Add AI response to history
        self.chat_history.append(AIMessage(content=response.content))

        return response.content

    def reset(self):
        """Reset chat history"""
        system_message = SystemMessage(
            content=(
                "あなたは親切で知識豊富なAIアシスタントです。"
                "提供された文脈情報を使用して、正確で詳細な回答を提供してください。"
                "文脈に情報がない場合は、その旨を正直に伝えてください。"
                "回答は明確で簡潔にまとめてください。"
            )
        )
        self.chat_history = [system_message]

    def get_sources(self, query: str, k: int = 3) -> list:
        """
        Get source documents for a query

        Args:
            query: User query
            k: Number of documents to retrieve

        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(query, k=k)

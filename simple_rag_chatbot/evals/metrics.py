"""DeepEval evaluation system for RAG chatbot"""

import sys
from pathlib import Path

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

from simple_rag_chatbot.app.llm import SimpleRAGChatbot

# Load environment variables
load_dotenv(".env")

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Initialize chatbot
chatbot = SimpleRAGChatbot()

# Define metrics
answer_relevancy = AnswerRelevancyMetric(threshold=0.7)
faithfulness = FaithfulnessMetric(threshold=0.7)

# Test questions about AI knowledge
test_inputs = [
    "RAGとは何ですか？その利点を教えてください",
    "ベクトルデータベースの代表的な例を3つ挙げてください",
    "プロンプトエンジニアリングの主な手法は何ですか？",
    "ファインチューニングの種類について教えて",
    "LLMができることを5つ教えてください",
]

# Get chatbot responses and create test cases
test_cases = []
for input_text in test_inputs:
    # Get response
    output = chatbot.chat(input_text)

    # Get context (retrieval context)
    context = chatbot.get_sources(input_text, k=3)
    retrieval_context = [doc.page_content for doc in context]

    # Create test case
    test_case = LLMTestCase(
        input=input_text,
        actual_output=output,
        retrieval_context=retrieval_context,
    )
    test_cases.append(test_case)
    chatbot.reset()

# Run evaluation with evaluate()
if __name__ == "__main__":
    print("RAG Chatbot 評価を開始します...")
    print(f"テストケース数: {len(test_cases)}")
    print("-" * 50)

    evaluate(
        test_cases=test_cases,
        metrics=[answer_relevancy, faithfulness],
    )

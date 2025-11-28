"""DeepEval evaluation system"""

import sys
from pathlib import Path

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv

from simple_chatbot.app.llm import SimpleChatbot

# Load environment variables from examples/.env
load_dotenv(".env")

# Add parent directory to path to enable imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Initialize chatbot
chatbot = SimpleChatbot()

# Define metrics
answer_relevancy = AnswerRelevancyMetric(threshold=0.7)

# Test questions
test_inputs = [
    "おすすめの朝食メニューを教えてください",
    "効率的な勉強方法について教えて",
    "ストレス解消法を3つ教えてください",
    "東京のおすすめ観光スポットは？",
    "初心者向けのプログラミング言語を教えて",
]

# Get chatbot responses and create test cases
test_cases = []
for input_text in test_inputs:
    output = chatbot.chat(input_text)
    test_case = LLMTestCase(
        input=input_text,
        actual_output=output,
    )
    test_cases.append(test_case)
    chatbot.reset()

# Run evaluation with evaluate()
if __name__ == "__main__":
    evaluate(test_cases=test_cases, metrics=[answer_relevancy])

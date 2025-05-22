from typing import Union
from autogen import AssistantAgent
from src.config import LLM_CONFIG

def extract_answer(content: str, question: str) -> str:
    """Extract the answer to a question from content, or indicate if no answer exists"""
    agent = AssistantAgent(
        name="AnswerExtractorAgent",
        system_message="You are a helpful AI assistant. "
                      "You can extract answers to specific questions from content. "
                      "Given content and a question, you will either extract the answer or indicate that no answer exists. "
                      "If you find an answer, provide it clearly and concisely. "
                      "If no answer exists in the content, respond with 'NO_ANSWER_FOUND'. "
                      "Don't include any other text in your response beyond the answer or 'NO_ANSWER_FOUND'."
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )
    
    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": f'Extract the answer to this question from the content: "{question}"\n\nContent: {content}'}
        ],
    )

    if not reply:
        raise ValueError("No reply found")

    reply_value = ""
    if isinstance(reply, dict):
        reply_content = reply["content"]
        if reply_content:
            reply_value = reply_content
        else:
            raise ValueError("No content found in the reply")
    else:
        reply_value = reply

    return reply_value.strip()
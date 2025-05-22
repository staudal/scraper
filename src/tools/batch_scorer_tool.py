import re
from typing import Union, Literal
from autogen import AssistantAgent
from src.config import LLM_CONFIG, PERFECT_SCORE_THRESHOLD, GOOD_SCORE_THRESHOLD, FAIR_SCORE_THRESHOLD, POOR_SCORE_THRESHOLD

def score_batch_relevance(content: str, question: str) -> int:
    """Score how well a content batch answers the given question (1-100)"""
    agent = AssistantAgent(
        name="BatchScorerAgent",
        system_message="You are a helpful AI assistant that scores content relevance to questions. "
                      "You analyze content and provide a single numeric score (1-100) indicating how well "
                      "it answers a specific question. No explanations, only the number.",
        llm_config=LLM_CONFIG,
    )
    
    prompt = f"""Question: {question}

Content to analyze:
{content}

Score how well this content answers the question on a scale of 1-100 where:
- {PERFECT_SCORE_THRESHOLD} = Content directly and completely answers the question
- {GOOD_SCORE_THRESHOLD}-{PERFECT_SCORE_THRESHOLD-1} = Content partially answers with relevant information
- {FAIR_SCORE_THRESHOLD}-{GOOD_SCORE_THRESHOLD-1} = Content has some relevance but doesn't clearly answer
- {POOR_SCORE_THRESHOLD}-{FAIR_SCORE_THRESHOLD-1} = Content has little to no relevance to the question
- 1-{POOR_SCORE_THRESHOLD-1} = Content is completely irrelevant

Respond with ONLY the numeric score (1-100):"""
    
    reply = agent.generate_reply(
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    # Handle different reply formats and extract the score
    if not reply:
        return 1
        
    reply_text = reply["content"] if isinstance(reply, dict) and reply.get("content") else str(reply)
    
    # Extract number from response
    numbers = re.findall(r'\d+', reply_text.strip())
    return max(1, min(100, int(numbers[0]))) if numbers else 1
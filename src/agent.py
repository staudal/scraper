from autogen import ConversableAgent
import argparse
from src.tools.web_scraper_tool import initialize_website_scraper, get_next_batch, has_more_batches
from src.tools.batch_scorer_tool import score_batch_relevance
from src.tools.answer_extractor_tool import extract_answer
from src.config import LLM_CONFIG, EARLY_TERMINATION_SCORE

def create_web_scraping_agent() -> ConversableAgent:
    # define the agent
    agent = ConversableAgent(
        name="WebScrapingAgent",
        system_message="You are a helpful AI assistant. "
                      "You can scrape websites one batch at a time to avoid token limits. "
                      "You can score how well each batch answers a user's question. "
                      "You can extract answers from the best scoring batch. "
                      "You will use the initialize_scraper tool to start scraping a website. "
                      "You will use get_batch to get one batch at a time. "
                      "You will use has_more_batches to check if there are more batches. "
                      "You will use the batch_scorer tool to score each batch's relevance to a question. "
                      "You will use the answer_extractor tool to extract answers from the highest scoring batch. "
                      "Process batches one at a time, keep track of the highest scoring batch. "
                      f"You will return the answer immediately ONLY if the score is EXACTLY OR ABOVE {EARLY_TERMINATION_SCORE}. "
                      f"If the score is less than {EARLY_TERMINATION_SCORE}, you will continue to scrape the website and score the next batch until no more batches are available."
                      "When you have processed all batches, you will return the answer from the highest scoring batch using the answer_extractor tool. "
                      "Don't include any other text in your response. "
                      "Return 'TERMINATE' when the task is done.",
        llm_config=LLM_CONFIG,
    )

    # add the tools to the agent
    agent.register_for_llm(name="initialize_scraper", description="Initialize website scraper")(initialize_website_scraper)
    agent.register_for_llm(name="get_batch", description="Get next batch from scraper")(get_next_batch)
    agent.register_for_llm(name="has_more_batches", description="Check if more batches available")(has_more_batches)
    agent.register_for_llm(name="batch_scorer", description="Score how well a batch answers a question")(score_batch_relevance)
    agent.register_for_llm(name="answer_extractor", description="Extract answer from content")(extract_answer)

    return agent

def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )
    user_proxy.register_for_execution(name="initialize_scraper")(initialize_website_scraper)
    user_proxy.register_for_execution(name="get_batch")(get_next_batch)
    user_proxy.register_for_execution(name="has_more_batches")(has_more_batches)
    user_proxy.register_for_execution(name="batch_scorer")(score_batch_relevance)
    user_proxy.register_for_execution(name="answer_extractor")(extract_answer)
    return user_proxy


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Web scraping agent for answering questions from websites')
    parser.add_argument('--url', type=str, required=True, help='URL to scrape')
    parser.add_argument('--question', type=str, required=True, help='Question to answer')
    args = parser.parse_args()
    
    user_proxy = create_user_proxy()
    web_scraping_agent = create_web_scraping_agent()
    user_proxy.initiate_chat(
        web_scraping_agent, 
        message=f"Please answer this question: '{args.question}' by scraping this URL: '{args.url}'"
    )

if __name__ == "__main__":
    main()
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from search_tools import SearchTool


SYSTEM_PROMPT_TEMPLATE = """
You are a helpful AI documentation assistant.

Use the search tool before answering questions.
Answer based on retrieved documentation whenever possible.

Always include references by mentioning the filename used.
If the retrieved documentation is not enough, clearly say that you could not find enough information.

Keep answers clear, practical, and beginner-friendly.
""".strip()


def init_agent(index, model_name="mistral:latest"):
    search_tool = SearchTool(index=index)

    ollama_model = OpenAIChatModel(
        model_name=model_name,
        provider=OpenAIProvider(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
    )

    agent = Agent(
        model=ollama_model,
        name="docs_agent_ollama",
        instructions=SYSTEM_PROMPT_TEMPLATE,
        tools=[search_tool.search]
    )

    return agent

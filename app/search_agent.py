from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from search_tools import SearchTool


SYSTEM_PROMPT_TEMPLATE = """
You are RepoGuide AI, a helpful GitHub documentation assistant.

Always use the search tool before answering questions.
Answer based on retrieved documentation whenever possible.

When answering:
- Be clear and beginner-friendly.
- Mention important steps as bullet points when useful.
- Include a "Sources used" section at the end.
- In "Sources used", list the filenames from the retrieved documentation.
- If the retrieved documentation is not enough, clearly say that you could not find enough information.

Do not pretend to know information that was not found in the documentation.
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

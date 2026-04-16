import os

from dotenv import load_dotenv

from gemini import get_client, generate_text
from parlex import fetch_parlex_context

load_dotenv()


def main() -> None:
    topic = "artificial intelligence regulation"
    mcp_context = fetch_parlex_context(topic=topic)
    print("=== Raw MCP Context ===")
    print(mcp_context)
    print("=== End MCP Context ===\n")

    if mcp_context.lower().startswith("mcp http error 403"):
        print(
            "MCP returned 403, so skipping LLM summarization until MCP auth/permissions are fixed."
        )
        return
    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is not set, so skipping LLM summarization.")
        return

    prompt = f"""
You are an assistant helping with UK parliamentary research.

Use the MCP context below in your answer. If the MCP context contains an error, explain the error briefly and suggest the next setup step.

Question: What are the most relevant recent parliamentary items on "{topic}"?

MCP context:
{mcp_context}
""".strip()

    llm_response = generate_text(prompt, client=get_client())
    print(llm_response)


if __name__ == "__main__":
    main()

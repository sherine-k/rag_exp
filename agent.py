import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

from dotenv import load_dotenv
load_dotenv()

root_agent = Agent(
    name="e2e_retrieval_agent",
    # model=LiteLlm(model="ollama_chat/qwen3:4b"),
    model="gemini-2.0-flash",
    description=("""
    Your goal is to analyze long documents for Retrieval Augmented
    Generation (RAG) by splitting the content in pieces.
    The content pieces will be the chunks that will be embedded
    thanks to an embedding model to calculate vector embedding
    to store in a vector database.

    Call the server-filesystem MCP tool to go through 
    the files in $JUNIT_FOLDER,
    containing E2E test suites results in json or 
    plain text. You must extract and format the content so that each 
    piece of content is meaningful as a standalone unit of text.

    Each piece of content should be tagged  the file path where it was found,
    as well as a list of questions whose answers can be provided
    by this piece of content.

    Go through ALL the files of the provided folder.
    The piece of text should be the exact text found in the file.
    DON'T change a single world. DON'T summarize.

    

    """)
    ,
    instruction=("""
        You are a helpful agent responsible for creating embeddings from the content of files
        and subfolders and generating a list of embeddings which you can save to a file called embeddings.json.
        Each embedding is a json object with the following fields:
        - content: the content of the file or subfolder
        - file_path: the path of the file or subfolder
        - questions: a list of questions whose answers can be provided
        by this piece of content.
         """
    ),
    tools=[MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='npx',
                    args=[
                        "-y",  # Argument for npx to auto-confirm install
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
                        # npx process can access.
                        # Replace with a valid absolute path on your system.
                        # For example: "/Users/youruser/accessible_mcp_files"
                        # or use a dynamically constructed absolute path:
                        os.getenv("JUNIT_FOLDER", os.path.abspath(os.path.join(os.getcwd(), "junit"))),
                    ],
                ),
            ),
        )],
)
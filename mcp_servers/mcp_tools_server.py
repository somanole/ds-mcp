import os
import sys
from mcp.server.fastmcp import FastMCP
from duckduckgo_search import DDGS


############## For NOTEBOOK 3_MCP_with_memory.ipynb ##############
## Uncomment the following lines to connect to Redis for the notebook exercises.

# from mcp.server.transport_security import TransportSecuritySettings
# mcp: FastMCP = FastMCP("MemoryServer", 
#                        host="127.0.0.1", 
#                        port=8000,
#                        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
#                        )


############### For NOTEBOOK 3_MCP_with_memory.ipynb ##############
## Comment this line out if you want to connect to Redis.
mcp: FastMCP = FastMCP("SuperServer")



@mcp.tool()
def search_web(query: str) -> str:
    """Searches the web for current information using DuckDuckGo."""
    sys.stderr.write(f"DEBUG: Searching web for {query}\n") # FastMCP redirects prints safely
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
        return "\n---\n".join(results) if results else "No results found."

@mcp.tool()
def read_local_file(file_path: str) -> str:
    """Reads the content of a local text file. Provide the full path."""
    if not os.path.exists(file_path):
        return f"Error: File at {file_path} not found."
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

    
if __name__ == "__main__":
    # mcp.run()
    
    ## For NOTEBOOK 3_MCP_with_memory.ipynb, use this line instead to run with SSE transport:
    # comment the above line
    
    mcp.run(transport="sse")
from mcp.server.fastmcp import FastMCP

from tools import buscar_material

mcp = FastMCP(
    "TutorPython"
)

@mcp.tool()
def pesquisar_contexto(
    pergunta: str
):

    return buscar_material(
        pergunta
    )

if __name__ == "__main__":
    mcp.run()
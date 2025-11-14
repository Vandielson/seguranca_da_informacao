from fastapi import FastAPI

app = FastAPI(
    title="Pipeline de Segurança para LLMs",
    description="PoC para aplicar controles (Firewall, RAG, RBAC) em APIs de LLM."
)

@app.get("/")
def read_root():
    return {"status": "API de Segurança de LLM está no ar!"}

# Endpoint principal que passa pelo pipeline
# @app.post("/chat")
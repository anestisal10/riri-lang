import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger
import interpreter

# Setup JSON logger
logger = logging.getLogger("riri_api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(
    title="Riri Lang execution API",
    description="Backend API to execute Riri_lang code securely.",
    version="1.0.0"
)

class ExecuteRequest(BaseModel):
    code: str
    timeout: float = 2.0  # default 2 seconds timeout

class ExecuteResponse(BaseModel):
    output: str
    status: str
    error: str = None

class AstResponse(BaseModel):
    mermaid: str
    status: str
    error: str = None

@app.post("/execute", response_model=ExecuteResponse)
async def execute_code(request: ExecuteRequest):
    logger.info(f"Received execution request.", extra={"code_length": len(request.code), "timeout": request.timeout})
    try:
        output = interpreter.run(
            request.code, 
            timeout=request.timeout, 
            capture_output=True
        )
        logger.info("Execution successful")
        return ExecuteResponse(output=output, status="success")
    
    except interpreter.TimeoutException as e:
        logger.warning(f"Execution timeout: {str(e)}")
        return ExecuteResponse(output="", status="error", error=str(e))
    except Exception as e:
        logger.error(f"Execution error: {str(e)}")
        return ExecuteResponse(output="", status="error", error=str(e))

@app.post("/ast", response_model=AstResponse)
async def generate_ast(request: ExecuteRequest):
    logger.info(f"Received AST generation request.", extra={"code_length": len(request.code)})
    try:
        mermaid_graph = interpreter.visualize_ast(request.code)
        logger.info("AST Generation successful")
        return AstResponse(mermaid=mermaid_graph, status="success")
    except Exception as e:
        logger.error(f"AST Generation error: {str(e)}")
        return AstResponse(mermaid="", status="error", error=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

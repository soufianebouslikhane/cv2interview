from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from app.schemas.models import AgentRequest
from app.agent.cv_agent import run_cv_agent, run_career_recommendation
from app.config.config import UPLOAD_DIR
from app.services.utils import save_uploaded_file
from app.tools.pdf_tool import PDFConverterTool

router = APIRouter()

# ✅ Smart wrapper for better agent prompt control
def prepare_prompt(instruction: str) -> str:
    instruction = instruction.strip()
    # If user sends raw CV, auto-wrap it
    if len(instruction) > 500 and ("Skills" in instruction or "Experience" in instruction or "Education" in instruction):
        return (
            "You are an expert technical recruiter.\n"
            "Please extract the key skills, experience, and education from the CV below.\n"
            "Then, based on that, generate exactly 15 professional interview questions.\n\n"
            f"{instruction}\n\n"
            "Return only the list of questions, clearly numbered. No explanation."
        )
    # Otherwise, use instruction as-is
    return instruction

@router.post("/chat")
async def chat_with_agent(request: AgentRequest):
    try:
        smart_prompt = prepare_prompt(request.instruction)
        response = await run_cv_agent(smart_prompt)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

@router.post("/career")
async def career_from_cv(request: AgentRequest):
    try:
        result = await run_career_recommendation(request.instruction)
        return {"recommendation": result}
    except Exception as e:
        return {"error": str(e)}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    saved_path = save_uploaded_file(file, UPLOAD_DIR)
    text = PDFConverterTool()._run(str(saved_path))

    return JSONResponse(content={
        "text": text
    })

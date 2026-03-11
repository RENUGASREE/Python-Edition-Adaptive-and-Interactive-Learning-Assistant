from fastapi import APIRouter, HTTPException
from .. import schemas

router = APIRouter()

@router.post("/run", response_model=schemas.GradeResult)
def grade_submission(req: schemas.GradeRequest):
    # WARNING: This is a placeholder. A real grader must run code in an isolated sandbox.
    # Here, we implement a dummy checker that looks for a target string for demo.
    code = req.code or ""
    if "def solve" in code:
        return {"passed": True, "score": 1.0, "feedback": "Basic function found. Write tests to validate behavior."}
    return {"passed": False, "score": 0.0, "feedback": "No solve function found. Make sure to define 'def solve(...)'"}

from fastapi import APIRouter
from .. import schemas

router = APIRouter()

@router.post("/next", response_model=list)
def recommend_next(req: schemas.RecommendRequest):
    # Placeholder: rule-based recommendations stub
    # In later iterations: replace with knowledge-tracing model + rules
    recommendations = [
        {"id": "topic-1", "title": "Variables & Types", "reason": "low mastery"},
        {"id": "topic-2", "title": "Control Flow", "reason": "prerequisite for loops"},
    ]
    return recommendations[: req.limit]

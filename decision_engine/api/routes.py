from fastapi import APIRouter
from models.schemas import UserInput
from services.retrieval import get_context
from services.llm_services import call_llm

router = APIRouter()

@router.post("/recommend")
def recommend(data: UserInput):

    # 🔹 Step 1: Convert years → category
    years = data.duration_years

    if years <= 2:
        query = "short term investment stocks"
    elif years <= 5:
        query = "medium term investment stocks"
    else:
        query = "long term investment stocks"

    # 🔹 Step 2: Retrieve context
    context = get_context(query)

    # 🔹 Step 3: Call Gemini
    result = call_llm(data, context)

    return {
        "portfolio": result if result else [],
        "context": context,
        "risk_match": data.risk
    }
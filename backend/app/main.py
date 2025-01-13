from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.feedback import Feedback
from .services.feedback_service import FeedbackService
from .services.sentiment_service import SentimentService

app = FastAPI(title="Feedback Chatbot API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

feedback_service = FeedbackService()
sentiment_service = SentimentService()

@app.post("/feedback", response_model=Feedback)
async def create_feedback(feedback: Feedback):
    try:
        # Save feedback without sentiment analysis for now
        saved_feedback = await feedback_service.save(feedback)
        return saved_feedback
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class Feedback(BaseModel):
    text: str
    feedback_type: str
    responses: Dict
    created_at: datetime = datetime.now()
    user_id: Optional[str] = None
    sentiment_score: Optional[float] = None  # Make sentiment score optional 
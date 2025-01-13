import json
import os
from typing import List
from ..models.feedback import Feedback

class FeedbackService:
    def __init__(self):
        self.feedback_file = "data/feedback.json"
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump([], f)

    async def save(self, feedback: Feedback) -> Feedback:
        try:
            with open(self.feedback_file, 'r+') as f:
                data = json.load(f)
                feedback_dict = feedback.dict()
                feedback_dict['created_at'] = feedback_dict['created_at'].isoformat()
                data.append(feedback_dict)
                f.seek(0)
                json.dump(data, f, indent=2)
                return feedback
        except Exception as e:
            raise Exception(f"Error saving feedback: {str(e)}") 
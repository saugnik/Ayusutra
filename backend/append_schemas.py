# Script to append new schemas to schemas.py

new_schemas = '''

# ==================== HEALTH SUPPORT SCHEMAS ====================
class SymptomCreate(BaseModel):
    symptom_name: str
    severity: str  # low, moderate, high, severe
    notes: Optional[str] = None
    duration_days: Optional[int] = None

class SymptomResponse(BaseSchema):
    id: int
    patient_id: int
    symptom_name: str
    severity: str
    notes: Optional[str] = None
    duration_days: Optional[int] = None
    created_at: datetime

class AIHealthRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

class AIHealthResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    conversation_id: str

class HealthRecommendation(BaseModel):
    category: str  # diet, lifestyle, herbs, therapy
    suggestion: str
    reason: str
    priority: Optional[str] = "normal"  # low, normal, high

class HealthRecommendationsResponse(BaseModel):
    recommendations: List[HealthRecommendation]
    dosha_analysis: Optional[Dict[str, Any]] = None

# ==================== CHAT SUPPORT SCHEMAS ====================
class ChatMessageCreate(BaseModel):
    recipient_id: int
    recipient_type: str  # patient or practitioner
    content: str

class ChatMessageResponse(BaseSchema):
    id: int
    sender_id: int
    sender_type: str
    recipient_id: int
    recipient_type: str
    content: str
    read: bool
    created_at: datetime

class PractitionerAvailability(BaseModel):
    id: int
    name: str
    specialization: Optional[str] = None
    online: bool
    last_seen: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class AIChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class AIChatResponse(BaseModel):
    reply: str
    conversation_id: str
'''

with open('backend/schemas.py', 'a', encoding='utf-8') as f:
    f.write(new_schemas)

print("Schemas appended successfully!")

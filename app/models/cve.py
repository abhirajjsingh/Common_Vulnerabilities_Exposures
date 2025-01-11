from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CVEBase(BaseModel):
    cve_id: str
    description: str
    published_date: datetime
    last_modified_date: datetime
    base_score_v2: Optional[float] = None
    base_score_v3: Optional[float] = None
    
class CVECreate(CVEBase):
    pass

class CVEResponse(CVEBase):
    id: str

class CVEList(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[CVEResponse]
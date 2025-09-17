from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

@dataclass
class Presentation:
    id: str = field(default_factory=lambda: str(uuid4()))
    company: str = ""
    prompt: str = ""
    slide_count: int = 5
    template: str = "general"
    branding: str = "default"
    filename: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "prompt": self.prompt,
            "slide_count": self.slide_count,
            "template": self.template,
            "branding": self.branding,
            "filename": self.filename,
            "created_at": self.created_at.isoformat()
        }

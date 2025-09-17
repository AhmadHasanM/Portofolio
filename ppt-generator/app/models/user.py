from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = "Guest"
    email: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

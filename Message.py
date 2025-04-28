from enum import Enum
from openai.types.chat import ChatCompletionMessage

class Role(Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"

class Message:
    role: Role
    content: str

    def __init__(self, role: Role, content: str):
        self.role = role
        self.content = content

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content
        }

    @classmethod
    def from_gpt_message(cls, gpt_message: ChatCompletionMessage) -> "Message":
        role = Role(value=gpt_message.role)
        return cls(role=role, content=gpt_message.content)
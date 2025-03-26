import json
from dataclasses import dataclass
from typing import List

@dataclass
class StoryScene:
    title: str
    content: str
    options: List[str]
    isStoryEnded: bool

    @staticmethod
    def from_json(json_str: str):
        data = json.loads(json_str)
        return StoryScene(
            title=data["title"],
            content=data["content"],
            options=data["options"],
            isStoryEnded=data["isStoryEnded"]
        )

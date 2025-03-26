from Message import *
from ApiService import ApiService
from StoryScene import StoryScene

class ViewModel:
    _callbacks: list[callable(StoryScene)] = []
    _is_story_ended = False
    _previous_messages: [Message] = []
    _story_scene: StoryScene

    def bind_to(self, callback: callable(StoryScene)):
        # 將視圖的回調函數綁定到模型
        self._callbacks.append(callback)

    def start_story(self):
        self._previous_messages = []
        self._send_api()

    def _send_api(self):
        response = ApiService().start_story(previous_messages=self._previous_messages)
        content = response.content
        # 紀錄 server response
        self._previous_messages.append(Message(role=Role.SYSTEM, content=content))
        self._story_scene = StoryScene.from_json(json_str=content)
        self._is_story_ended = self._story_scene.isStoryEnded
        for callback in self._callbacks:
            callback(self._story_scene)

    def select_index(self, index: int):
        select_option = self._story_scene.options[index]
        self._previous_messages.append(Message(role=Role.USER, content=select_option))
        self._send_api()
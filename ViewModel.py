from Message import *
from typing import Callable, List
from ApiService import ApiService
from StoryScene import StoryScene
import json

# isStory_ended = False
# previous_messages: [Message] = []
#
# while not isStory_ended:
#     response = ApiService().start_story(previous_messages=previous_messages)
#     content = response.content
#     # 紀錄 server response
#     previous_messages.append(Message(role=Role.SYSTEM, content=content))
#     print(content)
#     json_obj = json.loads(content)
#     isStory_ended = json_obj["isStoryEnded"]
#     if isStory_ended:
#         print("故事結束")
#         break
#
#     select_index = input("選擇: ")
#     select_option = json_obj["options"][int(select_index)]
#     print("選擇了:", select_option)
#     previous_messages.append(Message(role=Role.USER, content=select_option))
#     print("下一幕")


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
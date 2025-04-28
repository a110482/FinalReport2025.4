from openai import OpenAI
import tkinter as tk
from enum import Enum
from openai.types.chat import ChatCompletionMessage
import json
from dataclasses import dataclass
from typing import List
from apikey import api_key

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

class ApiService:
    # 傳入 API 金鑰，確保能夠存取 OpenAI 服務
    _client = OpenAI(api_key=api_key)

    _storyPrompt = """
    隨機選一則格林童話為大綱 (不要小紅帽)
    分成 5 個段落跟我玩文字遊戲
    每次給我三個選項選
    回應json格式
    {
        "title": "第一幕: 森林的邂逅",
        "content": "小紅帽是一位天真可愛的小女孩，有一天，她的媽媽讓她帶著一籃食物去探望生病的外婆。小紅帽帶著母親交代的點心，踏入了幽深的森林。陽光穿透樹葉，映照在她紅色的斗篷上。沒多久，她遇見了一隻狼，狼露出微笑，問她要去哪裡。",
        "options": [
            "老實回答：「我要去奶奶家！」",
            "假裝不知道：「我只是隨便走走。」",
            "轉身就跑：「不跟陌生人說話！」"
        ],
        isStoryEnded: false
    }
    isStoryEnded 表示故事是否結束
    如果故事結束我就不會再發送消息給你
    最後故事結束時 options 給我空的就好，只要給 content 內容
    """

    _storyStartContent = "請開始"

    def start_story(self, previous_messages: [Message]) -> "Message":
        # 預設訊息
        messages = [
            Message(role=Role.SYSTEM, content=self._storyPrompt),
            Message(role=Role.USER, content=self._storyPrompt),
        ]
        # 對話紀錄
        messages += previous_messages
        messages_dict = [message.to_dict() for message in messages]

        # 呼叫 OpenAI API，讓 ChatGPT 生成回應
        completion = self._client.chat.completions.create(
            model="chatgpt-4o-latest",  # 使用最新版本的 ChatGPT 模型
            messages=messages_dict,
            response_format={"type": "json_object"}
        )

        # 取得 AI 回應的內容
        chatgpt_output = completion.choices[0].message
        orm = Message.from_gpt_message(chatgpt_output)
        return orm

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

class MainView:
    _view_model: ViewModel
    _view: tk.Tk
    _text: tk.Text
    _options: tk.Frame

    def __init__(self):
        self._setup_ui()

    def bind_view_model(self, view_model: ViewModel):
        self._view_model = view_model
        view_model.bind_to(self.update_ui)

    def run(self):
        self._view_model.start_story()
        self._view.mainloop()

    # === UI ===
    def _setup_ui(self):
        self._setup_view()
        self._setup_text()
        self._setup_options()

    def _setup_view(self):
        self._view = tk.Tk()
        self._view.title("final_exam_report")
        self._view.geometry("600x400")
        self._view.grid_rowconfigure(0, weight=3)  # 上半部較大
        self._view.grid_rowconfigure(1, weight=1)  # 下半部較小
        self._view.grid_columnconfigure(0, weight=1)

    # 顯示故事
    def _setup_text(self):
        self._text = tk.Text(self._view, height=10, wrap="word", font=("Arial", 12))
        self._text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # 按鈕區域
    def _setup_options(self):
        self._options = tk.Frame(self._view)
        self._options.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self._add_options()

    # 加入選項
    def _add_options(self):
        for widget in self._options.winfo_children():
            widget.destroy()
        # 選項按鈕
        btn1 = tk.Button(self._options, text="選項 1", font=("Arial", 10), command=lambda: self._on_option_selected(0))
        btn2 = tk.Button(self._options, text="選項 2", font=("Arial", 10), command=lambda: self._on_option_selected(1))
        btn3 = tk.Button(self._options, text="選項 3", font=("Arial", 10), command=lambda: self._on_option_selected(2))

        # 安排按鈕位置
        btn1.grid(row=0, column=0, sticky="ew", padx=5)
        btn2.grid(row=0, column=1, sticky="ew", padx=5)
        btn3.grid(row=0, column=2, sticky="ew", padx=5)

    def _add_next_story(self):
        for widget in self._options.winfo_children():
            widget.destroy()
        btn1 = tk.Button(self._options, text="下一個故事", font=("Arial", 10), command=self._view_model.start_story)
        btn1.grid(row=0, column=0, sticky="ew", padx=5)

    # === logic ===
    # 更新畫面
    def update_ui(self, story_scene: StoryScene):
        self._text.delete(1.0, tk.END)
        self._text.insert(tk.END, story_scene.title + "\n\n")
        self._text.insert(tk.END, story_scene.content + "\n\n")
        if story_scene.isStoryEnded:
            self._add_next_story()
        else:
            self._add_options()
            self._text.insert(tk.END, "選項 1: " + story_scene.options[0] + "\n")
            self._text.insert(tk.END, "選項 2: " + story_scene.options[1] + "\n")
            self._text.insert(tk.END, "選項 3: " + story_scene.options[2] + "\n")

    def _on_option_selected(self, index):
        self._view_model.select_index(index=index)

if __name__ == "__main__":
    view_model = ViewModel()
    main_view = MainView()
    main_view.bind_view_model(view_model=view_model)
    main_view.run()
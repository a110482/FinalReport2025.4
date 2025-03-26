from openai import OpenAI
from apikey import api_key
from Message import *

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

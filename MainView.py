from ViewModel import ViewModel
from StoryScene import StoryScene
import tkinter as tk
from ViewModel import ViewModel
from tkinter.font import Font
import threading

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
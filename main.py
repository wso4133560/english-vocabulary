import tkinter as tk
import random
from FileManager import FileManager

fileManager = FileManager()

# 单词列表
word_list = fileManager.get_words_list()

# 随机选择一个单词
current_word, current_meaning = random.choice(word_list)

# 处理用户点击“提交”按钮的函数
def submit():
    # 随机选择一个新单词
    global current_word
    global current_meaning

    user_answer = entry.get() # 获取用户输入的答案
    if user_answer == current_meaning:
        result_label.config(text="正确！")
    else:
        result_label.config(text="错误，正确答案是：" + current_meaning)

    
    current_word, current_meaning = random.choice(word_list)
    word_label.config(text=current_word)
    entry.delete(0, tk.END)
    entry.focus()

# 创建窗口
window = tk.Tk()
window.title("背单词")

# 创建标签和输入框
word_label = tk.Label(window, text=current_word, font=("Arial", 36))
word_label.pack(pady=20)
entry = tk.Entry(window, font=("Arial", 24))
entry.pack(pady=10)

# 创建“提交”按钮
submit_button = tk.Button(window, text="提交", command=submit)
submit_button.pack(pady=10)

# 创建显示答案的标签
result_label = tk.Label(window, font=("Arial", 24))
result_label.pack(pady=20)

# 运行窗口
window.mainloop()
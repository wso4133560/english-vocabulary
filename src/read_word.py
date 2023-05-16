import os
from playsound import playsound
from gtts import gTTS

def read_word(word):
    word = word.lower()
    # check ../mp3/下是否有此单词的mp3文件
    filePath = f"../mp3/{word}.mp3"
    if os.path.isfile(filePath):
        playsound(filePath)
        return

    language = 'en'

    speech = gTTS(text=word, lang=language, slow=True)
    speech.save(filePath)
    playsound(filePath)

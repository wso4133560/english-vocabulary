import gtts
import pygame
from io import BytesIO

# 获取语音合成
tts = gtts.gTTS('Hello, world!')

# 获取语音合成的音频数据
fp = BytesIO()
tts.write_to_fp(fp)
fp.seek(0)

# 初始化 pygame mixer
pygame.mixer.init()
pygame.init()

# 加载音频数据
pygame.mixer.music.load(fp)

# 播放音频
pygame.mixer.music.play()

# 持续等待音频播放完成
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
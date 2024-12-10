# -*- coding: utf-8 -*-
from naoqi import ALProxy
import random
import time
import sys
import os
import subprocess

# ポート番号を指定
PORT = 

behavior_manager = ALProxy("ALBehaviorManager", "127.0.0.1", PORT)
talk = ALProxy("ALTextToSpeech", "127.0.0.1", PORT)
postureProxy = ALProxy("ALRobotPosture", "127.0.0.1", PORT)
motion = ALProxy("ALMotion", "127.0.0.1", PORT)
audio_player = ALProxy("ALAudioPlayer", "127.0.0.1", PORT)

str = ["僕の勝ちだね", "あいこだね", "負けちゃった･･･"]
path = "./" + "hand.txt"
stand = "stand-811386/behavior_1"
file_contents = ""
hand_gesture = ""
random_num = 0

def open_file():
    global file_contents
    with open(path, 'r') as file:
        file_contents = file.read().strip()
    file_contents = file_contents.split("\n")[0]

def random_robot():
    global random_num, hand_gesture
    random_num = random.randint(1, 3)
    if random_num == 1:
        behavior_name = r"jannkenn_reaction-02a063/jannkenn_reaction/rock"
        hand_gesture = "rock"
    elif random_num == 2:
        behavior_name = r"jannkenn_reaction-02a063/jannkenn_reaction/scissors"
        hand_gesture = "scissors"
    elif random_num == 3:
        behavior_name = r"jannkenn_reaction-02a063/jannkenn_reaction/paper"
        hand_gesture = "paper"

    behavior_manager.startBehavior(behavior_name)

def win_or_lose():
    global file_contents, random_num
    outcomes = {
        1: {"rock": str[1], "scissors": str[0], "paper": str[2]},
        2: {"rock": str[2], "scissors": str[1], "paper": str[0]},
        3: {"rock": str[0], "scissors": str[2], "paper": str[1]}
    }
    if str[1] == outcomes[random_num][file_contents]:
        # Python3のパスを指定
        subprocess.call(["", ".\\hand_decide.py", "restart"])
    else:
        talk.say(outcomes[random_num][file_contents])
        if str[0] == outcomes[random_num][file_contents]:
            behavior_name = "expression_reaction-82d091/expression_reaction/joy"
        elif str[2] == outcomes[random_num][file_contents]:
            behavior_name = "expression_reaction-82d091/expression_reaction/sadness"
        behavior_manager.startBehavior(behavior_name)

if __name__ == '__main__':
    open_file()
    random_robot()
    talk.say("Me："+hand_gesture+"  "+"You："+file_contents) #Meがロボット
    time.sleep(3)
    win_or_lose()
    time.sleep(4)
    behavior_manager.startBehavior(stand)
    exit()

import time
import subprocess
import sys

OUTPUT_TXT_FILE = "./" + "hand.txt"
hand_count = [0,0,0]
jp_str = ""
error_txt = "読み取れませんでした。"+"\n"+"再度じゃんけんで出す手をカメラに向けて下さい"
judge = False

def reset_txt():
    with open(OUTPUT_TXT_FILE, 'w') as f:
        f.write("")

def hand_decide():
    global jp_str
    print("じゃんけんで出す手をカメラに向けて下さい")
    max_count = 0
    while max_count == 0:
        ready = False
        while not ready:
            ready = (input("準備はできましたか？ (y/n)") == "y")
        start_time = time.time()

        if ready:
            reset_txt()
            finish_time = time.time()
            while (finish_time-start_time < 2):
                finish_time = time.time()
            with open(OUTPUT_TXT_FILE, 'r') as f:
                for line in f:
                    if line.strip() == "Rock":
                        hand_count[0] = hand_count[0] + 1
                    elif line.strip() == "Scissors":
                        hand_count[1] = hand_count[1] + 1
                    elif line.strip() == "Paper":
                        hand_count[2] = hand_count[2] + 1
            max_count = max(hand_count)
            if max_count == 0:
                print(error_txt)

        max_index = hand_count.index(max_count)
        if max_index == 0:
            str = "rock"
            jp_str = "グー"
        elif max_index == 1:
            str = "scissors"
            jp_str = "チョキ"
        elif max_index == 2:
            str = "paper"
            jp_str = "パー"
        with open(OUTPUT_TXT_FILE, 'w') as f:
            f.write(str + '\n')

def confirm():
    global jp_str, judge
    judge_txt = "あなたが出したのは"+jp_str+"ですか？ (y/n)"
    judge = (input(judge_txt) == "y")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("あいこでした")
    while not judge:
        hand_decide()
        confirm()
    # Python2.7のパスを指定
    subprocess.call(["", ".\\hand_jannkenn.py"])

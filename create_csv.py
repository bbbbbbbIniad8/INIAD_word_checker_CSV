import pandas as pd
import numpy as np
from GPT import GPT


s = """単語[{inp}]の日本語訳と品詞をどれも日本語で答えよ。
ただし、指定したフォーマット以外の出力はいらない。
また、品詞は以下のリストの中に含むもののみ出力せよ。
なお、入力された英語にスペルミスがある場合、修正してもよい。
[品詞]
代名詞
動詞
形容詞
副詞
助動詞
前置詞
冠詞
間投詞
接続詞
[format]
英語;日本語訳;品詞
"""

def create_csv():
    global s
    lst = []
    mode = ""

    while True:
        mode = input("Select mode(create|append)")
        if mode != "create":
                try:
                    csv_in = mode
                    df = pd.read_csv(mode+ ".csv", sep = ",", header = 0,index_col=0)
                    break
                except:
                    print("error")
                    continue
    while True:     
        try:
            print("Plz input a word which you wanna add[q->end]")
            inp = input(":").replace(' ', '')
            if inp == "q":
                break

            translate = GPT.ResSimple(s.format(inp = inp)).split(";")
            print(f"{translate[0]}:{translate[1]}:{translate[2]}\n")
            if input("That OK?(y/n)") != "y":
                continue
            print("Success")
            appends = [translate[0], translate[1], translate[2]]
            lst.append(appends)
        except Exception as e:
            print("error")
            print(translate)
            print(e)
            continue

    
    if len(lst) != 0 and mode == "create":
        df = pd.DataFrame(lst,columns=["English","Japanese","part"])
        df.to_csv(input("Plz input file name") + "csv")
    else:
        new_df = pd.DataFrame(lst, columns=["English","Japanese","part"])
        df_connect = pd.concat([df, new_df], ignore_index=True)
        df_connect.to_csv(csv_in + ".csv")
    



create_csv()    

import pandas as pd
from GPT import GPT


s = """単語[{inp}]の日本語訳(1つ以上)と品詞をどれも日本語で答えよ。
ただし、指定したフォーマット以外の出力はいらない。
また、品詞は以下のリストの中に含むもののみ出力せよ。
なお、入力された英語にスペルミスがある場合、修正してもよい。改行する必要はない。
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
英語;日本語訳;品詞"""

def file_save(mode,lst,df,csv_in):
    new_df = pd.DataFrame(lst,columns=["English","Japanese","part"])
    if len(lst) != 0 and mode == "create": 
        new_df.to_csv(input("Plz input file name") + "csv")
    else:
        pd.concat([df, new_df], ignore_index=True).to_csv(csv_in + ".csv")

def create_csv():
    global s
    lst = []
    mode = ""

    while True:
        mode = input("Plz input file_name you wanna edit(if you wanna new file, input 'create'.\n:")
        if mode != "create":
            try:
                csv_in = mode
                df = pd.read_csv(f"{mode}.csv", sep=",", header=0,index_col=0)
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
            translate = GPT.ResSimple(s.format(inp=inp)).split(";")
            print(f"{translate[0]}:{translate[1]}:{translate[2]}\n")
            if input("That OK?(y/n)\n:") != "y":
                continue
            print("\nSuccess\n")
            lst.append(translate)
            file_save(mode, lst, df, csv_in)
        except Exception as e:
            print(f"error:\n{translate}\n:{e}")
            continue

    file_save(mode, lst, df, csv_in)


create_csv()

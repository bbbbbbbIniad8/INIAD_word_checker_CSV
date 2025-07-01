import pandas as pd
import numpy as np
from GPT import GPT
import random

class EJC:
    def __init__(self,mode,path,first,second):
        self.mode = mode
        self.ENJNlst = self.process_csv(path, first, second)
        self.MissLst = []
        self.AIjudge = ""
        self.line = "=" * 80
        self.GPT = GPT(0.1,"") if mode == "英和" else None

    def process_csv(self, path, first, second):
        if second - first <= 0 and not (first == 0 and second == 0):
            raise ValueError(f"値が不正です。first({first})はsecond({second})以下の値にしてください。")
        
        try:
            df = pd.read_csv(path, sep=",", comment="#")
        except FileNotFoundError:
            print(f"エラー: CSVファイルが見つかりません: {path}")
            exit()

        if first == 0 and second == 0:
            ENLst = df["English"]
            JLst = df["Japanese"]
        else:
            try:
                ENLst = df.loc[first:second, "English"]
                JLst = df.loc[first:second, "Japanese"]
            except KeyError:
                print(f"エラー: 指定された範囲({first}～{second})がCSVファイルの範囲外か、列名が正しくありません。")
                exit()
    
        return list(zip(ENLst, JLst))

    def main(self):
        random.shuffle(self.ENJNlst)
        for i, (EN, JP) in enumerate(self.ENJNlst, start=1):
            print(f"{self.line}\n第{i}問\n{{Q}}".format(Q = f"以下の日本語を英語に直しなさい\n{JP}" if self.mode == "和英" else f"以下の英語を日本語に直しなさい\n{EN}"))
            answer = input("入力:")
            if self.mode == "英和":
                self.AIjudge = self.GPT.Res(f"以下を採点してください。YESかNOのみで答えてください【 [{EN}]の日本語訳はは[{answer}]である】")
            if answer.strip() == EN and self.mode == "和英":
                print(f"正解!!\n{self.line}\n")
            elif (answer.strip() == JP or self.AIjudge == "YES") and self.mode == "英和":
                print(f"正解!!\n{self.line}\n")
            else:
                A = A = EN if self.mode == "和英" else JP
                peke  = ""
                for i in range(len(A)):
                    try:
                        if A[i] == answer[i]:
                            peke += "-"
                        else:
                            peke += "^"
                    except:
                        peke += "^"
                print(f"不正解\n正解は\n{{A}}\n{peke}\n{self.line}".format(A = A))
                self.MissLst.append((EN,JP))
        
        if len(self.MissLst) != 0:
            print(f"{self.line}\n{len(self.ENJNlst)}問中{len(self.MissLst)}問間違えました。\n間違えた単語は以下の通りです。")
            for i in self.MissLst:
                print(f"[{i[0]}:{i[1]}]")
            print(f"\n{self.line}\n")
        else:
            print(f"{self.line}\n全問正解しました\n{self.line}\n")


main = EJC(
        mode = "和英",
        path = "master.csv",
        first = 0,
        second = 9)
main.main()    

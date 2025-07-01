import random
import os
from GPT import GPT
import os
import random
import openpyxl



class EJC:
    def __init__(self,mode,path,first,second):
        self.mode = mode
        self.ENJNlst = self.process_excel(path,first,second)
        self.MissLst = []
        self.AIjudge = ""
        self.line = "=" * 80
        self.GPT = GPT(0.1,"") if mode == "英和" else None

    def process_excel(self,path, first, second):
        ward_file = os.path.join(os.path.dirname(__file__), f'{path}.xlsx')
        sheet = openpyxl.load_workbook(ward_file).active
        
        ENLst, JLst = [], []
        
        rows = [(str(row[1].value), str(row[0].value)) for row in sheet.iter_rows(min_row=2, max_row=1000, max_col=2) if row[1].value is not None]
        
        if first == 0 and second == 0:
            ENLst, JLst = zip(*rows) if rows else ([], [])
        elif second - first <= 0:
            print("error1:値が不正です")
            exit()
        else:
            ENLst, JLst = zip(*rows[first-1:second]) if rows[first-1:second] else ([], [])
    
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
                print(f"不正解\n正解は{{A}}\n{self.line}\n".format(A = EN if self.mode == "和英" else JP))
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
        path = "resson.3",
        first = 0,
        second = 0)
main.main()    
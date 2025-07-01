import openai
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv('.env')

client = openai.OpenAI(
    api_key= os.getenv('APIKEY'),
    base_url="https://api.openai.iniad.org/api/v1"
)

class GPT:
    def __init__(self,temperature,prompt):
        self.Temperature = temperature
        self.Prompt = prompt

    def Res(self, question):
        #実際にAIにリクエストを送ってるところ
        response = client.chat.completions.create(
            model  = 'gpt-4o-mini',
            temperature=self.Temperature,
            messages = [
                {"role": "system", "content": f"{self.Prompt}"},
                {'role':'user','content':question},
            ]
            
        )

        return response.choices[0].message.content
    
    @classmethod
    def ResSimple(cls, question):
        #実際にAIにリクエストを送ってるところ
        response = client.chat.completions.create(
            model  = 'gpt-4o-mini',
            temperature = 0.1,
            messages = [
                {"role": "system", "content": "Your best system."},
                {'role':'user','content':question},
            ]
            
        )

        return response.choices[0].message.content
from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()
app = Flask(__name__)
# user_input = input("오늘의 기분을 알려줘!")
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
message = [] # 메시지들이 담기는 공간 => 챗봇(채팅 내역은 6개월동안 보관이 법적으로 필요) / 유럽진출 = 유료6
#웹서버 - Nginx ( 리버스 프록시 )
# (1) 로드 밸런서 => 트래픽 분산
# (2) 보안 => 다이렉트로 여러분들 자바 서버로 접근하게 되면 보안이 취약
# - 불법 토토 => VM-VM-VM (IP 우회)
# (포워드 프록시)
# - 우리 회사가 이번에 미국에 런칭했어
# - (유저) 아 서버 왜이리 느려 => 한국 서버를 안거치고 미국 웹서버(포워드 - 프록시- 정책 파일)
def make_prompt(user_input):
    res = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages=[{"role": "user", "content": user_input}]
    )
    return res.choices[0].message.content


@app.route('/', methods = ["GET","POST"])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        bot_reqonse = make_prompt(user_input)
        message.append({"role":"user","text": user_input})
        message.append({"role":"bot", "text":bot_reqonse })
    return render_template('index.html', messages=message)
if __name__ == "__main__":
    app.run(debug=True)
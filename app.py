from flask import Flask, render_template as ren, request, redirect, url_for, session
import hashlib

app = Flask(__name__)

#Flask 서버 실행
if __name__ == "__main__":
    app.run(debug=True) #코드 수정 시 자동 반영 및 에러 디버깅
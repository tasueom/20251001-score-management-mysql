from flask import Flask, render_template as ren, request, redirect, url_for, session
import hashlib
import db

app = Flask(__name__)
app.secret_key = "dev_key123"

#Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True) #코드 수정 시 자동 반영 및 에러 디버깅
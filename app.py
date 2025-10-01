from flask import Flask, render_template as ren, request, redirect, url_for, session, flash
import hashlib
import db

app = Flask(__name__)
app.secret_key = "dev_key123"

#실행 시
@app.route("/")
def index():
    return ren("index.html", sno=session.get("sno"))

#회원가입
@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == "POST":
        sid = request.form["sid"]
        ban = request.form["ban"]
        sname = request.form["sname"]
        password = request.form["password"]
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            db.signup(sid,ban,sname,hashed_pw)
        except:
            flash("이미 존재하는 학번입니다.")
            return redirect(url_for("signup"))
        return redirect(url_for("signin"))
    return ren("signup.html")

#로그인
@app.route("/signin", methods=['GET','POST'])
def signin():
    if request.method == "POST":
        sid = request.form["sid"]
        password = request.form["password"]
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        check = db.signin_check(sid, hashed_pw)
        if check:
            flash("로그인 성공")
        else:
            flash("로그인 실패")
            return redirect(url_for("signin"))
        return ren("index.html", sid = session.get("sid"))
    return ren("signin.html")

#Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True) #코드 수정 시 자동 반영 및 에러 디버깅
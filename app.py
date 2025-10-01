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
            session["sid"] = sid
            page = "index.html"
        else:
            flash("로그인 실패")
            return redirect(url_for("signin"))
        return ren(page, sid = session.get("sid"))
    return ren("signin.html")

#로그아웃
@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

# 본인 성적 조회
@app.route("/my_score")
def my_score():
    sid = session.get("sid")
    
    score = db.get_score(sid)
    if score:
        return ren("my_score.html", score=score)
    else:
        flash("입력된 성적이 없습니다. 성적 입력 화면으로 이동합니다.")
        return redirect(url_for("insert_score"))

# 성적 입력
@app.route("/insert_score", methods=['GET','POST'])
def insert_score():
    sid = session.get("sid")
    if request.method == "POST":
        kor = int(request.form["kor"])
        eng = int(request.form["eng"])
        mat = int(request.form["mat"])
        tot, avg, grade = calculate(kor, eng, mat)
        
        db.insert_score(sid, kor, eng, mat, tot, avg, grade)
        
        flash("성적이 입력되었습니다.")
        score = db.get_score(sid)
        return ren("my_score.html", score=score, sid=sid)
    return ren("insert_score.html", sid = sid)

def calculate(kor, eng, mat):
    tot = kor+eng+mat
    avg = round(tot/3,2)
    match int(avg//10):
        case 10|9:
            grade = "A"
        case 8:
            grade = "B"
        case 7:
            grade = "C"
        case 6:
            grade = "D"
        case _:
            grade = "F"
    return tot, avg, grade

#Flask 서버 실행
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True) #코드 수정 시 자동 반영 및 에러 디버깅
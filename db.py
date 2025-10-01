import mysql.connector

# MySQL 기본 연결 설정 (데이터베이스를 지정하지 않고 접속)
base_config = {
    "host": "localhost",   # MySQL 서버 주소 (로컬)
    "user": "root",        # MySQL 계정
    "password": "1234"     # MySQL 비밀번호
}

# 사용할 데이터베이스 이름
DB_NAME = "scoredb"

# 커넥션과 커서 반환하는 함수
def conn_db():
    conn = mysql.connector.connect(database=DB_NAME, **base_config)
    cur = conn.cursor()
    return conn, cur

def init_db():
    # DB 생성 (없으면 자동 생성)
    conn = mysql.connector.connect(**base_config)
    cur = conn.cursor()
    cur.execute(f"create database if not exists {DB_NAME} default character set utf8mb4")
    conn.commit()
    conn.close()
    
    # 생성된 DB에 접속해서 테이블 생성
    conn, cur = conn_db()
    cur.execute("""
                create table if not exists students(
                    sid varchar(20) primary key,
                    ban int,
                    sname varchar(40),
                    password varchar(200)
                )
                """)
    cur.execute("""
                create table if not exists scores(
                    sid varchar(20),
                    kor int,
                    eng int,
                    mat int,
                    tot int,
                    average double,
                    grade char(1),
                    foreign key (sid) references students(sid)
                )
                """)
    conn.commit()
    conn.close()

# 회원가입
def signup(sid, ban, sname, hashed_pw):
    conn, cur = conn_db()
    try:
        cur.execute("""
                    insert into students(sid, ban, sname, password) 
                    values(%s, %s, %s, %s)
                    """,(sid, ban, sname, hashed_pw))
        conn.commit()
    finally:
        conn.close()

# 로그인 판별
def signin_check(sid, hashed_pw):
    conn, cur = conn_db()
    cur.execute("select sid from students where sid=%s and password=%s",(sid, hashed_pw))
    result = cur.fetchone()
    conn.close()
    
    return result

# 학번으로 성적 조회
def get_score(sid):
    conn, cur = conn_db()
    cur.execute("""
                select * from scores
                where sid = %s
                """,(sid,))
    result = cur.fetchone()
    conn.close()
    
    return result

# 성적 삽입
def insert_score(sid, kor, eng, mat, tot, avg, grade):
    conn, cur = conn_db()
    cur.execute("""
        INSERT INTO scores (sid, kor, eng, mat, tot, average, grade)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (sid, kor, eng, mat, tot, avg, grade))
    conn.commit()
    conn.close()

# 성적 수정
def update_score(sid, kor, eng, mat, tot, avg, grade):
    conn, cur = conn_db()
    cur.execute("""
                update scores set
                kor = %s,
                eng = %s,
                mat = %s,
                tot = %s,
                average = %s,
                grade = %s
                where sid = %s
                """,(kor, eng, mat, tot, avg, grade, sid))
    conn.commit()
    conn.close()
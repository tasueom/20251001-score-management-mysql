function checkSignUp(f) {
    // sid가 숫자로만 이루어져 있는지 확인
    let sid = f.sid.value.trim();
    let sidPattern = /^[0-9]+$/;
    if (!sidPattern.test(sid)) {
        alert("학번은 숫자만 입력 가능합니다.");
        f.sid.focus();
        return false;
    }

    // 비밀번호와 비밀번호 확인 일치 여부
    let pw = f.password.value;
    let pwCheck = f.passwordCheck.value;
    if (pw !== pwCheck) {
        alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.");
        f.password.focus();
        return false;
    }

    return true; // 모든 검증 통과 시 제출 진행
}

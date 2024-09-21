USER_SERIALIZE_ERRORS = {
    "password": {},
    "email": {
        "required": {"이메일": "이메일을 입력해주세요."},
        "unique": {"이메일": "이미 가입한 이메일입니다."},
    },
    "username": {
        "required": {"이름": "이름을 입력해주세요."},
    },
    "phone": {"required": {"전화번호": "전화번호를 입력해주세요."}},
}

SIGNIN_SERIALIZE_ERRORS = {
    "email": {"not_found": {"이메일": "존재하지 않는 유저입니다"}},
    "password": {"match": {"비밀번호": "일치하지 않는 비밀번호입니다."}},
S3_URL_SERIALIZE_ERRORS = {
    "file": {
        "required": {"file": "파일을 첨부해주세요."},
        "over_size": {"file": "각 파일 크기는 10MB 이하여야 합니다."},
    }
}

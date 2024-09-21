USER_SERIALIZE_ERRORS = {
    "password": {},
    "email": {
        "required": {"email": "이메일을 입력해주세요."},
        "unique": {"email": "이미 가입한 이메일입니다."},
    },
    "username": {
        "required": {"username": "이름을 입력해주세요."},
    },
    "phone": {"required": {"phone": "전화번호를 입력해주세요."}},
}

SIGNIN_SERIALIZE_ERRORS = {
    "email": {"not_found": {"email": "존재하지 않는 유저입니다"}},
    "password": {"match": {"password": "일치하지 않는 비밀번호입니다."}},
}

S3_URL_SERIALIZE_ERRORS = {
    "file": {
        "required": {"file": "파일을 첨부해주세요."},
        "over_size": {"file": "각 파일 크기는 10MB 이하여야 합니다."},
        "invalid_extension": {"file": "유효하지 않은 파일 확장자입니다."},
    }
}

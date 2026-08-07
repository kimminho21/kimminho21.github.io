# 언누운크루 로컬 개발 서버

이 프로젝트는 정적 HTML 파일과 로컬 Flask 서버를 사용해 각 페이지의 데이터를 JSON 파일로 저장합니다.

서버 실행 방법 (Windows, Python 필요):

1. 가상환경(선택)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 의존성 설치

```powershell
pip install flask google-api-python-client google-auth
```

3. Google Sheets 서비스 계정 설정

- Google Cloud Console에서 서비스 계정 생성
- JSON 키 파일 다운로드
- `credentials/service_account.json` 위치에 저장하거나 환경 변수 `GOOGLE_APPLICATION_CREDENTIALS`로 경로 지정
- Google Sheets에서 공유 설정에 서비스 계정 이메일 추가
- Google Sheets ID를 환경 변수로 설정

4. 서버 실행

```powershell
$env:GOOGLE_SHEET_ID='your_sheet_id_here'
$env:GOOGLE_APPLICATION_CREDENTIALS='c:\project\gorich\credentials\service_account.json'
python save_server.py
```

- 서버는 기본적으로 `http://localhost:5000`에서 동작합니다.
- 정적 파일은 `python -m http.server 8000` 같은 명령으로 서빙하세요.
- 서버가 실행되면 먼저 Google Sheets에 저장/불러오기를 시도합니다.
- Google Sheets 사용이 실패하면 `data/data.json`로 자동 폴백됩니다.

데이터 파일:
- `data/data.json` (Google Sheets 연결 실패 시 사용)

주의: 이 서버는 개발/로컬 용이며 인증, 보안, 동시성 처리가 되어 있지 않습니다. 공개된 환경에서 사용하지 마세요.

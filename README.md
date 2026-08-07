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
pip install flask
```

3. 서버 실행

```powershell
python save_server.py
```

- 서버는 기본적으로 `http://localhost:5000`에서 동작합니다.
- 정적 파일은 이미 `python -m http.server 8000` 같은 명령으로 서빙하고 있으므로, 브라우저에서 `http://localhost:8000`을 열어 페이지를 사용하세요.
- 서버가 실행되면 각 페이지에서 저장/불러오기 시 `data/` 폴더 아래에 JSON 파일이 생성됩니다.

데이터 파일:
- `data/schedule.json`
- `data/shoes.json`
- `data/weight.json`

주의: 이 서버는 개발/로컬 용이며 인증, 보안, 동시성 처리가 되어 있지 않습니다. 공개된 환경에서 사용하지 마세요.

# 📝 이미지 텍스트 추출기 (OCR)

Streamlit과 Gemini AI를 사용한 이미지 텍스트 추출 웹 애플리케이션입니다.

## 주요 기능

- 🤖 **AI 기반 추출**: Gemini AI로 정확한 고객 정보 추출
- 🖼️ 이미지 파일 업로드 (PNG, JPG, JPEG)
- 📊 구조화된 데이터 추출 (전화번호, 고객명, 비고)
- ✏️ 실시간 데이터 편집
- 📥 CSV/Excel 다운로드
- 🔒 HTTPS 보안 연결
- 🎨 직관적인 사용자 인터페이스

## 설치 방법

### 1. Tesseract OCR 설치

#### macOS
```bash
brew install tesseract
brew install tesseract-lang
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-kor
```

#### Windows
1. https://github.com/UB-Mannheim/tesseract/wiki 에서 설치 파일 다운로드
2. 설치 시 "Additional language data" 옵션에서 한국어 선택
3. 환경 변수에 Tesseract 경로 추가 (예: `C:\Program Files\Tesseract-OCR`)

### 2. Python 패키지 설치

```bash
pip install -r requirements.txt
```

## 실행 방법

### 간단한 실행 (스크립트 사용)

```bash
# 서버 시작
./start_server.sh

# 서버 중지
./stop_server.sh
```

### 수동 실행

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
```

## 접속 주소

- **네트워크**: http://172.30.1.26:8501
- **로컬**: http://localhost:8501

💡 같은 Wi-Fi/내부망에 연결된 모든 기기에서 접속 가능합니다.

## 사용 방법

1. 웹 브라우저에서 애플리케이션을 엽니다
2. 좌측 사이드바에서 OCR 언어를 선택합니다 (한글+영문, 한글만, 영문만)
3. 이미지 파일을 업로드합니다 (드래그 앤 드롭 또는 클릭)
4. 자동으로 텍스트가 추출되어 화면에 표시됩니다
5. 결과를 복사하거나 텍스트 파일로 다운로드합니다

## 더 나은 OCR 결과를 위한 팁

- ✅ 고해상도 이미지 사용
- ✅ 텍스트가 선명하고 대비가 높은 이미지
- ✅ 텍스트가 수평으로 정렬된 이미지
- ✅ 배경이 단순한 이미지
- ❌ 손글씨는 인식률이 낮음
- ❌ 너무 작은 글자는 인식이 어려움

## 기술 스택

- **Frontend**: Streamlit
- **OCR Engine**: Tesseract OCR
- **이미지 처리**: PIL (Pillow)
- **언어**: Python 3.8+

## 프로젝트 구조

```
images_extract/
├── app.py              # 메인 Streamlit 애플리케이션
├── requirements.txt    # Python 패키지 의존성
└── README.md          # 프로젝트 문서
```

## 문제 해결

### Tesseract를 찾을 수 없다는 오류
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
```
app.py 파일 상단에 위 코드를 추가하세요.

### 한글이 인식되지 않는 경우
Tesseract의 한국어 언어 데이터가 설치되어 있는지 확인하세요:
```bash
tesseract --list-langs
```
목록에 'kor'이 있어야 합니다.

## 라이선스

이 프로젝트는 회사 내부 도구로 사용됩니다.

## 개선 예정 사항

- [ ] 여러 이미지 일괄 처리
- [ ] PDF 파일 지원
- [ ] 이미지 전처리 옵션 (대비, 밝기 조정)
- [ ] OCR 결과 신뢰도 표시
- [ ] 다양한 출력 형식 지원 (JSON, CSV)

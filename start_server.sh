#!/bin/bash

# 이미지 텍스트 추출기 서버 시작 스크립트

echo "🚀 이미지 텍스트 추출기 서버를 시작합니다..."

# 작업 디렉토리로 이동
cd /Users/bagchanhyo/Desktop/images_extract

# Streamlit 서버 시작
echo "📝 Streamlit 서버 시작 중..."
streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true &

echo ""
echo "✅ 서버가 성공적으로 시작되었습니다!"
echo ""
echo "접속 주소:"
echo "  - 네트워크: http://172.30.1.26:8501"
echo "  - 로컬:    http://localhost:8501"
echo ""
echo "💡 같은 Wi-Fi에 연결된 기기에서 위 주소로 접속하세요!"
echo ""

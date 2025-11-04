#!/bin/bash

# 이미지 텍스트 추출기 서버 중지 스크립트

echo "🛑 이미지 텍스트 추출기 서버를 중지합니다..."

# Streamlit 프로세스 종료
echo "📝 Streamlit 서버 중지 중..."
pkill -f "streamlit run app.py"

echo ""
echo "✅ 서버가 성공적으로 중지되었습니다!"
echo ""

import streamlit as st
from PIL import Image
import pandas as pd
from google import genai
from google.genai import types
import json
import io
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="이미지 텍스트 추출기",
    page_icon="📝",
    layout="wide"
)

# Gemini AI를 사용한 구조화된 데이터 추출
def extract_with_gemini(image, api_key):
    """Gemini AI를 사용하여 이미지에서 고객 정보 추출"""
    try:
        # 새로운 Google GenAI SDK 방식
        client = genai.Client(api_key=api_key)

        # PIL Image를 bytes로 변환
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        # 이미지 Part 생성
        image_part = types.Part.from_bytes(
            data=img_bytes,
            mime_type='image/png'
        )

        prompt = """
이 이미지에서 고객 정보를 추출해주세요.

다음 형식의 JSON 배열로 반환해주세요:
[
  {"전화번호": "010-1234-5678", "고객명": "홍길동", "비고": ""},
  {"전화번호": "02-123-4567", "고객명": "김철수", "비고": ""}
]

규칙:
1. 전화번호는 하이픈 포함 형식으로 (010-1234-5678)
2. 고객명은 사람 이름만 추출 (한글 또는 영문)
3. 비고는 항상 빈 문자열("")
4. 표 헤더는 제외
5. 전화번호가 있는 행만 추출
6. JSON 형식만 반환 (다른 설명 없이)
7. 이름이 명확하지 않으면 빈 문자열로 두기
8. 반드시 전화번호, 고객명, 비고 순서로 반환
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[image_part, prompt]
        )

        text = response.text.strip()

        # JSON 추출
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)
        return data

    except Exception as e:
        error_str = str(e)
        if "API key not valid" in error_str or "API_KEY_INVALID" in error_str:
            st.error("API 키가 유효하지 않습니다. Gemini API 키를 확인해주세요.")
            st.info("API 키는 https://aistudio.google.com/app/apikey 에서 발급받을 수 있습니다.")
        else:
            st.error(f"Gemini API 오류: {error_str}")
        return None

# 타이틀
st.title("📝 이미지 텍스트 추출기 (OCR)")
st.markdown("이미지에서 텍스트를 자동으로 추출합니다. (한글/영문 지원)")

# 사이드바 - 설정
st.sidebar.header("설정")

# 환경 변수에서 API 키 가져오기
default_api_key = os.getenv("GEMINI_API_KEY", "")

st.sidebar.markdown("### 🤖 Gemini API 키")

if default_api_key:
    gemini_api_key = default_api_key
    st.sidebar.success("✅ API 키가 환경 변수에서 로드되었습니다")
else:
    gemini_api_key = st.sidebar.text_input(
        "Gemini API 키 입력",
        type="password",
        help="https://aistudio.google.com/app/apikey 에서 발급"
    )
    if gemini_api_key:
        st.sidebar.success("✅ API 키가 설정되었습니다")
    else:
        st.sidebar.warning("⚠️ API 키를 입력해주세요")

st.sidebar.markdown("---")
st.sidebar.markdown("### 사용 방법")
st.sidebar.markdown("""
1. Gemini API 키를 입력하세요
2. 이미지 파일을 업로드하세요
3. 자동으로 고객 정보가 추출됩니다
4. 결과를 확인하고 다운로드하세요

**💡 팁**: Gemini AI가 표 형식의 데이터도 정확하게 추출합니다!
""")

# 메인 영역 - 파일 업로더
uploaded_file = st.file_uploader(
    "이미지를 업로드하세요 (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"],
    help="드래그 앤 드롭 또는 클릭하여 파일을 선택하세요"
)

if uploaded_file is not None:
    # 2개 컬럼 생성
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📷 업로드된 이미지")
        image = Image.open(uploaded_file)
        st.image(image, caption="원본 이미지", use_column_width=True)
        st.caption(f"파일명: {uploaded_file.name}")
        st.caption(f"크기: {image.size[0]} x {image.size[1]} pixels")

    with col2:
        st.subheader("📝 추출된 정보")

        # Gemini API 키가 있는 경우
        if gemini_api_key:
            # 파일 이름을 기준으로 캐시 키 생성
            cache_key = f"extracted_data_{uploaded_file.name}"

            # 이미 추출된 데이터가 없으면 추출
            if cache_key not in st.session_state:
                with st.spinner("🤖 Gemini AI로 정보 추출 중..."):
                    data = extract_with_gemini(image, gemini_api_key)
                    if data:
                        st.session_state[cache_key] = data

            # 추출된 데이터가 있으면 표시
            if cache_key in st.session_state:
                st.success("✅ AI 추출이 완료되었습니다!")

                # DataFrame으로 변환
                df = pd.DataFrame(st.session_state[cache_key])

                # 데이터 편집 가능한 테이블
                st.info("💡 아래 테이블을 직접 수정할 수 있습니다")
                edited_df = st.data_editor(
                    df,
                    num_rows="dynamic",
                    use_container_width=True,
                    hide_index=True,
                    key=f"editor_{uploaded_file.name}"
                )

                st.caption(f"📊 총 {len(edited_df)}건의 고객 정보")

                # CSV 다운로드
                csv = edited_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 CSV 파일로 다운로드",
                    data=csv,
                    file_name=f"customer_info_{uploaded_file.name.split('.')[0]}.csv",
                    mime="text/csv"
                )

                # Excel 다운로드
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    edited_df.to_excel(writer, index=False, sheet_name='고객정보')

                st.download_button(
                    label="📥 Excel 파일로 다운로드",
                    data=buffer.getvalue(),
                    file_name=f"customer_info_{uploaded_file.name.split('.')[0]}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        # API 키가 없는 경우
        else:
            st.warning("⚠️ Gemini API 키를 입력해주세요")
            st.info("""
**API 키 발급 방법:**
1. https://aistudio.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 생성된 키를 복사하여 좌측 사이드바에 입력
4. 무료 할당량: 하루 1,500회
            """)

else:
    st.info("👆 이미지 파일을 업로드하여 시작하세요")

    st.markdown("---")
    st.subheader("💡 사용 팁")
    st.markdown("""
    **Gemini AI 기능:**
    - 이미지에서 자동으로 이름과 전화번호를 정확하게 추출
    - 표 형식, 복잡한 레이아웃도 잘 인식
    - 구조화된 데이터로 자동 변환 (CSV/Excel)
    - 무료 할당량: 하루 1,500회

    **지원 형식:**
    - PNG, JPG, JPEG 이미지
    - 한글 및 영문 텍스트
    - 표 형식 데이터
    """)

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Made with Streamlit & Gemini AI</div>",
    unsafe_allow_html=True
)

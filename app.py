import streamlit as st
from google import genai

# 📌 여기에 발급받으신 Google AI Studio API Key를 직접 입력하세요.
API_KEY = "AQ.Ab8RN6LcpBwAaf8Br3PlrD0ZXRheaP1s9lO7-nEB8Jh5iL9QGQ"

# 페이지 설정
st.set_page_config(
    page_title="✨ 오늘의 AI 운세",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 AI 실시간 오늘의 운세")
st.write("오늘 하루의 운세를 확인해보세요!")

# 메인 입력 폼
with st.form("fortune_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("이름 또는 닉네임", placeholder="예: 김진환")
    with col2:
        birth_date = st.date_input("생년월일")
    
    category = st.selectbox(
        "궁금한 운세 테마를 선택하세요",
        ["종합 운세", "재물/사업 운", "연애/대인관계 운", "직장/학업 운", "오늘의 럭키 아이템"]
    )
    
    submit_button = st.form_submit_button(label="✨ 운세 확인하기")

# 운세 생성 로직
if submit_button:
    if API_KEY == "여기에_본인의_API_KEY를_입력하세요" or not API_KEY:
        st.error("⚠️ 코드 상단의 `API_KEY` 변수에 유효한 Google AI Studio API Key를 입력해주세요!")
    elif not name:
        st.warning("⚠️ 이름을 입력해주세요.")
    else:
        try:
            # 설정한 API Key로 클라이언트 초기화
            client = genai.Client(api_key=API_KEY)
            
            # 프롬프트 구성
            prompt = f"""
            당신은 유쾌하고 통찰력 있는 전문 점술가이자 AI 운세 상담사입니다.
            다음 정보를 바탕으로 오늘의 운세를 흥미롭고 구체적으로 작성해주세요.
            
            - 이름/닉네임: {name}
            - 생년월일: {birth_date}
            - 관심 테마: {category}
            - 오늘 날짜: 2026년 10월 16일
            
            다음 형식으로 마크다운을 활용해 예쁘고 보기 쉽게 출력해주세요:
            1. 🌟 **총운 요약** (한 줄 평 포함)
            2. 🎯 **선택 테마 상세 운세** ({category}에 집중해서)
            3. 🍀 **오늘의 럭키 포인트** (행운의 색상, 숫자, 시간대, 아이템)
            4. 💪 **오늘의 조언 및 응원 메시지**
            
            말투는 다정하고 긍정적이면서도 재치 있게 작성해주세요.
            """
            
            with st.spinner("🔮 우주의 기운을 모아 오늘의 운세를 점치는 중입니다..."):
                # 무료 플랜으로 가장 빠르고 안정적인 gemini-2.5-flash 모델 사용
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
            
            # 결과 출력
            st.success("🎉 운세 분석이 완료되었습니다!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.error("API Key가 올바른지, 인터넷 연결이 원활한지 확인해주세요.")
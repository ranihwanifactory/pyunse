from datetime import date, timedelta
import streamlit as st
from google import genai

# 📌 여기에 발급받으신 Google AI Studio API Key를 직접 입력하세요.
API_KEY = "AQ.Ab8RN6LcpBwAaf8Br3PlrD0ZXRheaP1s9lO7-nEB8Jh5iL9QGQ"

# 페이지 설정
st.set_page_config(
    page_title="✨ 오늘의 AI 운세 & 궁합", page_icon="🔮", layout="centered"
)

st.title("🔮 AI 실시간 운세 & 궁합 서비스")
st.write("오늘의 운세를 확인하거나, 소중한 인연과의 궁합을 확인해보세요!")

# 상단 탭 메뉴 생성 (1. 오늘의 운세 / 2. 운명적 궁합 보기)
tab1, tab2 = st.tabs(["✨ 오늘의 운세", "💕 AI 운명 궁합 보기"])

# ==================== [탭 1] 오늘의 운세 ====================
with tab1:
  st.subheader("🌟 오늘의 운세 확인하기")

  with st.form("fortune_form"):
    col1, col2 = st.columns(2)
    with col1:
      name = st.text_input("이름 또는 닉네임", placeholder="예: 김진환")
    with col2:
      today = date.today()
      min_birth_date = today - timedelta(days=365 * 100)
      birth_date = st.date_input(
          "생년월일",
          value=date(1980, 11, 21),
          min_value=min_birth_date,
          max_value=today,
          key="fortune_birth",
      )

    category = st.selectbox(
        "궁금한 운세 테마를 선택하세요",
        [
            "종합 운세",
            "재물/사업 운",
            "연애/대인관계 운",
            "직장/학업 운",
            "오늘의 럭키 아이템",
        ],
    )

    submit_fortune = st.form_submit_button(label="✨ 운세 확인하기")

  if submit_fortune:
    if API_KEY == "여기에_본인의_API_KEY를_입력하세요" or not API_KEY:
      st.error(
          "⚠️ 코드 상단의 `API_KEY` 변수에 유효한 Google AI Studio API Key를"
          " 입력해주세요!"
      )
    elif not name:
      st.warning("⚠️ 이름을 입력해주세요.")
    else:
      try:
        client = genai.Client(api_key=API_KEY)
        prompt = f"""
                당신은 유쾌하고 통찰력 있는 전문 점술가이자 AI 운세 상담사입니다.
                다음 정보를 바탕으로 오늘의 운세를 흥미롭고 구체적으로 작성해주세요.
                
                - 이름/닉네임: {name}
                - 생년월일: {birth_date}
                - 관심 테마: {category}
                - 오늘 날짜: {today.strftime('%Y년 %m월 %d일')}
                
                다음 형식으로 마크다운을 활용해 예쁘고 보기 쉽게 출력해주세요:
                1. 🌟 **총운 요약** (한 줄 평 포함)
                2. 🎯 **선택 테마 상세 운세** ({category}에 집중해서)
                3. 🍀 **오늘의 럭키 포인트** (행운의 색상, 숫자, 시간대, 아이템)
                4. 💪 **오늘의 조언 및 응원 메시지**
                
                말투는 다정하고 긍정적이면서도 재치 있게 작성해주세요.
                """

        with st.spinner("🔮 우주의 기운을 모아 오늘의 운세를 점치는 중입니다..."):
          response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=prompt,
          )

        st.success("🎉 운세 분석이 완료되었습니다!")
        st.markdown("---")
        st.markdown(response.text)

      except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# ==================== [탭 2] AI 운명 궁합 보기 ====================
with tab2:
  st.subheader("💕 두 사람의 운명적 궁합 보기")
  st.write("연인, 친구, 비즈니스 파트너 등 궁금한 상대와의 궁합을 확인해보세요!")

  with st.form("compatibility_form"):
    st.markdown("##### 👤 첫 번째 분 정보")
    col1, col2 = st.columns(2)
    with col1:
      person1_name = st.text_input("이름 (첫 번째)", placeholder="예: 김진환")
    with col2:
      person1_birth = st.date_input(
          "생년월일 (첫 번째)",
          value=date(1980, 11, 21),
          min_value=min_birth_date,
          max_value=today,
          key="p1_birth",
      )

    st.markdown("---")
    st.markdown("##### 🧑 두 번째 분 정보")
    col3, col4 = st.columns(2)
    with col3:
      person2_name = st.text_input("이름 (두 번째)", placeholder="예: 아내")
    with col4:
      person2_birth = st.date_input(
          "생년월일 (두 번째)",
          value=date(1982, 5, 15),
          min_value=min_birth_date,
          max_value=today,
          key="p2_birth",
      )

    relation_type = st.selectbox(
        "두 사람의 관계를 선택하세요",
        ["연인 / 부부", "비즈니스 / 동업자", "친구 / 동료", "가족"],
    )

    submit_compat = st.form_submit_button(label="💖 궁합 확인하기")

  if submit_compat:
    if API_KEY == "여기에_본인의_API_KEY를_입력하세요" or not API_KEY:
      st.error(
          "⚠️ 코드 상단의 `API_KEY` 변수에 유효한 Google AI Studio API Key를"
          " 입력해주세요!"
      )
    elif not person1_name or not person2_name:
      st.warning("⚠️ 두 분의 이름을 모두 입력해주세요.")
    else:
      try:
        client = genai.Client(api_key=API_KEY)
        compat_prompt = f"""
                당신은 통찰력 있고 유머 감각 넘치는 최고급 사주/궁합 전문가 AI입니다.
                다음 두 사람의 정보를 바탕으로 깊이 있고 흥미진진한 궁합 분석을 제공해주세요.
                
                - 첫 번째 사람: {person1_name} (생년월일: {person1_birth})
                - 두 번째 사람: {person2_name} (생년월일: {person2_birth})
                - 관계 유형: {relation_type}
                
                다음 형식으로 마크다운을 활용해 예쁘고 보기 쉽게 출력해주세요:
                1. 💘 **종합 궁합 요약 및 점수** (100점 만점 점수 및 한 줄 평)
                2. ✨ **두 사람의 성향과 시너지** (서로의 장단점이 어떻게 보완되는지)
                3. ⚠️ **주의해야 할 점 및 갈등 해소 팁** ({relation_type} 관계에서 조심할 점)
                4. 🌟 **함께 할 때 운을 높여주는 방법 / 행운의 아이템**
                
                말투는 다정하고 재치 있으며, 두 사람이 서로를 더 이해할 수 있도록 따뜻하게 작성해주세요.
                """

        with st.spinner("💖 두 분의 별자리와 사주 기운을 조율하는 중입니다..."):
          compat_response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=compat_prompt,
          )

        st.success("🎉 궁합 분석이 완료되었습니다!")
        st.markdown("---")
        st.markdown(compat_response.text)

      except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

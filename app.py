from datetime import date, timedelta
import random
import streamlit as st
from google import genai

# 📌 여기에 발급받으신 Google AI Studio API Key를 직접 입력하세요.
API_KEY = "AQ.Ab8RN6LcpBwAaf8Br3PlrD0ZXRheaP1s9lO7-nEB8Jh5iL9QGQ"

# 페이지 설정
st.set_page_config(
    page_title="✨ AI 운세 & 궁합 & 로또 & 연예인",
    page_icon="🔮",
    layout="centered",
)

st.title("🔮 AI 실시간 운세 & 궁합 & 로또 & 연예인 매칭")
st.write(
    "운세, 궁합, 로또 번호는 물론 나와 생일이 같은 연예인과 닮은꼴 매칭까지"
    " 확인해보세요!"
)

# 상단 탭 메뉴 생성 (4개 탭)
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "✨ 오늘의 운세",
        "💕 AI 운명 궁합 보기",
        "🍀 나만의 로또 번호",
        "🌟 생일 연예인 & 닮은꼴",
    ]
)

# 공통 날짜 범위 (100년 전부터 오늘까지)
today = date.today()
min_birth_date = today - timedelta(days=365 * 100)


# ==================== [탭 1] 오늘의 운세 ====================
with tab1:
  st.subheader("🌟 오늘의 운세 확인하기")

  with st.form("fortune_form"):
    col1, col2 = st.columns(2)
    with col1:
      name = st.text_input("이름 또는 닉네임", placeholder="예: 김진환")
    with col2:
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


# ==================== [탭 3] 나만의 로또 번호 생성기 ====================
with tab3:
  st.subheader("🍀 AI 맞춤 로또 번호 생성기")
  st.write(
      "이름과 생년월일의 기운을 담아, AI가 특별한 로또 번호 조합을"
      " 선물해드립니다!"
  )

  with st.form("lotto_form"):
    col1, col2 = st.columns(2)
    with col1:
      lotto_name = st.text_input("이름 또는 닉네임", placeholder="예: 김진환")
    with col2:
      lotto_birth = st.date_input(
          "생년월일",
          value=date(1980, 11, 21),
          min_value=min_birth_date,
          max_value=today,
          key="lotto_birth",
      )

    lotto_style = st.selectbox(
        "로또 번호 추출 스타일",
        [
            "🔮 AI 기운 집중형 (사주/별자리 맞춤 번호)",
            "🔥 대박 재물운 집중형",
            "🎲 순수 행운 무작위형",
        ],
    )

    submit_lotto = st.form_submit_button(label="🎰 행운의 로또 번호 조합하기")

  if submit_lotto:
    if API_KEY == "여기에_본인의_API_KEY를_입력하세요" or not API_KEY:
      st.error(
          "⚠️ 코드 상단의 `API_KEY` 변수에 유효한 Google AI Studio API Key를"
          " 입력해주세요!"
      )
    elif not lotto_name:
      st.warning("⚠️ 이름을 입력해주세요.")
    else:
      try:
        client = genai.Client(api_key=API_KEY)
        random_sets = [
            sorted(random.sample(range(1, 46), 6)) for _ in range(5)
        ]

        lotto_prompt = f"""
                당신은 재치 있고 영감 넘치는 로또 번호 추천 도사입니다.
                다음 사용자의 정보를 바탕으로 1부터 45 사이의 수 중 6개로 이루어진 로또 번호 조합 5게임을 추천해주고, 각 게임별 의미와 오늘의 재물운 조언을 들려주세요.
                
                - 사용자: {lotto_name}
                - 생년월일: {lotto_birth}
                - 스타일: {lotto_style}
                - 오늘 날짜: {today.strftime('%Y년 %m월 %d일')}
                
                출력 형식:
                - 5게임의 번호 (예: 1게임: [3, 12, 22, 27, 33, 41])
                - 각 번호 조합에 대한 재치 있는 해설 및 오늘의 재물 기운 조언
                - 마지막에 대박을 기원하는 유쾌한 응원 한마디!
                """

        with st.spinner("🍀 행운의 주파수를 맞추고 로또 번호를 조합 중입니다..."):
          lotto_response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=lotto_prompt,
          )

        st.success("🎉 나만의 행운 로또 번호가 완성되었습니다!")
        st.markdown("---")

        st.markdown("### 🎲 시스템 추천 행운 번호 (5게임)")
        for i, s_num in enumerate(random_sets, 1):
          formatted_nums = ", ".join([f"`{n:02d}`" for n in s_num])
          st.markdown(f"**{i}게임:** {formatted_nums}")

        st.markdown("---")
        st.markdown("### 📜 AI 도사의 맞춤 로또 해설 & 조언")
        st.markdown(lotto_response.text)

      except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")


# ==================== [탭 4] 생일 연예인 & 닮은꼴 매칭 ====================
with tab4:
  st.subheader("🌟 생일이 같은 연예인 & 닮은꼴 매칭")
  st.write(
      "나와 생년월일(또는 생일)이 같은 연예인을 알아보고, AI가 분석해 주는"
      " 연예인 닮은꼴 스타일을 확인해보세요!"
  )

  with st.form("celeb_form"):
    col1, col2 = st.columns(2)
    with col1:
      celeb_name = st.text_input("이름 또는 닉네임", placeholder="예: 김진환")
    with col2:
      celeb_birth = st.date_input(
          "생년월일",
          value=date(1980, 11, 21),
          min_value=min_birth_date,
          max_value=today,
          key="celeb_birth",
      )

    submit_celeb = st.form_submit_button(label="✨ 연예인 매칭 분석하기")

  if submit_celeb:
    if API_KEY == "여기에_본인의_API_KEY를_입력하세요" or not API_KEY:
      st.error(
          "⚠️ 코드 상단의 `API_KEY` 변수에 유효한 Google AI Studio API Key를"
          " 입력해주세요!"
      )
    elif not celeb_name:
      st.warning("⚠️ 이름을 입력해주세요.")
    else:
      try:
        client = genai.Client(api_key=API_KEY)

        celeb_prompt = f"""
                당신은 유머러스하고 트렌드에 밝은 연예계 전문 AI 분석가입니다.
                다음 사용자의 생년월일과 이름을 바탕으로 흥미로운 연예인 매칭 정보를 제공해주세요.
                
                - 사용자 이름: {celeb_name}
                - 생년월일: {celeb_birth} (월/일 및 연도 참고)
                
                다음 형식으로 마크다운을 활용해 예쁘고 보기 쉽게 출력해주세요:
                1. 🎂 **같은 생일(월/일)을 가진 대표 연예인** (실제로 해당 생일이거나 비슷한 시기에 태어난 국내외 유명 연예인, 배우, 가수 등을 2~3명 언급하고 간단한 설명 첨부)
                2. ✨ **나와 분위기/스타일이 닮은 연예인 닮은꼴 매칭** (사주적 기운, 성향, 이미지 매칭을 통해 가장 닮았거나 매치가 잘 되는 연예인 1~2명을 재치 있게 선정하고 이유 설명)
                3. 🎭 **두 사람의 공통적인 매력 포인트 및 기운**
                4. 💖 **오늘 하루 연예인처럼 빛날 수 있는 스타일링 팁**
                
                말투는 매우 재치 있고 유쾌하며, 기분 좋게 읽을 수 있도록 작성해주세요.
                """

        with st.spinner(
            "🌟 연예계 데이터베이스와 기운을 스캔하여 닮은꼴을 찾는 중입니다..."
        ):
          celeb_response = client.models.generate_content(
              model="gemini-2.5-flash",
              contents=celeb_prompt,
          )

        st.success("🎉 연예인 닮은꼴 매칭 분석이 완료되었습니다!")
        st.markdown("---")
        st.markdown(celeb_response.text)

      except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

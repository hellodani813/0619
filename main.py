import streamlit as st
import random

st.set_page_config(
    page_title="🌟 MBTI 진로 탐험대 🌟",
    page_icon="🚀",
    layout="wide"
)

# =========================
# 스타일
# =========================

st.markdown("""
<style>
.main {
    background: linear-gradient(180deg,#fef6ff,#f5f9ff);
}

.big-title{
    text-align:center;
    font-size:3rem;
    font-weight:800;
    color:#6c4df6;
    margin-bottom:0;
}

.sub-title{
    text-align:center;
    font-size:1.2rem;
    color:#555;
    margin-bottom:30px;
}

.career-card{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom:15px;
}

.result-box{
    background:linear-gradient(135deg,#fff5cc,#ffe7f3);
    padding:25px;
    border-radius:25px;
    border:3px solid #ffd54f;
}

.footer{
    text-align:center;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 데이터
# =========================

career_data = {
    "INTJ": [
        ("🧠 데이터 과학자", "데이터를 분석하여 미래를 예측해요."),
        ("🏗️ 건축가", "창의적인 공간을 설계해요."),
        ("💻 AI 개발자", "인공지능 기술을 만들어요.")
    ],
    "INTP": [
        ("🔬 연구원", "새로운 지식을 발견해요."),
        ("💻 소프트웨어 개발자", "프로그램을 만들어요."),
        ("📊 분석가", "복잡한 문제를 해결해요.")
    ],
    "ENTJ": [
        ("🏢 CEO", "회사를 이끌어요."),
        ("📈 경영 컨설턴트", "기업의 성장을 도와요."),
        ("⚖️ 변호사", "법률 전문가예요.")
    ],
    "ENTP": [
        ("🚀 창업가", "새로운 사업을 만들어요."),
        ("📣 마케터", "사람들에게 제품을 알려요."),
        ("🎤 방송인", "재미있는 콘텐츠를 만들어요.")
    ],
    "INFJ": [
        ("🧑‍🏫 교사", "학생들의 성장을 도와요."),
        ("💚 상담사", "사람들의 고민을 들어줘요."),
        ("✍️ 작가", "이야기를 창작해요.")
    ],
    "INFP": [
        ("🎨 디자이너", "창의적인 작품을 만들어요."),
        ("📚 작가", "글을 통해 생각을 표현해요."),
        ("🎼 음악가", "음악을 만들고 연주해요.")
    ],
    "ENFJ": [
        ("🎓 교수", "학생들을 가르쳐요."),
        ("🤝 HR 전문가", "사람과 조직을 연결해요."),
        ("🎤 강연가", "영감을 주는 이야기를 해요.")
    ],
    "ENFP": [
        ("🎬 콘텐츠 크리에이터", "재미있는 콘텐츠를 만들어요."),
        ("🎭 배우", "다양한 역할을 연기해요."),
        ("🌏 여행 작가", "세상을 경험하고 기록해요.")
    ],
    "ISTJ": [
        ("🏦 회계사", "기업의 재정을 관리해요."),
        ("👮 경찰관", "사회를 안전하게 지켜요."),
        ("🏛️ 공무원", "국민을 위해 일해요.")
    ],
    "ISFJ": [
        ("🏥 간호사", "환자를 돌봐요."),
        ("👩‍🏫 초등교사", "아이들을 가르쳐요."),
        ("💊 약사", "의약품 전문가예요.")
    ],
    "ESTJ": [
        ("📋 프로젝트 매니저", "프로젝트를 관리해요."),
        ("🏢 관리자", "조직을 운영해요."),
        ("⚖️ 판사", "공정한 판결을 내려요.")
    ],
    "ESFJ": [
        ("🎉 이벤트 기획자", "행사를 준비해요."),
        ("🏨 호텔리어", "고객을 응대해요."),
        ("👩‍⚕️ 의료 코디네이터", "병원 서비스를 지원해요.")
    ],
    "ISTP": [
        ("✈️ 항공정비사", "비행기를 점검해요."),
        ("🔧 엔지니어", "기술 문제를 해결해요."),
        ("🚗 자동차 전문가", "자동차를 설계·정비해요.")
    ],
    "ISFP": [
        ("📸 사진작가", "순간을 기록해요."),
        ("🎨 일러스트레이터", "그림을 그려요."),
        ("🌸 플로리스트", "꽃을 디자인해요.")
    ],
    "ESTP": [
        ("🏅 스포츠 선수", "경기에 참여해요."),
        ("📢 영업 전문가", "고객을 만나 소통해요."),
        ("🎤 MC", "행사를 진행해요.")
    ],
    "ESFP": [
        ("🎬 연예인", "대중에게 즐거움을 줘요."),
        ("🎪 공연 기획자", "멋진 공연을 만들어요."),
        ("📺 유튜버", "영상 콘텐츠를 제작해요.")
    ]
}

# =========================
# 헤더
# =========================

st.markdown(
    "<h1 class='big-title'>🌟 MBTI 진로 탐험대 🌟</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>🚀 나의 MBTI로 알아보는 미래 직업 추천!</p>",
    unsafe_allow_html=True
)

st.balloons()

# =========================
# 선택
# =========================

mbti = st.selectbox(
    "✨ 나의 MBTI를 선택해보세요!",
    sorted(career_data.keys())
)

st.write("")

if st.button("🔮 진로 추천 받기!", use_container_width=True):

    careers = career_data[mbti]

    st.markdown(
        f"""
        <div class='result-box'>
        <h2>🎉 {mbti} 유형 추천 결과 🎉</h2>
        <p>당신의 성향과 잘 어울리는 직업들을 소개할게요!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    for job, desc in careers:

        score = random.randint(85, 99)

        st.markdown(
            f"""
            <div class='career-card'>
            <h3>{job}</h3>
            <p>{desc}</p>
            <p>🌟 적합도: <b>{score}%</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(score / 100)

    st.success("🎯 진로 탐색은 참고용입니다. 다양한 경험을 통해 나만의 꿈을 찾아보세요!")

    st.snow()

# =========================
# 하단
# =========================

st.write("")
st.write("")

st.markdown(
    """
    <div class='footer'>
    💜 꿈은 정해지는 것이 아니라 만들어가는 것입니다 💜<br>
    🌈 여러분의 미래를 응원합니다! 🌈
    </div>
    """,
    unsafe_allow_html=True
)

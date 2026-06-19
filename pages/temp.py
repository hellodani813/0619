import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울 날씨 타임머신",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 날씨 타임머신")
st.markdown(
    """
오늘의 기온과 가장 비슷했던 과거의 날짜를 찾아보세요.
"""
)

# ----------------------------
# 데이터 로드
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "ta_20260619190504(1).csv",
        encoding="cp949"
    )

    df.columns = [
        "date",
        "station",
        "avg_temp",
        "min_temp",
        "max_temp"
    ]

    df["date"] = pd.to_datetime(df["date"])

    return df


df = load_data()

# ----------------------------
# 날짜 선택
# ----------------------------
selected_date = st.date_input(
    "날짜 선택",
    value=df["date"].max().date()
)

selected_date = pd.to_datetime(selected_date)

row = df[df["date"] == selected_date]

if row.empty:
    st.error("선택한 날짜 데이터가 없습니다.")
    st.stop()

target_temp = row.iloc[0]["avg_temp"]

# ----------------------------
# 현재 날짜 정보
# ----------------------------
st.subheader("선택한 날짜")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("평균기온", f"{target_temp:.1f}℃")

with col2:
    st.metric("최저기온", f"{row.iloc[0]['min_temp']:.1f}℃")

with col3:
    st.metric("최고기온", f"{row.iloc[0]['max_temp']:.1f}℃")

# ----------------------------
# 비슷한 날 찾기
# ----------------------------
similar_df = df.copy()

similar_df["temp_diff"] = (
    similar_df["avg_temp"] - target_temp
).abs()

similar_df = similar_df[
    similar_df["date"] != selected_date
]

top10 = (
    similar_df
    .sort_values("temp_diff")
    .head(10)
)

st.subheader("🔍 역사상 가장 비슷한 날 TOP 10")

display_df = top10[
    [
        "date",
        "avg_temp",
        "min_temp",
        "max_temp",
        "temp_diff"
    ]
].copy()

display_df.columns = [
    "날짜",
    "평균기온",
    "최저기온",
    "최고기온",
    "차이"
]

st.dataframe(
    display_df,
    use_container_width=True
)

# ----------------------------
# 그래프
# ----------------------------
chart_df = top10.copy()

chart_df["label"] = (
    chart_df["date"]
    .dt.strftime("%Y-%m-%d")
)

fig = px.bar(
    chart_df,
    x="label",
    y="avg_temp",
    title="비슷한 날짜 평균기온 비교",
)

fig.add_hline(
    y=target_temp,
    line_dash="dash",
    annotation_text=f"선택 날짜 ({target_temp:.1f}℃)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------
# 가장 비슷한 날
# ----------------------------
best_match = top10.iloc[0]

st.subheader("🏆 가장 비슷했던 날")

st.success(
    f"""
    {best_match['date'].strftime('%Y-%m-%d')}

    평균기온: {best_match['avg_temp']:.1f}℃
    
    차이: {best_match['temp_diff']:.2f}℃
    """
)

# ----------------------------
# 통계
# ----------------------------
st.subheader("📊 선택 기온의 위치")

percentile = (
    (df["avg_temp"] < target_temp).mean()
    * 100
)

st.info(
    f"""
    평균기온 {target_temp:.1f}℃ 는

    1907~2026 서울 관측 데이터 기준
    상위 {100-percentile:.1f}% 수준입니다.
    """
)

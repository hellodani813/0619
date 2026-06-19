import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

st.set_page_config(
page_title="서울 기후 타임머신",
page_icon="🌡️",
layout="wide"
)

# --------------------

# 데이터 로드

# --------------------

@st.cache_data
def load_data():
df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")


# 컬럼명 정리
df.columns = [
    "date",
    "station",
    "avg_temp",
    "min_temp",
    "max_temp"
]

df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day

return df
```

df = load_data()

# --------------------

# 헤더

# --------------------

st.title("🌡️ 서울 기후 타임머신")
st.caption("1907 ~ 2026 서울 기온 데이터 탐험")

col1, col2, col3 = st.columns(3)

with col1:
st.metric("총 데이터 수", f"{len(df):,}")

with col2:
st.metric("시작 연도", int(df["year"].min()))

with col3:
st.metric("마지막 연도", int(df["year"].max()))

st.divider()

# --------------------

# 날짜 선택

# --------------------

st.header("📅 특정 날짜의 역사")

col1, col2 = st.columns(2)

with col1:
selected_month = st.selectbox(
"월 선택",
list(range(1, 13)),
index=datetime.now().month - 1
)

with col2:
selected_day = st.selectbox(
"일 선택",
list(range(1, 32)),
index=min(datetime.now().day - 1, 30)
)

filtered = df[
(df["month"] == selected_month)
& (df["day"] == selected_day)
]

if len(filtered) > 0:


fig = px.line(
    filtered,
    x="year",
    y="avg_temp",
    title=f"{selected_month}월 {selected_day}일 평균기온 변화",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

hottest = filtered.loc[filtered["max_temp"].idxmax()]
coldest = filtered.loc[filtered["min_temp"].idxmin()]

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"""


가장 더웠던 날

연도: {int(hottest['year'])}
최고기온: {hottest['max_temp']:.1f}℃
"""
)


with col2:
    st.info(
        f"""


가장 추웠던 날

연도: {int(coldest['year'])}
최저기온: {coldest['min_temp']:.1f}℃
"""
)

st.divider()

# --------------------

# 태어난 해 비교

# --------------------

st.header("🎂 내가 태어난 해와 비교")

birth_year = st.number_input(
"출생연도",
min_value=int(df["year"].min()),
max_value=int(df["year"].max()),
value=1990
)

birth_data = df[df["year"] == birth_year]
latest_data = df[df["year"] == df["year"].max()]

if len(birth_data) > 0:


birth_avg = birth_data["avg_temp"].mean()
latest_avg = latest_data["avg_temp"].mean()

diff = latest_avg - birth_avg

st.metric(
    "연평균기온 변화",
    f"{latest_avg:.2f}℃",
    f"{diff:+.2f}℃"
)


st.divider()

# --------------------

# 연도별 평균기온

# --------------------

st.header("📈 서울 평균기온 추세")

yearly = (
df.groupby("year")["avg_temp"]
.mean()
.reset_index()
)

fig2 = px.line(
yearly,
x="year",
y="avg_temp",
title="1907~2026 연평균기온"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --------------------

# 역대 기록

# --------------------

st.header("🔥 역대 최고기온 TOP 10")

top_hot = (
df.sort_values(
by="max_temp",
ascending=False
)
[["date", "max_temp"]]
.head(10)
)

st.dataframe(
top_hot,
use_container_width=True
)

st.header("❄️ 역대 최저기온 TOP 10")

top_cold = (
df.sort_values(
by="min_temp",
ascending=True
)
[["date", "min_temp"]]
.head(10)
)

st.dataframe(
top_cold,
use_container_width=True
)

st.divider()

# --------------------

# 오늘 날짜의 역사적 위치

# --------------------

st.header("🏆 오늘은 역사상 얼마나 더운 날일까?")

today = datetime.now()

today_hist = df[
(df["month"] == today.month)
& (df["day"] == today.day)
]

if len(today_hist) > 0:


current_temp = today_hist.iloc[-1]["avg_temp"]

percentile = (
    today_hist["avg_temp"]
    .rank(pct=True)
    .iloc[-1]
    * 100
)

st.metric(
    "역사적 백분위",
    f"{percentile:.1f}%"
)

fig3 = px.histogram(
    today_hist,
    x="avg_temp",
    nbins=20,
    title="같은 날짜의 역사적 기온 분포"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


st.success("서울 기후 타임머신 MVP 실행 완료 🚀")

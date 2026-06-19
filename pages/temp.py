import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="서울 기후 타임머신",
page_icon="🌡️",
layout="wide"
)

st.title("🌡️ 서울 기후 타임머신")

# CSV 읽기

try:
df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")
except:
df = pd.read_csv("ta_20260619190504.csv", encoding="cp949")

# 컬럼명 확인

st.subheader("원본 컬럼")
st.write(df.columns.tolist())

# 컬럼이 5개라고 가정

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

st.success("데이터 로드 성공")

st.metric("총 데이터 수", len(df))

# 연평균 기온

yearly = (
df.groupby("year")["avg_temp"]
.mean()
.reset_index()
)

fig = px.line(
yearly,
x="year",
y="avg_temp",
title="서울 연평균 기온 변화"
)

st.plotly_chart(fig, use_container_width=True)

# 날짜 선택

month = st.selectbox("월", range(1, 13))
day = st.selectbox("일", range(1, 32))

filtered = df[
(df["month"] == month)
& (df["day"] == day)
]

if len(filtered) > 0:
fig2 = px.line(
filtered,
x="year",
y="avg_temp",
title=f"{month}월 {day}일 기온 변화"
)


st.plotly_chart(fig2, use_container_width=True)

hottest = filtered.loc[filtered["max_temp"].idxmax()]

st.write(
    f"역대 최고기온: {hottest['max_temp']}℃ ({int(hottest['year'])}년)"
)
```

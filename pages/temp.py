import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="서울 기후 타임머신",
page_icon="🌡️",
layout="wide"
)

@st.cache_data
def load_data():
df = pd.read_csv(
"ta_20260619190504.csv",
encoding="utf-8-sig"
)

```
df["날짜"] = (
    df["날짜"]
    .astype(str)
    .str.strip()
)

df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month
df["일"] = df["날짜"].dt.day

return df
```

df = load_data()

st.title("🌡️ 서울 기후 타임머신")
st.caption("1907 ~ 2026 서울 기온 데이터")

col1, col2, col3 = st.columns(3)

with col1:
st.metric(
"총 데이터 수",
f"{len(df):,}"
)

with col2:
st.metric(
"시작 연도",
int(df["연도"].min())
)

with col3:
st.metric(
"마지막 연도",
int(df["연도"].max())
)

st.divider()

st.header("📈 서울 평균기온 변화")

yearly = (
df.groupby("연도")["평균기온(℃)"]
.mean()
.reset_index()
)

fig = px.line(
yearly,
x="연도",
y="평균기온(℃)",
markers=True,
title="1907~2026 연평균 기온"
)

st.plotly_chart(
fig,
use_container_width=True
)

st.divider()

st.header("📅 특정 날짜 비교")

month = st.selectbox(
"월 선택",
list(range(1, 13))
)

day = st.selectbox(
"일 선택",
list(range(1, 32))
)

filtered = df[
(df["월"] == month)
& (df["일"] == day)
]

if len(filtered) > 0:

```
fig2 = px.line(
    filtered,
    x="연도",
    y="평균기온(℃)",
    title=f"{month}월 {day}일 기온 변화",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

hottest = filtered.loc[
    filtered["최고기온(℃)"].idxmax()
]

coldest = filtered.loc[
    filtered["최저기온(℃)"].idxmin()
]

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"""
```

역대 가장 더운 {month}월 {day}일

연도: {int(hottest['연도'])}

최고기온: {hottest['최고기온(℃)']}℃
"""
)

```
with col2:
    st.info(
        f"""
```

역대 가장 추운 {month}월 {day}일

연도: {int(coldest['연도'])}

최저기온: {coldest['최저기온(℃)']}℃
"""
)

st.divider()

st.header("🔥 역대 최고기온 TOP 10")

top_hot = (
df.sort_values(
"최고기온(℃)",
ascending=False
)
[["날짜", "최고기온(℃)"]]
.head(10)
)

st.dataframe(
top_hot,
use_container_width=True
)

st.divider()

st.header("❄️ 역대 최저기온 TOP 10")

top_cold = (
df.sort_values(
"최저기온(℃)",
ascending=True
)
[["날짜", "최저기온(℃)"]]
.head(10)
)

st.dataframe(
top_cold,
use_container_width=True
)

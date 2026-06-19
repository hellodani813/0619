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
df = pd.read_csv("ta_20260619190504.csv", encoding="cp949")
except Exception:
df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")

st.write("컬럼명 확인:")
st.write(df.columns.tolist())

# 날짜 컬럼 자동 찾기

date_col = df.columns[0]

df[date_col] = pd.to_datetime(df[date_col])

df["year"] = df[date_col].dt.year
df["month"] = df[date_col].dt.month
df["day"] = df[date_col].dt.day

# 숫자 컬럼 찾기

numeric_cols = []

for col in df.columns:
try:
pd.to_numeric(df[col])
numeric_cols.append(col)
except Exception:
pass

st.write("숫자 컬럼:", numeric_cols)

if len(numeric_cols) == 0:
st.error("숫자형 기온 컬럼을 찾을 수 없습니다.")
st.stop()

temp_col = numeric_cols[0]

df[temp_col] = pd.to_numeric(df[temp_col], errors="coerce")

st.success("데이터 로드 성공")

st.metric("총 데이터 수", len(df))

# 연도별 평균

yearly = (
df.groupby("year")[temp_col]
.mean()
.reset_index()
)

fig = px.line(
yearly,
x="year",
y=temp_col,
title="서울 기온 변화"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("특정 날짜 비교")

month = st.selectbox("월", list(range(1, 13)))
day = st.selectbox("일", list(range(1, 32)))

filtered = df[
(df["month"] == month)
& (df["day"] == day)
]

if len(filtered) > 0:

```
fig2 = px.line(
    filtered,
    x="year",
    y=temp_col,
    title=f"{month}월 {day}일 기온 변화"
)

st.plotly_chart(fig2, use_container_width=True)

st.write(filtered[[date_col, temp_col]].tail())
```

st.subheader("원본 데이터")

st.dataframe(df.head(20))

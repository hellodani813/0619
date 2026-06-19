import streamlit as st
import pandas as pd

# -----------------------------------
# 페이지 설정
# -----------------------------------

st.set_page_config(
    page_title="CSV 데이터 조회",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV 데이터 조회")

# -----------------------------------
# CSV 읽기
# -----------------------------------

csv_file = "ta_20260619190504.csv"

try:

    df = None

    encodings = [
        "utf-8-sig",
        "utf-8",
        "cp949",
        "euc-kr"
    ]

    for enc in encodings:
        try:
            df = pd.read_csv(csv_file, encoding=enc)
            st.success(f"✅ 파일 로드 성공 (인코딩: {enc})")
            break
        except:
            pass

    if df is None:
        st.error("❌ 파일을 읽을 수 없습니다.")
        st.stop()

    # -----------------------------------
    # 데이터 정보
    # -----------------------------------

    st.subheader("📋 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 데이터 정보")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("행 개수", len(df))

    with col2:
        st.metric("열 개수", len(df.columns))

    st.subheader("🏷️ 컬럼 목록")

    for col in df.columns:
        st.write(f"• {col}")

except Exception as e:

    st.error(
        f"""
        데이터를 읽어오는 중 오류가 발생했습니다.

        오류 메시지:
        {e}
        """
    )
# -----------------------------------
# 날짜 검색
# -----------------------------------

st.subheader("📅 날짜 검색")

# 날짜 컬럼 선택
date_column = st.selectbox(
    "날짜 컬럼 선택",
    df.columns
)

search_date = st.date_input(
    "조회할 날짜 선택"
)

try:
    # 날짜형 변환
    df[date_column] = pd.to_datetime(
        df[date_column],
        errors="coerce"
    )

    filtered_df = df[
        df[date_column].dt.date == search_date
    ]

    st.write(
        f"🔍 {search_date} 검색 결과: {len(filtered_df)}건"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

except Exception:
    st.warning(
        "선택한 컬럼이 날짜 형식이 아닙니다."
    )

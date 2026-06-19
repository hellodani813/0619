import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="서울 기온 역사 데이터 분석", layout="wide", page_icon="☀️")

st.title("☀️ 서울 기온 역사 데이터 대시보드 (1907~2026)")
st.markdown("업로드된 기상청 데이터를 바탕으로 서울의 기온 변화 트렌드를 분석하는 웹 앱입니다.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 데이터 읽기 (첫 번째 열의 공백 문자 제거 및 인코딩 처리)
    df = pd.read_csv("ta_20260619190504.csv", encoding="cp949")
    
    # 컬럼명 공백 제거 및 정리
    df.columns = df.columns.str.strip()
    
    # '날짜' 컬럼의 공백이나 탭 문자 제거 후 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거
    df = df.dropna(subset=['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    
    # 분석을 위한 연도, 월 컬럼 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    
    return df

try:
    df = load_data()
    
    # 3. 사이드바 - 필터링 설정
    st.sidebar.header("🔍 데이터 필터링")
    min_year = int(df['연도'].min())
    max_year = int(df['연도'].max())
    
    year_range = st.sidebar.slider(
        "조회할 연도 범위를 선택하세요:",
        min_value=min_year,
        max_value=max_year,
        value=(1980, max_year)
    )
    
    # 필터링된 데이터
    filtered_df = df[(df['연도'] >= year_range[0]) & (df['연o'] <= year_range[1])] if '연o' in df else df[(df['연도'] >= year_range[0]) & (df['연도'] <= year_range[1])]

    # 4. 주요 지표 (Metrics) 시각화
    st.subheader("📊 역대 최고 & 최저 기온 기록 (전체 기간)")
    col1, col2, col3 = st.columns(3)
    
    max_temp_row = df.loc[df['최고기온(℃)'].idxmax()]
    min_temp_row = df.loc[df['최저기온(℃)'].idxmin()]
    
    col1.metric("역대 최고 기온", f"{max_temp_row['최고기온(℃)']} ℃", f"{max_temp_row['날짜'].strftime('%Y-%m-%d')}")
    col2.metric("역대 최저 기온", f"{min_temp_row['최저기온(℃)']} ℃", f"{min_temp_row['날짜'].strftime('%Y-%m-%d')}")
    col3.metric("총 데이터 일수", f"{len(filtered_df):,} 일", f"선택 기간: {year_range[0]}~{year_range[1]}")
    
    st.markdown("---")
    
    # 5. 차트 섹션
    st.subheader("📈 연도별 평균 기온 변화 트렌드")
    # 연도별 평균 계산
    yearly_avg = filtered_df.groupby('연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].mean().reset_index()
    
    fig_line = px.line(
        yearly_avg, 
        x='연도', 
        y=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'],
        labels={'value': '기온 (℃)', 'variable': '구분'},
        title=f"{year_range[0]}년 ~ {year_range[1]}년 연평균 기온 추이"
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📅 월별 기온 분포 (박스플롯)")
        fig_box = px.box(
            filtered_df, 
            x='월', 
            y='평균기온(℃)',
            title="선택 기간 내 월별 평균기온 분포"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_right:
        st.subheader("🔝 선택 기간 역대 가장 더웠던 날 TOP 5")
        top5_hot = filtered_df.sort_values(by='최고기온(℃)', ascending=False).head(5)
        top5_hot['날짜'] = top5_hot['날짜'].dt.strftime('%Y-%m-%d')
        st.table(top5_hot[['날짜', '최고기온(℃)', '평균기온(℃)']].reset_index(drop=True))

    # 6. 데이터 원본 보기
    st.markdown("---")
    with st.expander("📄 필터링된 데이터 원본 보기"):
        st.dataframe(filtered_df.sort_values(by='날짜', ascending=False))

except Exception as e:
    st.error(f"데이터를 읽어오는 중 오류가 발생했습니다. 파일 형식을 확인해주세요. 오류 메시지: {e}")

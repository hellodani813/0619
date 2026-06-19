import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="서울 기온 역사 데이터 분석", layout="wide", page_icon="☀️")

st.title("☀️ 서울 기온 역사 데이터 및 날짜 검색 대시보드")
st.markdown("원하는 날짜를 선택하여 과거 서울의 기온 기록을 검색하고, 100년간의 기후 트렌드를 확인해 보세요.")

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data():
    # 데이터 읽기 (인코딩 처리)
    df = pd.read_csv("ta_20260619190504.csv")
    
    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()
    
    # '날짜' 컬럼의 공백 제거 및 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거
    df = df.dropna(subset=['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    
    # 분석용 연도, 월, 일 컬럼 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

try:
    df = load_data()
    
    # ----------------------------------------------------
    # 🔥 [기능 추가] 1. 특정 날짜 검색 섹션
    # ----------------------------------------------------
    st.header("🔍 특정 날짜 기온 검색")
    
    min_date = df['날짜'].min().to_pydatetime()
    max_date = df['날짜'].max().to_pydatetime()
    
    # 사용자에게 날짜 입력 받기 (기본값은 데이터의 가장 마지막 날짜)
    search_date = st.date_input(
        "궁금한 날짜를 선택하세요:",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )
    
    # 선택한 날짜 데이터 필터링
    target_date = pd.to_datetime(search_date)
    day_data = df[df['날짜'] == target_date]
    
    if not day_data.empty:
        row = day_data.iloc[0]
        st.success(f"📅 **{search_date.strftime('%Y년 %m월 %d일')}**의 서울 기온 기록입니다.")
        
        # 메트릭 카드로 깔끔하게 표시
        c1, c2, c3 = st.columns(3)
        c1.metric("💡 평균 기온", f"{row['평균기온(℃)']} ℃")
        c2.metric("💙 최저 기온", f"{row['최저기온(℃)']} ℃")
        c3.metric("❤️ 최고 기온", f"{row['최고기온(℃)']} ℃")
        
        # 역대 같은 날짜(월-일)의 기온 변화 그래프 시각화
        st.subheader(f"📈 역대 {search_date.strftime('%m월 %d일')}의 기온 변화 추이")
        same_day_df = df[(df['월'] == target_date.month) & (df['일'] == target_date.day)].sort_values('연도')
        
        fig_same_day = px.line(
            same_day_df,
            x='연도',
            y=['평균기온(℃)', '최저기온(℃)', '최고기온(℃)'],
            labels={'value': '기온 (℃)', 'variable': '구분'},
            title=f"역대 {target_date.month}월 {target_date.day}일의 기온 추이 ({same_day_df['연도'].min()}년 ~ {same_day_df['연도'].max()}년)"
        )
        st.plotly_chart(fig_same_day, use_container_width=True)
        
    else:
        st.warning("해당 날짜의 데이터가 존재하지 않습니다.")
        
    st.markdown("---")
    
    # ----------------------------------------------------
    # 2. 기간별 데이터 분석 및 트렌드 섹션 (기존 기능 유지)
    # ----------------------------------------------------
    st.header("📊 기간별 기후 트렌드 분석")
    
    # 사이드바 필터
    st.sidebar.header("🔍 기간 필터링")
    year_range = st.sidebar.slider(
        "조회할 연도 범위를 선택하세요:",
        min_value=int(df['연도'].min()),
        max_value=int(df['연도'].max()),
        value=(1980, int(df['연도'].max()))
    )
    
    filtered_df = df[(df['연도'] >= year_range[0]) & (df['연도'] <= year_range[1])]
    
    # 연도별 평균 기온 그래프
    yearly_avg = filtered_df.groupby('연度' if '연度' in df else '연도')[['평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].mean().reset_index()
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
        fig_box = px.box(filtered_df, x='월', y='평균기온(℃)', title="선택 기간 내 월별 평균기온 분포")
        st.plotly_chart(fig_box, use_container_width=True)
        
    with col_right:
        st.subheader("🔝 선택 기간 내 가장 더웠던 날 TOP 5")
        top5_hot = filtered_df.sort_values(by='최고기온(℃)', ascending=False).head(5).copy()
        top5_hot['날짜'] = top5_hot['날짜'].dt.strftime('%Y-%m-%d')
        st.table(top5_hot[['날짜', '최고기온(℃)', '평균기온(℃)']].reset_index(drop=True))

except Exception as e:
    st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Global Market Cap Top10 Dashboard",
    layout="wide"
)

st.title("🌎 Global Market Cap Top10 - Last 1 Year Performance")

# 글로벌 시총 상위 기업 (2025~2026 기준)
stocks = {
    "NVIDIA": "NVDA",
    "Microsoft": "MSFT",
    "Apple": "AAPL",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Saudi Aramco": "2222.SR",
    "Berkshire Hathaway": "BRK-B"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data
def load_data():
    df = yf.download(
        list(stocks.values()),
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )["Close"]

    return df

prices = load_data()

# 시작값 100 기준 정규화
normalized = prices.div(prices.iloc[0]).mul(100)

fig = go.Figure()

for company, ticker in stocks.items():
    fig.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[ticker],
            mode="lines",
            name=company,
            hovertemplate=
            f"<b>{company}</b><br>" +
            "Date: %{x}<br>" +
            "Index: %{y:.2f}<extra></extra>"
        )
    )

fig.update_layout(
    title="Top 10 Global Companies - Normalized Performance (Base=100)",
    xaxis_title="Date",
    yaxis_title="Performance Index",
    height=700,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

st.plotly_chart(fig, use_container_width=True)

# 수익률 테이블
returns = (
    normalized.iloc[-1] - 100
).sort_values(ascending=False)

st.subheader("📊 1-Year Return Ranking")

ranking = pd.DataFrame({
    "Company": returns.index,
    "Return (%)": returns.values.round(2)
})

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

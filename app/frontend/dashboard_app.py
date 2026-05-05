import streamlit as st
import requests
import time
import yfinance as yf

st.set_page_config(
    page_title="AIRA Dashboard",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("📊 AIRA Investment Dashboard")
st.caption("Autonomous Investment Research Agent")

st.sidebar.header("🔎 Stock Analysis")
ticker = st.sidebar.text_input("Enter Ticker", "AAPL")

analyze_btn = st.sidebar.button("Run Analysis")

if analyze_btn:
    if ticker:
        with st.spinner("Running AI analysis..."):
            res = requests.post(
                f"{API_URL}/analyze",
                json={"ticker": ticker}
            ).json()

            job_id = res.get("job_id")

            result = None
            for _ in range(15):
                time.sleep(1)
                r = requests.get(f"{API_URL}/result/{job_id}").json()

                if r["status"] == "completed":
                    result = r["result"]
                    break

        if result:
            st.success("Analysis Complete")

            col1, col2, col3 = st.columns(3)

            signal = result["signal"]
            if signal == "Bullish":
                col1.success(f"📈 {signal}")
            elif signal == "Bearish":
                col1.error(f"📉 {signal}")
            else:
                col1.warning(f"➖ {signal}")

            col2.metric("Confidence", result["confidence"])
            col3.metric("Trend", result.get("trend", "N/A"))

            st.subheader("📈 Price Chart")
            data = yf.download(ticker, period="1mo", interval="1d")
            st.line_chart(data["Close"])

            st.subheader("📌 Thesis")
            st.write(result["thesis"])

            st.subheader("💡 Insights")
            for i in result["insights"]:
                st.write(f"• {i}")

            st.subheader("⚠️ Risks")
            for r in result["risks"]:
                st.write(f"• {r}")

        else:
            st.error("Analysis timed out")

    else:
        st.warning("Please enter a ticker")

st.divider()
st.subheader("📊 Portfolio Comparison")

tickers = st.text_input("Enter multiple tickers (comma separated)", "AAPL,TSLA,META")

if st.button("Compare Portfolio"):
    ticker_list = [t.strip() for t in tickers.split(",")]

    reports = []

    with st.spinner("Analyzing portfolio..."):
        for t in ticker_list:
            res = requests.post(
                f"{API_URL}/analyze",
                json={"ticker": t}
            ).json()

            job_id = res["job_id"]

            result = None
            for _ in range(10):
                time.sleep(1)
                r = requests.get(f"{API_URL}/result/{job_id}").json()

                if r["status"] == "completed":
                    result = r["result"]
                    break

            if result:
                reports.append(result)

    if reports:
        portfolio = requests.post(
            f"{API_URL}/portfolio",
            json={"reports": reports}
        ).json()

        st.subheader("🏆 Best Stock")
        st.success(f"{portfolio['best_stock']['ticker']}")

        st.subheader("📊 Ranking")

        for r in portfolio["ranking"]:
            st.write(
                f"{r['ticker']} | Confidence: {r['confidence']} | Signal: {r['signal']}"
            )

st.divider()
st.subheader("📊 System Overview")

try:
    dashboard = requests.get(f"{API_URL}/dashboard").json()
    metrics = requests.get(f"{API_URL}/metrics").json()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Jobs", dashboard["total_jobs"])
    col2.metric("Completed", dashboard["completed_jobs"])
    col3.metric("Bullish", metrics["bullish"])
    col4.metric("Bearish", metrics["bearish"])

    st.subheader("🕒 Recent Jobs")
    for job in dashboard["latest_jobs"]:
        st.write(f"{job['ticker']} → {job['status']}")

except:
    st.warning("API not reachable")
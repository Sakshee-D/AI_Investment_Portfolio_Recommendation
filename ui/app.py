import streamlit as st
import requests
import pandas as pd

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Portfolio Advisor",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .main { max-width: 720px; margin: auto; }
        .stButton > button {
            width: 100%;
            background-color: #1f77b4;
            color: white;
            font-size: 16px;
            padding: 0.6em 1em;
            border-radius: 8px;
            border: none;
            margin-top: 8px;
        }
        .stButton > button:hover { background-color: #1560a0; }
        .stock-card {
            background: #f7f9fb;
            border-left: 4px solid #1f77b4;
            border-radius: 6px;
            padding: 12px 16px;
            margin-bottom: 10px;
        }
        .stock-name { font-size: 17px; font-weight: 700; color: #1a1a2e; }
        .stock-alloc { font-size: 15px; color: #1f77b4; font-weight: 600; }
        .stock-reason { font-size: 13px; color: #555; margin-top: 4px; }
        .context-card {
            background: #f0f4f8;
            border-radius: 6px;
            padding: 10px 14px;
            margin-bottom: 8px;
            font-size: 13px;
            color: #333;
        }
        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 6px;
        }
        .badge-low    { background: #d4edda; color: #155724; }
        .badge-medium { background: #fff3cd; color: #856404; }
        .badge-high   { background: #f8d7da; color: #721c24; }
        hr { margin: 20px 0; border: none; border-top: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("## 📊 AI Portfolio Advisor")
st.markdown("_Powered by RAG + LLM. Retrieves real financial context, then reasons about your portfolio._")
st.markdown("---")

# ─── User Inputs ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    risk = st.selectbox(
        "🎯 Risk Level",
        options=["low", "medium", "high"],
        index=1,
        help="Low = stable returns, Medium = balanced, High = aggressive growth"
    )

with col2:
 years = st.slider(
    "📅 Investment Duration (years)",
    min_value=1,
    max_value=20,
    value=5,
    help="Select how many years you plan to invest"
)

st.caption(f"Investment duration: {years} years")

budget = st.number_input(
    "💰 Investment Amount (₹)",
    min_value=1000,
    max_value=10_000_000,
    value=50000,
    step=1000,
    help="Total amount you want to invest"
)

# ─── Risk Badge Helper ───────────────────────────────────────────────────────
def risk_badge(risk_level):
    cls = f"badge-{risk_level.lower()}" if risk_level.lower() in ["low", "medium", "high"] else "badge-medium"
    label = risk_level.capitalize()
    return f'<span class="badge {cls}">{label}</span>'


# ─── API Config ──────────────────────────────────────────────────────────────
PERSON_A_URL = "http://localhost:9000/recommend"

# ─── Main Button ─────────────────────────────────────────────────────────────
st.markdown(" ")

if st.button("🚀 Get My Portfolio Recommendation"):

    # --- Validation ---
    if budget <= 0:
        st.warning("⚠️ Please enter a valid investment amount greater than ₹0.")
        st.stop()

    with st.spinner("🔍 Retrieving financial insights & generating your portfolio..."):
        try:
            response = requests.post(
                PERSON_A_URL,
                json={
                    "risk": risk,
                    "duration_years": int(years),
                    "budget": int(budget)
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.ConnectionError:
            st.error("❌ **Cannot connect to the backend.** Make sure Person A API is running on port 9000.")
            st.code("uvicorn main:app --port 9000", language="bash")
            st.stop()

        except requests.exceptions.Timeout:
            st.error("⏱️ **Request timed out.** The backend took too long to respond. Try again.")
            st.stop()

        except requests.exceptions.HTTPError as e:
            st.error(f"❌ **API returned an error:** {e}")
            st.stop()

        except Exception as e:
            st.error(f"❌ **Unexpected error:** {e}")
            st.stop()

    # ─── Validate Response Structure ─────────────────────────────────────────
    if "portfolio" not in data:
        st.error("⚠️ The API response is missing expected fields. Check your Person A output format.")
        st.json(data)
        st.stop()

    portfolio = data.get("portfolio", [])
    risk_match = data.get("risk_match", risk.capitalize())
    context   = data.get("context", [])   # optional RAG context

    # ─── Section: Portfolio Cards ─────────────────────────────────────────────
    st.markdown("### 📌 Recommended Portfolio")

    total_allocated = sum(int(item.get("allocation", 0)) for item in portfolio)

    for item in portfolio:
        stock      = item.get("stock", "Unknown")
        allocation = item.get("allocation", "0")
        reason     = item.get("reason", "No reason provided.")
        pct        = round(int(allocation) / budget * 100, 1) if budget else 0

        st.markdown(f"""
        <div class="stock-card">
            <div class="stock-name">🏢 {stock}</div>
            <div class="stock-alloc">₹{int(allocation):,}  <span style="color:#999;font-size:13px;">({pct}% of budget)</span></div>
            <div class="stock-reason">💬 {reason}</div>
        </div>
        """, unsafe_allow_html=True)

    # --- Allocation sum warning ---
    if total_allocated != int(budget):
        diff = int(budget) - total_allocated
        st.warning(f"⚠️ Total allocated ₹{total_allocated:,} differs from budget ₹{int(budget):,} by ₹{diff:,}. Check LLM output.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ─── Section: Allocation Bar Chart ──────────────────────────────────────
    st.markdown("### 📈 Allocation Breakdown")

    if portfolio:
        chart_data = {
            item.get("stock", f"Stock {i}"): int(item.get("allocation", 0))
            for i, item in enumerate(portfolio)
        }
        df = pd.DataFrame.from_dict(chart_data, orient="index", columns=["Amount (₹)"])
        st.bar_chart(df)

    st.markdown("<hr>", unsafe_allow_html=True)


    # ─── Section: RAG Context (if returned by Person A) ──────────────────────
    if context:
        with st.expander("📚 Retrieved Market Insights (RAG Context)", expanded=False):
            st.markdown("_These insights were fetched from the vector database and used to generate your portfolio._")
            for c in context:
                stock_name = c.get("stock", "Unknown")
                summary    = c.get("summary", "No summary available.")
                sector     = c.get("sector", "—")
                c_risk     = c.get("risk", "medium")

                st.markdown(f"""
                <div class="context-card">
                    <strong>{stock_name}</strong> &nbsp;{risk_badge(c_risk)}
                    <span style="color:#888;font-size:12px;">Sector: {sector}</span><br>
                    {summary}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.caption("_ℹ️ No RAG context returned. Ask Person A to include `context` in the API response to display insights here._")

    # ─── Section: Summary Stats ───────────────────────────────────────────────
    st.markdown("### 🧮 Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Invested", f"₹{total_allocated:,}")
    m2.metric("Stocks Selected", len(portfolio))
    m3.metric("Risk Level", risk_match)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("✅ Portfolio generated successfully!")

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown(" ")
st.markdown(
    "<p style='text-align:center;color:#aaa;font-size:12px;'>AI Portfolio Advisor · RAG + LLM System · Built with Streamlit</p>",
    unsafe_allow_html=True
)

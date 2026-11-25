import streamlit as st
import pandas as pd
import random
from datetime import date

st.set_page_config(
    page_title="Smart Savings Analyzer",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Custom UI
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #10243b 55%, #07111f 100%);
}
h1, h2, h3 {
    color: #38d39f !important;
}
[data-testid="stMetricValue"] {
    color: #38d39f !important;
}
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(56,211,159,0.25);
    border-radius: 16px;
    padding: 18px;
    margin: 8px 0;
    color: white;
}
.goal {
    background: linear-gradient(90deg, rgba(56,211,159,.20), rgba(61,169,245,.12));
    border: 1px solid rgba(56,211,159,.45);
    border-radius: 16px;
    padding: 20px;
}
.tip {
    background: rgba(61,169,245,.12);
    border-left: 5px solid #3da9f5;
    padding: 14px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Smart Savings Analyzer")
st.caption("A Python + Streamlit mini project for income, expense and savings analysis")

# -----------------------------
# Session state
# -----------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# -----------------------------
# Sidebar input
# -----------------------------
st.sidebar.header("📥 Monthly Financial Input")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0.0, value=30000.0, step=1000.0)

st.sidebar.subheader("Expense Categories")
categories = ["Food", "Travel", "Shopping", "Bills", "Education", "Entertainment", "Health", "Other"]
expense_values = {}
for cat in categories:
    expense_values[cat] = st.sidebar.number_input(
        f"{cat} (₹)", min_value=0.0, value=0.0, step=100.0
    )

target_saving = st.sidebar.number_input(
    "Monthly Savings Target (₹)",
    min_value=0.0,
    value=5000.0,
    step=500.0
)

# -----------------------------
# Calculations
# -----------------------------
total_expense = sum(expense_values.values())
monthly_saving = income - total_expense
saving_rate = (monthly_saving / income * 100) if income > 0 else 0
expense_rate = (total_expense / income * 100) if income > 0 else 0
target_gap = monthly_saving - target_saving
annual_saving = monthly_saving * 12
annual_income = income * 12
annual_expense = total_expense * 12

# -----------------------------
# Dashboard
# -----------------------------
st.markdown("## 📊 Financial Dashboard")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Monthly Income", f"₹{income:,.0f}")
c2.metric("Total Expenses", f"₹{total_expense:,.0f}")
c3.metric("Monthly Savings", f"₹{monthly_saving:,.0f}")
c4.metric("Saving Rate", f"{saving_rate:.1f}%")

if monthly_saving > 0:
    st.success("✅ You are currently saving money every month.")
elif monthly_saving == 0:
    st.warning("⚠️ Your income and expenses are exactly equal.")
else:
    st.error("❌ Your expenses are higher than your income.")

# -----------------------------
# Goal analysis
# -----------------------------
st.markdown("## 🎯 Savings Goal Analysis")
g1, g2 = st.columns(2)

with g1:
    st.markdown(
        f"""
        <div class="goal">
        <h3>Monthly Target</h3>
        <h2>₹{target_saving:,.0f}</h2>
        <p>Current monthly saving: ₹{monthly_saving:,.0f}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with g2:
    if target_saving == 0:
        goal_text = "No monthly target has been set."
    elif target_gap >= 0:
        goal_text = f"🎉 Target achieved by ₹{target_gap:,.0f}."
    else:
        goal_text = f"📌 You need ₹{abs(target_gap):,.0f} more savings this month."
    st.info(goal_text)

# -----------------------------
# Expense analysis
# -----------------------------
st.markdown("## 🧾 Expense Analysis")

expense_df = pd.DataFrame({
    "Category": list(expense_values.keys()),
    "Amount": list(expense_values.values())
})
expense_df = expense_df[expense_df["Amount"] > 0].sort_values("Amount", ascending=False)

if not expense_df.empty:
    left, right = st.columns(2)
    with left:
        st.dataframe(expense_df, use_container_width=True, hide_index=True)
    with right:
        st.bar_chart(expense_df.set_index("Category"))
    highest_category = expense_df.iloc[0]["Category"]
    highest_amount = expense_df.iloc[0]["Amount"]
    st.info(
        f"🔎 Highest spending category: **{highest_category}** "
        f"with **₹{highest_amount:,.0f}**."
    )
else:
    st.info("Enter at least one expense category to view the expense analysis.")

# -----------------------------
# 50/30/20 style planning helper
# -----------------------------
st.markdown("## 🧠 Budget Planning Helper")
recommended_needs = income * 0.50
recommended_wants = income * 0.30
recommended_savings = income * 0.20

b1, b2, b3 = st.columns(3)
b1.metric("Needs Guide (50%)", f"₹{recommended_needs:,.0f}")
b2.metric("Wants Guide (30%)", f"₹{recommended_wants:,.0f}")
b3.metric("Savings Guide (20%)", f"₹{recommended_savings:,.0f}")

if monthly_saving >= recommended_savings:
    st.success("🌟 Your current savings meet or exceed the 20% planning guide.")
else:
    st.warning(
        f"Your current saving is ₹{monthly_saving:,.0f}. "
        f"The 20% guide is ₹{recommended_savings:,.0f}."
    )

# -----------------------------
# Annual projection
# -----------------------------
st.markdown("## 📅 Annual Projection")
a1, a2, a3 = st.columns(3)
a1.metric("Annual Income", f"₹{annual_income:,.0f}")
a2.metric("Annual Expenses", f"₹{annual_expense:,.0f}")
a3.metric("Projected Annual Savings", f"₹{annual_saving:,.0f}")

# -----------------------------
# Savings goal calculator
# -----------------------------
st.markdown("## 🏆 Goal Completion Calculator")
goal_amount = st.number_input(
    "Enter a future savings goal (₹)",
    min_value=0.0,
    value=60000.0,
    step=5000.0
)

if monthly_saving > 0 and goal_amount > 0:
    months_needed = math.ceil(goal_amount / monthly_saving)
    years = months_needed // 12
    months = months_needed % 12
    duration = f"{years} year(s) and {months} month(s)" if years else f"{months} month(s)"
    st.success(
        f"At the current monthly saving of ₹{monthly_saving:,.0f}, "
        f"you can reach ₹{goal_amount:,.0f} in approximately **{duration}**."
    )
elif goal_amount == 0:
    st.info("Enter a goal amount greater than zero.")
else:
    st.error("A positive monthly saving is required for this projection.")

# -----------------------------
# Quick savings scenarios
# -----------------------------
st.markdown("## 🔄 Savings Scenario Simulator")
scenario_cut = st.slider(
    "Reduce monthly expenses by (%)",
    min_value=0,
    max_value=50,
    value=10,
    step=5
)
scenario_expense = total_expense * (1 - scenario_cut / 100)
scenario_saving = income - scenario_expense
scenario_annual = scenario_saving * 12

s1, s2, s3 = st.columns(3)
s1.metric("Scenario Expenses", f"₹{scenario_expense:,.0f}")
s2.metric("Scenario Monthly Saving", f"₹{scenario_saving:,.0f}")
s3.metric("Scenario Annual Saving", f"₹{scenario_annual:,.0f}")

# -----------------------------
# Financial health score
# -----------------------------
st.markdown("## ❤️ Financial Health Score")
score = 0
if income > 0:
    if saving_rate >= 20:
        score += 40
    elif saving_rate >= 10:
        score += 25
    elif saving_rate > 0:
        score += 15

    if expense_rate <= 70:
        score += 30
    elif expense_rate <= 85:
        score += 20
    elif expense_rate <= 100:
        score += 10

    if target_saving > 0 and monthly_saving >= target_saving:
        score += 30
    elif monthly_saving > 0:
        score += 15

if score >= 80:
    health = "Excellent"
elif score >= 60:
    health = "Good"
elif score >= 40:
    health = "Needs Improvement"
else:
    health = "Critical"

st.progress(min(score, 100))
st.metric("Financial Health Score", f"{score}/100")
st.write(f"Status: **{health}**")

# -----------------------------
# Tips
# -----------------------------
tips = [
    "Track small recurring expenses because they can become large monthly totals.",
    "Set a savings target before planning discretionary spending.",
    "Review your largest expense category first when trying to increase savings.",
    "Automating a fixed monthly transfer can make saving more consistent.",
    "Use the scenario simulator to estimate the effect of reducing non-essential expenses."
]
st.markdown("## 💡 Smart Saving Tip")
st.markdown(f'<div class="tip">{random.choice(tips)}</div>', unsafe_allow_html=True)

# -----------------------------
# Reset
# -----------------------------
if st.button("🔄 Reset Inputs"):
    for cat in categories:
        st.session_state.expenses = []
    st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding:18px;">
        <h3>💰 Smart Savings Analyzer</h3>
        <p>Developed using Python • Streamlit • Pandas</p>
        <p>Educational Mini Project • 2026</p>
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st

# --- Page setup ---
st.set_page_config(page_title="ALGO Manipulation in Non-Liquid Option", layout="centered")
st.title("🎯 ALGO Manipulation in a Non-Liquid Option Market")

# --- Sidebar Inputs ---
st.sidebar.header("Simulation Settings")

fair_value = st.sidebar.number_input("Fair Value of Option", min_value=10, value=40, step=1)
algo_bid = st.sidebar.number_input("ALGO Bid Price", min_value=1, value=20, step=1)
algo_ask = st.sidebar.number_input("ALGO Ask Price", min_value=10, value=80, step=1)
human_entry = st.sidebar.number_input("Human Entry Price", min_value=1, value=21, step=1)
manipulation_margin = st.sidebar.slider("ALGO Sell Threshold (% above Fair Value)", 10, 50, 20)

st.sidebar.markdown("---")
st.sidebar.info("💡 ALGO manipulates prices above fair value before selling to HUMAN.")

# --- Simulation Logic ---
simulation_steps = []

# Step 1: Initial ALGO control
simulation_steps.append(f"ALGO places fake liquidity: Bid @ {algo_bid}, Ask @ {algo_ask}")

# Step 2: Human enters at entry price
simulation_steps.append(f"HUMAN enters the market and buys at ₹{human_entry}")

# Step 3: ALGO starts pushing the bid upward to attract human
current_price = human_entry
while current_price < fair_value * (1 + manipulation_margin / 100):
    current_price += 1
    simulation_steps.append(f"ALGO increases bid to ₹{current_price}")

# Step 4: ALGO sells to human at inflated price
sell_price = fair_value * (1 + manipulation_margin / 100)
simulation_steps.append(f"ALGO sells the option to HUMAN at ₹{sell_price:.2f} (20% above fair value)")

# Step 5: ALGO resets fake bid/ask
simulation_steps.append(f"After selling, ALGO resets back to Bid @ {algo_bid}, Ask @ {algo_ask}")

# --- Display the steps ---
st.subheader("🧩 Simulation Steps:")
for step in simulation_steps:
    st.write(f"• {step}")

# --- Outcome ---
human_loss = sell_price - fair_value
st.markdown("---")
st.subheader("📊 Simulation Summary")
st.write(f"**Fair Value:** ₹{fair_value}")
st.write(f"**ALGO Sell Price:** ₹{sell_price:.2f}")
st.write(f"**HUMAN's Unrealized Loss:** ₹{human_loss:.2f}")
st.markdown(
    f"""
**Explanation:**  
- ALGO manipulates both buy and sell sides in an illiquid option.  
- HUMAN buys above fair value thinking demand is real.  
- Once price hits {manipulation_margin}% above fair value (₹{sell_price:.2f}),  
  ALGO sells and resets the order book.  
- HUMAN is left holding at a loss since the fair price remains ₹{fair_value}.
"""
)

st.warning("⚠️ In illiquid options, ALGO can control both sides of the order book, creating fake market depth and trapping manual traders.")

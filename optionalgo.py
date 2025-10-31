import streamlit as st
import matplotlib.pyplot as plt

# --- Page setup ---
st.set_page_config(page_title="ALGO Manipulation in Non-Liquid Option", layout="wide")
st.title("🎯 ALGO Manipulation in a Non-Liquid Option Market")

# --- User Inputs ---
st.sidebar.header("Simulation Settings")

fair_value = st.sidebar.number_input("Fair Value of Option", min_value=10, value=40, step=1)
algo_bid = st.sidebar.number_input("ALGO Bid Price", min_value=1, value=20, step=1)
algo_ask = st.sidebar.number_input("ALGO Ask Price", min_value=10, value=80, step=1)
human_entry = st.sidebar.number_input("Human Entry Price", min_value=1, value=21, step=1)
manipulation_margin = st.sidebar.slider("ALGO Sell Threshold (% above Fair Value)", 10, 50, 20)

st.sidebar.markdown("---")
st.sidebar.info("💡 ALGO manipulates price up to the chosen percentage above fair value, then sells to HUMAN.")

# --- Simulation Logic ---
price_history = []
participants = []

# Step 1: Initial ALGO control
price_history.append((algo_bid + algo_ask) / 2)
participants.append("ALGO (controls both sides)")

# Step 2: Human enters at entry price
price_history.append(human_entry)
participants.append("HUMAN buys at " + str(human_entry))

# Step 3: ALGO pushes bid up gradually
current_price = human_entry
while current_price < fair_value * (1 + manipulation_margin / 100):
    current_price += 1
    price_history.append(current_price)
    participants.append("ALGO pushing bid up")

# Step 4: ALGO sells to human at inflated price
sell_price = fair_value * (1 + manipulation_margin / 100)
price_history.append(sell_price)
participants.append(f"ALGO sells at inflated price ({sell_price:.2f})")

# Step 5: ALGO resets fake bid/ask
price_history.append((algo_bid + algo_ask) / 2)
participants.append("ALGO resets to 20/80")

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(price_history, marker='o', color='blue', linewidth=2)

for i, label in enumerate(participants):
    ax.text(i, price_history[i] + 0.8, label, fontsize=8, rotation=30)

ax.axhline(y=fair_value, color='green', linestyle='--', label=f'Fair Value ({fair_value})')
ax.set_title("ALGO Manipulation Simulation in a Non-Liquid Option Market", fontsize=12)
ax.set_xlabel("Simulation Step")
ax.set_ylabel("Option Price")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# --- Output Summary ---
human_loss = sell_price - fair_value
st.markdown("### 📊 Simulation Summary")
st.write(f"""
- **Fair Value:** {fair_value}  
- **ALGO starts as buyer @ {algo_bid} and seller @ {algo_ask}**  
- **Human enters @ {human_entry}**  
- **ALGO sells at inflated price:** {sell_price:.2f}  
- **Actual Fair Value:** {fair_value}  
- **Human's Immediate Unrealized Loss:** {human_loss:.2f}
""")

st.warning("⚠️ In illiquid markets, ALGO can manipulate both bid and ask prices — retail traders often end up buying above fair value and incur losses once the ALGO resets its positions.")

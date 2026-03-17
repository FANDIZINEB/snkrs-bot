import streamlit as st
import time
from datetime import datetime
from bot import run_task, start_browser
from config import URL, DROP_TIME, SIZES, RETRY, DELAY
from notifier import notify

st.title("🚀 SNKRS Assistant Bot PRO")

# --- STATE ---
if "running" not in st.session_state:
    st.session_state.running = False

if "logs" not in st.session_state:
    st.session_state.logs = []

# --- UI ---
drop_time = st.text_input("Heure du drop", DROP_TIME)
sizes = st.text_input("Tailles (séparées par ,)", ",".join(SIZES))

# --- BUTTONS ---
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# START
if col1.button("▶️ Lancer le bot"):
    st.session_state.running = True
    st.session_state.logs.append("Bot lancé")

# STOP
if col2.button("⛔ STOP"):
    st.session_state.running = False
    st.session_state.logs.append("Bot arrêté")

# TEST OPEN
if col3.button("🧪 Tester ouverture Nike"):
    st.session_state.logs.append("Test ouverture navigateur")
    start_browser(URL)

# TEST FULL
if col4.button("🔥 Test complet"):
    st.session_state.logs.append("Test complet lancé")
    run_task(URL, ["42"], 1, 1)

# --- COUNTDOWN ---
def get_remaining_time(target):
    now = datetime.now()

    target_time = datetime.strptime(target, "%H:%M:%S").replace(
        year=now.year, month=now.month, day=now.day
    )

    if target_time < now:
        target_time = target_time.replace(day=now.day + 1)

    return (target_time - now).total_seconds()

# --- MAIN LOOP ---
if st.session_state.running:
    remaining = get_remaining_time(drop_time)

    minutes = int(remaining // 60)
    seconds = int(remaining % 60)

    if remaining > 0:
        st.write(f"⏳ Temps restant : {minutes} min {seconds} sec")
        st.session_state.logs.append(f"Attente... {minutes}m {seconds}s")
        time.sleep(1)
        st.rerun()

    else:
        st.write("🔥 DROP EN COURS !!!")
        notify("DROP !")

        sizes_list = sizes.split(",")

        run_task(URL, sizes_list, RETRY, DELAY)

        st.session_state.logs.append("Tentative terminée")
        st.session_state.running = False

# --- LOG DISPLAY ---
st.subheader("📜 Logs en direct")

for log in st.session_state.logs[-10:]:
    st.text(log)
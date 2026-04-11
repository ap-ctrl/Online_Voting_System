import streamlit as st
from models import *
import pandas as pd


# import base64

# # ---------- BACKGROUND IMAGE ----------
# def get_base64(file):
#     with open(file, "rb") as f:
#         return base64.b64encode(f.read()).decode()

# bg_img = get_base64("background.jpeg")

# st.markdown(f"""
# <style>
# .stApp {{
#     background-image: url("data:image/jpg;base64,{bg_img}");
#     background-size: cover;
#     background-position: center;
#     background-repeat: no-repeat;
# }}

# .overlay {{
#     position: fixed;
#     top: 0;
#     left: 0;
#     width: 100%;
#     height: 100%;
#     background: rgba(0,0,0,0.6);
#     z-index: -1;
# }}

# .title {{
#     text-align: center;
#     color: white;
#     font-size: 50px;
#     font-weight: bold;
# }}

# .subtitle {{
#     text-align: center;
#     color: #d1d5db;
#     font-size: 18px;
# }}

# .stButton>button {{
#     background: linear-gradient(135deg, #6366f1, #a855f7);
#     color: white;
#     border-radius: 12px;
#     height: 3.5em;
#     width: 100%;
#     font-size: 18px;
#     font-weight: bold;
#     border: none;
# }}

# .stButton>button:hover {{
#     transform: scale(1.05);
#     transition: 0.2s;
# }}
# </style>

# <div class="overlay"></div>
# """, unsafe_allow_html=True)

st.title("🗳️ Online Voting System")

# INIT
if "step" not in st.session_state:
    st.session_state.step = "start"

# ---------------- START ----------------
if st.session_state.step == "start":
    role = st.selectbox("Select Role", ["Admin", "Voter"])

    if st.button("Continue"):
        if role == "Admin":
            st.session_state.step = "admin_login"
        else:
            st.session_state.step = "voter_choice"   # ✅ CHANGED

        st.rerun()
# if st.session_state.step == "start":

#     st.markdown('<div class="title">🗳️ Online Voting System</div>', unsafe_allow_html=True)
#     st.markdown('<div class="subtitle">Make your voice count</div>', unsafe_allow_html=True)

#     st.markdown("<br><br>", unsafe_allow_html=True)

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("👨‍💼 Admin"):
#             st.session_state.step = "admin_login"
#             st.rerun()

#     with col2:
#         if st.button("🧑‍💻 Voter"):
#             st.session_state.step = "voter_choice"
#             st.rerun()

# ================= ADMIN =================

elif st.session_state.step == "admin_login":
    st.subheader("🔐 Admin Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_admin(u, p):
            st.session_state.step = "admin_dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

elif st.session_state.step == "admin_dashboard":
    st.subheader("👨‍💼 Admin Dashboard")

    option = st.selectbox("Action", [
        "Add Candidate",
        "Delete Candidate",
        "View Results",
        "View Voters",
        "Start Voting",
        "Stop Voting"
    ])

    if option == "Add Candidate":
        name = st.text_input("Candidate Name")
        party = st.text_input("Party")

        if st.button("Add"):
            add_candidate(name, party)
            st.success("Candidate added")

    elif option == "Delete Candidate":
        for c in get_candidates():
            if st.button(f"Delete {c[1]}"):
                delete_candidate(c[0])
                st.rerun()

    elif option == "View Results":
        df = pd.DataFrame(get_results(), columns=["Candidate", "Votes"])
        st.bar_chart(df.set_index("Candidate"))

        if not is_voting_open():
            winner = get_winner()
            if winner:
                st.success(f"🏆 Winner: {winner[0]}")

    elif option == "View Voters":
        for v in get_voters():
            st.write(f"{v[1]} | Age: {v[2]} | Username: {v[3]} | Voted: {v[4]}")

    elif option == "Start Voting":
        candidates=get_candidates()
        if len(candidates)<2:
            st.error("❌ Add at least 2 candidates before starting voting")
        else:
            
            
         set_voting_status(1)
         st.success("Voting Started")

    elif option == "Stop Voting":
        set_voting_status(0)
        st.success("Voting Stopped")

        winner = get_winner()
        if winner:
            st.success(f"🏆 Winner: {winner[0]}")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ================= VOTER =================

# 🔹 NEW PAGE
elif st.session_state.step == "voter_choice":
    st.subheader("Voter Options")

    choice = st.radio("Choose", ["Login", "Register"])

    if st.button("Continue"):
        if choice == "Login":
            st.session_state.step = "voter_login"
        else:
            st.session_state.step = "voter_register"

        st.rerun()
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 🔹 REGISTER
elif st.session_state.step == "voter_register":
    st.subheader("📝 Register")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        res = register_voter(name, age, u, p)

        if res == "Success":
            st.session_state.step = "voter_login"
            st.rerun()
        else:
            st.error(res)
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 🔹 LOGIN
elif st.session_state.step == "voter_login":
    st.subheader("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_voter(u, p)

        if user:
            st.session_state.user = user
            st.session_state.step = "vote"
            st.rerun()
        else:
            st.error("Invalid credentials")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 🔹 VOTING PAGE
elif st.session_state.step == "vote":
    st.subheader("🗳️ Cast Vote")

    # Check voting status
    if not is_voting_open():
        winner = get_winner()

        if winner:
            st.success(f"🏆 Winner: {winner[0]}")
        else:
            st.warning("Voting not started yet")

    else:
        for c in get_candidates():
            if st.button(f"Vote for {c[1]} ({c[2]})"):
                res = cast_vote(st.session_state.user[0], c[0])

                if res == "Already voted":
                    st.error("You already voted")
                else:
                    st.success("Vote casted")
                    st.session_state.step = "result"
                    st.rerun()
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# 🔹 RESULT PAGE
elif st.session_state.step == "result":
    st.subheader("📊 Your Vote & Results")

    # Show user's vote
    vote = get_user_vote(st.session_state.user[0])
    if vote:
        st.info(f"You voted for: {vote[0]}")

    # Graph
    df = pd.DataFrame(get_results(), columns=["Candidate", "Votes"])
    st.bar_chart(df.set_index("Candidate"))

    # Winner
    if not is_voting_open():
        winner = get_winner()
        if winner:
            st.success(f"🏆 Winner: {winner[0]}")
    else:
        st.warning("Voting still ongoing")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()


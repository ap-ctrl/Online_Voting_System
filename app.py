import streamlit as st
from models import *
import pandas as pd
import base64
import os

# INIT
if "step" not in st.session_state:
    st.session_state.step = "start"

if st.session_state.step != "start":
    st.title("🗳️ Online Voting System")

# ---------------- START ----------------
if st.session_state.step == "start":
    # --- Custom CSS for Light UI ---
    st.markdown("""
    <style>
    /* Soft pastel gradient background */
    .stApp {
        background: linear-gradient(135deg, #e6d3ff 0%, #acc2ff 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Top padding removal slightly for hero title */
    .main .block-container {
        padding-top: 3rem;
        max-width: 900px;
    }
    
    /* Text Styling */
    .hero-title {
        text-align: center;
        color: #31306b;
    }
    .hero-title h1 {
        font-weight: 800;
        font-size: 3.2rem;
        margin-top: 0;
        margin-bottom: 5px;
        color: #31306b;
    }
    .hero-title p {
        color: #5c629e;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }
    
    /* Global Cards format */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        border: 2px solid transparent;
        margin-bottom: 15px; /* Spacing before native button */
    }
    
    .voter-card {
        border-color: #a3e4b7;
    }
    .admin-card {
        border-color: #a4bdf6;
    }
    
    .card-title {
        font-weight: 700;
        font-size: 1.8rem;
        margin-bottom: 10px;
    }
    .card-sub {
        color: #6b7280;
        font-size: 1.1rem;
        line-height: 1.4;
    }
    
    /* Make buttons solid black */
    div.stButton > button {
        width: 100% !important;
        background-color: #111111 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 0 !important;
    }
    div.stButton > button p {
        color: white !important;
        font-weight: 600 !important;
    }
    div.stButton > button:hover {
        background-color: #2b2b2b !important;
        color: white !important;
        border-color: transparent !important;
    }
    </style>
    
    <div class="hero-title">
        <h1>Select Your Role</h1>
        <p>Choose your role to proceed.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f'''
        <div class="info-card admin-card">
            <h2 class="card-title" style="color:#3b5998;">👨‍💼 I am an Admin</h2>
            <p class="card-sub">Manage voter applications and oversee the voting process.</p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Continue as Admin", key="admin_btn", use_container_width=True):
            st.session_state.step = "admin_login"
            st.rerun()
            
    with col2:
        st.markdown(f'''
        <div class="info-card voter-card">
            <h2 class="card-title" style="color:#2d8a4e;">💻 I am a Voter</h2>
            <p class="card-sub">Register, view candidates, and cast your vote online.</p>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Continue as Voter", key="voter_btn", use_container_width=True):
            st.session_state.step = "voter_choice"
            st.rerun()

    st.write("") # Spacer

# ================= ADMIN =================

elif st.session_state.step == "admin_login":
    st.subheader("🔐 Admin Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", use_container_width=True):
            if login_admin(u, p):
                st.session_state.step = "admin_dashboard"
                st.rerun()
            else:
                st.error("Invalid credentials")
    with col2:
        if st.button("⬅️ Back", use_container_width=True):
            st.session_state.step = "start"
            st.rerun()

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
            if add_candidate(name, party):
                st.success("Candidate added")
            else:
                st.error("Fields cannot be empty")

    elif option == "Delete Candidate":
        for c in get_candidates():
            if st.button(f"Delete {c['name']}"):
                delete_candidate(c['id'])
                st.rerun()

    elif option == "View Results":
        results = get_results()
        if results:
            df = pd.DataFrame(results, columns=["Candidate", "Votes"])
            st.bar_chart(df.set_index("Candidate"))
        else:
            st.info("No votes cast yet.")

        if not is_voting_open():
            winner = get_winner()
            if winner:
                st.success(f"🏆 Winner: {winner['name']} with {winner['total']} votes")

    elif option == "View Voters":
        for v in get_voters():
            st.write(f"{v['name']} | Age: {v['age']} | Username: {v['username']} | Voted: {v['has_voted']}")

    elif option == "Start Voting":
        candidates = get_candidates()
        if len(candidates) < 2:
            st.error("❌ Add at least 2 candidates before starting voting")
        else:
            set_voting_status(1)
            st.success("Voting Started")

    elif option == "Stop Voting":
        set_voting_status(0)
        st.success("Voting Stopped")

        winner = get_winner()
        if winner:
            st.success(f"🏆 Winner: {winner['name']} with {winner['total']} votes")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ================= VOTER =================

elif st.session_state.step == "voter_choice":
    st.subheader("Voter Options")

    choice = st.radio("Choose", ["Login", "Register"])

    if st.button("Continue"):
        if choice == "Login":
            st.session_state.step = "voter_login"
        else:
            st.session_state.step = "voter_register"

        st.rerun()
        
    if st.button("⬅️ Back"):
        st.session_state.step = "start"
        st.rerun()

elif st.session_state.step == "voter_register":
    st.subheader("📝 Register")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    
    sec_q = st.selectbox("Security Question", [
        "What city were you born in?",
        "What is your favorite pet's name?",
        "What is your mother's maiden name?"
    ])
    sec_a = st.text_input("Security Answer", type="password")

    if st.button("Register"):
        res = register_voter(name, age, u, p, sec_q, sec_a)

        if res == "Success":
            st.success("Registered successfully!")
            st.session_state.step = "voter_login"
            st.rerun()
        else:
            st.error(res)
            
    if st.button("⬅️ Back"):
        st.session_state.step = "voter_choice"
        st.rerun()

elif st.session_state.step == "voter_login":
    st.subheader("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_voter(u, p)

        if user:
            st.session_state.user = dict(user) # Store dict in session
            st.session_state.step = "vote"
            st.rerun()
        else:
            st.error("Invalid credentials")
            
    if st.button("⬅️ Back"):
        st.session_state.step = "voter_choice"
        st.rerun()

elif st.session_state.step == "vote":
    st.subheader("🗳️ Cast Vote")

    if not is_voting_open():
        winner = get_winner()
        if winner:
            st.success(f"🏆 Election Closed! Winner: {winner['name']}")
        else:
            st.warning("Voting not started yet")

    else:
        for c in get_candidates():
            if st.button(f"Vote for {c['name']} ({c['party']})"):
                # Intercept the vote and go to security verification
                st.session_state.pending_vote = c['id']
                st.session_state.step = "verify_vote"
                st.rerun()
                    
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.step == "verify_vote":
    st.subheader("🔒 Security Verification Required")
    st.warning("Please answer your security question to unlock the ballot box and cast your vote!")
    
    st.write(f"**Question:** {st.session_state.user['security_question']}")
    answer = st.text_input("Your Answer", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm Vote"):
            if answer.strip().lower() == st.session_state.user['security_answer']:
                res = cast_vote(st.session_state.user['id'], st.session_state.pending_vote)
                if res == "Already voted":
                    st.error("You already voted")
                else:
                    st.success("Verification successful! Vote casted.")
                    st.session_state.step = "result"
                    st.rerun()
            else:
                st.error("Incorrect security answer!")
                
    with col2:
        if st.button("Cancel & Go Back"):
            st.session_state.step = "vote"
            st.rerun()
            
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.step == "result":
    st.subheader("📊 Your Vote & Results")

    vote = get_user_vote(st.session_state.user['id'])
    if vote:
        st.info(f"You voted for: {vote['name']}")

    results = get_results()
    if results:
        df = pd.DataFrame(results, columns=["Candidate", "Votes"])
        st.bar_chart(df.set_index("Candidate"))

    if not is_voting_open():
        winner = get_winner()
        if winner:
            st.success(f"🏆 Winner: {winner['name']} with {winner['total']} votes")
    else:
        st.warning("Voting still ongoing")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
        
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()



# import streamlit as st
# from models import *
# import pandas as pd




# st.title("🗳️ Online Voting System")

# # INIT
# if "step" not in st.session_state:
#     st.session_state.step = "start"

# # ---------------- START ----------------
# if st.session_state.step == "start":
#     role = st.selectbox("Select Role", ["Admin", "Voter"])

#     if st.button("Continue"):
#         if role == "Admin":
#             st.session_state.step = "admin_login"
#         else:
#             st.session_state.step = "voter_choice"   # ✅ CHANGED

#         st.rerun()

# # ================= ADMIN =================

# elif st.session_state.step == "admin_login":
#     st.subheader("🔐 Admin Login")

#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if login_admin(u, p):
#             st.session_state.step = "admin_dashboard"
#             st.rerun()
#         else:
#             st.error("Invalid credentials")

# elif st.session_state.step == "admin_dashboard":
#     st.subheader("👨‍💼 Admin Dashboard")

#     option = st.selectbox("Action", [
#         "Add Candidate",
#         "Delete Candidate",
#         "View Results",
#         "View Voters",
#         "Start Voting",
#         "Stop Voting"
#     ])

#     if option == "Add Candidate":
#         name = st.text_input("Candidate Name")
#         party = st.text_input("Party")

#         if st.button("Add"):
#             add_candidate(name, party)
#             st.success("Candidate added")

#     elif option == "Delete Candidate":
#         for c in get_candidates():
#             if st.button(f"Delete {c[1]}"):
#                 delete_candidate(c[0])
#                 st.rerun()

#     elif option == "View Results":
#         df = pd.DataFrame(get_results(), columns=["Candidate", "Votes"])
#         st.bar_chart(df.set_index("Candidate"))

#         if not is_voting_open():
#             winner = get_winner()
#             if winner:
#                 st.success(f"🏆 Winner: {winner[0]}")

#     elif option == "View Voters":
#         for v in get_voters():
#             st.write(f"{v[1]} | Age: {v[2]} | Username: {v[3]} | Voted: {v[4]}")

#     elif option == "Start Voting":
#         candidates=get_candidates()
#         if len(candidates)<2:
#             st.error("❌ Add at least 2 candidates before starting voting")
#         else:
            
            
#          set_voting_status(1)
#          st.success("Voting Started")

#     elif option == "Stop Voting":
#         set_voting_status(0)
#         st.success("Voting Stopped")

#         winner = get_winner()
#         if winner:
#             st.success(f"🏆 Winner: {winner[0]}")

#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

# # ================= VOTER =================

# # 🔹 NEW PAGE
# elif st.session_state.step == "voter_choice":
#     st.subheader("Voter Options")

#     choice = st.radio("Choose", ["Login", "Register"])

#     if st.button("Continue"):
#         if choice == "Login":
#             st.session_state.step = "voter_login"
#         else:
#             st.session_state.step = "voter_register"

#         st.rerun()
#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

# # 🔹 REGISTER
# elif st.session_state.step == "voter_register":
#     st.subheader("📝 Register")

#     name = st.text_input("Name")
#     age = st.number_input("Age", min_value=1)
#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")

#     if st.button("Register"):
#         res = register_voter(name, age, u, p)

#         if res == "Success":
#             st.session_state.step = "voter_login"
#             st.rerun()
#         else:
#             st.error(res)
#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

# # 🔹 LOGIN
# elif st.session_state.step == "voter_login":
#     st.subheader("🔐 Login")

#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = login_voter(u, p)

#         if user:
#             st.session_state.user = user
#             st.session_state.step = "vote"
#             st.rerun()
#         else:
#             st.error("Invalid credentials")
#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

# # 🔹 VOTING PAGE
# elif st.session_state.step == "vote":
#     st.subheader("🗳️ Cast Vote")

#     # Check voting status
#     if not is_voting_open():
#         winner = get_winner()

#         if winner:
#             st.success(f"🏆 Winner: {winner[0]}")
#         else:
#             st.warning("Voting not started yet")

#     else:
#         for c in get_candidates():
#             if st.button(f"Vote for {c[1]} ({c[2]})"):
#                 res = cast_vote(st.session_state.user[0], c[0])

#                 if res == "Already voted":
#                     st.error("You already voted")
#                 else:
#                     st.success("Vote casted")
#                     st.session_state.step = "result"
#                     st.rerun()
#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

# # 🔹 RESULT PAGE
# elif st.session_state.step == "result":
#     st.subheader("📊 Your Vote & Results")

#     # Show user's vote
#     vote = get_user_vote(st.session_state.user[0])
#     if vote:
#         st.info(f"You voted for: {vote[0]}")

#     # Graph
#     df = pd.DataFrame(get_results(), columns=["Candidate", "Votes"])
#     st.bar_chart(df.set_index("Candidate"))

#     # Winner
#     if not is_voting_open():
#         winner = get_winner()
#         if winner:
#             st.success(f"🏆 Winner: {winner[0]}")
#     else:
#         st.warning("Voting still ongoing")

#     if st.button("Restart"):
#         st.session_state.clear()
#         st.rerun()
#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()


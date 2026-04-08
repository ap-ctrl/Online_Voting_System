import streamlit as st
from models import *
import pandas as pd

st.title("🗳️ Online Voting System")

# INIT
if "step" not in st.session_state:
    st.session_state.step = "start"

# ---------------- START ----------------
if st.session_state.step == "start":
    role = st.selectbox("Select Role", ["Admin", "Voter"])

    if st.button("Continue"):
        st.session_state.role = role

        if role == "Admin":
            st.session_state.step = "admin_register"
        else:
            st.session_state.step = "voter_register"

        st.rerun()

# ================= ADMIN =================

elif st.session_state.step == "admin_register":
    st.subheader("Admin Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        res = register_admin(u, p)
        if res == "Success":
            st.session_state.step = "admin_login"
            st.rerun()
        else:
            st.error(res)

elif st.session_state.step == "admin_login":
    st.subheader("Admin Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        admin = login_admin(u, p)
        if admin:
            st.session_state.step = "admin_dashboard"
            st.rerun()
        else:
            st.error("Invalid")

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
        name = st.text_input("Name")
        party = st.text_input("Party")

        if st.button("Add"):
            add_candidate(name, party)
            st.success("Added")

    elif option == "Delete Candidate":
        candidates = get_candidates()

        for c in candidates:
            if st.button(f"Delete {c[1]}"):
                delete_candidate(c[0])
                st.rerun()

    elif option == "View Results":
        data = get_results()
        df = pd.DataFrame(data, columns=["Candidate", "Votes"])
        st.bar_chart(df.set_index("Candidate"))

        if not is_voting_open():
            winner = get_winner()
            st.success(f"🏆 Winner: {winner[0]}")

    elif option == "View Voters":
        voters = get_voters()

        for v in voters:
            st.write(f"{v[1]} | Age: {v[2]} | Username: {v[3]} | Voted: {v[4]}")

    elif option == "Start Voting":
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

elif st.session_state.step == "voter_register":
    st.subheader("Voter Register")

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

elif st.session_state.step == "voter_login":
    st.subheader("Voter Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_voter(u, p)
        if user:
            st.session_state.user = user
            st.session_state.step = "vote"
            st.rerun()
        else:
            st.error("Invalid")

elif st.session_state.step == "vote":
    st.subheader("Vote")

    if not is_voting_open():
        st.warning("Voting Closed")
    else:
        candidates = get_candidates()

        for c in candidates:
            if st.button(f"{c[1]} ({c[2]})"):
                res = cast_vote(st.session_state.user[0], c[0])

                if res == "Already voted":
                    st.error(res)
                else:
                    st.session_state.step = "result"
                    st.rerun()

elif st.session_state.step == "result":
    st.subheader("Results")

    data = get_results()
    df = pd.DataFrame(data, columns=["Candidate", "Votes"])
    st.bar_chart(df.set_index("Candidate"))

    if not is_voting_open():
        winner = get_winner()
        st.success(f"🏆 Winner: {winner[0]}")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
        
# import streamlit as st
# from models import *
# import pandas as pd

# st.title("🗳️ Online Voting System")

# # -------- INIT --------
# if "step" not in st.session_state:
#     st.session_state.step = "start"

# # -------- START PAGE --------
# if st.session_state.step == "start":
#     st.subheader("Select Role")

#     role = st.selectbox("Choose", ["Admin", "Voter"])

#     if st.button("Continue"):
#         st.session_state.role = role

#         if role == "Admin":
#             st.session_state.step = "admin_register"
#         else:
#             st.session_state.step = "voter_register"

#         st.rerun()

# # ================= ADMIN FLOW =================

# elif st.session_state.step == "admin_register":
#     st.subheader("Admin Registration")

#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")

#     if st.button("Register"):
#         res = register_admin(u, p)
#         if res == "Success":
#             st.session_state.step = "admin_login"
#             st.rerun()
#         else:
#             st.error(res)

# elif st.session_state.step == "admin_login":
#     st.subheader("Admin Login")

#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")

#     if st.button("Login"):
#         admin = login_admin(u, p)
#         if admin:
#             st.session_state.step = "admin_dashboard"
#             st.rerun()
#         else:
#             st.error("Invalid")

# elif st.session_state.step == "admin_dashboard":
#     st.subheader("Admin Dashboard")

#     option = st.selectbox("Action", ["Add Candidate", "View Results"])

#     if option == "Add Candidate":
#         name = st.text_input("Name")
#         party = st.text_input("Party")

#         if st.button("Add"):
#             add_candidate(name, party)
#             st.success("Added")

#     elif option == "View Results":
#         data = get_results()
#         df = pd.DataFrame(data, columns=["Candidate", "Votes"])

#         st.write(df)
#         st.bar_chart(df.set_index("Candidate"))

#     if st.button("Logout"):
#         st.session_state.clear()
#         st.rerun()

# # ================= VOTER FLOW =================

# elif st.session_state.step == "voter_register":
#     st.subheader("Voter Registration")

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

# elif st.session_state.step == "voter_login":
#     st.subheader("Voter Login")

#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")

#     if st.button("Login"):
#         user = login_voter(u, p)
#         if user:
#             st.session_state.user = user
#             st.session_state.step = "vote"
#             st.rerun()
#         else:
#             st.error("Invalid")

# elif st.session_state.step == "vote":
#     st.subheader("Vote")

#     candidates = get_candidates()

#     for c in candidates:
#         if st.button(f"{c[1]} ({c[2]})"):
#             res = cast_vote(st.session_state.user[0], c[0])
#             if res == "Already voted":
#                 st.error(res)
#             else:
#                 st.session_state.step = "result"
#                 st.rerun()

# elif st.session_state.step == "result":
#     st.subheader("Results")

#     data = get_results()
#     df = pd.DataFrame(data, columns=["Candidate", "Votes"])

#     st.bar_chart(df.set_index("Candidate"))

#     if st.button("Restart"):
#         st.session_state.clear()
#         st.rerun()
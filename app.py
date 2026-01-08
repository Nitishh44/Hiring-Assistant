import streamlit as st

st.markdown("""
<style>
/* Page background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Force all text to be visible */
html, body, [class*="css"] {
    color: #ffffff !important;
}

/* Chat message cards */
[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.25);
    color: #ffffff !important;
}

/* User message */
[data-testid="stChatMessage"][aria-label="user"] {
    background-color: rgba(0, 123, 255, 0.25);
    color: #ffffff !important;
}

/* Assistant message */
[data-testid="stChatMessage"][aria-label="assistant"] {
    background-color: rgba(40, 167, 69, 0.25);
    color: #ffffff !important;
}

/* Input box */
textarea, input {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #444 !important;
}

/* Progress bar */
div[role="progressbar"] > div {
    background-color: #00ffcc !important;
}

/* Buttons */
button {
    border-radius: 10px !important;
    background-color: #00b894 !important;
    color: white !important;
    border: none !important;
}

/* ========================= */
/* REMOVE ONLY THESE ELEMENTS */
/* ========================= */

/* Top right Fork button */
button[title="Fork"] {
    display: none !important;
}

/* Top right GitHub icon */
a[title="View source on GitHub"] {
    display: none !important;
}

/* Bottom right red Streamlit button */
[data-testid="stFloatingActionButton"] {
    display: none !important;
}

/* Bottom right profile picture */
img[alt="profile"],
button[aria-label="View profile"] {
    display: none !important;
}

/* ===== STREAMLIT CLOUD FINAL OVERRIDES ===== */

/* Hide top-right fork + github icon */
[data-testid="stToolbar"] button,
[data-testid="stToolbar"] a {
    visibility: hidden !important;
}

/* Hide bottom-right profile avatar */
[data-testid="stProfileAvatar"],
img[src*="avatar"],
img[src*="profile"] {
    visibility: hidden !important;
}

/* Attempt to hide red streamlit button (best effort) */
[data-testid="stFloatingActionButton"] {
    opacity: 0 !important;
    pointer-events: none !important;
}

/* ===== REMOVE BOTTOM RIGHT GITHUB PROFILE + RED BADGE ===== */

/* Profile picture */
img[src*="githubusercontent.com"],
img[src*="avatars"],
img[alt*="Nitish"],
img[alt*="profile"] {
    display: none !important;
}

/* Red "Created by" badge */
div[style*="position: fixed"][style*="bottom"],
div[style*="bottom: 0"],
div[style*="right: 0"],
div[class*="st-emotion-cache"] svg,
div[class*="st-emotion-cache"] button {
    display: none !important;
}

/* Streamlit cloud footer branding */
footer {
    visibility: hidden !important;
}



</style>
""", unsafe_allow_html=True)




st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")

st.markdown("""
<div style="text-align:center; padding: 25px 0 15px 0;">
    <h1 style="font-size:46px; margin-bottom:8px; color:white;">
        🤖 TalentScout Hiring Assistant
    </h1>
    <p style="font-size:18px; color:#e0e0e0;">
        Smart AI assistant for candidate screening & technical evaluation
    </p>
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns([8,1])
with col2:
    if st.button("🔄 Reset"):
        st.session_state.clear()
        st.rerun()



# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "candidate" not in st.session_state:
    st.session_state.candidate = {
        "name": "",
        "email": "",
        "phone": "",
        "experience": "",
        "position": "",
        "location": "",
        "tech_stack": ""
    }

if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []

if "tech_q_index" not in st.session_state:
    st.session_state.tech_q_index = 0

with st.sidebar:
    st.markdown("## 📋 Candidate Profile")
    st.write("Live profile preview")

    c = st.session_state.candidate
    st.markdown(f"""
    **Name:** {c.get('name', '')}  
    **Email:** {c.get('email', '')}  
    **Phone:** {c.get('phone', '')}  
    **Experience:** {c.get('experience', '')}  
    **Position:** {c.get('position', '')}  
    **Location:** {c.get('location', '')}  
    **Tech Stack:** {c.get('tech_stack', '')}
    """)


# Initial info questions
info_questions = [
    "What is your full name?",
    "What is your email address?",
    "What is your phone number?",
    "How many years of experience do you have?",
    "What position are you applying for?",
    "What is your current location?",
    "Please list your tech stack (e.g. Python, Django, MySQL):"
]

# Question bank
TECH_QUESTIONS = {
    "python": [
        "What is the difference between list and tuple in Python?",
        "Explain Python decorators.",
        "What are generators in Python?",
        "How does memory management work in Python?",
        "What is the Global Interpreter Lock (GIL)?"
    ],
    "django": [
        "What is Django ORM?",
        "Explain Django middleware.",
        "What are migrations in Django?",
        "Difference between function-based and class-based views?",
        "What is Django REST Framework?"
    ],
    "java": [
        "Explain OOP principles in Java.",
        "What is JVM and how does it work?",
        "Difference between abstract class and interface?",
        "What is garbage collection in Java?",
        "Explain multithreading in Java."
    ],
    "spring": [
        "What is Spring Boot?",
        "Explain dependency injection.",
        "What are Spring annotations?",
        "Difference between @Component and @Service?",
        "What is Spring MVC?"
    ],
    "react": [
        "What is JSX?",
        "Difference between state and props?",
        "What are React hooks?",
        "Explain useEffect hook.",
        "What is virtual DOM?"
    ],
    "mysql": [
        "What is normalization?",
        "Difference between INNER JOIN and LEFT JOIN?",
        "What are indexes in MySQL?",
        "Explain ACID properties.",
        "What is a primary key?"
    ]
}

total_steps = len(info_questions)
current_step = min(st.session_state.step, total_steps)
progress = int((current_step / total_steps) * 100)
st.progress(progress, text=f"Profile Completion: {progress}%")


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Greeting
if len(st.session_state.messages) == 0:
    greeting = "Hello 👋 Welcome to TalentScout Hiring Assistant! Let's start with your details."
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)

    first_question = info_questions[0]
    st.session_state.messages.append({"role": "assistant", "content": first_question})
    with st.chat_message("assistant"):
        st.markdown(first_question)

# Chat input
user_input = st.chat_input("💬 Type your answer here and press Enter...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # =========================
    # INFO COLLECTION PHASE
    # =========================
    if st.session_state.step < len(info_questions):
        step = st.session_state.step

        if step == 0:
            st.session_state.candidate["name"] = user_input
        elif step == 1:
            st.session_state.candidate["email"] = user_input
        elif step == 2:
            st.session_state.candidate["phone"] = user_input
        elif step == 3:
            st.session_state.candidate["experience"] = user_input
        elif step == 4:
            st.session_state.candidate["position"] = user_input
        elif step == 5:
            st.session_state.candidate["location"] = user_input
        elif step == 6:
            st.session_state.candidate["tech_stack"] = user_input

        st.session_state.step += 1

        if st.session_state.step < len(info_questions):
            next_q = info_questions[st.session_state.step]
            st.session_state.messages.append({"role": "assistant", "content": next_q})
            with st.chat_message("assistant"):
                st.markdown(next_q)
        else:
            # Generate tech questions
            tech_input = st.session_state.candidate["tech_stack"].lower()
            techs = [t.strip() for t in tech_input.split(",")]

            st.session_state.tech_questions = []

            for tech in techs:
                if tech in TECH_QUESTIONS:
                    st.session_state.tech_questions.extend(TECH_QUESTIONS[tech][:4])

            if not st.session_state.tech_questions:
                st.session_state.tech_questions.append("Please explain your main technical skills in detail.")

            intro = "✅ Thank you! Now let's start the technical round."
            st.session_state.messages.append({"role": "assistant", "content": intro})
            with st.chat_message("assistant"):
                st.markdown(intro)

            first_tech_q = f"**Question 1/{len(st.session_state.tech_questions)}:** {st.session_state.tech_questions[0]}"
            st.session_state.messages.append({"role": "assistant", "content": first_tech_q})
            with st.chat_message("assistant"):
                st.markdown(first_tech_q)

    # =========================
    # TECHNICAL QUESTIONS PHASE
    # =========================
    else:
        st.session_state.tech_q_index += 1

        if st.session_state.tech_q_index < len(st.session_state.tech_questions):
            q_no = st.session_state.tech_q_index + 1
            total_q = len(st.session_state.tech_questions)
            next_tech_q = f"**Question {q_no}/{total_q}:** {st.session_state.tech_questions[st.session_state.tech_q_index]}"
            st.session_state.messages.append({"role": "assistant", "content": next_tech_q})
            with st.chat_message("assistant"):
                st.markdown(next_tech_q)
        else:
            end_msg = "🎉 Thank you! You have completed the technical screening. Our team will get back to you soon."
            st.session_state.messages.append({"role": "assistant", "content": end_msg})
            with st.chat_message("assistant"):
                st.markdown(end_msg)


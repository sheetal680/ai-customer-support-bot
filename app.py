import streamlit as st

from faq_loader import load_faqs, build_faq_vectors
from embedder import get_embedding
from retriever import retrieve_best_faq
from responder import generate_answer
from moderator import is_safe
from chat_logger import log_conversation

# =========================================================
# 🔹 GLOBAL UI STYLE — CENTER CHAT (PROFESSIONAL SaaS LOOK)
# =========================================================
st.markdown("""
<style>
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 🔹 PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Customer Support Bot",
    layout="wide"
)

# =========================================================
# 🔹 SIDEBAR — BUSINESS SETTINGS
# =========================================================
st.sidebar.header("⚙️ Business Settings")
st.sidebar.caption("These settings affect how the AI responds.")

business_name = st.sidebar.text_input(
    "Business Name",
    value="My Business"
)

tone = st.sidebar.selectbox(
    "Support Tone",
    ["Friendly", "Formal"]
)

# =========================================================
# 🔹 APP TITLE
# =========================================================
st.title("🤖 AI Customer Support Bot")
st.caption("Ask any question related to the business FAQs.")

# =========================================================
# 🔹 LOAD FAQs (CACHED)
# =========================================================
@st.cache_resource
def load_faq_data():
    faqs = load_faqs()
    vectors = build_faq_vectors(faqs)
    return faqs, vectors

faqs, faq_vectors = load_faq_data()

# =========================================================
# 🔹 SESSION STATE (WELCOME MESSAGE — CHAT UX)
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            f"Hello 👋 Welcome to **{business_name}** support. "
            "How can I assist you today?"
        )
    }]

# =========================================================
# 🔹 DISPLAY CHAT HISTORY
# =========================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================================================
# 🔹 CHAT INPUT
# =========================================================
question = st.chat_input("Ask a question")

# =========================================================
# ✅ USER MESSAGE — FORCE RERUN (INSTANT DISPLAY)
# =========================================================
if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })
    st.rerun()

# =========================================================
# ✅ ASSISTANT RESPONSE — TRUST-FIRST LOGIC
# =========================================================
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_message = st.session_state.messages[-1]["content"]

    # A. Chat-style moderation (NO st.error)
    if not is_safe(last_user_message):
        answer = (
            "I’m here to help with business-related questions only. "
            "Please feel free to ask about our services."
        )
        matched_faq = ""
    else:
        with st.spinner("AI is typing..."):
            q_vec = get_embedding(last_user_message)
            best_faq, confidence = retrieve_best_faq(
                q_vec,
                faq_vectors,
                faqs
            )

            # B + C. Confidence-based blocking + human handoff
            if confidence < 0.35:
                answer = (
                    "I’m not fully sure about this. "
                    "Please contact our support team for accurate assistance."
                )
            else:
                answer = generate_answer(
                    best_faq,
                    last_user_message,
                    business_name,
                    tone
                )

            matched_faq = best_faq

            # Log conversation
            log_conversation(
                last_user_message,
                matched_faq,
                answer
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

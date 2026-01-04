import streamlit as st
from faq_loader import load_faqs
from retriever import retrieve_best_faq
from moderator import is_safe
from chat_logger import log_conversation

# ---------------- UI STYLE ----------------
st.set_page_config(page_title="AI Customer Support Bot", layout="wide")

st.markdown("""
<style>
.block-container { max-width: 900px; padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Business Settings")
business_name = st.sidebar.text_input("Business Name", "My Business")
tone = st.sidebar.selectbox("Support Tone", ["Friendly", "Formal"])

# ---------------- TITLE ----------------
st.title("🤖 AI Customer Support Bot")
st.caption("Ask any question related to the business FAQs.")

# ---------------- LOAD FAQS ----------------
@st.cache_resource
def load_data():
    return load_faqs()

faqs = load_data()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": f"Hello 👋 Welcome to **{business_name}** support. How can I help you?"
    }]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
question = st.chat_input("Ask a question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# ---------------- RESPONSE ----------------
if st.session_state.messages[-1]["role"] == "user":
    user_q = st.session_state.messages[-1]["content"]

    if not is_safe(user_q):
        answer = "I can help with business-related questions only."
        matched = ""
    else:
        best_faq, confidence = retrieve_best_faq(user_q, faqs)

        if confidence < 0.6:
            answer = (
                "I’m not fully sure about this. "
                "Please contact our support team for accurate assistance."
            )
            matched = ""
        else:
            answer = best_faq["answer"]
            matched = best_faq["question"]

        log_conversation(user_q, matched, answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

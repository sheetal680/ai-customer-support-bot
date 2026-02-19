import streamlit as st
from faq_loader import load_faqs
from retriever import retrieve_best_faq
from moderator import is_safe
from chat_logger import log_conversation
import tempfile
import os

# ---------------- UI STYLE ----------------
st.set_page_config(page_title="AI Customer Support Bot", layout="wide")

st.markdown("""
<style>
.block-container { max-width: 900px; padding-top: 2rem; }
.source-tag {
    font-size: 0.75rem;
    color: #888;
    margin-top: 4px;
    padding: 2px 8px;
    background: #1e1e1e;
    border-radius: 4px;
    display: inline-block;
}
.sample-q {
    font-size: 0.85rem;
    color: #aaa;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Business Settings")
business_name = st.sidebar.text_input("Business Name", "My Business")
tone = st.sidebar.selectbox("Support Tone", ["Friendly", "Formal"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Upload Custom FAQ")
uploaded_faq = st.sidebar.file_uploader("Upload FAQ file (.txt)", type=["txt"])

st.sidebar.markdown("---")
st.sidebar.markdown("**🤖 Powered by:** Groq LLaMA-3")
st.sidebar.markdown("**🔍 Mode:** RAG + Local Embeddings")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [{
        "role": "assistant",
        "content": f"Hello 👋 Welcome to **{business_name}** support. How can I help you?"
    }]
    st.rerun()

# ---------------- LOAD FAQS ----------------
@st.cache_resource
def load_data():
    return load_faqs()

@st.cache_resource
def load_custom_data(content):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        tmp_path = f.name
    faqs = load_faqs(tmp_path)
    os.unlink(tmp_path)
    return faqs

if uploaded_faq is not None:
    content = uploaded_faq.read().decode("utf-8")
    faqs = load_custom_data(content)
    st.sidebar.success("✅ Custom FAQ loaded!")
else:
    faqs = load_data()

# ---------------- TITLE ----------------
st.title("🤖 AI Customer Support Bot")
st.caption("Ask any question related to the business FAQs.")

# ---------------- SAMPLE QUESTIONS ----------------
st.markdown("**💡 Try asking:**")
col1, col2, col3 = st.columns(3)
sample_q = None
with col1:
    if st.button("🕐 Opening hours?"):
        sample_q = "What are your opening hours?"
with col2:
    if st.button("🚚 Home delivery?"):
        sample_q = "Do you offer home delivery?"
with col3:
    if st.button("💳 Payment methods?"):
        sample_q = "What payment methods do you accept?"

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
        if msg.get("source"):
            st.markdown(f'<span class="source-tag">📎 Source: {msg["source"]}</span>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
question = st.chat_input("Ask a question") or sample_q

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

# ---------------- RESPONSE ----------------
if st.session_state.messages[-1]["role"] == "user":
    user_q = st.session_state.messages[-1]["content"]

    if not is_safe(user_q):
        answer = "I can help with business-related questions only."
        matched = ""
        source = ""
    else:
        best_faq, confidence = retrieve_best_faq(user_q, faqs)

        if confidence < 0.6:
            answer = (
                "I'm not fully sure about this. "
                "Please contact our support team for accurate assistance."
            )
            matched = ""
            source = ""
        else:
            answer = best_faq["answer"]
            matched = best_faq["question"]
            source = f'FAQ: "{matched}"'

        log_conversation(user_q, matched, answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "source": source
    })
    st.rerun()
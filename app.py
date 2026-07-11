import matplotlib
matplotlib.use("Agg")
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# LOAD CSS
# ==============================

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

local_css("style.css")

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.title("📱 WhatsApp Chat Analyzer")

    st.markdown("---")

    st.markdown("### 📂 Upload Chat")

    uploaded_file = st.file_uploader(
        "Choose exported WhatsApp chat (.txt)",
        type=["txt"]
    )

    if uploaded_file:
        st.success("✅ Chat Loaded Successfully")

    st.markdown("---")

# ==============================
# HERO SECTION
# ==============================

st.markdown("""
<div class="hero">
    <h1>📱 WhatsApp Chat Analyzer</h1>
    <p>
        Discover insights from your WhatsApp conversations using
        Python, Data Analytics and NLP.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================
# START ANALYSIS
# ==============================

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df["user"].unique().tolist()

    if "group_notification" in user_list:
        user_list.remove("group_notification")

    user_list.sort()

    user_list.insert(0, "Overall")

    st.sidebar.markdown("### 👤 Select User")

    selected_user = st.sidebar.selectbox(
        "Choose user",
        user_list
    )

    analyze = st.sidebar.button(
        "🚀 Show Analysis",
        use_container_width=True
    )

    if analyze:
        st.write("Starting analysis...")

        st.write("1")
        helper.fetch_stats(selected_user, df)
    
        st.write("2")
        helper.monthly_timeline(selected_user, df)
    
        st.write("3")
        helper.daily_timeline(selected_user, df)
    
        st.write("4")
        helper.week_activity_map(selected_user, df)
    
        st.write("5")
        helper.month_activity_map(selected_user, df)
    
        st.write("6")
        helper.activity_heatmap(selected_user, df)
    
        st.write("7")
        helper.create_wordcloud(selected_user, df)
    
        st.write("8")
        helper.most_common_words(selected_user, df)
    
        st.write("9")
        helper.emoji_helper(selected_user, df)
    
        st.success("All helper functions executed successfully!")

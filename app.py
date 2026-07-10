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
        # =====================================
        # DASHBOARD OVERVIEW
        # =====================================

        st.subheader("📊 Dashboard Overview")

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user,
            df
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="💬 Messages",
                value=f"{num_messages:,}"
            )

        with col2:
            st.metric(
                label="📝 Words",
                value=f"{words:,}"
            )

        with col3:
            st.metric(
                label="🖼️ Media",
                value=f"{num_media_messages:,}"
            )

        with col4:
            st.metric(
                label="🔗 Links",
                value=f"{num_links:,}"
            )

        st.divider()

        # =====================================
        # MONTHLY TIMELINE
        # =====================================

        st.subheader("📈 Monthly Timeline")

        timeline = helper.monthly_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(12,4))

        ax.plot(
            timeline["time"],
            timeline["message"],
            color="#25D366",
            linewidth=3
        )

        ax.grid(alpha=.3)

        plt.xticks(rotation=45)

        st.pyplot(fig, use_container_width=True)

        st.divider()

        # =====================================
        # DAILY TIMELINE
        # =====================================

        st.subheader("📅 Daily Timeline")

        daily_timeline = helper.daily_timeline(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(12,4))

        ax.plot(
            daily_timeline["only_date"],
            daily_timeline["message"],
            color="#075E54",
            linewidth=3
        )

        ax.grid(alpha=.3)

        plt.xticks(rotation=45)

        st.pyplot(fig, use_container_width=True)

        st.divider()

        # =====================================
        # ACTIVITY MAP
        # =====================================

        st.divider()

        st.subheader("🔥 Activity Map")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📅 Most Active Day")

            busy_day = helper.week_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(6, 4))

            ax.bar(
                busy_day.index,
                busy_day.values,
                color="#25D366"
            )

            ax.set_ylabel("Messages")

            ax.grid(axis="y", alpha=.3)

            plt.xticks(rotation=45)

            st.pyplot(fig, use_container_width=True)

        with col2:

            st.markdown("### 🗓️ Most Active Month")

            busy_month = helper.month_activity_map(
                selected_user,
                df
            )

            fig, ax = plt.subplots(figsize=(6, 4))

            ax.bar(
                busy_month.index,
                busy_month.values,
                color="#128C7E"
            )

            ax.set_ylabel("Messages")

            ax.grid(axis="y", alpha=.3)

            plt.xticks(rotation=45)

            st.pyplot(fig, use_container_width=True)

        # =====================================
        # WEEKLY ACTIVITY HEATMAP
        # =====================================

        st.divider()

        st.subheader("📊 Weekly Activity Heatmap")

        user_heatmap = helper.activity_heatmap(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        sns.heatmap(
            user_heatmap,
            cmap="YlGn",
            linewidths=.5,
            ax=ax
        )

        plt.xticks(rotation=45)

        st.pyplot(fig, use_container_width=True)

        # =====================================
        # MOST ACTIVE USERS
        # =====================================

        if selected_user == "Overall":
            st.divider()

            st.subheader("👥 Most Active Users")

            x, new_df = helper.most_busy_users(df)

            col1, col2 = st.columns([2, 1])

            with col1:
                fig, ax = plt.subplots(figsize=(8, 4))

                ax.bar(
                    x.index,
                    x.values,
                    color="#25D366"
                )

                ax.set_ylabel("Messages")

                ax.grid(axis="y", alpha=.3)

                plt.xticks(rotation=45)

                st.pyplot(fig, use_container_width=True)

            with col2:
                st.markdown("### 📋 Ranking")

                st.dataframe(
                    new_df,
                    use_container_width=True,
                    hide_index=True
                )

        # =====================================
        # WORD CLOUD
        # =====================================

        st.divider()

        st.subheader("☁️ Word Cloud")

        df_wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.imshow(df_wc)

        ax.axis("off")

        st.pyplot(fig, use_container_width=True)

        # =====================================
        # MOST COMMON WORDS
        # =====================================

        st.divider()

        st.subheader("📝 Most Common Words")

        most_common_df = helper.most_common_words(
            selected_user,
            df
        )

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.barh(
            most_common_df[0],
            most_common_df[1],
            color="#25D366"
        )

        ax.set_xlabel("Frequency")

        ax.grid(axis="x", alpha=.3)

        st.pyplot(fig, use_container_width=True)

        # =====================================
        # EMOJI ANALYSIS
        # =====================================

        st.divider()

        st.subheader("😊 Emoji Analysis")

        emoji_df = helper.emoji_helper(
            selected_user,
            df
        )

        col1, col2 = st.columns([1, 1])

        with col1:

            st.markdown("### Emoji Frequency")

            st.dataframe(
                emoji_df,
                use_container_width=True,
                hide_index=True
            )

        with col2:

            if not emoji_df.empty:

                fig, ax = plt.subplots(figsize=(6, 6))

                ax.pie(
                    emoji_df["Count"].head(),
                    labels=emoji_df["Emoji"].head(),
                    autopct="%1.1f%%",
                    startangle=90
                )

                ax.axis("equal")

                st.pyplot(fig, use_container_width=True)

            else:

                st.info("No emojis found in this chat.")


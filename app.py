import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import helper
import preprocessor

st.sidebar.title("Whatsapp Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.remove('Meta AI')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analyse"):
        num_msg,words,num_media,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Stats")
       
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.markdown("<h4>Total Messages</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px;'>{num_msg}</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<h4>Total Words</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px;'>{words}</p>", unsafe_allow_html=True)
        with col3:
            st.markdown("<h4>Total Media</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px;'>{num_media}</p>", unsafe_allow_html=True)
        with col4:
            st.markdown("<h4>Total Links</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px;'>{num_links}</p>", unsafe_allow_html=True)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #find active user
        if selected_user=='Overall':
            st.title("Most busy users")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #wordcloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            top_5_emojis = emoji_df.head(5)
            top_5_emojis['percentage'] = (top_5_emojis['count'] / top_5_emojis['count'].sum()) * 100

            # Plot the pie chart
            fig, ax = plt.subplots()
            ax.pie(
                top_5_emojis['count'],
                labels=top_5_emojis['emoji'],
                autopct='%1.1f%%',
                startangle=140
            )
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the pie chart in Streamlit
            st.pyplot(fig)



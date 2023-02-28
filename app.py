import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer and Sentiment Analyser")
st.sidebar.subheader("Sameer Edlabadkar")
app_mode = st.sidebar.selectbox('Choose the App mode',
['About App','Statastical Analyser for Group Message','Statastical Analyser for Personal Message','Sentiment Analyser']
)

if app_mode =='About App':
    st.title("Message from Devloper:")
    st.write("Hello Users, please note that this application is intended for educational purposes only. To use it, please refer to the sidebar on the left-hand side of the screen and select the TXT format file. Before uploading your file, please ensure that the datetime format in your text file is in 24-hour format and follows the British English date format (i.e in this format: 13/02/2023, 14:47). We hope you enjoy using this application for your coding needs. Thank you!")

    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    st.title('Gallery')
    col1, col2 = st.columns(2)
    with col1:
        st.image('1.png')
        st.image('2.png')
        st.image('3.png')
    with col2:
        st.image('5.png')
        st.image('4.png')


    st.markdown('''
              # About Me \n 
                Hey this is **Sameer Edlabadkar**. Working on the technologies such as **Data Science, Machine Learning, Tensorflow, ResNet50, IoT**. \n

                Also check me out on **Social Media**
                - [YouTube](https://www.youtube.com/@edlabadkarsameer/videos)
                - [LinkedIn](https://www.linkedin.com/in/sameer-edlabadkar-43b48b1a7/)
                - [GitHub](https://github.com/edlabadkarsameer)
                - If you are facing any issue while working feel free to mail me on **edlabadkarsameer@gmail.com**

                ''')



elif app_mode =='Statastical Analyser for Group Message':
    uploaded_file = st.sidebar.file_uploader("Choose a TXT file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis on",user_list)

        if st.sidebar.button("Analyse"):

            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
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
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

            # finding the busiest users in the group(Group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x,new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # WordCloud
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # most common words
            most_common_df = helper.most_common_words(selected_user,df)

            fig,ax = plt.subplots()

            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Frequently Used Words')
            st.pyplot(fig)

            # emoji analysis
            emoji_df = helper.emoji_helper(selected_user,df)
            st.title("Emoji Analysis")

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
elif app_mode =='Statastical Analyser for Personal Message':
    uploaded_file = st.sidebar.file_uploader("Choose a TXT file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis on",user_list)

        if st.sidebar.button("Analyse"):

            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
            st.title("Top Statistics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(num_links)

            # monthly timeline
            st.title("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='green')
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
            col1,col2 = st.columns(2)

            with col1:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Most busy month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

            # finding the busiest users in the group(Group level)
            if selected_user == 'Overall':
                st.title('Most Busy Users')
                x,new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values,color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)

            # WordCloud
            st.title("Wordcloud")
            df_wc = helper.create_wordcloud(selected_user,df)
            fig,ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)

            # most common words
            most_common_df = helper.most_common_words(selected_user,df)

            fig,ax = plt.subplots()

            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')

            st.title('Frequently Used Words')
            st.pyplot(fig)

            # emoji analysis
            emoji_df = helper.emoji_helper(selected_user,df)
            st.title("Emoji Analysis")

            col1,col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)


else:
    uploaded_file = st.sidebar.file_uploader("Choose a TXT file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")

        selected_user = st.sidebar.selectbox("Show analysis on",user_list)

        if st.sidebar.button("Analyse"):

            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)


            # sentiment analysis
            st.title("Sentiment Analysis")
            sameer = helper.sentiment_ana(selected_user,df)
            import nltk
            from nltk.sentiment import SentimentIntensityAnalyzer
            l = num_messages
            neg_score = 0
            neu_score = 0
            pos_score = 0
            compound_score = 0
            for i in range(1, l - 1):
                text = df.message[i]
                sia = SentimentIntensityAnalyzer()
                sentiment = sia.polarity_scores(text)
                neg_score = sentiment['neg'] + neg_score
                neu_score = sentiment['neu'] + neu_score
                pos_score = sentiment['pos'] + pos_score
                compound_score = sentiment['compound'] + compound_score

            neg_score = neg_score / l
            neu_score = neu_score / l
            pos_score = pos_score / l
            compound_score = compound_score / l
            print('Negative score:', neg_score)
            print('Neutral score:', neu_score)
            print('Positive score:', pos_score)
            print('Compound score:', compound_score)

            max_score = max((neg_score, 'Negative'), (neu_score, 'Neutral'), (pos_score, 'Positive'),
                            key=lambda x: x[0])
            sentiment = str('Sentiment: '+max_score[1])
            st.title(sentiment)
            st.write("Negative Score: ",neg_score)
            st.write("Positive Score: ", pos_score)
            st.write("Neutral Score: ", neu_score)
            st.write("Compound Score: ", compound_score)











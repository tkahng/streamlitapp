import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import sqlite3
import plotly.express as px
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt

plotlydb = 'data/plotly.db'
# naverblogdb = 'data/NaverBlogDB.db'

st.title('My first app')


@st.cache
def dfFromSql(dbpath, query, params=None):
    con = sqlite3.connect(dbpath)
    df = pd.read_sql(query, con, params=params).reset_index(drop=True)
    con.close()
    return df

st.subheader('Categories')
# st.header("Chart with two lines")
catlvls = dfFromSql(plotlydb, 'SELECT * FROM ALLCAT_DF').convert_dtypes()
fig = px.sunburst(catlvls, path=['ct_1_text', 'ct_2_text', 'ct_3_text'], values='count', color='ct_2_text', branchvalues='total')
# fig.show()

st.write(fig)

st.subheader('Daily mt_view Availability')
mt_view_avail = dfFromSql(plotlydb, 'SELECT * FROM daily_mt_view_avail').convert_dtypes()
fig2 = px.bar(mt_view_avail, x="date", y="lv_no", color="mt_isdelivery", title="Daily-Material-View-Availability", barmode='relative')
# fig2.show()
st.write(fig2)


st.subheader('Daily top 3 categories')
user_mt_log = dfFromSql(plotlydb, 'SELECT * FROM user_mt_log').convert_dtypes()
fig3 = px.bar(user_mt_log, x="date", y="counts", color="ct_2_text", title="Daily-Material-View-Top3", barmode='relative')
# fig3.show()
st.write(fig3)

# st.subheader('hastagwordcloud')
# hastags = dfFromSql(naverblogdb, 'SELECT * FROM post_tags').convert_dtypes()
# words = ' '.join(hastags['tags'])
# wordcloud = WordCloud().generate(words)
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()
# st.pyplot()
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import sqlite3
import plotly.express as px
# import altair as alt
# alt.data_transformers.disable_max_rows()
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

def fndf(df, fn, cols):
    df[cols] = fn(df[cols])
    return df

mt_catmap_df = dfFromSql(plotlydb, 'SELECT * FROM mt_catmap_df').convert_dtypes()
# catlvls = dfFromSql(plotlydb, 'SELECT * FROM ALLCAT_DF').convert_dtypes()
# df = dfFromSql(plotlydb, 'SELECT * FROM mtdf').convert_dtypes()

st.subheader('Categories')
# st.header("Chart with two lines")
fig = px.treemap(
#     mt_catmap_df.pipe(cfilter, lambda x: x.ct_1_text.str.contains('자재 카테고리')), 
    mt_catmap_df,
    path=['ct_1_text', 'ct_2_text', 'ct_3_text', 'mt_name'], 
#     values='mt_no', 
#     color='ct_2_text', 
#     branchvalues='total',
    maxdepth=2
)
# fig = px.sunburst(catlvls, path=['ct_1_text', 'ct_2_text', 'ct_3_text'], values='count', color='ct_2_text', branchvalues='total')
# fig.show()

st.write(fig)

# st.subheader('daily vendor mt views')
# histfig = px.histogram(df, x="lv_registerdate", color="vd_name", marginal="rug")
# st.write(histfig)

# st.subheader('daily vendor mt views stripplot')
# stripfig = px.strip(df, x='lv_registerdate', y='vd_name', color='vd_name')
# st.write(stripfig)

# st.subheader('daily vendor mt views scatter bin')
# binplot = alt.Chart(df.copy().pipe(fndf, lambda x: x.astype('datetime64[ns]').dt.strftime('%Y%m%d').astype('datetime64[ns]'), 'lv_registerdate')).mark_circle().encode(
#     alt.X('lv_registerdate', bin=True),
#     alt.Y('vd_name'),
#     size='count()',
#     color='vd_name:N'
# )
# st.altair_chart(binplot, use_container_width=True)


# st.subheader('Daily mt_view Availability')
# # mt_view_avail = dfFromSql(plotlydb, 'SELECT * FROM daily_mt_view_avail').convert_dtypes()
# # fig2 = px.bar(mt_view_avail, x="date", y="lv_no", color="mt_isdelivery", title="Daily-Material-View-Availability", barmode='relative')
# fig2 = px.histogram(df, x="lv_registerdate", color="mt_isdelivery")
# # fig2.show()
# st.write(fig2)


# st.subheader('Daily categories')
# fig3 = px.histogram(df, x="lv_registerdate", color="ct_text", marginal="rug")
# # user_mt_log = dfFromSql(plotlydb, 'SELECT * FROM user_mt_log').convert_dtypes()
# # fig3 = px.bar(user_mt_log, x="date", y="counts", color="ct_2_text", title="Daily-Material-View-Top3", barmode='relative')
# # fig3.show()
# st.write(fig3)

# # st.subheader('hastagwordcloud')
# # hastags = dfFromSql(naverblogdb, 'SELECT * FROM post_tags').convert_dtypes()
# # words = ' '.join(hastags['tags'])
# # wordcloud = WordCloud().generate(words)
# # plt.imshow(wordcloud, interpolation='bilinear')
# # plt.axis("off")
# # plt.show()
# # st.pyplot()
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.title("CSV Reader")
expected = st.file_uploader('Inserte el archivo csv de expected', type = 'csv')
counted = st.file_uploader('Inserte el archivo csv de counted', type = 'csv')

if (expected & counted):
    df_expected = pd.read_csv(expected)
    df2_counted = pd.read_csv(counted)
    st.dataframe(df_expected, 200, 100)
    st.dataframe(df2_counted, 200, 100)
    st.markdown("---")
    # fig1 = plt.figure(figsize=(10,4))
    # sns.countplot(x='Pclass', data=df)

    # st.pyplot(fig1)

    # fig2 = plt.figure(figsize=(10,4))
    # sns.boxplot(x='Pclass', 
    #             y='Age',
    #             data=df
    # )

    # st.pyplot(fig2)



import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.title("CSV Reader")
expected = st.file_uploader('Inserte el archivo csv de expected', type = 'csv')
counted = st.file_uploader('Inserte el archivo csv de counted', type = 'csv')

if (expected and counted):
    df_expected = pd.read_csv(expected, encoding="latin-1", dtype=str)
    df2_counted = pd.read_csv(counted, encoding="latin-1", dtype=str)
    #st.dataframe(df_expected)
    #st.dataframe(df2_counted)
    st.markdown("---")

# Data engineering over the two source of information

    df2_counted = df2_counted.drop_duplicates('RFID')
    df_B = df2_counted.groupby ("Retail_Product_SKU"). count()[["RFID"]].reset_index().rename(columns={"RFID":"Retail_CCQTY"})

    columnas = ['Retail_Product_Color' , 
    'Retail_Product_Level1',
    'Retail_Product_Level1Name',
    'Retail_Product_Level2Name',
    'Retail_Product_Level3Name',
    'Retail_Product_Level4Name',
    'Retail_Product_Name',
    'Retail_Product_SKU',
    'Retail_Product_Size',
    'Retail_Product_Style',
    'Retail_SOHQTY'
    ]

    df_A = df_expected[columnas]

    df_discrepancy = pd.merge(df_A, df_B, how='outer', left_on='Retail_Product_SKU', right_on='Retail_Product_SKU', indicator = True)

    df_discrepancy['Retail_CCQTY'] =  df_discrepancy['Retail_CCQTY'].fillna(0).astype(int)
    df_discrepancy['Retail_SOHQTY'] =  df_discrepancy['Retail_SOHQTY'].fillna(0).astype(int)

    df_discrepancy['Diff'] = df_discrepancy["Retail_CCQTY"] - df_discrepancy["Retail_SOHQTY"]

    df_discrepancy.loc[df_discrepancy["Diff"]<0, "Unders"] = df_discrepancy["Diff"] * (-1)
    df_discrepancy['Unders'] =  df_discrepancy['Unders'].fillna(0).astype(int)

    df_discrepancy.loc[(df_discrepancy["Retail_SOHQTY"]>0) & (df_discrepancy["Retail_CCQTY"]>0), "match"]  = 1.0
    df_discrepancy['match'] =  df_discrepancy['match'].fillna(0).astype(int)

    #st.dataframe(df_discrepancy)

    # Using a sidebar
    st.sidebar.header("Por favor utilice los siguientes filtros")

    Retail_Product_Level1Name = st.sidebar.multiselect(
        'Seleccione un tipo de producto:',
        options = df_discrepancy['Retail_Product_Level1Name'].unique(),
        default = df_discrepancy['Retail_Product_Level1Name'].unique()
    )

    Retail_Product_Color = st.sidebar.multiselect(
        'Seleccione el tipo de color del producto:',
        options = df_discrepancy['Retail_Product_Color'].unique(),
        default = df_discrepancy['Retail_Product_Color'].unique()
    )


    df_selection = df_discrepancy.query(
        "Retail_Product_Level1Name == @Retail_Product_Level1Name & Retail_Product_Color == @Retail_Product_Color"
    )

    st.dataframe(df_selection)

    st.title('Inventory Discrepancy')
    st.markdown('##')

    df_barras = df_selection.groupby ("Retail_Product_Level1"). sum()[["Retail_SOHQTY", "Retail_CCQTY"]].reset_index()

    # KPIs 
    operational_accuracy = (int( df_selection['match'].sum()) / int( df_selection['Retail_SOHQTY'].sum()))*100
    inventory_accuracy = (int( df_selection['match'].sum()) / int( df_selection['Retail_CCQTY'].sum()))*100


    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader('Operational Accuracy: ')
        st.subheader( f" {operational_accuracy:,}")
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x="Retail_SOHQTY", y="Retail_Product_Level1", data=df_barras)


    with right_column:
        st.subheader('Inventory Accuracy: ')
        st.subheader( f" {inventory_accuracy:,}")
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x="Retail_CCQTY", y="Retail_Product_Level1", data=df_barras)



    st.markdown('---')










import os
import pandas as pd
import streamlit as st

# Display information in Streamlit app
st.title("***Developed By Priyank Tomar***")
st.write("Current Working Directory: ", os.getcwd())

# File upload via Streamlit interface
file = st.file_uploader("Please select a file", type=["xlsx", "xls"])
if file is not None:
    df = pd.read_excel(file)

    # Display first few rows of the dataframe
    st.write(df.head())

    # Sheet type input
    type = st.selectbox("Input sheet is on", ["BBH", "Continue"])

    # Define KPI Object
    KPI_Obj = ['Cell Avail excl BLU', 'RRC_CONN_UE_MAX (M8001C200)', 'Avg PDCP cell thp DL',
               'Avg IP thp DL QCI9', 'Total LTE data volume, DL + UL', 'Perc DL PRB Util',
               'Avg UE distance', 'Average CQI', 'Avg RRC conn UE', 'inter eNB E-UTRAN HO SR X2',
               'Intra eNB HO SR', 'E-RAB DR RAN', 'E-UTRAN E-RAB stp SR', 'Total E-UTRAN RRC conn stp SR']

    # Processing Functions
    def DayPLMN(df):
        st.write("Processing Day PLMN Level...")
        df1 = df.copy()
        df1 = df1.drop([0], axis=0)
        df1['Start Time'] = pd.to_datetime(df1['Period start time'])
        df1["Date"] = df1["Period start time"].dt.date
        df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
        pivot1 = pd.pivot_table(df1, index=['MRBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')
        pivot1 = pivot1.stack(level=0).reset_index(drop=False)
        pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)
        st.write(pivot1)

    def DaySite(df):
        st.write("Processing Day Site Level...")
        df1 = df.copy()
        df1 = df1.drop([0], axis=0)
        df1['Start Time'] = pd.to_datetime(df1['Period start time'])
        df1["Date"] = df1["Period start time"].dt.date
        df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
        pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')
        pivot1 = pivot1.stack(level=0).reset_index(drop=False)
        pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)
        st.write(pivot1)

    def DaySEG(df):
        st.write("Processing Day Cell Level...")
        df1 = df.copy()
        df1 = df1.drop([0], axis=0)
        df1['Start Time'] = pd.to_datetime(df1['Period start time'])
        df1["Date"] = df1["Period start time"].dt.date
        df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
        pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')
        pivot1 = pivot1.stack(level=0).reset_index(drop=False)
        pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)
        st.write(pivot1)

    def HourCellWithoutInput(df):
        st.write("Processing Hour Cell Level Without Input...")
        df1 = df.copy()
        df1 = df1.drop([0], axis=0)
        df1['Start Time'] = pd.to_datetime(df1['Period start time'])
        df1["Date"] = df1["Period start time"].dt.date
        df1["Hour"] = df1["Period start time"].dt.hour
        df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
        pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNCEL name'], columns=['Date', 'Hour'], values=KPI_Obj, aggfunc='sum', dropna=False)
        pivot1 = pivot1.stack(level=0).reset_index(drop=False)
        pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)
        st.write(pivot1)

    def HourCell(df, Hourinput):
        st.write(f"Processing Hour Cell Level for Hour {Hourinput}...")
        df1 = df.copy()
        df1 = df1.drop([0], axis=0)
        df1['Start Time'] = pd.to_datetime(df1['Period start time'])
        df1["Date"] = df1["Period start time"].dt.date
        df1["Hour"] = df1["Period start time"].dt.hour
        df1 = df1[(df1['Hour'] == Hourinput)]
        df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
        pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')
        pivot1 = pivot1.stack(level=0).reset_index(drop=False)
        pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)
        st.write(pivot1)

    # Logic to choose based on sheet type and date uniqueness
    df['Start Time'] = pd.to_datetime(df['Period start time'])
    df["Date"] = df["Period start time"].dt.date
    unique_dates = df['Date'].nunique()

    if type == "BBH" and "LNCEL name" in df.columns:
        DaySEG(df)
    elif type == "Continue" and "PLMN Name" in df.columns and "CS RRC SR" in df.columns:
        if len(df.iloc[2, 0]) <= 10:
            DayPLMN(df)
    elif type == "Continue" and "LNCEL name" in df.columns:
        if unique_dates == 1:
            st.write("Unique date found, processing without Hour input.")
            HourCellWithoutInput(df)
        else:
            Hourinput = st.number_input("Input Hour", min_value=0, max_value=23)
            HourCell(df, Hourinput)
    else:
        st.write("Wrong input file provided")

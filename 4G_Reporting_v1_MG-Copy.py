import os
import pandas as pd
import streamlit as st

# List of KPIs to process
KPI_Obj = [
    'Cell Avail excl BLU', 'RRC_CONN_UE_MAX (M8001C200)', 'Avg PDCP cell thp DL',
    'Avg IP thp DL QCI9', 'Total LTE data volume, DL + UL', 'Perc DL PRB Util',
    'Avg UE distance', 'Average CQI', 'Avg RRC conn UE', 'inter eNB E-UTRAN HO SR X2',
    'Intra eNB HO SR', 'E-RAB DR RAN', 'E-UTRAN E-RAB stp SR', 'Total E-UTRAN RRC conn stp SR'
]

# Function to read the file (using Streamlit file uploader)
def read_file():
    st.write("***Developed By Priyank Tomar***")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df['Period start time'] = pd.to_datetime(df['Period start time'])
        df["Date"] = df["Period start time"].dt.date
        return df, uploaded_file.name
    else:
        st.write("Please upload a file to proceed.")
        return None, None

# Function for Day Cell Level Processing (updated)
def DaySEG(df):
    st.write("Processing Day Cell Level...")
    df1 = df.copy()
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')

    pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')

    # Ensure 'Date' is included properly in the output
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)

    # Reset the index and drop serial number (index)
    pivot1.reset_index(drop=True, inplace=True)

    st.write(pivot1)

# Function for Day PLMN Level Processing (updated)
def DayPLMN(df):
    st.write("Processing Day PLMN Level...")
    df1 = df.copy()
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')

    pivot1 = pd.pivot_table(df1, index=['MRBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')

    # Ensure 'Date' is included properly in the output
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)

    # Reset the index and drop serial number (index)
    pivot1.reset_index(drop=True, inplace=True)

    st.write(pivot1)

# Function for Hour Cell Level Processing without hour input (updated)
def HourCellWithoutInput(df):
    st.write("Processing Hour Cell Level Without Input...")
    df1 = df.copy()
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1["Hour"] = df1["Period start time"].dt.hour
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')

    pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNCEL name'], columns=['Date', 'Hour'], values=KPI_Obj, aggfunc='sum', dropna=False)

    # Ensure 'Date' is included properly in the output
    pivot1 = pivot1.stack(level=[0,1]).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)

    # Reset the index and drop serial number (index)
    pivot1.reset_index(drop=True, inplace=True)

    st.write(pivot1)

# Function for Hour Cell Level Processing with hour input (updated)
def HourCell(df, Hourinput):
    st.write("Processing Hour Cell Level with Input...")
    df1 = df.copy()
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1["Hour"] = df1["Period start time"].dt.hour
    df1 = df1[(df1['Hour'] == Hourinput)]
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')

    pivot1 = pd.pivot_table(df1, index=['MRBTS name', 'LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')

    # Ensure 'Date' is included properly in the output
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)

    # Reset the index and drop serial number (index)
    pivot1.reset_index(drop=True, inplace=True)

    st.write(pivot1)

# Main logic to choose based on sheet type and date uniqueness
def process_data():
    df, filename = read_file()

    if df is not None:
        unique_dates = df['Date'].nunique()
        df_columns_list = df.columns

        # Ask user for input on the sheet type
        sheet_type = st.selectbox("Select Sheet Type", ["BBH", "Continue"])

        if sheet_type == "BBH" and "LNCEL name" in df_columns_list:
            DaySEG(df)
        elif sheet_type == "Continue" and "PLMN Name" in df_columns_list and "CS RRC SR" in df_columns_list:
            len_period = len(df.iloc[2, 0])
            if len_period <= 10:
                DayPLMN(df)
        elif sheet_type == "Continue" and "LNCEL name" in df_columns_list:
            if unique_dates == 1:
                st.write("Unique date found, processing without Hour input.")
                HourCellWithoutInput(df)
            else:
                Hourinput = st.number_input("Input Hour", min_value=0, max_value=23)
                HourCell(df, Hourinput)
        else:
            st.write("Wrong input file provided")

# Run the Streamlit app
if __name__ == "__main__":
    st.title('LTE Data Processing Application')
    process_data()

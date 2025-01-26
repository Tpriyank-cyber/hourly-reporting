import streamlit as st
import pandas as pd

# Streamlit App Title
st.title("LTE KPI Processing Tool")

# File Uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

# KPI Object List
KPI_Obj = [
    'Cell Avail excl BLU','RRC_CONN_UE_MAX (M8001C200)','Avg PDCP cell thp DL',
    'Avg IP thp DL QCI9','Total LTE data volume, DL + UL','Perc DL PRB Util',
    'Avg UE distance','Average CQI','Avg RRC conn UE','inter eNB E-UTRAN HO SR X2',
    'Intra eNB HO SR','E-RAB DR RAN','E-UTRAN E-RAB stp SR','Total E-UTRAN RRC conn stp SR'
]

# Function for Processing Data
def process_data(df, processing_type, hour_input=None):
    df['Start Time'] = pd.to_datetime(df['Period start time'])
    df["Date"] = df["Period start time"].dt.date

    # Convert KPI columns to float
    for kpi in KPI_Obj:
        if kpi in df.columns:
            df[kpi] = df[kpi].astype('float32', errors='ignore')

    # Process based on selected type
    if processing_type == "Day PLMN":
        pivot1 = pd.pivot_table(df, index=['PLMN Name'], columns='Date', values=KPI_Obj, aggfunc='sum')

    elif processing_type == "Day Site":
        pivot1 = pd.pivot_table(df, index=['MRBTS name','LNBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')

    elif processing_type == "Day Cell":
        pivot1 = pd.pivot_table(df, index=['MRBTS name','LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')

    elif processing_type == "Hour Cell":
        df["Hour"] = df["Period start time"].dt.hour
        df = df[df["Hour"] == hour_input]
        pivot1 = pd.pivot_table(df, index=['MRBTS name','LNCEL name'], columns=['Date', 'Hour'], values=KPI_Obj, aggfunc='sum')

    else:
        st.error("Invalid processing type selected!")
        return None

    # Convert Pivot Table to DataFrame
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)

    return pivot1

# Check if file is uploaded
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Select Processing Type
    process_type = st.selectbox("Select Processing Type", ["Day PLMN", "Day Site", "Day Cell", "Hour Cell"])

    # Hour input if Hour Cell is selected
    hour_input = None
    if process_type == "Hour Cell":
        hour_input = st.number_input("Enter Hour (0-23)", min_value=0, max_value=23, step=1)

    if st.button("Process Data"):
        result = process_data(df, process_type, hour_input)

        if result is not None:
            st.write("### Processed Data")
            st.dataframe(result)

            # Download Processed Data
            csv = result.to_csv(index=False).encode('utf-8')
            st.download_button("Download Processed CSV", csv, "processed_data.csv", "text/csv")

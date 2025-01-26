import os
import pandas as pd
import streamlit as st

# App title
st.title("LTE KPI Processing Tool")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

# KPI Object List
KPI_Obj = ['Cell Avail excl BLU','RRC_CONN_UE_MAX (M8001C200)','Avg PDCP cell thp DL',
           'Avg IP thp DL QCI9','Total LTE data volume, DL + UL','Perc DL PRB Util',
           'Avg UE distance','Average CQI','Avg RRC conn UE','inter eNB E-UTRAN HO SR X2',
           'Intra eNB HO SR','E-RAB DR RAN','E-UTRAN E-RAB stp SR','Total E-UTRAN RRC conn stp SR'
]

# Function to Process Data
def process_data(df):
    df['Period start time'] = pd.to_datetime(df['Period start time'])
    df["Date"] = df["Period start time"].dt.date
    df[KPI_Obj] = df[KPI_Obj].astype('float32', errors='ignore')

    pivot1 = pd.pivot_table(df, index=['MRBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)

    return pivot1

# Check if a file was uploaded
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Choose processing type
    process_type = st.selectbox("Select Processing Type", ["Day PLMN", "Day Site", "Day SEG", "Hour Cell"])

    if st.button("Process Data"):
        if process_type == "Day PLMN":
            result = process_data(df)
            st.write("### Processed Data")
            st.dataframe(result)  # Display in Streamlit

            # Provide a download link
            csv = result.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "processed_data.csv", "text/csv")

        elif process_type == "Day Site":
            st.write("Day Site processing coming soon...")  # Placeholder

        elif process_type == "Day SEG":
            st.write("Day SEG processing coming soon...")  # Placeholder

        elif process_type == "Hour Cell":
            hour_input = st.number_input("Enter Hour (0-23)", min_value=0, max_value=23, step=1)
            df["Hour"] = df["Period start time"].dt.hour
            df = df[df["Hour"] == hour_input]
            result = process_data(df)

            st.write("### Processed Hourly Data")
            st.dataframe(result)

            # Download processed hourly data
            csv = result.to_csv(index=False).encode('utf-8')
            st.download_button("Download Hourly CSV", csv, "hourly_data.csv", "text/csv")

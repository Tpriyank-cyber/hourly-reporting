import os
import pandas as pd
import tkinter
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory


currentDirectory = os.getcwd()
print('***Developed By Priyank Tomar***\n')
print("Current Working Directory", os.getcwd())


root = tkinter.Tk()
filename = askopenfilename(parent=root, initialdir='C:\\', title="Please select file")
root.withdraw()
print(filename)


type = input("Input sheet is on (0) BBH, (1) Continue : ")


df = pd.read_excel(filename)
df['Period start time'] = df['Period start time'].astype(str)
len= len(df.iloc[2,0])
df_columns_list = df.columns


KPI_Obj = ['Cell Avail excl BLU','RRC_CONN_UE_MAX (M8001C200)','Avg PDCP cell thp DL',
           'Avg IP thp DL QCI9','Total LTE data volume, DL + UL','Perc DL PRB Util',
           'Avg UE distance','Average CQI','Avg RRC conn UE','inter eNB E-UTRAN HO SR X2',
           'Intra eNB HO SR','E-RAB DR RAN','E-UTRAN E-RAB stp SR','Total E-UTRAN RRC conn stp SR'

]


# Function for Day PLMN Level Processing
def DayPLMN():
    df1 = pd.read_excel(filename)
    print("Processing...")
    df1 = df.copy()
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
    pivot1 = pd.pivot_table(df1, index=['PLMN Name'], columns='Date', values=KPI_Obj, aggfunc='sum')
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)
    pivot1.to_csv('LTE_Day_PLMN_Level_KPIs_output.csv', index=False)
    print("__________Processing Done_____________")

# Function for Day Site Level Processing
def DaySite():
    df1 = pd.read_excel(filename)
    print("Processing...")
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
    pivot1 = pd.pivot_table(df1, index=['MRBTS name','LNBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_1': 'KPI NAME'}, inplace=True)
    pivot1.to_csv('LTE_Day_Site_Level_KPIs_output.csv', index=False)
    print("__________Processing Done_____________")

# Function for Day Cell Level Processing
def DaySEG():
    df1 = pd.read_excel(filename)
    print("Processing...")
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
    pivot1 = pd.pivot_table(df1, index=['MRBTS name','LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)
    pivot1.to_csv('LTE_Day_Cell_Level_KPIs_output.csv', index=False)
    print("__________Processing Done_____________")


# Function for Hour Cell Level Processing without asking for hour input
def HourCellWithoutInput():
    df1 = pd.read_excel(filename)
    print("Processing...")
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1["Hour"] = df1["Period start time"].dt.hour

    for kpi in KPI_Obj:
        if kpi in df1.columns:
            df1[kpi] = df1[kpi].astype('float32')   

    pivot1 = pd.pivot_table(df1, index=['MRBTS name','LNCEL name'], columns=['Date', 'Hour'] ,values=KPI_Obj, aggfunc='sum', dropna=False)    

    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)   
    pivot1['Pre'] = ''
    pivot1['Post'] = ''
    pivot1['Delta'] = ''
    pivot1['Remarks'] = ''

    pivot1.to_csv('LTE_Hourly_Cell_Level_KPIs_output.csv', index=False)
    print("__________Processing Done_____________")


# Function for Hour Cell Level Processing with hour input
def HourCell():
    Hourinput = int(input("Input Hour "))
    df1 = pd.read_excel(filename)
    print("Processing...")
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1["Hour"] = df1["Period start time"].dt.hour
    df1 = df1[(df1['Hour'] == Hourinput)]
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
    pivot1 = pd.pivot_table(df1, index=['MRBTS name','LNCEL name'], columns='Date', values=KPI_Obj, aggfunc='sum')
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)
    pivot1['Pre'] = ''
    pivot1['Post'] = ''
    pivot1['Delta'] = ''
    pivot1['Remarks'] = ''
    pivot1.to_csv('LTE_Hourly_Cell_Level_KPIs_output.csv', index=False)
    print("__________Processing Done_____________")
    
def HourBCF():
    Hourinput = int(input("Input Hour "))
    df1 = pd.read_excel(filename)
    print("Processing...")
    df1 = df1.drop([0], axis=0)
    df1['Start Time'] = pd.to_datetime(df1['Period start time'])
    df1["Date"] = df1["Period start time"].dt.date
    df1["Hour"] = df1["Period start time"].dt.hour
    df1 = df1[(df1['Hour'] == Hourinput)]
    df1[KPI_Obj] = df1[KPI_Obj].astype('float32')
    pivot1 = pd.pivot_table(df1, index=['MRBTS name','LNBTS name'], columns='Date', values=KPI_Obj, aggfunc='sum')
    pivot1 = pivot1.stack(level=0).reset_index(drop=False)
    pivot1.rename(columns={'level_2': 'KPI NAME'}, inplace=True)
    pivot1.to_csv('LTE_Hourly_Level_KPIs_output.csv', index=False)
    print("__________Processing Done_____________")

# Logic to choose based on sheet type and date uniqueness
df1 = pd.read_excel(filename)
df1['Start Time'] = pd.to_datetime(df1['Period start time'])
df1["Date"] = df1["Period start time"].dt.date
unique_dates = df1['Date'].nunique()

if type == "0" and "LNCEL name" in df_columns_list:
    DaySEG()
elif type == "1" and  "PLMN Name" in df_columns_list and "CS RRC SR" in df_columns_list:
    if len <=10 :
        DayPLMN()
elif type == "1" and "LNCEL name" in df_columns_list:
    if unique_dates == 1:
        print("Unique date found, processing without Hour input.")
        HourCellWithoutInput()
    else:
        HourCell()
else:
    print("Wrong input file provided")

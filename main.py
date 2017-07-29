import operator
import pandas as pd
import numpy as np
import getpass
import inputfuncs
import statistics
import printthings

#/users/trevorgrant/python/programs/eprimepar/trypandas/bl2_data/samplepvt.csv
#/users/trevorgrant/python/programs/eprimepar/trypandas/mTBI_Data/samplepvt.csv

user = getpass.getuser()

printthings.dash_split()
print("""This script will take a filepath as input and return an out_csv to a
directory of your chosing. To begin, please chose which type of computerized
assessment you would like to score.
1 - Go No Go
2 - PVT""")
printthings.dash_split()

ans = inputfuncs.get_proper_user_response("Go No Go or PVT?: ")
bl2_tbi = inputfuncs.get_proper_user_response("Bl2 or mTBI?: ")

if ans in inputfuncs.pvt_answers:

    list_of_cols = ["Subject", "Session", "TextDisplay1.RT", "WaitATwoSec.RT",
    "WaitBThreeSec.RT", "WaitCFourSec.RT", "WaitDFiveSec.RT", "WaitESixSec.RT",
    "WaitFSevenSec.RT", "WaitGEightSec.RT", "WaitHNineSec.RT"]

    list_of_final_cols = ["Subject", "Session", "TextDisplay1.RT", "Too Early",
    "Too Fast", "Lapses", "False Starts", "Rejected Trials", "Reaction Time", "Speed", "Id With Session"]

    if bl2_tbi in inputfuncs.bl2_answers:
        df = pd.read_csv("/users/" + user + "/python/programs/eprimepar/trypandas/bl2_data/samplepvt.csv")
    elif bl2_tbi in inputfuncts.mtbi_answers:
        df = pd.read_csv("/users/" + user + "/python/programs/eprimepar/trypandas/mTBI_Data/samplepvt.csv")

    #df = pd.read_csv(inputfuncs.is_valid_path("Please enter the filepath: "))

    df = df[list_of_cols]

    df["Too Early"] = np.where((df["WaitATwoSec.RT"] > 0) | (df["WaitBThreeSec.RT"] > 0) |
    (df["WaitCFourSec.RT"] > 0) | (df["WaitDFiveSec.RT"] > 0) | (df["WaitESixSec.RT"] > 0) |
    (df["WaitFSevenSec.RT"] > 0) | (df["WaitGEightSec.RT"] > 0) | (df["WaitHNineSec.RT"]) > 0, 1, 0)

    df["Lapses"] = np.where(df["TextDisplay1.RT"] >= 500, 1, 0)

    df["Too Fast"] = np.where(df["TextDisplay1.RT"] <= 100, 1, 0)

    df["False Starts"] = np.where((df["Too Early"] == 1) | (df["Too Fast"] ==  1), 1, 0)

    df["Rejected Trials"] = np.where((df["Too Fast"] ==  1) | (df["Lapses"] ==  1), 1, 0)

    df["Reaction Time"] = np.where((df["Rejected Trials"] == 1), None, df["TextDisplay1.RT"])

    df["Speed"] = (1 / df["Reaction Time"]) * 1000

    df["Id With Session"] = df["Subject"].map(str) + "_" + (df["Session"]).map(str)

    df = df[list_of_final_cols]

    ind_session = df["Id With Session"].unique()

    #create a data frame dictionary based on combo of session ID and participant ID.
    DataFrameDict = {elem : pd.DataFrame for elem in ind_session}

    df_export = pd.DataFrame()
    df_3 = pd.DataFrame()

    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df["Id With Session"] == key]

        df_2 = pd.DataFrame()

        df_2["Subject"] = DataFrameDict[key]["Subject"].unique()
        df_2["Session"] = DataFrameDict[key]["Session"].unique()
        df_2["Sum of Too Early"] = DataFrameDict[key]["Too Early"].sum()
        df_2["Sum of Lapses"] = DataFrameDict[key]["Lapses"].sum()
        df_2["Sum of Too Fast"] = DataFrameDict[key]["Too Fast"].sum()
        df_2["Sum of False Starts"] = DataFrameDict[key]["False Starts"].sum()
        df_2["Sum of Rejected Trials"] = DataFrameDict[key]["Rejected Trials"].sum()
        df_2["Average Reaction Time"] = DataFrameDict[key]["Reaction Time"].mean()
        df_2["Average Speed"] = DataFrameDict[key]["Speed"].mean()
        df_2["Standard Deviation"] = DataFrameDict[key]["Reaction Time"].std()

        df_3 = df_3.append(df_2)

    df_3.to_csv("Final.csv")
    print("K. Done.")

elif ans in inputfuncs.gng_answers:

    list_of_cols = ["Subject", "Session", "CorrectResponse", "CueType", "Image.ACC",
    "Image.RESP", "Image.RT", "MainCondition"]

    if bl2_tbi in inputfuncs.bl2_answers:
        df = pd.read_csv("/users/" + user + "/python/programs/eprimepar/trypandas/bl2_data/samplegng.csv")
    elif bl2_tbi in inputfuncts.mtbi_answers:
        df = pd.read_csv("/users/" + user + "/python/programs/eprimepar/trypandas/mTBI_Data/samplegng.csv")

    df = df[list_of_cols]
    df["Total Go"] = np.where(df["MainCondition"] == "Go", 1, None)
    df["Total No-Go"] = np.where(df["MainCondition"] == "No Go", 1, None)
    df["Go Accuracy"] = np.where((df["MainCondition"] == "Go") & (df["Image.ACC"] == 1), 1, None)
    df["No-Go Accuracy"] = np.where((df["MainCondition"] == "No Go") & (df["Image.ACC"] == 0), 1, None)
    df["Go Reaction Time"] = np.where(df["Go Accuracy"] == 1, df["Image.RT"], None)
    df["No-Go Reaction Time"] = np.where(df["No-Go Accuracy"] == 1, df["Image.RT"], None)

    df["Id With Session"] = df["Subject"].map(str) + "_" + (df["Session"]).map(str)

    ind_session = df["Id With Session"].unique()

    #create a data frame dictionary based on combo of session ID and participant ID.
    DataFrameDict = {elem : pd.DataFrame for elem in ind_session}

    df_export = pd.DataFrame()
    df_3 = pd.DataFrame()

    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df["Id With Session"] == key]

        def make_list(column, ret):

            list_1 = column.tolist()

            list_2 = []
            list_3 = []
            for row in list_1:
                if row == 1:
                    list_2.append(row)
                elif row == None:
                    list_3.append(1)

            if ret == 1:
                return(len(list_2))
            if ret == 0:
                return(len(list_3))

        df_2 = pd.DataFrame()

        go_correct = make_list(DataFrameDict[key]["Go Accuracy"], 1)
        go_total = len(DataFrameDict[key]["Go Accuracy"].tolist())
        nogo_correct = make_list(DataFrameDict[key]["No-Go Accuracy"], 1)

        df_2["Subject"] = DataFrameDict[key]["Subject"].unique()
        df_2["Session"] = DataFrameDict[key]["Session"].unique()
        df_2["Go Reaction Time"] = DataFrameDict[key]["Go Reaction Time"].mean()
        df_2["No-Go Reaction Time"] = DataFrameDict[key]["No-Go Reaction Time"].mean()

        df_3 = df_3.append(df_2)

    df_3.to_csv("Final.csv")
    print("K. Done.")

else:
    print("Not valid.")

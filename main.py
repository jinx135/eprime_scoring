import operator
import pandas as pd
import numpy as np
import getpass
import inputfuncs
import statistics
import printthings
import datetime
import os
from shutil import copy2, move

cwd = os.getcwd()

def update_files(date):

    if ans in inputfuncs.pvt_answers:
        if bl2_tbi in inputfuncs.bl2_answers:
            dir_to_update = f"{cwd}/bl2_data/"
            updated_file_name = f"{date}_mTBI_pvt.csv"
            for row in os.listdir(dir_to_update):
                row = row.lower()
                if "pvt" in row:
                    file_to_update = row
            print(f"File to replace: {file_to_update}")
        else:
            dir_to_update = f"{cwd}/mTBI_Data/"
            updated_file_name = f"{date}_mTBI_pvt.csv"
            for row in os.listdir(dir_to_update):
                row = row.lower()
                if "pvt" in row:
                    file_to_update = row
            print(f"File to replace: {file_to_update}")
    elif ans in inputfuncs.gng_answers:
        if bl2_tbi in inputfuncs.bl2_answers:
            dir_to_update = f"{cwd}/bl2_data/"
            updated_file_name = f"{date}_bl2_gng.csv"
            for row in os.listdir(dir_to_update):
                row = row.lower()
                if "gng" in row:
                    file_to_update = row
            print(f"File to replace: {file_to_update}")
        else:
            dir_to_update = f"{cwd}/mTBI_Data/"
            updated_file_name = f"{date}_mTBI_gng.csv"
            for row in os.listdir(dir_to_update):
                row = row.lower()
                if "gng" in row:
                    file_to_update = row
            print(f"File to replace: {file_to_update}")

    new_file = inputfuncs.is_valid_path("Please enter the filepath of the file you wish to update: ")
    new_file = copy2(new_file, f"{dir_to_update}/{updated_file_name}")

def show_files(date):

    printthings.dash_split()
    print("""Before we score these puppies - we should find out if all your files
are currently up to date: here are the TBI model e-prime files:""")
    printthings.dash_split()
    mtbi_dir = (os.listdir("{}/mTBI_Data/".format(cwd)))
    for row in mtbi_dir:
        print(row)
    printthings.dash_split()
    print("...And the files for Bright Light 2: ")
    printthings.dash_split()
    bl2_dir = (os.listdir("{}/bl2_Data".format(cwd)))
    for row in bl2_dir:
        print(row)
    printthings.dash_split()
    print("""If the dates on the files are not the most recent versions of these files,
type 'update' move the most recent version into the program directory. Press
enter to continue to main program.""")
    printthings.dash_split()
    update_files_yn = input("Update?: ").lower()
    if update_files_yn in inputfuncs.update_files_yn_ans:
        printthings.dash_split()
        update_files(date)
    else:
        printthings.dash_split()
        pass

user = getpass.getuser() #used in naming export file
date = datetime.date.today() #used in naming export file

printthings.dash_split()
print("""Version 0.0 of SCAN LAB E-Prime Scoring Script:
The author of this application wishes you well,
and hopes that you do not blow up your compter
while using this application.

Please just give the program the info it wants (things
will go poorly for you if you do not).

Any questions can be directed to: tjgran01@syr.edu.
Be sure to wait at least six(6) months for a reply.""")
printthings.dash_split()

print("""This script will take a filepath as input and return an out_csv to a
directory of your chosing. To begin, please chose which type of computerized
assessment you would like to score.
1 - Go No Go
2 - PVT
3 - Update Data Files""")
printthings.dash_split()

ans = inputfuncs.get_proper_user_response("Go No Go or PVT?: ") #user chooses PVT or GoNoGo
if ans in inputfuncs.update_answer:
    show_files(date)
    print("""please chose which type of computerized assessment you would like to score.
1 - Go No Go
2 - PVT""")
    ans = inputfuncs.get_proper_user_response("Go No Go or PVT?: ")
bl2_tbi = inputfuncs.get_proper_user_response("Bl2 or mTBI?: ") #user chooses Bl2 or mTBI

#PVT SCORING BELOW
if ans in inputfuncs.pvt_answers:

    #pandas DF will == these collumn names.
    list_of_cols = ["Subject", "Session", "TextDisplay1.RT", "WaitATwoSec.RT",
    "WaitBThreeSec.RT", "WaitCFourSec.RT", "WaitDFiveSec.RT", "WaitESixSec.RT",
    "WaitFSevenSec.RT", "WaitGEightSec.RT", "WaitHNineSec.RT"]

    #export == these collumn names.
    list_of_final_cols = ["Subject", "Session", "TextDisplay1.RT", "Too Early",
    "Too Fast", "Lapses", "False Starts", "Rejected Trials", "Reaction Time", "Speed", "Id With Session"]

    if bl2_tbi in inputfuncs.bl2_answers:
        for row in os.listdir(f"{cwd}/bl2_data/"):
            row = row.lower()
            if "pvt" in row:
                file_to_update = row
        df = pd.read_csv(f"{cwd}/bl2_Data/{file_to_update}")
    elif bl2_tbi in inputfuncs.mtbi_answers:
        for row in os.listdir(f"{cwd}/mTBI_data/"):
            row = row.lower()
            if "pvt" in row:
                file_to_update = row
        df = pd.read_csv(f"{cwd}/mTBI_Data/{file_to_update}")
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

    if bl2_tbi in inputfuncs.bl2_answers:
        if not os.path.exists("/users/{}/Desktop/Exports{}/".format(user, date)):
            os.mkdir("/users/{}/Desktop/Exports{}/".format(user, date))
        df_3.to_csv("/users/{}/Desktop/Exports{}/bl2PVT.csv".format(user, date))
    elif bl2_tbi in inputfuncs.mtbi_answers:
        if not os.path.exists("/users/{}/Desktop/Exports{}/".format(user, date)):
            os.mkdir("/users/{}/Desktop/Exports{}/".format(user, date))
        df_3.to_csv("/users/{}/Desktop/Exports{}/mTBIPVT.csv".format(user, date))
    print("K. Done.")

#GO-NOGO SCORING BELOW:
elif ans in inputfuncs.gng_answers:

    list_of_cols = ["Subject", "Session", "CorrectResponse", "CueType", "Image.ACC",
    "Image.RESP", "Image.RT", "MainCondition"]

    if bl2_tbi in inputfuncs.bl2_answers:
        for row in os.listdir(f"{cwd}/bl2_data/"):
            row = row.lower()
            if "gng" in row:
                file_to_update = row
        df = pd.read_csv(f"{cwd}/bl2_data/{file_to_update}")
    elif bl2_tbi in inputfuncs.mtbi_answers:
        for row in os.listdir(f"{cwd}/mTBI_Data/"):
            row = row.lower()
            if "gng" in row:
                file_to_update = row
        df = pd.read_csv(f"{cwd}/mTBI_Data/{file_to_update}")

    df = df[list_of_cols]
    df["Total Go"] = np.where(df["MainCondition"] == "Go", 1, None)
    df["Total No-Go"] = np.where(df["MainCondition"] == "No Go", 1, None)
    df["Go Accuracy"] = np.where((df["MainCondition"] == "Go") & (df["Image.ACC"] == 1), 1, None)
    df["No-Go Accuracy"] = np.where((df["MainCondition"] == "No Go") & (df["Image.ACC"] == 1), 1, None)
    df["No-Go Accuracy-RT"] = np.where((df["MainCondition"] == "No Go") & (df["Image.ACC"] == 0), 1, None)
    df["Go Reaction Time"] = np.where(df["Go Accuracy"] == 1, df["Image.RT"], None)
    df["No-Go Reaction Time"] = np.where((df["No-Go Accuracy-RT"] == 1), df["Image.RT"], None)
    df["Id With Session"] = df["Subject"].map(str) + "_" + (df["Session"]).map(str)

    ind_session = df["Id With Session"].unique()

    #create a data frame dictionary based on combo of session ID and participant ID.
    DataFrameDict = {elem : pd.DataFrame for elem in ind_session}

    df_export = pd.DataFrame()
    df_3 = pd.DataFrame()

    for key in DataFrameDict.keys():
        DataFrameDict[key] = df[:][df["Id With Session"] == key]

        total_trials = len(DataFrameDict[key])

        df_2 = pd.DataFrame()

        df_2["Subject"] = DataFrameDict[key]["Subject"].unique()
        df_2["Session"] = DataFrameDict[key]["Session"].unique()
        df_2["Go Reaction Time"] = DataFrameDict[key]["Go Reaction Time"].mean()
        df_2["Go Accuracy"] = DataFrameDict[key]["Go Accuracy"].count() / DataFrameDict[key]["Total Go"].count()
        df_2["No-Go Reaction Time"] = DataFrameDict[key]["No-Go Reaction Time"].mean()
        df_2["No-Go Accuracy"] = DataFrameDict[key]["No-Go Accuracy"].count() / DataFrameDict[key]["Total No-Go"].count()
        df_3 = df_3.append(df_2)

    if bl2_tbi in inputfuncs.bl2_answers:
        if not os.path.exists("/users/{}/Desktop/Exports{}/".format(user, date)):
            os.mkdir("/users/{}/Desktop/Exports{}/".format(user, date))
        df_3.to_csv("/users/{}/Desktop/Exports{}/bl2gonogo.csv".format(user, date))
    elif bl2_tbi in inputfuncs.mtbi_answers:
        if not os.path.exists("/users/{}/Desktop/Exports{}/".format(user, date)):
            os.mkdir("/users/{}/Desktop/Exports{}/".format(user, date))
        df_3.to_csv("/users/{}/Desktop/Exports{}/mTBIgonogo.csv".format(user, date))
    print("K. Done.")

else:
    print("Not valid.")

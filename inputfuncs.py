import os
import printthings

yes_answers = ["yes", "y", "ye", "ys", "1"]
no_answers = ["no", "on", "n", "2"]
gng_answers = ["1", "go", "gng", "go no go", "gonogo"]
pvt_answers = ["2", "pvt", "pv", "pt"]
bl2_answers = ["1", "bl2", "l2", "b2", "blue light 2"]
mtbi_answers = ["2", "mtbi", "tbimodel", "tbi model", "tbi"]
update_files_yn_ans = ["update"]

def make_file_path(path):

    if not os.path.exists(path):
        try:
            os.mkdir(path)
            return(path)
        except PermissionError:
            print("Hm...that Doesn't look like a path...are you sure your syntax is valid?")
            print("Quitting application ... ... ...")
            printthings.dash_split()
            printthings.plus_split()
            sys.exit(0)

def is_valid_path(prompt):

    valid_path = False
    while valid_path == False:

        path = input(prompt)
        path = add_slash(path)

        if not os.path.exists(path):
            printthings.dash_split()
            if prompt == "Enter the directory you want to copy the files into: ":
                print("That is not a valid file path. Would you like to create: ")
                print(path + "?")
                printthings.dash_split()

                choice_made = False
                while choice_made == False:
                    ans = input("Create File Path? (y/n): ")
                    if ans in listsforpybash.yes_answers:
                        valid_path = True
                        choice_made = True
                        path = make_file_path(path)
                        printthings.dash_split()
                        return(path)
                    elif ans in listsforpybash.no_answers:
                        choice_made = True
                        printthings.dash_split()
                    else:
                        printthings.dash_split()
                        print("That is not a valid response")
                        printthings.dash_split()
            else:
                print("That is not a valid file path. Try entering it again.")
                printthings.dash_split()
        else:
            return(path)
            valid_path = True

def add_slash(string):

    is_file = check_if_file(string)

    if is_file == True:

        if string[0] != "/":
            string = "/" + string

        return(string)

    elif is_file == False:

        if string[-1:] != "/":
            string = string + "/"

        if string[0] != "/":
            string = "/" + string

        return(string)

def check_if_file(string):

    if string[-4] == ".":
        return(True)
    else:
        return(False)

def get_proper_user_response(prompt):

    def valid_yes_no(response):

        if response in yes_answers:
            return(True)
        elif response in no_answers:
            return(True)
        else:
            printthings.dash_split()
            print("That is not a valid answer")
            printthings.dash_split()
            return(False)

    def valid_gng_or_pvt(response):

        if response in gng_answers:
            return(True)
            response = "gonogo"
        elif response in pvt_answers:
            return(True)
            response = "pvt"
        else:
            return(False)

    def valid_bl2(response):

        if response in bl2_answers:
            return(True)
            response = "bl2"
        elif response in mtbi_answers:
            return(True)
            response = "tbi"
        else:
            return(False)

    good_response = False
    while good_response == False:

        response = (input(prompt))
        response = response.lower()

        if "(y/n)" in prompt:
            good_response = valid_yes_no(response)
        elif ("Go No Go") in prompt:
            good_response = valid_gng_or_pvt(response)
        elif ("Bl2 or") in prompt:
            good_response = valid_bl2(response)

        return(response)

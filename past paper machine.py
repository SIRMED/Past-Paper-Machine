import os
import requests
import concurrent.futures
from colorama import Fore, Back, Style
import time


def subject_code_to_name(SUBJECT_CODE):
    # Dictionary mapping subject codes to subject names
    subject_code_to_name_dict = {
        "0580": "Mathematics",
        "0610": "Biology",
        "0620": "Chemistry",
        "0625": "Physics",
        "0478": "Computer Science",
        "0452": "Accounting",
        "0450": "Business Studies",
        "0455": "Economics",
        "0520": "French",
        "0525": "German",
        "0510": "Urdu",
        "0493": "Islamiyat",
        "0500": "First Language English",
        "0606": "Additional Mathematics"
    }

    # Returning the subject name if it exists in the dictionary
    if SUBJECT_CODE in subject_code_to_name_dict:
        return subject_code_to_name_dict[SUBJECT_CODE]
    else:
        return SUBJECT_CODE

def paper_session_to_name(PAPER_SESSION):
    #extract the first letter 
    PAPER_SESSION = PAPER_SESSION[0]
    # Dictionary mapping paper sessions to paper session names
    paper_session_to_name_dict = {
        "w": "Winter",
        "s": "Summer",
        "m": "March"
    }

    # Returning the paper session name if it exists in the dictionary
    if PAPER_SESSION in paper_session_to_name_dict:
        return paper_session_to_name_dict[PAPER_SESSION]
    else:
        return PAPER_SESSION

def paper_year(PAPER_SESSION):
    #extract the second number from PAPER_SESSION, eg w19 is returned as 19
    PAPER_YEAR = PAPER_SESSION[1:]
    return PAPER_YEAR

def download_past_paper(SUBJECT_CODE, PAPER_SESSION, PAPER_TYPE, PAPER_NUMBER):
    url = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{SUBJECT_CODE}_{PAPER_SESSION}_{PAPER_TYPE}_{PAPER_NUMBER}.pdf#view=FitH"
    
    #extract the second number from PAPER_NUMBER, eg 4 from 34
    PAPER_VARIANT = PAPER_NUMBER[1]
    PAPER_NUMBER_FIRSTONE = PAPER_NUMBER[0]

    custom_filename = f"{SUBJECT_CODE} {paper_session_to_name(PAPER_SESSION)} 20{paper_year(PAPER_SESSION)} V{PAPER_VARIANT} {PAPER_TYPE}.pdf"
    
    # Creating directory if it doesn't exist
    download_path = f"./testing_area/{SUBJECT_CODE} {subject_code_to_name(SUBJECT_CODE)}/Paper {PAPER_NUMBER_FIRSTONE}"
    os.makedirs(download_path, exist_ok=True)

    # Download the file in chunks
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(download_path, custom_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
        print(f"\033[92m{subject_code_to_name(SUBJECT_CODE)}\033[0m, Paper \033[92m{PAPER_NUMBER_FIRSTONE}\033[0m downloaded: \033[92m{custom_filename}\033[0m")

def download_all_papers():
    # List of subject codes
    subject_codes = ["0580", "0625", "0620", "0610", "0478"]

    # List of paper sessions
    paper_sessions = ["w21", "s21", "m21", "w20", "s20", "m20", "w19", "s19", "m19"]

    # List of paper types
    paper_types = ["ms", "qp"]

    # Dictionary mapping subject codes to paper numbers
    subject_code_to_paper_numbers_dict = {
        "0580": ["21", "22", "23", "41", "42", "43"],
        "0625": ["21", "22", "23", "41", "42", "43"],
        "0620": ["21", "22", "23", "41", "42", "43"],
        "0610": ["21", "22", "23", "41", "42", "43"],
        "0478": ["12", "22"]
    }

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_paper = {executor.submit(download_past_paper, subject_code, paper_session, paper_type, paper_number): (subject_code, paper_session, paper_type, paper_number) 
                           for subject_code in subject_codes 
                           for paper_session in paper_sessions 
                           for paper_type in paper_types 
                           for paper_number in subject_code_to_paper_numbers_dict[subject_code] 
                           if (paper_session[0] == "m" and paper_number[1] == "2") or paper_session[0] != "m"}

        for future in concurrent.futures.as_completed(future_to_paper):
            paper = future_to_paper[future]
            try:
                future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (paper, exc))
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print()
    print(f"\033[92mDownload sequence completed in {elapsed_time}s\033[0m")
    print("\033[92mAll files downloaded successfully\033[0m")
    print("\033[92mThank you for using the Past Paper Machine!\033[0m")


def start_program():
    print('\033[96m* Past Paper Machine for CAIE IGCSE Past Papers *\033[0m')
    print()

    print("\033[92mThe following subjects are avialable to download past papers of:\033[0m")
    print("- 0580 Mathematics")
    print("- 0606 Additional Mathematics")
    print("- 0478 Computer Science")
    print("- 0610 Biology")
    print("- 0620 Chemistry")
    print("- 0625 Physics")
    print("- 0452 Accounting")
    print("- 0450 Business Studies")
    print("- 0455 Economics")
    print("- 0520 French")
    print("- 0525 German")
    print("- 0510 Urdu")
    print("- 0493 Islamiyat")
    print("- 0500 First Language English")
    print()

    print("\033[92mEnter the subject codes you wish to download past papers of, separated by commas (eg. 0580, 0625, 0620):\033[0m")
    subject_codes_STR = str(input())
    subject_codes = subject_codes_STR.split(", ")
    print()
    
    # check if the subject codes are valid  
    for subject_code in subject_codes:
        if subject_code not in ["0580", "0606", "0478", "0610", "0620", "0625", "0452", "0450", "0455", "0520", "0525", "0510", "0493", "0500"]:
            print(f"\033[91mInvalid subject code: {subject_code} - Program terminated\033[0m")
            return

    print("\033[92mYou have selected the following subjects, currently only Paper 2 & 4 will be downloaded for all papers and paper 1 & 2 for 0478 CS:\033[0m")
    for subject_code in subject_codes:
        print(subject_code, subject_code_to_name(subject_code))
    print()

    print("\033[92mDo you wish to start the program? (Y/N)\033[0m")
    user_input = input()
    if user_input.lower() == "y":
        download_all_papers()
    else:
        print("\033[91mProgram terminated\033[0m")

start_program()



# SAMPLE USAGE
# SUBJECT_CODE = "0580"
# PAPER_SESSION = "m21"
# PAPER_TYPE = "ms"
# PAPER_NUMBER = "22"
# download_past_paper(SUBJECT_CODE, PAPER_SESSION, PAPER_TYPE, PAPER_NUMBER)




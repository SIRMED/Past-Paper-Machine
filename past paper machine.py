import os
import requests
import time

def request_download_paper(paper):
    download_past_paper(paper["subject_code"], paper["session"], paper["paper_type"], paper["variant"])

def arr_of_strings_to_string(arr):
    return ', '.join(arr)

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
        "0539": "Urdu",
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{SUBJECT_CODE}_{PAPER_SESSION}_{PAPER_TYPE}_{PAPER_NUMBER}.pdf#view=FitH"
    
    #extract the second number from PAPER_NUMBER, eg 4 from 34
    PAPER_VARIANT = PAPER_NUMBER[1]
    PAPER_NUMBER_FIRSTONE = PAPER_NUMBER[0]

    custom_filename = f"{SUBJECT_CODE} - 20{paper_year(PAPER_SESSION)} {paper_session_to_name(PAPER_SESSION)} V{PAPER_VARIANT} {PAPER_TYPE}.pdf"
    
    # Creating directory if it doesn't exist
    download_path = f"./Past Papers/{SUBJECT_CODE} {subject_code_to_name(SUBJECT_CODE)}/Paper {PAPER_NUMBER_FIRSTONE}"
    os.makedirs(download_path, exist_ok=True)

    # Download the file in chunks
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(os.path.join(download_path, custom_filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
        print(f"\033[92m{subject_code_to_name(SUBJECT_CODE)}\033[0m, Paper \033[92m{PAPER_NUMBER_FIRSTONE}\033[0m downloaded: \033[92m{custom_filename}\033[0m")

def download_all_papers(subject_codes, syllabus_type, practical_type, paper_years):

    paper_types = ["ms", "qp"]

    avialable_papers_for_subjects = {
        "0610": ["1", "2", "3", "4", "5", "6"], # [1and3] or [2and4] and [5 or 6]
        "0620": ["1", "2", "3", "4", "5", "6"], # [1and3] or [2and4] and [5 or 6]
        "0625": ["1", "2", "3", "4", "5", "6"], # [1and3] or [2and4] and [5 or 6]
        "0580": ["1", "2", "3", "4"],           # [1and3] or [2and4]
        "0520": ["1", "2", "3", "4"],           # [1 and 2 and 3 and 4]
        "0525": ["1", "2", "3", "4"],           # [1 and 2 and 3 and 4]
        "0606": ["1", "2"],                     # [1 and 2]
        "0478": ["1", "2"],                     # [1 and 2]
        "0452": ["1", "2"],                     # [1 and 2]
        "0450": ["1", "2"],                     # [1 and 2]
        "0455": ["1", "2"],                     # [1 and 2]
        "0539": ["1", "2"],                     # [1 and 2]
        "0493": ["1", "2"],                     # [1 and 2]
        "0500": ["1", "2", "3", "4"]            # 1 and [2 or 3], 4 optional
    }

    core_syallbus_papers = {
        "0610": ["1", "3"],
        "0620": ["1", "3"],
        "0625": ["1", "3"],
        "0580": ["1", "3"],
        "0520": ["1", "2", "3", "4"],
        "0525": ["1", "2", "3", "4"],
        "0606": ["1", "2"],
        "0478": ["1", "2"],
        "0452": ["1", "2"],
        "0450": ["1", "2"],
        "0455": ["1", "2"],
        "0539": ["1", "2"],
        "0493": ["1", "2"],
        "0500": ["1", "2"]
    }

    extended_syallbus_papers = {
        "0610": ["2", "4"],
        "0620": ["2", "4"],
        "0625": ["2", "4"],
        "0580": ["2", "4"],
        "0520": ["1", "2", "3", "4"],
        "0525": ["1", "2", "3", "4"],
        "0606": ["1", "2"],
        "0478": ["1", "2"],
        "0452": ["1", "2"],
        "0450": ["1", "2"],
        "0455": ["1", "2"],
        "0539": ["1", "2"],
        "0493": ["1", "2"],
        "0500": ["1", "3"]
    }

    atp_papers = {
        "0610": ["6"],
        "0620": ["6"],
        "0625": ["6"],
        "0580": [],
        "0520": [],
        "0525": [],
        "0606": [],
        "0478": [],
        "0452": [],
        "0450": [],
        "0455": [],
        "0539": [],
        "0493": [],
        "0500": []
    }

    practical_papers = {
        "0610": ["5"],
        "0620": ["5"],
        "0625": ["5"],
        "0580": [],
        "0520": [],
        "0525": [],
        "0606": [],
        "0478": [],
        "0452": [],
        "0450": [],
        "0455": [],
        "0539": [],
        "0493": [],
        "0500": []
    }

    syllabus_papers = {
        "core": core_syallbus_papers,
        "extended": extended_syallbus_papers
    }

    practical_papers = {
        "atp": atp_papers,
        "practical": practical_papers
    }

    papers_to_download = []

    start_time = time.time()

    # Loop over the subject codes
    for subject_code in subject_codes:

        # Downloads papers for core or extended syllabus
        papers = syllabus_papers[syllabus_type].get(subject_code, [])
        print(f"For \033[92m{subject_code} {subject_code_to_name(subject_code)}\033[0m: \033[92mPaper {arr_of_strings_to_string(papers)}\033[0m will be downloaded (\033[92m{syllabus_type}\033[0m syllabus)")

        # Add the variants for each paper
        for paper in papers:
            for year in paper_years:
                # If the paper session is in March, only use variant "2"
                variants = [] 
                if year.startswith("m"):
                    variants = ["2"] 
                else:
                    variants = ["1", "2", "3"]
                for variant in variants:
                    for paper_type in paper_types:
                        papers_to_download.append({
                            "subject_code": subject_code,
                            "session": year,
                            "variant": f"{paper}{variant}",
                            "paper_type": paper_type
                        })
        
        # Downloads papers for practical or alternative to practical
        papers = practical_papers[practical_type].get(subject_code, [])
        print(f"For \033[92m{subject_code} {subject_code_to_name(subject_code)}\033[0m: \033[92mPaper {arr_of_strings_to_string(papers)}\033[0m will be downloaded (\033[92m{practical_type}\033[0m syllabus)")

        # Add the variants for each paper
        for paper in papers:
            for year in paper_years:
                # If the paper session is in March, only use variant "2"
                variants = [] 
                if year.startswith("m"):
                    variants = ["2"] 
                else:
                    variants = ["1", "2", "3"]
                for variant in variants:
                    for paper_type in paper_types:
                        papers_to_download.append({
                            "subject_code": subject_code,
                            "session": year,
                            "variant": f"{paper}{variant}",
                            "paper_type": paper_type
                        })

    print(f"Downloading {len(papers_to_download)} papers...")

    for paper in papers_to_download:
        request_download_paper(paper)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    directory_path = os.path.dirname(os.path.realpath(__file__))
    print()
    print(f"Download sequence completed in \033[92m{elapsed_time}s\033[0m")
    print(f"\033[92mAll {len(papers_to_download)} files\033[0m downloaded successfully in \033[4;92m{directory_path}\Past Papers\033[0m")
    print("Thank you for using the Past Paper Machine!")
    print("\033[92mMade with 💖 by Sirmed Mehmood; from Pakistan, for the world 🌍\033[0m")


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
    print("- 0539 Urdu")
    print("- 0493 Islamiyat")
    print("- 0500 First Language English")
    print()

    print("\033[92mEnter the subject codes you wish to download past papers of, separated by commas:\033[0m")
    subject_codes_STR = str(input())
    subject_codes_without_spaces = subject_codes_STR.replace(" ", "")
    subject_codes = subject_codes_without_spaces.split(",")
    print()
    
    # check if the subject codes are valid  
    for subject_code in subject_codes:
        if subject_code not in ["0580", "0606", "0478", "0610", "0620", "0625", "0452", "0450", "0455", "0520", "0525", "0539", "0493", "0500"]:
            print(f"\033[91mInvalid subject code: {subject_code} - Program terminated\033[0m")
            return

    print("\033[92mYou have selected the following subjects:\033[0m")
    for subject_code in subject_codes:
        print("-",subject_code, subject_code_to_name(subject_code))
    print()

    # Ask syllabus type for downloading P1,2,3,4,5 or 6
    print("Are you studying the \033[92mcore syllabus\033[0m or the \033[92msupplement/extended syllabus\033[0m?")
    print("If a subject has no concept of core or extended syllabus, all avialable papers will be downloaded regardless of the syllabus you select.")
    print("For the subject 0500, the core syllabus includes papers 1 and 2, while the extended syllabus includes papers 1 and 3.")
    syllabus_type = str(input("Please enter \033[92mcore\033[0m or \033[92mextended\033[0m: "))
    if syllabus_type != "":
        if syllabus_type.lower() == "core" or syllabus_type.lower() == "core syllabus":
            syllabus_type = "core"
        elif syllabus_type.lower() == "extended" or syllabus_type.lower() == "extended syllabus" or syllabus_type.lower() == "supplement" or syllabus_type.lower() == "supplement syllabus":
            syllabus_type = "extended"
        else:
            print(f'\033[91mUnrecognized syllabus type "{syllabus_type}" detected - Program Terminated\033[0m')
            return
    else:
        print(f'\033[91mNo input provided - Program Terminated\033[0m')
        return
    print()


    print("If any subjects with practicals are selected, have you opted for a \033[92mpractical test\033[0m or an \033[92malternative to practical (ATP)\033[0m?")
    print("If a subject has no practical/ATP papers, none will be downloaded (exluding the core/extended papers).")
    practical_tpye = str(input("Please enter \033[92mpractical\033[0m or \033[92matp\033[0m: "))
    if practical_tpye != "":
        if practical_tpye.lower() == "atp" or practical_tpye.lower() == "alternative to practical" or practical_tpye.lower() == "alternative" or practical_tpye.lower() == "paper 6" or practical_tpye.lower() == "6":
            practical_tpye = "atp"
        elif practical_tpye.lower() == "practical" or practical_tpye.lower() == "practical exam" or practical_tpye.lower() == "paper 5" or practical_tpye.lower() == "5":
            practical_tpye = "practical"
        else:
            print(f'\033[91mUnrecognized practical type "{practical_tpye}" detected - Program Terminated\033[0m')
            return
    else:
        print(f'\033[91mNo input provided - Program Terminated\033[0m')
        return
    print()

    print("\033[92mHow many years of past papers do you need to download? (max. 6Y)\033[0m")
    print("Papers will be downloaded from the last year following the number of previous years you enter.")
    year_range = int(input("Enter a number from \033[92m1\033[0m to \033[92m6\033[0m: "))
    paper_years = []
    if year_range != "":
        if year_range > 6:
            print(f'\033[91mYear range exceeds 6 years - Program Terminated\033[0m')
        else:
            current_year = 23
            paper_sessions = ["w", "m", "s"]
            paper_years_without_letters = [str(current_year - i) for i in range(year_range)]
            for year in paper_years_without_letters:
                paper_years.append(f"s{year}")
                paper_years.append(f"w{year}")
                paper_years.append(f"m{year}")
    else:
        print(f'\033[91mNo input provided - Program Terminated\033[0m')
        return
    print()



    print("\033[92mDo you wish to start the program? (Y/N)\033[0m")
    user_input = str(input("Enter \033[92mY\033[0m or \033[92mN\033[0m: "))
    print()
    if user_input.lower() == "y":
        download_all_papers(subject_codes, syllabus_type, practical_tpye, paper_years)
    else:
        print("\033[91mProgram terminated\033[0m")

start_program()



# SAMPLE USAGE
# SUBJECT_CODE = "0580"
# PAPER_SESSION = "m21"
# PAPER_TYPE = "ms"
# PAPER_NUMBER = "22"
# download_past_paper(SUBJECT_CODE, PAPER_SESSION, PAPER_TYPE, PAPER_NUMBER)
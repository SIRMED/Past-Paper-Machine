import os
import glob
import msvcrt

all_past_papers = []
all_subjects = []
avaiailable_papers_for_subjects = []
parent_files_dir = os.path.dirname(os.path.realpath(__file__))
csv_file_of_solved_papers = f"{parent_files_dir}\\Past Papers\\opened_papers.csv"

def open_pdf(file_path):
    # Opens the pdf file in the default pdf reader/browser
    os.startfile(file_path)

def search_all_past_papers():
    # Finds the name (subjects) of all the folders in dir './Past Papers'
    subfolders = [f.path for f in os.scandir('./Past Papers') if f.is_dir()]

    # Add the name of all subfolders (subjects) to the top-level array
    for subfolder in subfolders:
        all_subjects.append(subfolder)

    # Adds an object to the aivailable_papers_for_subjects array stating which papers (sub-subfolders) are available for each subject (subfolder)
    for subfolder in subfolders:
        papers_available_temp = [f.path for f in os.scandir(subfolder) if f.is_dir()]
        papers_available = []
        
        for paper_type in papers_available_temp:
            papers_available.append(paper_type[-7:])
        
        avaiailable_papers_for_subjects.append({
            "subject": subfolder[14:],
            "papers_available": papers_available
        })

def open_unsolved_past_paper(subject, paper_number):
    paper_dir = f"{parent_files_dir}\\{subject[2:]}\\{paper_number}"
    all_papers_in_subdir_of_paper_dir = glob.glob(os.path.join(paper_dir, '**', '*.pdf'), recursive=True)
    all_question_papers = []
    csv_data = []
    papers_solved = []

    # Read the csv file and store the data in an array 'csv_data'
    with open(csv_file_of_solved_papers, 'r') as file:
        csv_data = file.readlines()

    # Store the names of all the papers in the subdirectory of the paper directory
    for line in csv_data:
        papers_solved.append(line.strip())
    
    # filter out the question papers from all the papers in the subdirectory of the paper directory
    for paper in all_papers_in_subdir_of_paper_dir:
        if "qp.pdf" in paper:
            all_question_papers.append(paper)
    
    # Open the first unsolved paper 
    for paper in all_question_papers:
        doc_name = paper.split("\\")[-1]

        if doc_name not in papers_solved:
            print()
            print(f"Opening \033[93m{paper_number}\033[0m of \033[93m{subject[14:]}\033[0m")
            print(f"Document: \033[93m{doc_name}\033[0m and \033[93m{doc_name.replace('qp.pdf', 'ms.pdf')}\033[0m")
            marking_scheme = paper.replace("qp.pdf", "ms.pdf")
            open_pdf(marking_scheme)
            open_pdf(paper)
            with open(csv_file_of_solved_papers, 'a') as file:
                file.write(f"{paper_number}/{doc_name}\n")
            break
    
    return

def start_program():
    print('\033[96m* Solved past papers recorder *\033[0m')
    print()

    # Ask user for the subject they want to print
    print('\033[93mWhich subjects past paper do you want to print?: \033[0m')
    subject_to_print = str(input('Enter the subject code/name: \033[93m'))
    subject_exists = bool(False)
    subject_matches_more_than_one = bool(False)

    # Check if the entered subject exists
    for sub_dir_name in all_subjects:
        if subject_to_print.lower() in sub_dir_name.lower():
            if subject_exists:
                subject_matches_more_than_one = bool(True)
            subject_exists = sub_dir_name

    if subject_exists:
        if subject_matches_more_than_one:
            print("\033[0mMultiple subjects found. Please enter a more specific subject code/name.")
            return
        else:
            print(f"\033[0mMatch found: \033[93m{subject_exists[14:]}\033[0m")
    else:
        print("\033[0mSubject does not exist")
        return
    print()

    # Ask user for the paper they want to print
    print(f'\033[93mWhich paper of {subject_exists[14:]} do you want to print?: \033[0m')
    paper_number_to_print = str(input('Enter the paper number (1-6): \033[93m'))
    paper_number_exists = bool(False)
    paper_numer_matches_more_than_one = bool(False)
    target_subject_object = next((obj for obj in avaiailable_papers_for_subjects if obj["subject"] == subject_exists[14:]), None)
    
    # Check if the entered paper exists
    for paper in target_subject_object["papers_available"]:
        if paper_number_to_print in paper:
            if paper_number_exists:
                paper_numer_matches_more_than_one = bool(True)
            paper_number_to_print = paper
            paper_number_exists = bool(True)

    if paper_number_exists:
        if paper_numer_matches_more_than_one:
            print("\033[0mMultiple papers found. Please enter a more specific paper number.")
            return
        else:
            print(f"\033[0mMatch found: \033[93m{paper_number_to_print}\033[0m")
    else:
        print("\033[0mPaper does not exist")
        return
    print()

    # Ask user if they want to open a past paper which they haven't solved
    print("Press any key to open a past paper which you haven't solved")
    print("or Esc to exit the program")
    while True:
        key = msvcrt.getch()
        if key == b'\x1b':  # ESC key
            print()
            print("\033[91mExiting program.\033[0m")
            break
        else:
            open_unsolved_past_paper(subject_exists, paper_number_to_print)
            break
        
search_all_past_papers()
start_program()
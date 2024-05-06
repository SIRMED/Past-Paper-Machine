# Past Paper Machine
This python script allows you to download Paper 2 & 4 for the subjects Mathematics, Biology, Chemistry, Physics, Accounting, Business Studies, Economics, French, German, Urdu, Islamiyat, First Language English, Additional Mathematics and Paper 1 & 2 for Computer Science. Currently
working to add possibility to select more options of papers

# Setup
Clone this repository into you local folder. Make sure it is empty and has only the python file. 

1) Make sure Python is installed and the required librarires:
   - reuests
   - colorama
   
   You can install them by running `pip install -r requirements.txt` in the command line
2) Open your terminal in the folder where the python files is located and type in `python "past paper machine.py"` which will start the script
3) Select which subjects you want to download past papers of by writing their subject codes and seperating them each with a comma then hit enter
4) It will ask you a final conformation to start the download process in which you have to type `Y` then press enter
5) They will start downloading and you will see which ones are downloading right now and any errors if they occur

# The program is not working/ working too slowly
The speed depends on your network speed and WiFi connection. The program installs the files using parallel processing. 5 requests will be made to the server for the files and be downloaded at 5 second intervals. This might cause some issues and if it does you can replace this block of code
```
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
```
with this code block
```
for subject_code in subject_codes:
        for paper_session in paper_sessions:
            for paper_type in paper_types:
                for paper_number in subject_code_to_paper_numbers_dict[subject_code]:
                    paper_session_month = paper_session[0]
                    if paper_session_month == "m" and paper_number[1] == "2":
                        download_past_paper(subject_code, paper_session, paper_type, paper_number)
                    elif paper_session_month != "m":
                        download_past_paper(subject_code, paper_session, paper_type, paper_number)
```
This will download the files one by one by waiting for the previous file to download then sending the next request for the download

# Services used
Past Papers are retrived from the website [PapaCambridge](https://papacambridge.com/). Big thanks to them for providing this service for free for all students worldwide. I made this tool to keep local copies of Past Papers so I can solce them locally using a stylus and save them which is not possible online

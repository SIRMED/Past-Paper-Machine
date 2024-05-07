# Past Paper Machine
This python script allows you to download any paper for the subjects Mathematics, Biology, Chemistry, Physics, Accounting, Business Studies, Economics, French, German, Urdu, Islamiyat, First Language English, Additional Mathematics and Computer Science.

# Setup
Clone this repository into you local folder. Make sure it is empty and has only the python file. 

1) Make sure Python is installed and the required librarires:
   - reuests
   
   You can install them by running `pip install -r requirements.txt` in the command line
2) Open your terminal in the folder where the python files is located and type in `python3 "past paper machine.py"` which will start the script
3) Select which subjects you want to download past papers of by writing their subject codes and seperating them each with a comma then hit enter
4) It will ask you a final conformation to start the download process in which you have to type `Y` then press enter
5) They will start downloading and you will see which ones are downloading right now and any errors if they occur

# The program is not working/ working too slowly
The speed depends on your network speed and WiFi connection. The program installs the files using parallel processing. 5 requests will be made to the server for the files and be downloaded at 5 second intervals. This might cause some issues and if it does you can change this block of code to your needs:
```
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(request_download_paper, papers_to_download) 
```
This will download the files one by one by waiting for the previous file to download then sending the next request for the download

# Services used
Past Papers are retrived from the website [PapaCambridge](https://papacambridge.com/). Big thanks to them for providing this service for free for all students worldwide. I made this tool to keep local copies of Past Papers so I can solce them locally using a stylus and save them which is not possible online

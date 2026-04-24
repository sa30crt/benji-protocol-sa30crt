

## Policy Summary

GenAI tools (ChatGPT) were used during development of the toolkit to support debugging, explain concepts, and help structure code.

AI was not used to generate complete solutions without understanding. All outputs were:

* reviewed critically
* tested manually
* modified to fit the assessment brief and field test requirements

All final submitted code has been understood and can be explained if needed.



## How AI Was Used

AI supported me with:

* Understanding Python concepts such as regex, sockets, threading, and HTTP parsing
* Fixing coding issues like indentation errors, missing logic, and runtime problems
* Suggesting approaches for libraries such as ftplib, paramiko, and BeautifulSoup

AI was not used for:

* Directly completing the Vulnerability Hunt task
* Producing exploit payloads without understanding how they work



## Entries

| Week   | Task   | Prompt Used                                                          | AI Output Summary                                     | My Verification / Changes Made                                                     |
| ------ | ------ | -------------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Week 1 | Task 1 | How to extract IP, timestamp, and username from auth.log using regex | Provided regex examples using Python’s re module      | Tested on sample logs and adjusted patterns to correctly capture usernames and IPs |
| Week 1 | Task 1 | How to write CSV output using csv.DictWriter                         | Gave sample structure for writing dictionaries to CSV | Implemented CSV output and fixed headers to match requirements                     |
| Week 1 | Task 1 | Why is my script failing pytest tests                                | Suggested checking file handling and output logic     | Found missing CSV generation and corrected output behaviour                        |
| Week 2 | Task 2 | How to build a TCP port scanner using sockets                        | Provided basic structure using socket.connect_ex()    | Built scanner and validated using tools like netcat and nmap                       |
| Week 2 | Task 2 | How to use ThreadPoolExecutor for scanning ports                     | Showed example of concurrent execution                | Added threading and confirmed improved performance                                 |
| Week 2 | Task 2 | How to grab service banners using sockets                            | Suggested recv() with timeout handling                | Implemented banner grabbing and handled encoding and timeouts                      |
| Week 2 | Task 2 | Why scanner shows no open ports                                      | Suggested checking network configuration              | Identified issue was VM networking rather than code                                |
| Week 3 | Task 3 | FTP authentication using ftplib                                      | Provided login and connection example                 | Tested against Metasploitable and fixed missing main execution block               |
| Week 3 | Task 3 | Debug brute.py not producing output                                  | Suggested checking program flow                       | Added missing `if __name__ == "__main__"` block                                    |
| Week 3 | Task 3 | How to log credential attempts                                       | Suggested logging within loop                         | Implemented logging and verified correct sequence                                  |
| Week 3 | Task 3 | SSH authentication using paramiko                                    | Provided SSHClient example                            | Implemented SSH login and handled failures correctly                               |
| Week 4 | Task 4 | Extract HTML comments using BeautifulSoup                            | Suggested using Comment objects                       | Parsed HTML successfully and validated results                                     |
| Week 4 | Task 4 | Fix requests install issue in Kali                                   | Suggested using virtual environment                   | Created venv, installed dependencies, updated requirements                         |

---

## Example of AI Output That Needed Fixing

The first FTP example from AI did not properly manage errors or cleanup.

### Problem:

* connections were not always closed properly
* error handling was incomplete
* script could crash if something failed

### Fix:

* added proper `try/except/finally` handling
* ensured `ftp.close()` always runs safely
* changed failure handling to return `False` instead of crashing

This aligned with the requirement:

 "Do NOT allow exceptions to propagate — return False on failure"



## Declaration

All code in this project has been:

* written or adapted by me
* tested using provided tests and manual checking
* fully understood and can be explained





# Google scholar Web Scraper - Research Assistant

A Python-based tool for gathering metadata and downloading full text pdfs through Google Scholar.

## Core Functions

- Automated Google Scholar scraping
- Metadata extraction (titles, authors, publication dates)
- PDF document retrieval
- Structured data storage in SQLite
- Session logging with timestamps

### Dependencies
- Python 3.8+
- Playwright for web automation
- BeautifulSoup4 for HTML parsing
- SQLite3 for data persistence
- Requests for HTTP operations

#### Database Schema
- URLs table: search queries, timestamps, result links
- Metadata tracking: titles, authors, dates
- Session logs: execution details, errors
- Single-page result processing (atm sorry, pagination can be supported easily)
- Basic metadata extraction patterns
- Rate limiting constraints
- Simple error handling implementation

### Setup Process

1. Clone repository:

git clone https://github.com/joelguff/scraperresearch.git. 

###### Execute:
Make sure you install the dependencies first.
pip install -r requirements.txt

###### Run the script:
python main.py

####### Development roadmap

Due to limitations with time and resources, the current version of the Scholar Scraper Supreme is a basic implementation with limited functionality. Future development will focus on the following areas:

1.) Multi-page result handling
2.) Advanced metadata parsing
3.) Robust error management
4.) Citation network analysis
5.) Data export functionality

However the current version is a functional tool for gathering metadata and downloading pdfs from Google Scholar.

######## Purpose

The tool was developed to take the time out of gathering research articles and downloading them.

######### License
Creative Commons Attribution-NonCommercial 4.0 International with Permission Clause
Copyright (c) 2024 Joel Guff (joel.guff@griffithuni.edu.au)

The full license text can be found in the LICENSE.md file.
Ultimately it is open source and free to use for non-commercial purposes.

########## Help me, help you.
As of 07/01/2024, I am a student of the Bachelor degree in Cybersecurity. 
Currently, I don't have a income but I would love to spend more time on these projects however I cannot do this due to lack of financial resources.
If this has helped you in any way, please consider donating to my PayPal account: joelguff1@gmail.com.
Please also consider sharing this project with your friends and colleagues.
Thank you for your support!
Joel

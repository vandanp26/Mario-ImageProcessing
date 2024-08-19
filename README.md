# Sluggers MVP Image Processing Project
This project is designed to automate the process of tracking and tallying stats for characters in the game Mario Super Sluggers. The motivation is for a league that my friends and I participate in weekly over the summer, where we keep track of character stats to determine the season MVP.
# Main Features
**Automated Stat Tracking:** Automatically processes screenshots from the Mario Super Sluggers MVP Board to match each character to their name and extract all relevant stats.

**Data Integration:** Extracted stats are automatically updated in Google Sheets, eliminating the need for manual entry and calculation.
# How It Works 
**Screenshot Input:** The user provides screenshots of the MVP board from Mario Super Sluggers.

**Character & Stat Matching:** The system uses OpenCV and PyTesseract to identify characters and extract their corresponding stats.

**Data Output:** The extracted data is then automatically uploaded to Google Sheets, where it is used to keep track of player stats and determine the MVP for the season.

# Technologies Used
Python: Core language used for processing and automation.

OpenCV: Image processing to match characters to their names.

NumPy: Data manipulation and processing.

PyTesseract: Optical Character Recognition (OCR) for extracting numerical stats from screenshots.

Google Sheets API: Automates the updating of stats in Google Sheets.

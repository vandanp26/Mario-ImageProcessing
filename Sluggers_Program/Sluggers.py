import cv2
import numpy as np
import requests
import pytesseract
from pytesseract import Output
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def enhance_image(roi):
    # Convert to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    return gray

def read_six_numbers_below_character(image, x, y, w, h, y_shift=50):
    numbers = []
    step = 145  # Adjust this value based on the spacing between rows in your image

    y += y_shift  # Shift the y-coordinate down to align the boxes properly

    for i in range(6):
        roi_y = y + i * step
        roi = extract_roi(image, x, roi_y, w, 120)

        # Enhance ROI for better OCR
        processed_roi = enhance_image(roi)
        
        # OCR with single number/character recognition
        text = pytesseract.image_to_string(
            processed_roi, 
            config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789'
        )
        
        # Clean up the text to only extract digits
        text = ''.join(filter(str.isdigit, text))
        
        if text:
            numbers.append(text)
        else:
            numbers.append('0')  # If no text is found, assume 0 or some default
        
        # Draw rectangle around the ROI on the original image for visualization
        cv2.rectangle(image, (x, roi_y), (x + w, roi_y + 120), (0, 255, 0), 2)
    
    # Display the image with the highlighted ROIs
    cv2.imshow('ROIs for Numbers', image)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    return numbers

def load_image_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
        return image
    else:
        print(f"Failed to download image from {url}")
        return None
    
def load_templates_from_github(urls):
    templates = {}
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
            template_name = url.split('/')[-1].split('.')[0]
            templates[template_name] = image
        else:
            print(f"Failed to download image from {url}")
    return templates

def extract_roi(image, x, y, w, h):
    roi = image[y:y+h, x:x+w]
    return roi

def match_template(roi, templates):
    best_match = None
    best_score = -1
    for name, template in templates.items():
        result = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > best_score:
            best_score = max_val
            best_match = name
    return best_match

def update_google_sheet(sheet, match_name, numbers):
    cell = sheet.find(match_name)
    if cell:
        for i, number in enumerate(numbers):
            col = cell.col + 1 + i  # Find the appropriate column for each number
            current_value = sheet.cell(cell.row, col).value
            
            # Handle cases where the cell might be empty
            current_value = int(current_value) if current_value else 0
            
            # Sum the current value with the new number
            new_value = current_value + int(number)
            
            # Update the cell with the new value
            sheet.update_cell(cell.row, col, new_value)

# scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
#          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Sluggers").sheet1

# Define URLs for the images in the GitHub repository
github_image_urls = [
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/baby_peach.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/blue_yoshi.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/boo.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/parakoopa.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/pink_pianta.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/waluigi.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/wario.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/yellow_pianta.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/yellow_toad.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/baby_dk.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/blue_toad.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/dark_drybones.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/donkey_kong.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/green_yoshi.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/mario.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/red_magikoopa.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/wiggler.jpg",
  "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/yellow_magikoopa.jpg",
]

# Load templates from GitHub
templates = load_templates_from_github(github_image_urls)

# Load the image
image_url = "https://raw.githubusercontent.com/vandanp26/Mario-ImageProcessing/main/Sluggers_Program/sluggers_elgato.png"
image = load_image_from_github(image_url)

# Define the coordinates for cropping (example coordinates)
x, y, w, h = 900, 425, 135, 140  # Adjust these coordinates as needed

# Loop to update x value and find best match
for i in range(9):
    roi = extract_roi(image, x, y, w, h)
    best_match = match_template(roi, templates)

    if best_match:
        print(f'The best match for x={x} is: {best_match}')

        # Skip updating the sheet if the match is "bones"
        if best_match.lower() == "bones":
            print("Match is 'bones'; skipping Google Sheet update.")
        else:
            # Shift the starting y-coordinate down by 60 pixels (adjust as needed)
            numbers = read_six_numbers_below_character(image, x, y, w, h, y_shift=200)
            
            if numbers:
                print(f'Read numbers: {numbers}')
                update_google_sheet(sheet, best_match, numbers)
            else:
                print('No numbers found in the column.')

    x += 170

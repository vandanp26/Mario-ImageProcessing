import cv2
import numpy as np
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

def update_google_sheet(sheet, match_name, x_value, y_value, w_value, h_value):
    cell = sheet.find(match_name)
    if cell:
        current_x = sheet.cell(cell.row, cell.col + 1).value
        current_y = sheet.cell(cell.row, cell.col + 2).value
        current_w = sheet.cell(cell.row, cell.col + 3).value
        current_h = sheet.cell(cell.row, cell.col + 4).value
        
        # Handle cases where the cell might be empty
        current_x = int(current_x) if current_x else 0
        current_y = int(current_y) if current_y else 0
        current_w = int(current_w) if current_w else 0
        current_h = int(current_h) if current_h else 0

        new_x = current_x + x_value
        new_y = current_y + y_value
        new_w = current_w + w_value
        new_h = current_h + h_value

        sheet.update_cell(cell.row, cell.col + 1, new_x)
        sheet.update_cell(cell.row, cell.col + 2, new_y)
        sheet.update_cell(cell.row, cell.col + 3, new_w)
        sheet.update_cell(cell.row, cell.col + 4, new_h)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Sluggers").sheet1

# Define URLs for the images in the GitHub repository
github_image_urls = [
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/blue_toad.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/mario.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/yoshi.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/dark_drybones.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/wiggler.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/yellow_magikoopa.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/red_magikoopa.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/donkeykong.jpg",
    "https://raw.githubusercontent.com/jacksonmacdonald21/Sluggers-MVP-Image-Processor/main/characters/baby_dk.jpg"






]

# Load templates from GitHub
templates = load_templates_from_github(github_image_urls)

# Load the image
image_path = '/Users/vandan/Sluggers_Proj/sluggers2.1.jpg'
image = cv2.imread(image_path)

# Define the coordinates for cropping (example coordinates)
x, y, w, h = 610, 50, 200, 300  # Adjust these coordinates as needed

# Loop to update x value and find best match
for i in range(9):
    roi = extract_roi(image, x, y, w, h)
    best_match = match_template(roi, templates)

    # Display the cropped image and the best match
    if best_match:
        print(f'The best match for x={x} is: {best_match}')
        update_google_sheet(sheet, best_match, x, y, w, h)
        cv2.imshow('Cropped Image', roi)
        cv2.imshow('Best Match', templates[best_match])
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    else:
        print(f'No match found for x={x}.')

    x += 300
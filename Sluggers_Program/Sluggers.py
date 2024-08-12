import cv2
import numpy as np
import requests
import os
import gspread

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
templates = load_templates(github_image_urls)

# Load the image, put the pictures I sent you in the path
image_path = ''
image = cv2.imread(image_path)

# Define the coordinates for cropping (example coordinates)
x, y, w, h = 900, 425, 135, 140  # Adjust these coordinates as needed

# Loop to update x value and find best match
for i in range(9):
    roi = extract_roi(image, x, y, w, h)
    best_match = match_template(roi, templates)

    if best_match:
        print(f'The best match for x={x} is: {best_match}')
        
        cv2.imshow('Cropped Image', roi)
        cv2.imshow('Best Match', templates[best_match])
        cv2.waitKey(2000)
        cv2.destroyAllWindows()
    else:
        print(f'No match found for x={x}.')

    x += 170

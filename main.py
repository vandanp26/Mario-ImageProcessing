import cv2
import os
# comment
def load_templates(folder_path):
    templates = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            template_name = os.path.splitext(filename)[0]
            template_image = cv2.imread(os.path.join(folder_path, filename))
            templates[template_name] = template_image
    return templates

def extract_roi(image_path):
    image = cv2.imread(image_path)
    # Define the coordinates for cropping (example coordinates)
    # x, y, w, h = 680, 92, 75, 90  # Adjust these coordinates as needed
    x, y, w, h = 395, 82, 125, 150
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

# Paths
image_path = '/Users/vandan/Sluggers_Proj/sluggers2.jpg'
template_folder_path = '/Users/vandan/Downloads/Sluggers_Characters'  # Change this to your folder path

# Load templates
templates = load_templates(template_folder_path)

# Extract ROI
roi = extract_roi(image_path)

# Match template
best_match = match_template(roi, templates)

# Display the cropped image and the best match
if best_match:
    print(f'The best match is: {best_match}')
    cv2.imshow('Cropped Image', roi)
    cv2.imshow('Best Match', templates[best_match])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('No match found.')

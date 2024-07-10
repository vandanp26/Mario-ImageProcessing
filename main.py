import cv2
import os
import pytesseract

def load_templates(folder_path):
    templates = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            template_name = os.path.splitext(filename)[0]
            template_image = cv2.imread(os.path.join(folder_path, filename), cv2.IMREAD_COLOR)
            if template_image is not None:
                templates[template_name] = template_image
    return templates

def extract_roi(image, x, y, w, h):
    roi = image[y:y+h, x:x+w]
    if roi.shape[0] < h or roi.shape[1] < w:
        raise ValueError('ROI dimensions are smaller than expected. Adjust cropping coordinates.')
    return roi

def match_template(roi, templates):
    best_match = None
    best_score = -1
    method = cv2.TM_CCOEFF_NORMED  # Template matching method

    print(f"ROI shape: {roi.shape}, ROI dtype: {roi.dtype}")
    
    for name, template in templates.items():
        print(f"Template '{name}' shape: {template.shape}, Template '{name}' dtype: {template.dtype}")
        if roi.shape[0] >= template.shape[0] and roi.shape[1] >= template.shape[1]:
            result = cv2.matchTemplate(roi, template, method)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            if max_val > best_score:
                best_score = max_val
                best_match = name
        else:
            print(f'Template {name} skipped due to size mismatch.')
    return best_match

def recognize_number(roi):
    # Use OCR to recognize the number
    config = '--psm 7'  # Single line mode
    text = pytesseract.image_to_string(roi, config=config)
    # Extract digits from the recognized text
    digits = ''.join(filter(str.isdigit, text))
    return digits

# Paths to your specific images and templates
image_path = '/Users/jacksonmacdonald/Desktop/SluggersProject/my-project/mvp-images/mvp_test.webp'
template_folder_path = '/Users/jacksonmacdonald/Desktop/SluggersProject/my-project/player-images'

# Load templates
templates = load_templates(template_folder_path)

# Load the image
image = cv2.imread(image_path)
if image is None:
    raise ValueError(f'Failed to load image: {image_path}')

# Extract ROI for the character
x_char, y_char, w_char, h_char = 395, 82, 80, 105
roi_char = extract_roi(image, x_char, y_char, w_char, h_char)

# Extract ROI for the number (adjust the coordinates as needed)
x_num, y_num, w_num, h_num = 395, 500, 20, 75
roi_num = extract_roi(image, x_num, y_num, w_num, h_num)

# Match template for the character
best_match = match_template(roi_char, templates)

# Recognize the number under the character
number = recognize_number(roi_num)

# Display the results
if best_match:
    print(f'The best match is: {best_match}')
    print(f'The number under the character is: {number}')
    cv2.imshow('Character ROI', roi_char)
    cv2.imshow('Number ROI', roi_num)
    cv2.imshow('Best Match', templates[best_match])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print('No match found.')

import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def replace_name_in_image(image_path, child_name, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT)

    found = False
    for i, word in enumerate(data['text']):
        if word.strip().lower() == "childname":
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

            # Clear existing text
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)

            # Write new name
            pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(pil_img)
            font = ImageFont.truetype("fonts/arialbd.ttf", size=h)
            
            # Compute text width and height correctly
            bbox = draw.textbbox((0, 0), child_name, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            
            draw.text((x, y), child_name, fill="black", font=font)

            image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            found = True
            break

    if not found:
        print(f"[⚠️] 'ChildName' not found in {image_path}")
    else:
        print(f"[✅] Replaced text with '{child_name}' in: {output_path}")

    cv2.imwrite(output_path, image)
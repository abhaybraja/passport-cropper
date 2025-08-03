from passport_cropper import crop_passport_photo
import os

CURRENT_DIR = os.path.dirname(__file__)
image_path = os.path.join(CURRENT_DIR, "admission_form.jpg")

cropped = crop_passport_photo(image_path, "output.jpg", 100)

from passport_cropper import crop_passport_photo

image_path = "admission_form.png"
cropped = crop_passport_photo(image_path, "output.jpg", max_kb=100)

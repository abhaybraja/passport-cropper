import cv2
from .utils import rotate_to_passport_orientation, save_cropped_with_size_limit


def crop_psp(file:str):
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_copy = image.copy()

    # Step 1: Detect the face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        print("No face detected.")
        exit()

    # Assume the first detected face is the one we want
    (x_face, y_face, w_face, h_face) = faces[0]
    cx, cy = x_face + w_face // 2, y_face + h_face // 2  # Center of face

    # Step 2: Find rectangular contours (possible photos)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidate_photo = None

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        if len(approx) == 4 and cv2.isContourConvex(approx):  # rectangle
            x, y, w, h = cv2.boundingRect(approx)

            # Check if face center is inside this rectangle
            if x < cx < x + w and y < cy < y + h:
                candidate_photo = (x, y, w, h)
                break

    if candidate_photo:
        x, y, w, h = candidate_photo

        # Draw the detected rectangle on the image
        cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Crop the rectangle
        cropped = image[y:y + h, x:x + w]
        file_name = file.split(".")[0]

        # Fix upside-down faces
        passport_ready = rotate_to_passport_orientation(cropped)
        save_cropped_with_size_limit(passport_ready, f"m{file_name}.jpg", 25)
        cv2.imwrite(f"c{file_name}.jpg", passport_ready)

        # Show result
        # cv2.imshow("Detected Passport Photo Area", image_copy)
        # cv2.imshow("Cropped Passport Photo", cropped)
    else:
        print("No surrounding rectangle found around the face.")

crop_psp("your_image_file_here.jpeg")


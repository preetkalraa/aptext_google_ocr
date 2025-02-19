import cv2

def preprocess_image(image_path):
    """Preprocess the image for better OCR results."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    preprocessed_image_path = "preprocessed_image.jpg"
    cv2.imwrite(preprocessed_image_path, binary)
    return preprocessed_image_path
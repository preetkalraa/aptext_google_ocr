from flask import Flask, request, jsonify, render_template
import os
import cv2
from google.cloud import vision
from pyngrok import ngrok

app = Flask(__name__, template_folder="/content/frontend/templates", static_folder="/content/frontend/static")

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/content/ap-text-ocr-c9b4ec6f0271.json"

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

def preprocess_image(image_path):
    """Preprocess the image for better OCR results."""
    print(f"Preprocessing image: {image_path}")
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Failed to load the image. Check the file path.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    preprocessed_image_path = "/content/preprocessed_image.jpg"
    cv2.imwrite(preprocessed_image_path, binary)
    print(f"Preprocessed image saved to: {preprocessed_image_path}")
    return preprocessed_image_path

def extract_text(image_path):
    """Extract text from the image using Google Cloud Vision API."""
    print(f"Extracting text from: {image_path}")
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        print(f"Extracted text: {texts[0].description}")
        return texts[0].description
    else:
        print("No text found.")
        return "No text found."

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle image upload and text extraction."""
    print("Upload endpoint called")  # Debug statement
    if "file" not in request.files:
        print("No file uploaded")  # Debug statement
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        print("No file selected")  # Debug statement
        return jsonify({"error": "No file selected"}), 400

    # Debug: Print the file name and size
    print(f"Uploaded file: {file.filename}, Size: {len(file.read())} bytes")
    file.seek(0)  # Reset file pointer after reading

    # Save the uploaded file
    image_path = "/content/uploaded_image.jpg"
    file.save(image_path)
    print(f"File saved to: {image_path}")

    # Check if the file exists
    if not os.path.exists(image_path):
        print("Failed to save the file")  # Debug statement
        return jsonify({"error": "Failed to save the file"}), 500

    # Preprocess the image
    preprocessed_image_path = preprocess_image(image_path)
    print(f"Preprocessed image saved to: {preprocessed_image_path}")

    # Extract text
    extracted_text = extract_text(preprocessed_image_path)
    print(f"Extracted text: {extracted_text}")

    # Return the extracted text
    return jsonify({"text": extracted_text})

# Run the Flask app with ngrok
if __name__ == "__main__":
    # Start ngrok tunnel
    public_url = ngrok.connect(5000).public_url
    print(f" * Running on {public_url}")
    app.run(host="0.0.0.0", port=5000)
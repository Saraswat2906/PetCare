import streamlit as st
from PIL import Image
import io
import torch
from ultralytics import YOLO

# Load the pre-trained YOLOv8 model
model = YOLO('yolov8s.pt')  # Use the appropriate YOLOv8 model path

# Function to analyze pet image using YOLOv8
def analyze_pet_image(image):
    # Convert the PIL image to a format compatible with YOLOv8
    image = image.convert('RGB')
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    # Perform object detection
    results = model(image_bytes)
    
    # Extract results
    detected_objects = results.pandas().xyxy[0]
    detections = detected_objects.to_dict(orient='records')

    # Generate a human-readable result
    if len(detections) > 0:
        # Example: Just return the first detected object and its confidence
        object_info = detections[0]
        label = object_info['name']
        confidence = object_info['confidence']
        return f"Detected: {label} with confidence {confidence:.2f}"
    else:
        return "No objects detected."

# Placeholder function for barcode scanning
def scan_barcode(barcode):
    if barcode == "1234567890":
        return "This food is suitable for your pet."
    else:
        return "This food may not be suitable for your pet."

# Placeholder function for age-based diet recommendations
def recommend_diet(age):
    if age < 1:
        return "Recommended diet for puppies: High protein and DHA for brain development."
    elif 1 <= age <= 7:
        return "Recommended diet for adult dogs: Balanced diet with proteins, vitamins, and minerals."
    else:
        return "Recommended diet for senior dogs: Low calorie, joint support supplements."

# Placeholder function for treat recommendations
def recommend_treats():
    return "Recommended Treats: Dental chews, peanut butter biscuits."

# Streamlit App Structure
st.title("Pet Care Assistant")

# Section 1: Upload pet image
st.header("1. Upload a picture of your pet")
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Pet Image.', use_column_width=True)
    st.write("")
    st.write("Analyzing...")
    # Analyze the uploaded pet image
    result = analyze_pet_image(image)
    st.write(result)

# Section 2: Scan food product barcode
st.header("2. Scan the barcode of a food product")
barcode = st.text_input("Enter or scan the barcode of the food product")
if barcode:
    result = scan_barcode(barcode)
    st.write(result)

# Section 3: Age-based diet recommendations
st.header("3. Get diet recommendations based on your pet's age")
age = st.slider('Select your pet\'s age (in years)', 0, 20)
if age is not None:
    diet_recommendation = recommend_diet(age)
    st.write(diet_recommendation)

# Section 4: Treat recommendations
st.header("4. Find suitable treats for your pet")
if st.button('Recommend Treats'):
    treats = recommend_treats()
    st.write(treats)

# Section 5: Links to food products (Static for demo)
st.header("5. Suggested food products for your pet")
st.write("[Buy Premium Dog Food](https://example.com/dog-food)")
st.write("[Buy Grain-Free Cat Food](https://example.com/cat-food)")

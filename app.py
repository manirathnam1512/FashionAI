import os
import torch
import torchvision.transforms as transforms
from flask import Flask, request, render_template, jsonify
from PIL import Image
from torchvision import models

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load a Pretrained Model (ResNet50)
model = models.resnet50(pretrained=True)
model.eval()  # Set to evaluation mode

# Define Transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Dummy Fashion Categories (Replace with actual dataset)
fashion_classes = ["Casual", "Formal", "Sportswear", "Streetwear", "Party", "Business Casual"]

# Function to Process Image and Predict Category
def process_image(image_path):
    img = Image.open(image_path).convert("RGB")  # Convert image to RGB mode
    img_tensor = transform(img).unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        outputs = model(img_tensor)
        _, predicted = outputs.max(1)  # Get the class with the highest probability

    return fashion_classes[predicted.item() % len(fashion_classes)]  # Dummy Mapping


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded!", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file!", 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Process the image using AI
        recommendation = process_image(file_path)

        return jsonify({"recommendation": recommendation, "image_url": file_path})

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

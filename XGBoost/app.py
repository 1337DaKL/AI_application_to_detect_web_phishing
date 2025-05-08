from flask import Flask, request, jsonify
import joblib
import pandas as pd
from extract_features import extract_features
from flask_cors import CORS
# Load model
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "xgboost_model.pkl")
model = joblib.load(model_path)


used_features = [
    "domain_length",
    "link_ratio",
    "domain_name_frequency",
    "is_https",
    "has_non_alpha_in_domain",
    "copyright_logo_match",
    "title_domain_match"
]

app = Flask(__name__)
CORS(app)  
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing 'url' field"}), 400

    try:
        features = extract_features(url)

        if features["can_extract"] != 1:
            return jsonify({"url": url, "label": -1, "message": "Không thể trích xuất nội dung"}), 200

        # Chuyển thành DataFrame chỉ lấy các feature cần
        input_df = pd.DataFrame([{k: features[k] for k in used_features}])
        label = int(model.predict(input_df)[0])

        return jsonify({"url": url, "label": label})  # label = 1: phishing, 0: hợp lệ

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

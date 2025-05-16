# myapp/utils.py
import tensorflow as tf
from tensorflow import keras
import tempfile
import requests

_model = None

# Replaced recommendation_model.h5 with S3 URL
S3_MODEL_URL = "https://<your-bucket-name>.s3.<your-region>.amazonaws.com/recommendation_model.h5"

def load_model():
    global _model
    if _model is None:
        response = requests.get(S3_MODEL_URL)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix=".h5") as tmp:
                tmp.write(response.content)
                tmp.flush()
                _model = keras.models.load_model(
                    tmp.name,
                    custom_objects={'mse': tf.keras.losses.MeanSquaredError()}
                )
        else:
            raise Exception(f"Failed to download model. Status code: {response.status_code}")
    return _model

def preprocess(user_id, user_behavior, context):
    # This is placeholder logic — real features should reflect your model
    recent_views = len(user_behavior.get("recent_views", []))
    cart_items = len(user_behavior.get("cart_items", []))
    purchases = len(user_behavior.get("purchase_history", []))
    location = 1 if context.get("location") == "UAE" else 0
    device = 1 if context.get("device_type") == "mobile" else 0
    return [user_id, recent_views, cart_items, purchases, location, device]

def postprocess(predictions):
    top_scores = predictions.flatten()
    product_ids = [f"product_{i+100}" for i in range(len(top_scores))]
    return sorted(
        [{"product_id": pid, "score": round(score, 2)} for pid, score in zip(product_ids, top_scores)],
        key=lambda x: x["score"],
        reverse=True
    )[:3]  # Top 3



import numpy as np
from tensorflow import keras
import tensorflow as tf

# Explicitly register the class of MSE (Mean Squared Error), not the instance
custom_objects = {"mse": tf.keras.losses.MeanSquaredError}

# Load the model with custom objects
model = keras.models.load_model("myapp/saved_models/recommendation_model.h5", custom_objects=custom_objects)

# Example content data
content_data = np.array([
    [1, 0, 0],  # Item 0
    [0, 1, 0],  # Item 1
    [0, 0, 1],  # Item 2
    [1, 1, 0]   # Item 3
])

def recommend_products(user_id, top_n=5):
    all_item_ids = np.array([0, 1, 2, 3])  # Example item IDs
    item_scores = []

    for item_id in all_item_ids:
        user_input = np.array([user_id]).reshape(1, -1)
        item_input = np.array([item_id]).reshape(1, -1)

        score = model.predict([user_input, item_input])[0][0]  # Get the score
        item_scores.append((item_id, score))

    # Sort by score (higher is better)
    item_scores.sort(key=lambda x: x[1], reverse=True)
    recommended_items = [item_id for item_id, score in item_scores[:top_n]]

    return recommended_items




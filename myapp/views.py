# myapp/views.py
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import load_model, preprocess, postprocess
import numpy as np

# Load model once
model = load_model()

@api_view(["GET"])
def get_recommendations(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        item_ids = np.arange(50)
        user_ids = np.full_like(item_ids, user_id)
        predictions = model.predict([user_ids, item_ids])
        top_indices = np.argsort(predictions.flatten())[-5:][::-1]
        return Response({
            "user": user.username,
            "user_id": user.id,
            "recommendations": top_indices.tolist()
        })
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(["GET", "POST"])
def recommend(request):
    if request.method == "GET":
        # Return API documentation or a test message
        return Response({
            "message": "POST to this endpoint with user_id, user_behavior, and context to receive recommendations.",
            "example_payload": {
                "user_id": "123456",
                "user_behavior": {
                    "recent_views": ["product_101", "product_204"],
                    "cart_items": ["product_304"],
                    "purchase_history": ["product_003", "product_004"]
                },
                "context": {
                    "location": "UAE",
                    "device_type": "mobile"
                }
            }
        })

    elif request.method == "POST":
        try:
            data = request.data
            user_id = data.get('user_id')
            user_behavior = data.get('user_behavior', {})
            context = data.get('context', {})

            # Preprocess features
            user_features = preprocess(user_id, user_behavior, context)

            # Predict and postprocess
            predictions = model.predict(np.array([user_features]))
            results = postprocess(predictions)

            return Response({
                "user_id": user_id,
                "recommendations": results
            })
        except Exception as e:   
            return Response({"error": str(e)}, status=500)

def home(request):
    return render(request, 'home.html')

            


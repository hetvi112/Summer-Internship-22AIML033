# EmotionDetection/emotion_detection.py

from transformers import pipeline

# Initialize the Hugging Face pipeline once (downloads the model on first run).
# Model labels: ['sadness','joy','love','anger','fear','surprise']
# We'll map them to your project's keys: anger, disgust, fear, joy, sadness
_emotion_clf = pipeline(
    task="text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion"
)

def _round3(x: float) -> float:
    return float(f"{x:.3f}")

def emotion_detector(text_to_analyze: str):
    """
    Runs local emotion detection using a Transformer model and returns a dict:
    {
      'anger': float,
      'disgust': float,   # model doesn't provide this -> 0.0
      'fear': float,
      'joy': float,
      'sadness': float,
      'dominant_emotion': str
    }
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            "anger": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "joy": 0.0,
            "sadness": 0.0,
            "dominant_emotion": None,
        }

    # Ask for all scores so we can map/aggregate them
    results = _emotion_clf(text_to_analyze, return_all_scores=True)
    # results is a list with one item (for one input); that item is a list of dicts
    # like: [{'label': 'joy', 'score': 0.97}, ...]
    scores_list = results[0]

    # Convert to lowercase key dict for easy access
    hf = {item["label"].lower(): float(item["score"]) for item in scores_list}

    # Map to your required keys.
    # 'love' is strongly positive; add it into 'joy'.
    anger = hf.get("anger", 0.0)
    fear = hf.get("fear", 0.0)
    joy = hf.get("joy", 0.0) + hf.get("love", 0.0)
    sadness = hf.get("sadness", 0.0)
    disgust = 0.0  # not provided by this model

    formatted = {
        "anger": _round3(anger),
        "disgust": _round3(disgust),
        "fear": _round3(fear),
        "joy": _round3(joy),
        "sadness": _round3(sadness),
    }

    # Determine dominant emotion among the five keys you display
    dominant_emotion = max(formatted.items(), key=lambda x: x[1])[0]
    formatted["dominant_emotion"] = dominant_emotion

    return formatted

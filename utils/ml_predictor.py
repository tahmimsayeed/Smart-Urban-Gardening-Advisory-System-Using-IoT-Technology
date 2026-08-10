"""
utils/ml_predictor.py

Loads the trained MobileNetV2 model (plant_model.keras, produced by
training in Google Colab per the project spec) and runs inference on an
uploaded leaf image. The Flask app never trains anything -- it only loads
an already-trained model file, exactly as specified.

Mock fallback: per the project's own testing rule ("Each completed module
must be testable independently"), Disease Detection needs to be fully
testable before the real dataset has been trained on Colab and the model
file copied in. If ml_model/plant_model.keras or labels.json aren't found,
predict() automatically returns a plausible-looking MOCK prediction instead
of crashing, and callers are told which mode they got back so they can
show an honest "this is a mock result" notice to the user. No code changes
are needed later -- once you drop the real files into ml_model/, this
module picks them up automatically and mock mode turns off by itself.
"""
import json
import os
import random

from utils.treatment_tips import TREATMENT_TIPS

IMG_SIZE = (224, 224)

_model = None
_labels = None
_mock_mode = False
_loaded = False

# Used only in mock mode, before a real model exists. Matches the label
# format documented in utils/treatment_tips.py so mock results still look
# and behave like real ones during development/testing.
_MOCK_LABELS = list(TREATMENT_TIPS.keys())


def _ensure_loaded(model_path, labels_path):
    global _model, _labels, _mock_mode, _loaded
    if _loaded:
        return

    if os.path.exists(model_path) and os.path.exists(labels_path):
        import tensorflow as tf  # imported lazily so the rest of the app
        #                          doesn't need TensorFlow installed just
        #                          to start up (only this module does).
        _model = tf.keras.models.load_model(model_path)
        with open(labels_path) as f:
            _labels = json.load(f)
        _mock_mode = False
    else:
        _labels = _MOCK_LABELS
        _mock_mode = True

    _loaded = True


def is_mock_mode(model_path, labels_path):
    """Lets a route check the mode without triggering a prediction, e.g.
    to show a banner on the upload page itself."""
    _ensure_loaded(model_path, labels_path)
    return _mock_mode


def predict(image_path, model_path, labels_path):
    """Returns (disease_label, confidence_score, mode) where mode is
    'trained-model' or 'mock'. confidence_score is a float in [0, 1]."""
    _ensure_loaded(model_path, labels_path)

    if _mock_mode:
        label = random.choice(_labels)
        confidence = round(random.uniform(0.55, 0.97), 3)
        return label, confidence, "mock"

    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    img = tf.keras.utils.load_img(image_path, target_size=IMG_SIZE)
    array = tf.keras.utils.img_to_array(img)
    array = tf.expand_dims(array, axis=0)
    array = preprocess_input(array)

    predictions = _model.predict(array, verbose=0)[0]
    idx = int(predictions.argmax())
    return _labels[idx], float(predictions[idx]), "trained-model"

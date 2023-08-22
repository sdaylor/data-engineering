import numpy.typing
from flask import Flask, request
from imageai.Classification import ImageClassification
import os
from io import BytesIO
import requests
from PIL import Image
import numpy as np
import typing

app = Flask(__name__)
model_url = "https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/inception_v3_google-1a9a5a14.pth/"
model_file_name = "inception_v3.pth"

with requests.get(model_url, stream=True) as r:
    r.raise_for_status()
    with open("inception_v3.pth", "wb") as f:
        f.write(r.content)

# Instantiate the model for inference
prediction = ImageClassification()
prediction.setModelTypeAsInceptionV3()
prediction.setModelPath(os.path.join(os.getcwd(), model_file_name))
prediction.loadModel()


def retrieve_convert_img(image_url: str):
    """
    Retrieves image data and converts it to a 3D tensor represented by Numpy

    :param image_url: HTTP URL containing the image to make inferences on
    :return: 3D Numpy tensor
    """
    r = requests.get(image_url, stream=True)
    f = BytesIO(r.content)
    img = Image.open(f)
    return np.asarray(img)


def predict(image, pred_count: int) -> typing.Dict[str, float]:
    """
    Perform inferences on the InceptionV3 image classification model

    :param image: 3D Numpy tensor representing image data
    :param pred_count: Number of times to infer
    :return: Dictionary of inferences
    """
    preds, probs = prediction.classifyImage(image, result_count=pred_count)
    return {pred: prob for pred, prob in zip(preds, probs)}


@app.route("/", methods=["GET", "POST"])
def infer():
    """
    If a GET request, return 200 to indicate the endpoint is up.
    If a POST request, expect 'image_url' and 'prediction_count' parameters in the POST body,
    retrieve the image via 'image_url', convert the image to a numpy array, and make
    'prediction_count' image classification inferences on the image.

    :return: Provided parameters and inference data
    """
    if request.method == "POST":
        post_data = request.get_json()
        image_url = post_data["image_url"]
        pred_count = post_data["prediction_count"]

        np_img = retrieve_convert_img(image_url)
        preds = predict(np_img, pred_count)

        res = {
            "parameters": {"image_url": image_url, "prediction_count": pred_count},
            "predictions": preds
        }
        return res, 200

    elif request.method == "GET":
        return "Heartbeat", 200


if __name__ == "__main__":
    app.run(debug=True)

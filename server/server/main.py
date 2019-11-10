from fastapi import FastAPI
import foolbox
from foolbox.criteria import TargetClassProbability
import keras
import numpy as np
from keras.applications.resnet50 import ResNet50, decode_predictions, preprocess_input
from PIL import Image
from io import BytesIO
import base64
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def get_image():
    image, label = foolbox.utils.imagenet_example()
    image_pil = Image.fromarray(np.uint8(image))
    output_image = BytesIO()
    image_pil.save(output_image, format="png")

    return {
        "image": base64.b64encode(output_image.getvalue()).decode().replace("'", ""),
        "label": int(label),
    }


def get_string_label(image, model):
    return decode_predictions(model.predict(preprocess_input(image[np.newaxis].copy())))[0][0][1]


@app.get("/fgsm")
def attack_fgsm():
    keras.backend.set_learning_phase(0)
    kmodel = ResNet50(weights="imagenet")
    preprocessing = dict(flip_axis=-1, mean=np.array([104, 116, 123]))
    fmodel = foolbox.models.KerasModel(
        kmodel, bounds=(0, 255), preprocessing=preprocessing
    )
    attack = foolbox.attacks.FGSM(fmodel)
    image, label = foolbox.utils.imagenet_example()
    adversarial = attack(np.array([image]), np.array([label]))
    image_pil = Image.fromarray(np.uint8(image))
    adv_pil = Image.fromarray(np.uint8(adversarial[0]))

    output_image = BytesIO()
    image_pil.save(output_image, format="png")

    output_adv = BytesIO()
    adv_pil.save(output_adv, format="png")

    return {
        "original": {
            "image": base64.b64encode(output_image.getvalue())
            .decode()
            .replace("'", ""),
            "label": get_string_label(image, kmodel),
        },
        "adversarial": {
            "image": base64.b64encode(output_adv.getvalue()).decode().replace("'", ""),
            "label": get_string_label(adversarial[0], kmodel),
        },
    }

@app.get("/deepfool")
def attack_deepfool():
    keras.backend.set_learning_phase(0)
    kmodel = ResNet50(weights="imagenet")
    preprocessing = dict(flip_axis=-1, mean=np.array([104, 116, 123]))
    fmodel = foolbox.models.KerasModel(
        kmodel, bounds=(0, 255), preprocessing=preprocessing
    )
    attack = foolbox.attacks.DeepFoolAttack(fmodel)
    image, label = foolbox.utils.imagenet_example()
    adversarial = attack(np.array([image]), np.array([label]))
    image_pil = Image.fromarray(np.uint8(image))
    adv_pil = Image.fromarray(np.uint8(adversarial[0]))

    output_image = BytesIO()
    image_pil.save(output_image, format="png")

    output_adv = BytesIO()
    adv_pil.save(output_adv, format="png")

    return {
        "original": {
            "image": base64.b64encode(output_image.getvalue())
            .decode()
            .replace("'", ""),
            "label": get_string_label(image, kmodel),
        },
        "adversarial": {
            "image": base64.b64encode(output_adv.getvalue()).decode().replace("'", ""),
            "label": get_string_label(adversarial[0], kmodel),
        },
    }

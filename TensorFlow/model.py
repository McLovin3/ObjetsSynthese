from lobe import ImageModel

model = ImageModel.load("./TensorFlow/")


def predict_image(path):
    return model.predict_from_file(path)

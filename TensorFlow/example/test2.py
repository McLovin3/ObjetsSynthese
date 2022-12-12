from lobe import ImageModel

model = ImageModel.load('..')

result = model.predict_from_file('Amog.jpg')
print(result)

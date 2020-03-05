from PIL import Image as PIL
class ColorImageParser:

    field = 'color_image'

    def parse(self, context, snapshot):
        path = context.path('color_image.jpg')
        size = snapshot.color_image.width, snapshot.color_image.height
        data = snapshot.color_image.data
        image = PIL.frombytes(data=data, mode='RGB', size=size)
        image.save(path)
        return path

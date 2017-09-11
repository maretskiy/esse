# -*- coding: utf-8 -*-

from PIL import Image


class PhotoProcessingError(Exception):
    pass


class Photo(object):

    FORMATS = {'JPEG': 'jpg'}

    def __init__(self, path):
        self._image = Image.open(path)
        self._format = self._image.format

        try:
            self._extension = self.FORMATS[self._format]
        except KeyError:
            raise PhotoProcessingError("Unexpected image format: %s" % self._format)

        mode = 'RGBA' # Transparent
        if self._image.mode != mode:
            self._image = self._image.convert(mode)
        w, h = map(float, self._image.size)
        self._path = path
        self._width = w
        self._height = h

    def save(self):
        self._image.save(self._path, self._format)
        return self

    def save_to(self, path):
        self._image.save(path, self._format)
        return self

    def scale(self, width, height):
        """Scale and crop image to given size."""
        if self._width == width and self._height == height:
            return self

        if (self._width / self._height) > (float(width) / height):
            scaleH = height
            scaleW = int(round(self._width / (self._height / height)))

            cropH0 = 0
            cropH1 = height
            cropW0 = (scaleW - width) / 2
            cropW1 = width + cropW0
        else:
            scaleH = int(round(self._height / (self._width / width)))
            scaleW = width

            cropH0 = (scaleH - height) / 2
            cropH1 = height + cropH0
            cropW0 = 0
            cropW1 = width

        self._image = self._image.resize(
            (scaleW, scaleH), Image.ANTIALIAS
        ).crop((cropW0, cropH0, cropW1, cropH1))

        return self

    def scale_adjust(self, width, height):
        """Adjust scale and crop image to given size."""
        if self._width == width and self._height == height:
            return self

        if (self._width / self._height) > (float(width) / height):
            scaleH = int(round(self._height / (self._width / width)))
            scaleW = width

            cropH0 = (scaleH - height) / 2
            cropH1 = height + cropH0
            cropW0 = 0
            cropW1 = width
        else:
            scaleH = height
            scaleW = int(round(self._width / (self._height / height)))

            cropH0 = 0
            cropH1 = height
            cropW0 = (scaleW - width) / 2
            cropW1 = width + cropW0

        image = self._image.resize(
            (scaleW, scaleH), Image.ANTIALIAS
        ).crop((cropW0, cropH0, cropW1, cropH1))

        bg_color = (255,255,255) # White
        self._image = Image.new('RGBA', image.size, bg_color)
        self._image.paste(image, (0,0), image)

        return self

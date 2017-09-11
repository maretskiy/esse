# -*- coding: utf-8 -*-

import os
import random
import time

from PIL import Image, ImageDraw, ImageFont, ImageFilter


PIL_FONT_DFLT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'fonts/MuktiNarrow.ttf')
PIL_MODIFY_DFLT = ((3, 3),[7.0,-4.0,-4.0,2.0,-5.0,-5.0,4.0,3.0,3.0])
PIL_CHARS_DFLT = 'abcdefghkmnopqrstuvwzyzABCDEFGHJKLMNPQRSTUVWZYZ123456789'

class Captcha(object):
    """Image captcha."""

    def __init__(self,
                 images_dir,
                 words_dir,
                 img_type='PNG',
                 img_extension='png',
                 txt_extension='txt',
                 color_rgb=(230,230,230),
                 bgcolor_rgb=(255,255,255),
                 img_size=(138,22),
                 img_position=(5,-7),
                 img_modify_kernel=None,
                 img_modify_rank=(3, 3),
                 chars=None,
                 chars_num=6,
                 font_file_ttf=None,
                 font_size=20,
                 ttl_seconds=3600):

        self.img_dir = images_dir
        self.txt_dir = words_dir

        # Try to create directories if absent
        if not os.path.isdir(self.img_dir):
            os.makedirs(self.img_dir)
        if not os.path.isdir(self.txt_dir):
            os.makedirs(self.txt_dir)

        self.img_type = img_type
        self.img_extension = ".%s" % img_extension
        self.txt_extension = ".%s" % txt_extension
        self.img_background = bgcolor_rgb
        self.img_color = color_rgb
        self.img_size = img_size
        self.img_position = img_position
        self.img_modify_kernel = img_modify_kernel or PIL_MODIFY_DFLT
        self.img_modify_rank = img_modify_rank
        self.chars = chars or PIL_CHARS_DFLT
        self.str_length = chars_num
        self.font_file = font_file_ttf or PIL_FONT_DFLT
        self.font_size = font_size
        self.ttl = ttl_seconds

        # Load TTF font
        self.font = ImageFont.truetype(self.font_file, self.font_size)
        self.tries = 5

    def __id(self, tries):
        """Generate new ID."""

        if tries is 0:
            raise RuntimeError('failed to create unique captcha file name')

        ts = time.localtime()

        captcha_id = "%0.4i%0.2i%0.2i%0.2i%0.2i%0.2i%0.2i" % (
            ts[0],ts[1],ts[2],ts[3],ts[4],ts[5], random.randint(1000,9999))

        captcha_file = os.path.join(
            self.img_dir, captcha_id + self.img_extension)

        if os.path.exists(captcha_file):
            captcha_id = self.__id(tries - 1)

        return captcha_id

    def new(self):
        """Create new captcha."""

        captcha_id = self.__id(self.tries)

        captcha_text = ""
        for i in range(0, self.str_length):
            captcha_text += self.chars[
                random.randint(0, 0xffffff) % len(self.chars)]

        image = Image.new('RGB', self.img_size, self.img_background)

        # Draw image
        draw = ImageDraw.Draw(image)
        draw.text(
            self.img_position,
            captcha_text,
            fill=self.img_color,
            font=self.font)

        # Modify image
        if self.img_modify_kernel:
            image = image.filter(ImageFilter.Kernel(*self.img_modify_kernel))
        if self.img_modify_rank:
            image = image.filter(ImageFilter.RankFilter(*self.img_modify_rank)) #3, 3

        # Save captcha image file
        captcha_image_file = os.path.join(
            self.img_dir, captcha_id + self.img_extension)
        image.save(captcha_image_file, self.img_type)

        # Save captcha text file
        captcha_text_file = os.path.join(
            self.txt_dir, captcha_id + self.txt_extension)

        fd = open(captcha_text_file, 'w')
        fd.write(captcha_text)
        fd.close()

        return captcha_id, captcha_image_file

    def verify(self, captcha_id, captcha_text):
        """Verify captcha text for specified captcha_id.

        :returns: bool, captcha verification status
        """

        captcha_text_file = os.path.join(
            self.txt_dir, captcha_id + self.txt_extension)
        captcha_image_file = os.path.join(
            self.img_dir, captcha_id + self.img_extension)
        status = False

        if os.path.exists(captcha_text_file):

            fd = open(captcha_text_file, 'r')
            captcha_text_true = fd.readline()
            fd.close()

            if captcha_text == captcha_text_true:
                status = True
                os.remove(captcha_text_file)
                os.remove(captcha_image_file)

        return status

    def delete(self, captcha_id):
        """Delete captcha file."""

        try:
            os.remove(os.path.join(
                self.img_dir, captcha_id + self.img_extension))

            os.remove(os.path.join(
                self.txt_dir, captcha_id + self.txt_extension))
        except OSError:
            pass # Silent

        return True

    def cleanup(self):
        """Remove expired images and text files."""

        removed_images = 0
        removed_texts = 0
        expired_time = time.time() - self.ttl

        if os.path.isdir(self.img_dir) and os.path.isdir(self.txt_dir):

            # Remove image files
            for image_file in os.listdir(self.img_dir):
                file_path = os.path.join(self.img_dir, image_file)

                if os.path.isfile(file_path)\
                    and os.path.getmtime(file_path) < expired_time:
                    os.remove(file_path)
                    removed_images += 1

            # Remove text files
            for text_file in os.listdir(self.txt_dir):
                file_path = os.path.join(self.txt_dir, text_file)

                if os.path.isfile(file_path)\
                    and os.path.getmtime(file_path) < expired_time:
                    os.remove(file_path)
                    removed_texts += 1

        return removed_images, removed_texts

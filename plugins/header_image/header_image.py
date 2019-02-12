# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools

import logging
import os
import textwrap
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from pelican import signals
from pelican.generators import ArticlesGenerator, PagesGenerator
from shutil import copyfile

from lxml import html
from lxml.html.clean import clean_html

# Size that will be used as a base for generating the thumbnails
# It should be at least as large as the largest of the thumbnail sizes.

base_size = [1200, 1200]

# Thumbnail sizes for different sharing platforms. The name will be appended to the name when resizing (or cropping).

th_sizes = {
    'thumbnail': [350, 175],
    'twitter': [800, 418],
    'facebook': [476, 249],
    'linkedin': [1200, 627],
}

logger = logging.getLogger(__name__)

# Load the fonts
cur_dir = os.path.dirname(os.path.realpath(__file__))
font_path_title = os.path.join(cur_dir, 'AmaticSC-Bold.ttf')
font_path_website = os.path.join(cur_dir, 'IndieFlower.ttf')

def attach_clipper(x):
    return x[9:] if x[9] == '/' else x[8:]

def filename_clipper(x):
    return x[11:] if x[11] == '/' else x[10:]


def process_image(generator, content, image):
    if image.startswith('{attach}'):
        image = attach_clipper(image)
        path = os.path.join(generator.settings.get('PATH'), content.relative_dir, image)
    elif image.startswith('{filename}'):
        image = filename_clipper(image)
        path = os.path.join(generator.settings.get('PATH'), image)
    else:
        logger.error('Header Image: Tag not recognized: {}'.format(image))
        return

    title = html.fromstring(content.title)
    title = clean_html(title).text_content().strip()
    if os.path.isfile(path):
        if content.slug:
            out_dir = os.path.join(generator.settings.get('HEADERS_FOLDER'), content.slug)

        else:
            out_dir = os.path.join(generator.settings.get('HEADERS_FOLDER'), content.relative_dir)

        output_path = os.path.join(generator.output_path, out_dir)

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        image = os.path.split(image)[-1]
        output_image_path = os.path.join(output_path, image)

        if not os.path.isfile(output_image_path) or generator.settings.get('FORCE_IMG_REBUILD', False):
            copyfile(path, output_image_path)
            im = Image.open(output_image_path)
            im.thumbnail((base_size[0], base_size[1]), Image.ANTIALIAS)
            im.save(output_image_path)

        for key in th_sizes:
            th_name = ''.join(image.split('.')[:-1]) + '_' + key + '.jpg'
            th_full_path = os.path.join(output_path, th_name)
            logger.info('Save image path: {}'.format(th_full_path))

            th_size = th_sizes[key]

            if not os.path.isfile(th_full_path) \
                    or generator.settings.get('FORCE_IMG_REBUILD', False):
                im = Image.open(output_image_path)
                width, height = im.size

                #  Compare the aspect ratios
                ar_image = width/height
                ar_th =th_size[0]/th_size[1]

                if ar_image > ar_th:
                    width_th = width * th_size[1] / height
                    im.thumbnail((width_th, th_size[1]), Image.ANTIALIAS)
                    # Crop the image to the desired size, assuming the height is correct
                    left = int((width_th - th_size[0]) / 2)
                    right = int((width_th + th_size[0]) / 2)
                    im_copped = im.crop((left, 0, right, th_size[1] - 1))

                else:
                    height_th = height * th_size[0]/width
                    im.thumbnail((th_size[0], height_th), Image.ANTIALIAS)
                    # Crop the image to the desired size, assuming the width is correct
                    bottom = int((height_th - th_size[1]) / 2)
                    top = int((height_th + th_size[1]) / 2)
                    im_copped = im.crop((0, bottom, th_size[0], top))

                # Make it darker, to display the text without problems
                brightness = ImageEnhance.Brightness(im_copped)
                im_dark = brightness.enhance(0.5)
                draw = ImageDraw.Draw(im_dark)

                # Using a font size equivalent to 1/5 of the height
                font_size = int(th_size[1] / 3.5 / 10 * 7.5)  #  The last bit: /10*7.5 is to convert to points from pixels
                font = ImageFont.truetype(font_path_title, font_size)
                text = textwrap.fill(title, width=24)
                text_size = draw.textsize(text)
                logger.info('Text size: {}, image width: {}'.format(text_size, th_size[0]))
                y_pos = int(th_size[1]*1/10)
                x_pos = int(th_size[0]/8)
                draw.text((x_pos, y_pos), text, (255, 255, 255), font=font)

                # Write the website name
                font = ImageFont.truetype(font_path_website, int(font_size*.8))
                text = textwrap.fill("Python for the Lab.com", width=24)
                text_size = draw.textsize(text)
                logger.info('Website text size: {}, image width: {}'.format(text_size, th_size[0]))
                x_pos = int(th_size[0] / 9)
                y_pos = int(th_size[1] * 3.8 / 5)
                draw.text((x_pos, y_pos), text, (255, 255, 255), font=font)

                im_dark.save(th_full_path)

            setattr(content, 'header_'+key, os.path.join(out_dir, th_name))

    else:
        logger.error('photo: No photo for {} at {}'.format(content.source_path, path))


def detect_header(generator, content):
    image = content.metadata.get('header', None)
    if image:
        process_image(generator, content, image)
    else:
        logger.warning('{} does not have a custom header image. Using default'.format(content))
        process_image(generator, content, '{filename}' + generator.settings.get('DEFAULT_HEADER'))



def detect_image_header(generators):
    """ Runs generator on both pages and articles."""
    for generator in generators:
        if isinstance(generator, ArticlesGenerator):
            for article in itertools.chain(generator.articles, generator.translations, generator.drafts):
                detect_header(generator, article)
        elif isinstance(generator, PagesGenerator):
            for page in itertools.chain(generator.pages, generator.translations, generator.hidden_pages):
                detect_header(generator, page)


def register():
    try:
        signals.all_generators_finalized.connect(detect_image_header)
    except Exception as e:
        logger.error(e)

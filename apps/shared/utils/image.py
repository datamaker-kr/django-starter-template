def get_cropped_thumbnail(image, width=300, height=300, box=None, crop=True):
    from easy_thumbnails.files import get_thumbnailer

    thumbnail_options = {
        'size': (width, height),
        'detail': True,
        'upscale': True
    }

    if crop:
        thumbnail_options['crop'] = '50, 50'

    if box:
        thumbnail_options['box'] = box

    return get_thumbnailer(image).get_thumbnail(thumbnail_options)


def get_cropped_thumbnail_url(image, width=300, height=300, box=None, crop=True):
    try:
        return get_cropped_thumbnail(image, width=width, height=height, box=box, crop=crop).url
    except:
        return ''

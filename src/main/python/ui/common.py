from collections import namedtuple


BACKGROUND = "BACKGROUND"
PRESENTATION = "PRESENTATION"
PRIMARY = "PRIMARY"
SECONDARY = "SECONDARY"
ZOOM_SELECTION = "ZOOM_SELECTION"
CROP_SELECTION = "CROP_SELECTION"

POSSIBLE_ORIGINS = [
    BACKGROUND, PRESENTATION, PRIMARY, SECONDARY, ZOOM_SELECTION, CROP_SELECTION
]

SVG_SCALE_FACTOR = 1

IMAGE_TYPES = ['svg', 'png', 'jpg', 'jpeg']

GenerationOptions = namedtuple('GenerationOptions', 'unsharp, override_images, upload_to_s3, bucket_name')

from collections import namedtuple


BACKGROUND = "BACKGROUND"
PRESENTATION = "PRESENTATION"
PRIMARY = "PRIMARY"
SECONDARY = "SECONDARY"

POSSIBLE_ORIGINS = [
    BACKGROUND, PRESENTATION, PRIMARY, SECONDARY
]

IMAGE_TYPES = ['svg', 'png', 'jpg', 'jpeg']

GenerationOptions = namedtuple('GenerationOptions', 'unsharp, override_images, upload_to_s3, bucket_name')

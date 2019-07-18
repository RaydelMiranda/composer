from collections import namedtuple

CompositionItem = namedtuple('CompositionItem', 'image_path, layer')
Rectangle = namedtuple('Rectangle', 'width, height')


def min_resize(r: Rectangle, ratio: float) -> Rectangle:
    """
    :param r: A rectangle.
    :param ratio: The desired aspect ratio
    :return: A rectangle with the desired R with the minimum change to r.
    """

    # Compute width change.
    x = (r.width - r.height * ratio) / ratio
    # Compute height change.
    y = (r.height - r.width * ratio) / ratio

    if abs(x) < abs(y):
        return Rectangle(r.width, r.height + x)

    return Rectangle(r.width + y, r.height)

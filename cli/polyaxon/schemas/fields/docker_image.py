from marshmallow import ValidationError

from polyaxon.schemas.fields.params import PARAM_REGEX


def validate_image(image):
    if not image:
        return
    param = PARAM_REGEX.search(image)
    if param:
        return
    if " " in image:
        raise ValidationError("Invalid docker image `{}`".format(image))
    tagged_image = image.split(":")
    if len(tagged_image) > 3:
        raise ValidationError("Invalid docker image `{}`".format(image))
    if len(tagged_image) == 3 and (
        "/" not in tagged_image[1] or tagged_image[1].startswith("/")
    ):
        raise ValidationError("Invalid docker image `{}`".format(image))

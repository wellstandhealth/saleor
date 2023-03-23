import mimetypes
import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from ..thumbnail.utils import is_icon_image_mimetype
from .error_codes import AppErrorCode


class AppURLValidator(URLValidator):
    validator = URLValidator
    host_re = "(" + validator.hostname_re + validator.domain_re + "|localhost)"
    regex = re.compile(
        r"^(?:[a-z0-9.+-]*)://"  # scheme is validated separately
        r"(?:[^\s:@/]+(?::[^\s:@/]*)?@)?"  # user:pass authentication
        r"(?:" + validator.ipv4_re + "|" + validator.ipv6_re + "|" + host_re + ")"
        r"(?::\d{2,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )


image_url_validator = AppURLValidator(
    message="Incorrect value for field: logo.default.",
    code=AppErrorCode.INVALID_URL_FORMAT.value,
)


def brand_validator(brand):
    try:
        logo_url = brand["logo"]["default"]
    except (TypeError, KeyError):
        raise ValidationError(
            "Missing required field: logo.default.", code=AppErrorCode.REQUIRED.value
        )
    image_url_validator(logo_url)
    filetype = mimetypes.guess_type(logo_url)[0]
    if not is_icon_image_mimetype(filetype):
        raise ValidationError(
            "Invalid file type for field: logo.default.",
            code=AppErrorCode.INVALID_URL_FORMAT.value,
        )

import re
from typing import Dict

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator

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
color_string_validator = RegexValidator(
    regex=re.compile(r"^#([A-Fa-f0-9]{6})$"),
    message="Incorrect value for field: colors.icon.",
    code=AppErrorCode.INVALID.value,
)


def brand_validator(brand) -> Dict:
    missing_fields = []
    try:
        logo_url = brand["logo"]["default"]
    except (TypeError, KeyError):
        missing_fields.append("logo.default")
    try:
        icon_color = brand["colors"]["icon"]
    except (TypeError, KeyError):
        missing_fields.append("colors.icon")
    if missing_fields:
        raise ValidationError(
            "Missing required fields for brand info: " f'{", ".join(missing_fields)}.',
            code=AppErrorCode.REQUIRED.value,
        )
    image_url_validator(logo_url)
    color_string_validator(icon_color)
    return {"logo": {"default": logo_url}, "colors": {"icon": icon_color}}

from typing import Any, Dict, Optional, Union

from ..account.models import User
from ..app.models import App
from ..app.types import AppEventType
from .models import AppEvent


def _requestor(requestor: Optional[Union[App, User]]) -> Dict:
    kwargs: Dict[str, Any] = {}
    if requestor:
        if isinstance(requestor, App):
            kwargs["requestor_app"] = requestor
        elif isinstance(requestor, User):
            kwargs["requestor_user"] = requestor
    return kwargs


def event_app_installed(app: App, requestor: Optional[Union[App, User]]):
    return AppEvent.objects.create(
        app=app, type=AppEventType.INSTALLED, **_requestor(requestor)
    )


def event_app_activated(app: App, requestor: Optional[Union[App, User]]):
    return AppEvent.objects.create(
        app=app, type=AppEventType.ACTIVATED, **_requestor(requestor)
    )


def event_app_deactivated(app: App, requestor: Optional[Union[App, User]]):
    return AppEvent.objects.create(
        app=app, type=AppEventType.DEACTIVATED, **_requestor(requestor)
    )

from typing import Any, Dict, Optional, Union

from ..account.models import User
from ..app.models import App
from ..app.types import AppEventType
from .models import AppEvent


def _set_requestor(
    requestor: Optional[Union[App, User]], kwargs: Optional[Dict] = None
):
    requestor_kwargs: Dict[str, Any] = {}
    if requestor:
        if isinstance(requestor, App):
            requestor_kwargs["requestor_app"] = requestor
        elif isinstance(requestor, User):
            requestor_kwargs["requestor_user"] = requestor
    if kwargs is not None:
        kwargs.update(requestor_kwargs)
    return requestor_kwargs


def event_app_installed(app: App, requestor: Optional[Union[App, User]]):
    return AppEvent.objects.create(
        app=app, type=AppEventType.INSTALLED, **_set_requestor(requestor)
    )


def event_app_activated(app: App, requestor: Optional[Union[App, User]]):
    return AppEvent.objects.create(
        app=app, type=AppEventType.ACTIVATED, **_set_requestor(requestor)
    )


def event_app_deactivated(app: App, requestor: Optional[Union[App, User]]):
    return AppEvent.objects.create(
        app=app, type=AppEventType.DEACTIVATED, **_set_requestor(requestor)
    )

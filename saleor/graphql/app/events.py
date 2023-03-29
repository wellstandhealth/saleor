import graphene

from ...account.models import User as UserModel
from ...app.models import App as AppModel
from ..account.types import User
from ..app.types import App
from ..core import ResolveInfo


class AppEventRequestor(graphene.Union):
    class Meta:
        types = (User, App)

    @classmethod
    def resolve_type(cls, instance, info: ResolveInfo):
        if isinstance(instance, AppModel):
            return App
        if isinstance(instance, UserModel):
            return User
        return super(AppEventRequestor, cls).resolve_type(instance, info)

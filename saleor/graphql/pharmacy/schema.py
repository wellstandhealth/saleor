import graphene

from ..core import ResolveInfo
from .types import SiteSettingsType
from .mutations import SiteSettingsCreate, SiteSettingsUpdate, SiteSettingsDelete
from .resolvers import (
    resolve_site_settings_by_slug,
    resolve_all_site_settings
)
from ...core.utils import build_absolute_uri
from ...pharmacy_settings import MEDIA_URL


class SiteSettingsQueries(graphene.ObjectType):
    site_settings = graphene.Field(SiteSettingsType, slug=graphene.String())
    all_site_settings = graphene.List(SiteSettingsType)

    @staticmethod
    def resolve_site_settings(_root, _info: ResolveInfo, *, slug=None, **kwargs):
        if slug:
            site_settings = resolve_site_settings_by_slug(slug)

            site_settings.image = \
                build_absolute_uri(f"{MEDIA_URL}{site_settings.image}")
            site_settings.css = \
                build_absolute_uri(f"{MEDIA_URL}{site_settings.css}") \
                if site_settings.css else ""

            return site_settings

    @staticmethod
    def resolve_all_site_settings(_root, _info: ResolveInfo):
        all_site_settings = resolve_all_site_settings()

        for site_settings in all_site_settings:
            site_settings.image = \
                build_absolute_uri(f"{MEDIA_URL}{site_settings.image}")
            site_settings.css = \
                build_absolute_uri(f"{MEDIA_URL}{site_settings.css}") \
                    if site_settings.css else ""

        return all_site_settings


class SiteSettingsMutations(graphene.ObjectType):
    site_settings_create = SiteSettingsCreate.Field()
    site_settings_update = SiteSettingsUpdate.Field()
    site_settings_delete = SiteSettingsDelete.Field()

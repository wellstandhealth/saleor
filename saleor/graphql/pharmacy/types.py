import graphene
from graphene import relay

from ..channel.types import Channel
from ..core.types import BaseObjectType
from ...pharmacy import models


class SiteSettingsType(BaseObjectType):
    class Meta:
        description = "The customer extensions for a Site Settings object."
        interfaces = [relay.Node]
        model = models.SiteSettings

    id = graphene.ID(required=True)
    name = graphene.String(required=True)
    slug = graphene.String(required=True)
    pharmacy_name = graphene.String(required=True)
    npi = graphene.String(required=True)
    phone_number = graphene.String(required=True)
    fax_number = graphene.String(required=True)
    image = graphene.String(required=True)
    cookies_src = graphene.String(required=True)
    css = graphene.String()
    is_default = graphene.Boolean()
    domain_name = graphene.String(required=True)
    channels = graphene.List(Channel)

    @staticmethod
    def resolve_channels(root: models.SiteSettings, info):
        return root.channels.all()


class SiteSettingsList(BaseObjectType):
    edge = graphene.List(SiteSettingsType)

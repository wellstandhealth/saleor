import graphene
from graphene import relay

from ..core.types import BaseObjectType, Money
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
    is_active = graphene.Boolean()
    fill_fee_regular = graphene.Float()
    fill_fee_cold_chain = graphene.Float()
    margin_regular = graphene.Float()
    margin_cold_chain = graphene.Float()
    ship_fee_regular = graphene.Float()
    ship_fee_cold_chain = graphene.Float()


class SiteSettingsList(BaseObjectType):
    edge = graphene.List(SiteSettingsType)

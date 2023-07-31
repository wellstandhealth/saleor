import importlib
from django.apps import AppConfig
from django.db import models
from tooling.constants import EXPORT_SALEOR_MODELS


def _get_by_natural_key(self, key):
    model = self.model()
    if hasattr(model, 'slug'):
        return self.get(slug=key)

    if hasattr(model, 'uuid'):
        return self.get(uuid=key)

    raise ValueError('Undefined natural key')


def _natural_key(self):
    if hasattr(self, 'slug'):
        return (self.slug,)

    if hasattr(self, 'uuid'):
        return (self.uuid,)

    raise ValueError('Undefined natural key')


class ToolingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tooling'

    def ready(self):
        models.Manager.get_by_natural_key = _get_by_natural_key

        for model in EXPORT_SALEOR_MODELS:
            app, object_name = model.split('.')
            module = importlib.import_module('saleor.{}.models'.format(app))
            object_ = getattr(module, object_name)
            # Skip undefined natural key
            if hasattr(object_, 'slug') or hasattr(object_, 'uuid'):
                object_.natural_key = _natural_key

from django.db import models


class LowerCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCharField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.lower()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(LowerCharField, self).pre_save(model_instance, add)


class LowerEmailField(models.EmailField):
    def __init__(self, *args, **kwargs):
        super(LowerEmailField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if value:
            value = value.lower()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(LowerEmailField, self).pre_save(model_instance, add)

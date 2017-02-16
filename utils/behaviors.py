from django.db import models


class Updateable(models.Model):

    class Meta:
        abstract = True

    def update(self, data):
        for (key, value) in data.items():
            try:
                setattr(self, key, value)
            except TypeError:
                pass
        self.save()

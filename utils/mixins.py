

class UpdateableMixin():

    @classmethod
    def update_related_model(cls, related_instance, data):
        for (key, value) in data.items():
            try:
                setattr(related_instance, key, value)
            except TypeError:
                pass
        related_instance.save()

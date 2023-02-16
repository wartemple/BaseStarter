

class ModelUtils:

    @classmethod
    def get_children(cls, queryset, label_key, model):
        results = []
        for obj in queryset:
            result = {
				"value": obj.id,
				"label": getattr(obj, label_key),
			}
            if model.objects.filter(parent=obj):
                result["children"] = cls.get_children(model.objects.filter(parent=obj), label_key, model)
            results.append(result)
        return results

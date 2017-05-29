
class FilterMixin:

    def _get_truth(inp, op, cut):
        return op(inp, cut)

    @classmethod
    def filter_dicts_by_attribute(cls, dicts=None, attribute=None, value=None, operator=None):
        """
            Filter a list of dicts by comparing the attribute value with the given value
            using operator param as comparing function.
        """
        return list(
            filter(
                lambda d: cls._get_truth(
                    d.get(attribute),
                    operator,
                    value
                ),
                dicts
            )
        )

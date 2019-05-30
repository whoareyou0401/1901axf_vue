from django_filters import rest_framework as filters
from .models import Goods
class GoodsFilter(filters.FilterSet):
    typeid = filters.NumberFilter("categoryid")
    childcid = filters.NumberFilter(method="filter_childcid")
    order_rule = filters.NumberFilter(method="filter_order_rule")
    def filter_childcid(self, queryset, name, value):
        if value == 0:
            return queryset
        else:
            return queryset.filter(childcid=value)

    def filter_order_rule(self, queryset, name, value):
        if value == 0:
            return queryset.order_by("price")
        elif value == 1:
            return queryset.order_by("-price")
        elif value == 2:
            return queryset.order_by("productnum")
        elif value == 3:
            return queryset.order_by("-productnum")
        else:
            return queryset

    class Meta:
        model = Goods
        fields = ["typeid", "childcid", "order_rule"]
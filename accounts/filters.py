import django_filters
from .models import User



class UserRoleFilter(django_filters.FilterSet):
    role = django_filters.CharFilter(method='filter_role')

    class Meta:
        model = User
        fields = []

    def filter_role(self, queryset, name, value):
        if value == 'doctor':
            return queryset.filter(is_doctor=True)
        elif value == 'patient':
            return queryset.filter(is_patient=True)
        return queryset
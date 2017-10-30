from datetime import date

from django.db.models import Value
from django.db.models.functions import Coalesce
from django_filters import DateFilter, Filter, FilterSet, NumberFilter

from timed.employment import models


class YearFilter(Filter):
    """Filter to filter a queryset by year."""

    def filter(self, qs, value):
        """Filter the queryset.

        :param QuerySet qs: The queryset to filter
        :param str   value: The year to filter to
        :return:            The filtered queryset
        :rtype:             QuerySet
        """
        return qs.filter(**{
            '%s__year' % self.name: value
        })


class PublicHolidayFilterSet(FilterSet):
    """Filter set for the public holidays endpoint."""

    year      = YearFilter(name='date')
    from_date = DateFilter(name='date', lookup_expr='gte')
    to_date   = DateFilter(name='date', lookup_expr='lte')

    class Meta:
        """Meta information for the public holiday filter set."""

        model  = models.PublicHoliday
        fields = ['year', 'location', 'date', 'from_date', 'to_date']


class UserFilterSet(FilterSet):
    active = NumberFilter(name='is_active')
    supervisor = Filter(name='supervisors__id', lookup_expr='contains')

    class Meta:
        model  = models.User
        fields = ['active', 'supervisor']


class EmploymentFilterSet(FilterSet):
    date = DateFilter(method='filter_date')

    def filter_date(self, queryset, name, value):
        queryset = queryset.annotate(
            end=Coalesce('end_date', Value(date.today()))
        )

        queryset = queryset.filter(
            start_date__lte=value,
            end__gte=value
        )

        return queryset

    class Meta:
        model  = models.Employment
        fields = ['user', 'location']


class OvertimeCreditFilterSet(FilterSet):
    year      = YearFilter(name='date')
    from_date = DateFilter(name='date', lookup_expr='gte')
    to_date   = DateFilter(name='date', lookup_expr='lte')

    class Meta:
        model  = models.OvertimeCredit
        fields = ['year', 'user', 'date', 'from_date', 'to_date']


class AbsenceCreditFilterSet(FilterSet):
    year      = YearFilter(name='date')
    from_date = DateFilter(name='date', lookup_expr='gte')
    to_date   = DateFilter(name='date', lookup_expr='lte')

    class Meta:
        model  = models.AbsenceCredit
        fields = [
            'year', 'user', 'date', 'from_date', 'to_date', 'absence_type'
        ]


class WorktimeBalanceFilterSet(FilterSet):
    user = NumberFilter(name='id')
    # additional filters analyzed in WorktimeBalanceView
    # date = DateFilter()
    # last_reported_date = NumberFilter()

    class Meta:
        model  = models.User
        fields = ['user']


class AbsenceBalanceFilterSet(FilterSet):
    absence_type = NumberFilter(name='id')

    class Meta:
        model  = models.AbsenceType
        fields = ['absence_type']

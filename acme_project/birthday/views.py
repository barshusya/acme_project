from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from birthday.forms import BirthdayForm
from birthday.models import Birthday


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 8


class BirthdayMixin:
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayCreateView(BirthdayMixin, BirthdayFormMixin, CreateView):
    pass


class BirthdayUpdateView(BirthdayMixin, BirthdayFormMixin, UpdateView):
    pass


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    pass

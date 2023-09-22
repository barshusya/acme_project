from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy, reverse

from birthday.forms import BirthdayForm, CongratulationForm
from birthday.models import Birthday, Congratulation
from birthday.utils import calculate_birthday_countdown


@login_required
def simple_view(request):
    return HttpResponse('Страница для залогиненных пользователей!')


class BirthdayListView(ListView):
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags',
    ).select_related(
        'author',
    )
    ordering = 'id'
    paginate_by = 8


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class BirthdayDeleteView(LoginRequiredMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Birthday, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday  # type: ignore
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related(  # type: ignore
                'author'
            )
        )
        return context


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})

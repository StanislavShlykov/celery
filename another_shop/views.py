from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView
from board.tasks import hello

def content(request):
    return render(request, 'flatpages/main.html')

class HelloView(View):
    def get(self, request):
        hello.delay()
        return HttpResponse('Hello!')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='author').exists()
        return context
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from board.tasks import mail_new
import logging

logger_cons = logging.getLogger('django')
# logger_info = logging.getLogger('file1')

# @cache_page(100)
def content(request):

    logger_cons.info('cons_information')
    # logger_cons.error('error logger')
    return render(request, 'flatpages/main.html')

@cache_page(100)
def cat_week(request, cat_id):
    today = datetime.today()
    week = today.strftime("%V")
    catList_7 = Post.objects.filter(time_in__week=week, category=cat_id)
    return render(request, template_name='news_7.html', context={'catList_7': catList_7})


class NewsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = Post.objects.all()
    #     if self.kwargs.get('cat_id', None):
    #         return self.queryset.filter(time_in__week=week, category='cat_id')
    #     return self.queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesList(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'news_list'
    queryset = Post.objects.filter(type=True)
    template_name = 'news_list.html'


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'news - {self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news - {self.kwargs["pk"]}', obj)
        return obj


class ArticlesDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news.html'
    queryset = Post.objects.filter(type=True)
    context_object_name = 'news'


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save()
        mail_new.delay(post.pk)
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     news = Post(
    #         post_name=request.POST['post_name'],
    #         post_text=request.POST['post_text'],
    #         author=Author.objects.get(id=request.POST['author']),
    #     )
    #     news.save()
    #     category_id = request.POST.getlist('category')
    #     for cat in category_id:
    #         news.category.add(Category.objects.get(pk=cat))
    #     categories = news.category.all()
    #     mail_new(categories, news)
    #     # subs_email = []
    #     # for categ in categories:
    #     #     subs_users = categ.users.all()
    #     #     for s_users in subs_users:
    #     #         subs_email.append(s_users.email)
    #     # html_content = render_to_string('sign/hello.html', {'news': news})
    #     # send_mail(
    #     #     subject=f'новая статья {news.post_name}',
    #     #     message=None,
    #     #     from_email=DEFAULT_FROM_EMAIL,
    #     #     recipient_list=subs_email,
    #     #     html_message=html_content,
    #     #     fail_silently=True
    #     # )
    #     return super().post(request, *args, **kwargs)


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = True
        mail_new.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class NewsSearch(NewsList):
    template_name = 'news_search.html'


def sign_me(request):
    user = request.user
    category = Category.objects.get(cat_name=request.GET['category'])
    category.users.add(user)
    return HttpResponse('вы подписались!')

    # if not user in category.users:

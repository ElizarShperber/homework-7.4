from django.shortcuts import render

# Create your views here.
from newsportal.filters import PostFilter
from newsportal.forms import NewsForm
from newsportal.models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class NewsListView(ListView):
    model=Post
    template_name = 'news_all.html'
    context_object_name = 'posts'
    ordering = ['-date_time_create']
    paginate_by = 5





class NewsDetailView(DetailView):
    model = Post
    template_name = 'news_single.html'

class NewsSearchView(ListView):
    model =Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    ordering = ['-date_time_create']
    paginate_by = 5


    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
            context = super().get_context_data(**kwargs)
            context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
            return context


class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm


class NewsUpdateView(UpdateView):
    template_name = 'news_update.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
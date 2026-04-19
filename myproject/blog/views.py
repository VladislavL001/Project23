from .models import Blog
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail


class BlogListView(ListView):
    model = Blog
    context_object_name = "blogs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_blogs'] = Blog.objects.filter(is_published=True).order_by('-views_count')[:5]
        return context

    def get_queryset(self):
        return Blog.objects.filter(is_published=True)

class BlogDetailView(DetailView):
    model = Blog
    context_object_name = "blog"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            send_mail(
                subject='🎉 100 просмотров!',
                message=f'Статья "{obj.title}" набрала 100 просмотров!',
                from_email='test@example.com',
                recipient_list=['test@example.com'],
                fail_silently=True,
            )

        return obj



class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.object.pk])


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/product_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
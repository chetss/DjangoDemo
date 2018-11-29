from django.shortcuts import render
from .models import Post
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# ! mixins like decortor for class
# these are used to gaurd the page from unauthorized access.
#  we have done this kind of thing using
# ! @login_required
# decorator on the fuction

# but decorator can't be used on the classes that's why
# we are using mixins which can be applied to the class
# but mixin should be the first attribute in the class
# ! ex ->  class PostCreateView(LoginRequiredMixin, CreateView):

#  This is to display the blog/home.html which is equivalent to the
# ! class PostListView


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    #  interally call httpresponse method
    # return HttpResponse('html inside it')
    return render(request, 'blog/home.html', context)


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    #  here we are overriding form_valid method to tell django
    # ! form_valid
    #  that the author of this post is the present logged in user

    #  if you don't do this then this will give
    # ! integrityError

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

        # after succesfully creating the post we have to redirect
        # user from POSTCREATVIEW  to BLOGHOME PAGE
        # for that you can use
        # ! success_url variable

        # but here we are sending the user to that post
        # that he created by using
        # ! get_absolute_url() in the model.py file for the post


class PostListView(ListView):
    model = Post

    # * by default class view will look for this type of html page
    # * <app>/<model>_<type of view>.html
    # ! blog/post_list.html

    # ? to change the default view we will add a variable
    template_name = 'blog/home.html'
    #  'posts' will be used same in the home.html file
    #  which we mention in the template_name
    # ? posts has nothing to do with the home fuction variable
    context_object_name = 'posts'

    # for sorting the post
    ordering = ['-data_posted']
    paginate_by = 2


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    
    def test_func(self):
        post = self.get_object()
        return True if self.request.user == post.author else False

    # here we have to define the success_url method because 
    # get_abus_path() fun will not be working because that fucntion 
    # is directing you to the particular post with the id
    # but after deleting that particular post will no longer 
    # will be there
    success_url = '/'    
    
def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

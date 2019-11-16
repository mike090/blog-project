from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.mail import send_mail

from . import models
from . import forms

# Create your views here.

def post_share(request, post_id):
	post = get_object_or_404(models.Post, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
		form = forms.EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True

	else:
		form = forms.EmailPostForm()
	
	return render(request,'blog/post_share.html', {'form': form, 'post': post, 'sent': sent}) 


class PostListView(generic.ListView):
	model = models.Post
	paginate_by = 3

	def get_queryset(self):
		return models.Post.objects.filter(status='published')

class PostDetailView(generic.DetailView,):
	
	def get_object(self):
		return models.Post.objects.get(slug = self.kwargs['post'],
			publish__year = self.kwargs['year'],
			publish__month = self.kwargs['month'],
			publish__day = self.kwargs['day']
		)
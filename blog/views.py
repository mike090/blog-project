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
	
	context_object_name = 'post'

	def setup(self, request, *args, **kwargs):
		super().setup(request, *args, **kwargs)
		
		if request.method == 'POST':
			self.comment_form = forms.CommentForm(data=self.request.POST)
		else:
			self.comment_form = forms.CommentForm()

		self.blog_post = get_object_or_404(models.Post,
			slug = kwargs['post'],
			status = 'published',
			publish__year = kwargs['year'],
			publish__month = kwargs['month'],
			publish__day = kwargs['day']
		)

		self.new_comment = None
		self.comments = self.blog_post.comments.filter(active=True)

	def get_object(self):
		return self.blog_post
	
	def get_context_data(self, **kwargs):
		
		context = super().get_context_data(**kwargs)
		context.update({
			'comments': self.comments,
			'new_comment': self.new_comment,
			'comment_form': self.comment_form
		})
		return context

	
	def post(self, request, *args, **kwargs):
		if self.comment_form.is_valid():
			self.new_comment = self.comment_form.save(commit=False)
			self.new_comment.post = self.blog_post
			self.new_comment.save()
#			self.new_comment = True
			self.comment_form.full_clean()
		return super().get(request, *args, **kwargs)
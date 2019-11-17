from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetailView.as_view(), name='post-detail'),
	path('', views.PostListView.as_view(), name='post-list'),
	path('<int:post_id>/share/', views.post_share, name='post-share'),
]

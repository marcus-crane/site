from django.utils import timezone
from django.views import generic

from .models import Review

class ReviewView(generic.ListView):
  template_name = 'reviews/list.html'
  context_object_name = 'reviews'

  def get_queryset(self):
    """ Fetch only published posts, and order by descending date """
    return Review.objects.filter(date__lte=timezone.now()).order_by('-date')

class ReviewDetailView(generic.DetailView):
	template_name = 'reviews/detail.html'
	model = Review

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['book_list'] = Review.objects.all()
		return context
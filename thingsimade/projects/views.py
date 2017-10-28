from django.utils import timezone
from django.views import generic

from .models import Project

class ProjectView(generic.ListView):
  template_name = 'projects/list.html'
  context_object_name = 'projects'

  def get_queryset(self):
    """ Order posts by date in descending order. """
    return Project.objects.all()

class ProjectDetailView(generic.DetailView):
  model = Project
  template_name = 'project/detail.html'
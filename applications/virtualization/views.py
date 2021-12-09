from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Tenant, Todo, VM
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
import datetime
from django.db.models.functions import Round
from django.db.models import Count
from django.db.models.functions.comparison import NullIf
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class projects(ListView):
    model = Project
    template_name = 'projectlist.html'
    ordering = ['project_title']
    paginate_by = 10

    queryset = Project.objects.annotate(
        todo_done=Round(Count('todo', filter=Q(todo__state=True)) * 100.0 / NullIf(Count('todo'), 0)),
        todo_left=Round(Count('todo', filter=Q(todo__state=False)) * 100.0 / NullIf(Count('todo'), 0)),
    )

    def get_queryset(self, *args, **kwargs):
        context = super().get_queryset(*args, **kwargs)
        search = self.request.GET.get('buscar', None)

        if search:
            context = context.filter(
				Q(project_title__icontains = search) |
				Q(resume__icontains = search) |
                Q(provider__provider_name__icontains = search)
			).distinct()
        return context

class projectdetail(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projectdetail.html'
    slug_field = 'slug'

    def get_context_data(self, *args, **kwargs):
        context = super(projectdetail, self).get_context_data(**kwargs)

        '''Rescatar todos las tareas del pryecto'''
        project = self.get_object()
        progress_field = project.todo_set.all()
        '''Listar el campo progress'''
        progress = []
        for todos in progress_field:
            progress.append(todos.progress)
        '''eliminar los NoneType de la lista'''
        progress_not_none = [x for x in progress if x is not None]
        '''Sumar la lista'''
        sum_progress = 0
        for num in progress_not_none:
            sum_progress += num
        ''''''

        if Todo.objects.filter(project=self.object).count() == 0:
            return context
        else:
            if Todo.objects.filter(project=self.object).filter(state=True).count() * 100 / Todo.objects.filter(
                    project=self.object).count() != 100:
                project.state = False
                project.save()
            else:
                project.state = True
                project.save()
        context['get_percentage_done'] = Todo.objects.filter(project=self.object).filter(
            state=True).count() * 100 / Todo.objects.filter(project=self.object).count()
        context['get_percentage_left'] = Todo.objects.filter(project=self.object).filter(
            state=False).count() * 100 / Todo.objects.filter(project=self.object).count()
        context['progress'] = sum_progress
        context['left_progress'] = 100 - sum_progress
        context['todo_done'] = Todo.objects.filter(project=self.object).filter(state=True).count()
        context['todo_total'] = Todo.objects.filter(project=self.object).all().count()

        return context

class hypervisor(ListView):
    model = Tenant
    template_name = 'hypervisorlist.html'
    ordering = ['tenant_hostname']
    # paginate_by = 10

class vm(ListView):
    model = VM
    template_name = 'vmlist.html'
    ordering = ['vm_name']

def todofinished(request, id):
    todo = get_object_or_404(Todo, id=id)

    todo.state = True
    todo.done_date = datetime.date.today()
    todo.save()

    project = todo.project
    all_todo = project.todo_set.all()
    done_todo = all_todo.filter(state=True).count() * 100 / all_todo.count()
    if done_todo == 100:
        project.state = True
        project.done_date = datetime.date.today()
        project.save()
        messages.add_message(request, messages.INFO,
                             'Excelente, has finalizado este proyecto ')
    else:
        project.state = False
        project.save()
    # print(done_todo)

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

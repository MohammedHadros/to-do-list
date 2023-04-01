from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import(ListView,CreateView,UpdateView,DeleteView)
from .models import List,Task
from django.contrib import messages

# Create your views here.

class ListListView(ListView):
    model=List
    queryset = List.objects.all().order_by("-created_at")
    template_name="todo_app/all_list.html"

class ListCreateView(CreateView):
    model=List
    fields = ["title"]
    success_url = reverse_lazy("list-create")
    def get_context_data(self):
        context = super(ListCreateView, self).get_context_data()
        context["title"] = "Add a new list"
        return context

class UpdateList(ListCreateView,UpdateView):
    # slug_field = 'product_slug'
    # slug_url_list_id = 'product_slug'
    def get_success_url(self):
        return reverse("list-task", args=[self.object.pk])
    def form_valid(self, form):
        messages.success(self.request, "The List was updated successfully.")
        return super(UpdateList,self).form_valid(form)
    
class DeleteListView(DeleteView):
    model:List
    slug_field = 'product_slug'
    template_name="todo_app/list_confirm_delete.html"
    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs["pk"])
    
    def get_success_url(self):
        return reverse("all_list")
    

def delete_List_view(request, pk):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(List, pk = pk)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    return render(request, "todo_app/list_confirm_delete.html", context)


class ItemListView(ListView):
    model=Task
    def get_queryset(self):
        return Task.objects.filter(list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context=super().get_context_data()
        context["List"]=List.objects.get(id=self.kwargs["list_id"])
        return context


class CreateTask(CreateView):
    model=Task
    fields=["list",
        "title",
        "description",
        "due_date"]
    # success_url = reverse_lazy("task-add") -->error -->Reverse for 'task-add' with no arguments not found
    

    def get_initial(self):
        initial_data = super(CreateTask, self).get_initial()
        todo_list = List.objects.get(id=self.kwargs["list_id"])
        initial_data["list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(CreateTask, self).get_context_data()
        todo_list = List.objects.get(id=self.kwargs["list_id"])
        context["list"] = todo_list
        context["title"] = "Create a new item"
        return context
        
    def get_success_url(self):
        return reverse("list-task", args=[self.object.list_id])



def taskView(request,list_id,task_id):
    task =Task.objects.get(pk=task_id)
    list=List.objects.get(pk=list_id)
    context={
        'task':task,
        'list':list
    }
    return render(request , "todo_app/task.html" , context)

class TaskUpdateView(CreateTask,UpdateView):
    def get_success_url(self):
        return reverse("task-details", args=[self.object.list_id ,self.object.id ])

class DeleteTask(DeleteView):
    model=Task
    slug_field = 'product_slug'
    def get_success_url(self):
        return reverse("list-task", args=[self.object.list_id])

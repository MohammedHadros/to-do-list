from django.urls import path
from . import views
from .views import UpdateList



urlpatterns = [
    path("" , views.ListListView.as_view(),name="all_list"),
    path("new" , views.ListCreateView.as_view(),name="list-create"),
    path("list/<int:list_id>/" , views.ItemListView.as_view(),name="list-task"),
    path("list/<int:pk>/edit/" , UpdateList.as_view(),name="list-update"),
    path("list/<int:pk>/delete/" , views.delete_List_view,name="list-delete"),
    path("list/<int:list_id>/task/<int:task_id>" , views.taskView,name="task-details"),
    path("list/<int:list_id>/task/add/",views.CreateTask.as_view(),name="task-add",),
    path("list/<int:list_id>/task/edit/<int:pk>/",views.TaskUpdateView.as_view(),
            name="task-edit"),
    path("list/<int:list_id>/task/delete/<int:pk>/",views.DeleteTask.as_view(),
        name="task-delete"),

]
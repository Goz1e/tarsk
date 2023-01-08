from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from native_auth.models import MyUser, Profile
from .forms import AddCommentForm,TaskCreateForm, TaskUpdateForm
from .models import Comment, Dependencies, Task
from django.db.models import Q
from django.contrib import messages
# Create your views here.

@login_required(login_url='native_auth:landing_page')
def dashboard(request):
    user = request.user
    user_tasks = Task.objects.user_tasks(user=user)
    active_tasks = Task.objects.active_tasks(user) or None
    completed_tasks = Task.objects.completed_tasks(user) or None
    user_collabs = user.collabs.all()
    collaborations = (active_tasks|user_collabs).distinct().exclude(user=user)
    print(collaborations)
    template_name = 'task/dashboard.html' 
    context = {'title':'dashboard','active_tasks':active_tasks,
    'completed_tasks':completed_tasks,'collaborations':collaborations,'dashboard':'true'}
    return render(request,template_name,context)


@login_required(login_url='native_auth:landing_page')
def create_task(request):
    user = request.user
    form = TaskCreateForm

    if request.POST:
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            form.save_m2m()
            messages.success(request,'task created successfully')
            return redirect('task:dashboard')

    context = {'title':'create','create_form':form}
    template_name = 'task/create_task.html' 

    return render(request,template_name,context)


@login_required(login_url='native_auth:landing_page')
def detail(request,slug):

    task = get_object_or_404(Task,slug=slug)
    comments = Comment.objects.filter(task=task)

    form = AddCommentForm(request.POST or None, instance=task)

    qs = MyUser.objects.all()

    task_collabs = task.collaborators.all().exclude(pk=task.user.pk)
    dep_qs = Task.objects.filter(slug=task.slug)
    task_dep = task.my_dependencies.dependent_on.all()
    
    context = {'title':f'detail | {task.title}','task':task,'comments':comments,
    'qs':qs,'comment_form':form, 'collabs':task_collabs,
    'dep_qs':dep_qs, 'task_dep':task_dep
    }
    if not task_collabs.exists():
        context['no_collab']='no_collab'
    if not task_dep.exists():
        context['no_dep']='no_dep'
        
    try:
        task_qs = Task.objects.filter(slug = task.slug)
        dep = task.my_dependencies
        dep_qs = dep.dependent_on.exclude(pk__in=task_qs)

        context['dep_qs']=dep_qs
    except:
        pass

    template_name = 'task/detail.html'
    return render(request,template_name,context)


@login_required(login_url='native_auth:landing_page')
def update(request,slug):
    
    context = {}
    task = get_object_or_404(Task,slug=slug)
    form = TaskUpdateForm(request.POST or None, instance=task)

    qs = MyUser.objects.all()
    
    if request.POST:
        
        if form.is_valid():
            task=form.save(commit=False)
            task.user = request.user
            task.edited = True
            task.save()
            form.save_m2m()
            
            return redirect('task:detail',slug=task.slug)

    context = {
        'title': f'update-{task.title}', 'task':task, 'update_form':form,
        'qs':qs
    }
    
    template_name = 'task/update.html' 

    return render(request,template_name,context)


@login_required(login_url='native_auth:landing_page')
def update_dependencies(request,slug):    
    
    if request.POST:
        task = get_object_or_404(Task,slug=slug)
        dep = get_object_or_404(Dependencies,main_task=task)
        dep_form = DependenciesForm(request.POST or None, instance=dep)

        if dep_form.is_valid():
            dependency = dep_form.save(commit=False)
            dependency.save()
            dep_form.save_m2m()
            return redirect('task:detail',slug=slug)


@login_required(login_url='native_auth:landing_page')
def update_collab(request,slug):
    
    if request.POST:
        task = get_object_or_404(Task,slug=slug)
        collab = task.collaborators
        if 'collab_add_form' in request.POST:
            collab_add = request.POST.get('collab_add_form')
            try:
                profile = get_object_or_404(Profile,first_name = collab_add)
                user = profile.user
                if user in collab.all():
                    messages.warning(request, f" adding '{user.profile.first_name}' failed ")  
                else:  
                    collab.add(user)
                    messages.success(request, f"'{user.profile.first_name}' added successfully")

            except:
                messages.info(request, f"'{collab_add}' does not match an existing users")
            
        # else:
        #     collab_form = CollabForm(request.POST,instance=collab)
        #     if collab_form.is_valid():
        #         collab_form.save()
            
        return redirect('task:detail',slug=slug)


@login_required(login_url='native_auth:landing_page')
def completed(request,slug):
    
    obj = get_object_or_404(Task,slug=slug)
    obj.completed = True
    obj.save() 
    return redirect('task:detail',slug=obj.slug)


@login_required(login_url='native_auth:landing_page')
def add_comment(request,slug):
    obj = get_object_or_404(Task,slug=slug)
    form = AddCommentForm

    if request.POST:
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = obj
            comment.save()
            
            return redirect('task:detail',slug=slug)

    

@login_required(login_url='native_auth:landing_page')
def search(request):
    query = request.GET.get('q')
    qs = Task.objects.all()

    if query:
        lookups = Q(title__icontains = query) | Q(description__icontains = query) | Q(slug__icontains = query)
        qs = Task.objects.filter(lookups).distinct()

    context = {'search_qs':qs, 'title':f'search for {query}', 'query':query}
    if not qs.exists():
        context['no_qs'] = 'no_qs'
    template_name = 'task/search.html'
    return render(request,template_name,context)


@login_required(login_url='native_auth:landing_page')
def delete_task(request,slug):
    task = get_object_or_404(Task,slug=slug)
    if task.user == request.user:
        task.delete()
    else:
        messages.info(request, "you don't have permission to delete this task")
        redirect('task:detail', slug = task.slug)
    return redirect('task:dashboard')

def delete_comment(request,id):
    comment = get_object_or_404(Comment,id=id)
    if request.user == comment.task.user or comment.author:
        comment.delete()
    else:
        messages.info(request, "you don't have permission to delete this comment")
    return redirect('task:detail',slug=comment.task.slug)

def remove_collab(request,slug,user_id,dashboard='true'or None):
    user = get_object_or_404(MyUser,id=user_id)
    task = get_object_or_404(Task,slug=slug)
    task.collaborators.remove(user)
    if dashboard == 'true':
        return redirect('task:dashboard')
    return redirect('task:detail',slug=slug)


@login_required(login_url='native_auth:landing_page')
def update_dep(request,slug):
    
    if request.POST:
        task = get_object_or_404(Task,slug=slug)
        dependency = task.my_dependencies

        try:
            dep_task = get_object_or_404(Task,title=request.POST.get('dep_form'))
            if dep_task == task:
                dep_task = None
                messages.info(request, "you cannot add current task as dependency")
                return redirect('task:detail',slug=slug)

            if dep_task in dependency.dependent_on.all():
                messages.success(request, f"'{dep_task}' already exists")  
            else:  
                dependency.dependent_on.add(dep_task)
                messages.success(request, "dependency added successfully")
        except:
            
            messages.success(request, f"failed to add to dependencies")  

    
        return redirect('task:detail',slug=slug)

def remove_dep(request,slug,dep_id):
    dep_task = get_object_or_404(Task,id=dep_id)
    task = get_object_or_404(Task,slug=slug)
    task.my_dependencies.dependent_on.remove(dep_task)
    return redirect('task:detail',slug=slug)

def test(request):
    template_name = 'task/test.html'
    context = {'title':'test'}
    return render(request,template_name,context)
from django.shortcuts import render, redirect, get_object_or_404
from groups.models import Group
from groups.forms import GroupForm
from django.contrib.auth. decorators import login_required

def cerate_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            form.save_m2m()
            return redirect('group_detail', pk=group.pk)
    else:
        form = GroupForm()
        return render(request, 'groups/create_group.html', {'form':form})


def group_lis(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups':groups})

def manage_group(request, pk):
    group = get_object_or_404(Group, id=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_detail', pk = group.pk)
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/manage_group.html', {'form':form})

@login_required
def join_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.members.add(request.user)
    return redirect('group_detail', pk=pk)

def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'groups/group_detail.html', {'group':group})
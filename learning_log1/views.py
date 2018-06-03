from django.shortcuts import render
from .models import Topic,Entry
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    context ={}
    return  render(request,'learning_log1/index.html',context)
@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries= topic.entry_set.order_by('-date_add')
    context = {'topic':topic,'entries':entries}
    return render(request,'learning_log1/topic.html',context)
@login_required
def topics(request):
    topics = Topic.objects.filter(owner= request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_log1/topics.html',context)
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_log1:topics'))
    context = {'form': form}
    return render(request,'learning_log1/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if request.method !='POST':
        form=EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic =topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_log1:topic',args=[topic_id]))
    context = {'topic':topic,'form':form}
    return render(request,'learning_log1/new_entry.html',context)
@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method !='POST':
        form =EntryForm(instance=entry)
    else :
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_log1:topic',
                                                args=[topic.id]))
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_log1/edit_entry.html',context)


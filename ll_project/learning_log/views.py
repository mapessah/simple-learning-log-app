from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404

def index(request):
    # returns the homepage
    return render(request, 'learning_log/index.html')

@login_required
def topics(request):
    # fetch topics belonging to the user, sorted by date added
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    # assemble the required data
    context = {'topics': topics}
    # return data and topics template
    return render(request, 'learning_log/topics.html', context)

@login_required
def topic(request, topic_id):
    # fetch topic and all its entries
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    # raise error if user isn't the owner
    if request.user != topic.owner:
        raise Http404
    
    # Assemble the data required and return it with the topic template
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_log/topic.html', context)

@login_required
def new_topic(request):
    # adding a new topic
    if request.method != 'POST':
        # create a new empty form
        form = TopicForm()
    else:
        # process the data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.owner = request.user
            new.save()
            return redirect('learning_log:topics')
    
    # assemble data and return it with template
    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # raise error if user isn't the owner
    if request.user != topic.owner:
        raise Http404
    
    if request.method != 'POST':
        # new blank form
        form = EntryForm()
    else:
        # process the data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.topic = topic
            new.save()
            return redirect('learning_log:topic', topic_id=topic.id)
    
    # assemble data and return 
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_log/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    # edit an entry
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    # raise error if user isn't owner
    if request.user != topic.owner:
        raise Http404
    
    if request.method != 'POST':
        # prefill form with current data
        form = EntryForm(instance=entry)
    else:
        # process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_log:topic', topic_id=topic.id)
        
    # assemble data and return data + template
    context = {'form': form, 'entry': entry, 'topic': topic}
    return render(request, 'learning_log/edit_entry.html', context)
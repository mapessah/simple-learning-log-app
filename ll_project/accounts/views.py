from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    '''Register a new user'''
    if request.method != 'POST':
        # create an empty form
        form = UserCreationForm()
        
    else:
        # process data
        form = UserCreationForm(data=request.POST)
        # validate the data
        if form.is_valid():
            new_user = form.save() # save the new user
            login(request, new_user) # log in to the users account
            return redirect('learning_log:index') # redirect to Homepage
        
    # assemble the needed data into context dictionary
    context = {'form': form}
    # return the context(data) and the html template for registration
    return render(request, 'registration/register.html', context)
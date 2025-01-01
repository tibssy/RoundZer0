from django.shortcuts import render

# Create your views here.
def jobs_index(request):
    return render(request, 'jobposts/index.html')

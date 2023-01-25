from django.shortcuts import render

# Create your views here.
def index(request):

    print('entering index')
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'pages/index.html')

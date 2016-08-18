from django.shortcuts import render
from django.views.decorators import csrf

def file_format(request,file):
    file_name=str(file)
    if not file_name.endswith('.csv'):
        return render(request, 'simulator/error.html')

# Create your views here.
def home(request):
    return render(request, 'simulator/home.html')

def tools(request):
    return render(request, 'simulator/tools.html')

def result(request):
    if request.method=="GET":
        return render(request, 'simulator/result.html')
    else:
        try:
            # upload data
            up_file=request.FILES["upfile"]
            # verified upload file format
            if not up_file.str(up_file).endswith('.csv'):
                raise NameError
            # type regression function
            type_of_f=request.POST["types"]
            # name of x_axis
            x_axis=request.POST["x_axis"]
            # name of y_axis
            y_axis=request.POST["y_axis"]
        except:
            return render(request, 'simulator/error.html')
        return render(request, 'simulator/example_result.html')

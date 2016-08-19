from django.shortcuts import render
from simu import fit_models



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
            # type of regression function
            type_of_f=str(request.POST["types"])
            # read content(x,y) within the upload file            
            x, y = read_file(upfile)
            # fit to simulation object
            fit = fit_models(y,x)
            if type_of_f=="1":
                # execute linear regression
                fit.linear_regression()
            elif type_of_f=='2':
                # execute polynomial regression up to power 3
                fit.polynomial_regression()
            elif type_of_f=='3':
                fit.sigmoid_regression()
            else:
                raise ValueError
                      
            # name of x_axis
            x_axis=request.POST["x_axis"]
            # name of y_axis
            y_axis=request.POST["y_axis"]
            html=generate_result(fit)  
        except:
            return render(request, 'simulator/error.html')
        return render(request, 'simulator/example_result.html')







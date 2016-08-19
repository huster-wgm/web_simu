from django.shortcuts import render
from .simu import fit_models,generate_result
import pandas as pd

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
    print("step 0")
    if request.method=="GET":
        return render(request, 'simulator/result.html')
    else:
        try:
            # upload data
            up_file=request.FILES["upfile"]
            # verified upload file format
            if not up_file.name.endswith('.csv'):
                print("step 1")
                raise NameError
            else:
                df=pd.read_csv(up_file)
                x = df.ix[:,0].values
                y = df.ix[:,1].values
                del df,up_file
                print("step 2")
            # type of regression function
            type_of_f=str(request.POST["types"])
            # fit to simulation object
            fit = fit_models(y,x)
            print("step 3")
            if type_of_f=="1":
                # execute linear regression
                fit.linear_regression()
            elif type_of_f=='2':
                # execute polynomial regression up to power 3
                fit.polynomial_regression()
            elif type_of_f=='3':
                fit.sigmoid_regression()
            elif type_of_f=='4':
                fit=fit.all_regression()
            else:
                raise ValueError 
            # name of x_axis
            x_axis=request.POST["x_axis"]
            # name of y_axis
            y_axis=request.POST["y_axis"]
            print("step 4")
            generate_result(fit, x_axis, y_axis)
            print ("run well!")
        except:
            return render(request, 'simulator/error.html')
        return render(request, 'simulator/home.html')

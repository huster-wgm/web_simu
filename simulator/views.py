from .simu import fit_models,generate_result
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np

def file_format(request,file):
    file_name=str(file)
    if not file_name.endswith('.csv'):
        return render(request, 'simulator/error.html')
def forms(request):
    return render(request, 'simulator/forms.html')

# Create your views here.
def home(request):
    return render(request, 'simulator/home.html')

def tools(request):
    return render(request, 'simulator/tools.html')

def result(request):
    print ("step 0")
    if request.method=="GET":
        print ("step 1")
        return render(request, 'simulator/empty_result.html')
    else:
        try:
            file_address="https://docs.google.com/spreadsheets/d/1dKGnbgr0ld1Ny17b-vN81Rubt3_cwpqcT3-9V5QqbjE/pub?gid=0&single=true&output=csv"
            df=pd.read_csv(file_address,header=None)
            print ("step 3")
            #number of NAN 
            null_rows=sum(df.iloc[:,-1].isnull())
            null_cols=sum(df.iloc[-1,:].isnull())
            print ("step 4")
            # remove NAN and header
            df=df.iloc[null_rows+1:,null_cols:]
            print ("step 5")
            # assign values to x and y
            x=np.array(df.iloc[:,0].values,dtype="int8")
            y=np.array(df.iloc[:,1].values,dtype="float16")
            # type of regression function
            type_of_f=str(request.POST["types"])
            # fit to simulation object
            fit = fit_models(y,x)
            print("step 7")
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

            # generate result and write into 'simulator/result.html'
            html=generate_result(fit, request)
            return HttpResponse(html)
        except:
            return render(request, 'simulator/error.html')


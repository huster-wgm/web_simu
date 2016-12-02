from .simu import fit_models,generate_result
from .bio_calc import Bio_calculator, Create_freq_map
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

def simulator(request):
    return render(request, 'simulator/simulator.html')

# return result of simulator   
def simu_result(request):
    if request.method=="GET":
        print ("request method == 'GET'")
        return render(request, 'simulator/empty_result.html')
    else:
        try:
            print("Start reading csv")
            address="https://docs.google.com/spreadsheets/d/1dKGnbgr0ld1Ny17b-vN81Rubt3_cwpqcT3-9V5QqbjE/pub?gid=0&single=true&output=csv"
            df=pd.read_csv(address,header=None)
            print ("step 0, pandas read_csv")
            print (df)
            #number of NAN 
            null_rows=sum(df.iloc[:,-1].isnull())
            null_cols=sum(df.iloc[-1,:].isnull())
            print ("step 1, %d null_rows, %d null_cols" %(null_rows,null_cols))
            # remove NAN and header
            df=df.iloc[null_rows+1:,null_cols:]
            print ("step 2, removed header : \n",df)
            # assign values to x and y
            x=np.array(df.iloc[:,0].values,dtype="int8")
            y=np.array(df.iloc[:,1].values,dtype="float16")
            # type of regression function
            type_of_f=str(request.POST["types"])
            # fit to simulation object
            fit = fit_models(y,x)
            print("step 3, fitting")
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


def bio_calculator(request):
    return render(request, 'simulator/bio_calculators.html')

# return result of bio_calculators
def bio_result(request):
    # using DNA calculator
    refer_freq = {}
    # initial gc_reduce
    gc_reduce = False
    if request.POST['submit']=='DNA_Calc':
        seq_type = request.POST["seq_type"]
        seq = request.POST['seq']
        if request.POST['gc_reduce'] == 'yes':
            gc_reduce = True
        measure_con = False
        # create calculator objects
        if request.POST['codon_ref'] == 'K12':
            path = 'https://docs.google.com/spreadsheets/d/1PaitzLRv3VIR0lTuI86eFLwzupdZpYwY8VPBaAS0WJc/pub?gid=0&single=true&output=csv'
            
        elif request.POST['codon_ref'] == 'yeast':
            path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTkB4PueNxiKl548CC39uFHBtEbSm4FA75l4bDTyAQlM7FmoOoPRGsbJFogcSgQWzKbQeqGx5sE74-Q/pub?gid=0&single=true&output=csv'
        else:
            path = None
        if path:
            refer_freq = dict(pd.read_csv(path).values)
        calc = Bio_calculator(seq, seq_type, refer_freq)
    # using Protein concentration calculator
    else:
        seq_type = request.POST["seq_type_2"]
        seq = request.POST['seq_2']
        measure_con = True
        # create calculator objects
        calc = Bio_calculator(seq, seq_type, refer_freq)        
        width = float(request.POST['width'])
        a_280 = float(request.POST['a_280'])
        dilution = float(request.POST['dilution'])
        
    calc.DNA_calculator()
    calc.Protein_calculator()
    if measure_con:
        calc.Protein_con(width, a_280, dilution)
    if gc_reduce:
        calc.Codon_optimize()
    if calc.refer_freq:
        data = pd.DataFrame(calc.freq_to_refer,
                            columns=['Amino', 'codon', 'freq', 'optimal_codon', 'optimal_freq'])
        script, div = Create_freq_map(data)
        context = {'calc': calc,'script':script,'div':div}
    else:
        context = {'calc': calc}

    return render(request, 'simulator/calc_result.html',context)

from .simu import FitModels, generate_result
from .bio_calc import BioCalculator, create_freq_map
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd


def file_format(request, file):
    file_name = str(file)
    if not file_name.endswith('.csv'):
        return render(request, 'simulator/error.html')


def forms(request):
    return render(request, 'simulator/forms.html')


def simulator(request):
    return render(request, 'simulator/simulator.html')


# return result of simulator
def simulation_result(request):
    if request.method == "GET":
        print("request method == 'GET'")
        return render(request, 'simulator/error.html')
    else:
        '''
        # read personal data from upload csv file
        print("Start reading csv")
        up_file = request.FILES["upfile"]
        # verified upload file format
        if not up_file.name.endswith('.csv'):
            raise NameError
        else:
            df = pd.read_csv(up_file, header=None)
            print(df.shape, df)
            # number of NAN
            null_rows = sum(df.iloc[:, -1].isnull())
            null_cols = sum(df.iloc[-1, :].isnull())
            print("step 1, %d null_rows, %d null_cols" % (null_rows, null_cols))
            # remove NAN and header
            df = df.iloc[null_rows + 1:, null_cols:]
            print("step 2, removed header.")
            # assign values to x and y
            x = np.array(df.iloc[:, 0].values, dtype="float16")
            y = np.array(df.iloc[:, 1].values, dtype="float16")
        '''
        standard = request.POST['standard'].strip('\r')
        unknown = request.POST['unknown'].strip('\r')
        print('start handling upload data')
        # change string to list
        standard = standard.replace("\r", "").split('\n')
        unknown = unknown.replace("\r", "").split('\n')
        print('type of standard and unknown', type(standard), type(unknown))
        print(standard, unknown)
        standard_x, standard_y = [], []
        for i in standard:
            if i:
                data_set = i.split('\t')
                if data_set[0] and data_set[1]:
                    x_val = float(data_set[0])
                    y_val = float(data_set[1])
                    standard_x.append(x_val)
                    standard_y.append(y_val)
                else:
                    # avoid input only x or y
                    continue
            else:
                # avoid empty line
                continue
        # print(standard_x, standard_y)
        unknown_y = []
        for j in unknown:
            if j:
                unknown_y.append(float(j))
            else:
                continue
        # print(standard.shape, unknown.shape)
        # type of regression function
        type_of_f = str(request.POST["types"])

        print("step 3, fitting")
        if type_of_f == "1":
            # execute linear regression
            # fit to simulation object
            fit = FitModels(standard_y, standard_x)
            fit = fit.linear_regression()
            fit.predict_unknown(unknown_y)
        elif type_of_f == '2':
            # execute polynomial regression up to power 3
            fit = FitModels(standard_y, standard_x)
            fit = fit.polynomial_regression()
            fit.predict_unknown(unknown_y)
        elif type_of_f == '3':
            fit = FitModels(standard_y, standard_x)
            fit = fit.sigmoid_regression()
            fit.predict_unknown(unknown_y)
        elif type_of_f == '4':
            fit = FitModels(standard_y, standard_x)
            fit = fit.all_regression()
            fit.predict_unknown(unknown_y)
        else:
            raise ValueError
        # generate result and write into 'simulator/result.html'
        print('fitting is ok!')
        html = generate_result(fit, request)
        print('succeed in generating html.')
        print(fit.predict_x)
        return HttpResponse(html)


def bio_calculator(request):
    return render(request, 'simulator/bio_calculators.html')


# return result of bio_calculators
def bio_result(request):
    # using DNA calculator
    refer_freq = {}
    # initial optimized
    optimized = False
    if request.POST['submit'] == 'DNA_Calc':
        seq_type = request.POST["seq_type"]
        seq = request.POST['seq']
        if request.POST['optimized'] != 'no':
            optimized = True
            optimized_method = request.POST['optimized']
        measure_con = False
        # create calculator objects
        if request.POST['codon_ref'] == 'K12':
            path = 'https://docs.google.com/spreadsheets/d/1PaitzLRv3VIR0lTuI86eFLwzupdZpYwY8VPBaAS0WJc/pub?gid=0' \
                   '&single=true&output=csv '

        elif request.POST['codon_ref'] == 'yeast':
            path = 'https://docs.google.com/spreadsheets/d/e/2PACX' \
                   '-1vTkB4PueNxiKl548CC39uFHBtEbSm4FA75l4bDTyAQlM7FmoOoPRGsbJFogcSgQWzKbQeqGx5sE74-Q/pub?gid=0' \
                   '&single=true&output=csv '
        else:
            path = None
        if path:
            refer_freq = dict(pd.read_csv(path).values)
        calc = BioCalculator(seq, seq_type, refer_freq)
    # using Protein concentration calculator
    else:
        seq_type = request.POST["seq_type_2"]
        seq = request.POST['seq_2']
        measure_con = True
        # create calculator objects
        calc = BioCalculator(seq, seq_type, refer_freq)
        width = float(request.POST['width'])
        a_280 = float(request.POST['a_280'])
        dilution = float(request.POST['dilution'])

    calc.dna_calculator()
    calc.protein_calculator()
    if measure_con:
        calc.protein_con(width, a_280, dilution)
    if optimized:
        calc.codon_optimize(optimized_method)
    if calc.refer_freq:
        data = pd.DataFrame(calc.freq_to_refer,
                            columns=['Amino', 'codon', 'freq', 'optimal_codon', 'optimal_freq'])
        script, div = create_freq_map(data)
        context = {'calc': calc, 'script': script, 'div': div}
    else:
        context = {'calc': calc}

    return render(request, 'simulator/calc_result.html', context)

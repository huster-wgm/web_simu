import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
from bokeh.plotting import figure
from bokeh.embed import components
from pynverse import inversefunc


# def linear function
def simu_linear(var_x, a, b):
    var_x = np.array(var_x)
    return a + (b * var_x)


# def quadratic function
def simu_quadratic(var_x, a, b, c):
    var_x = np.array(var_x)
    return a + (b * var_x) + (c * var_x ** 2)


# def polynomial function at ^3
def simu_poly(var_x, a, b, c, d):
    var_x = np.array(var_x)
    return a + (b * var_x) + (c * var_x ** 2) + (d * var_x ** 3)


# def power function
def simu_power(var_x, a, b, c):
    var_x = np.array(var_x)
    return a + b * np.power(var_x, c)


# def exponential function
def simu_exponential(var_x, a, b):
    var_x = np.array(var_x)
    return a * np.exp(var_x) + b


# def Logarithmic functions
def simu_logarithmic(var_x, a, b):
    var_x = np.array(var_x)
    return a * np.log(var_x) + b


# make simulation base on y_minus
def simu_sigmoid(var_x, a, b, c):
    var_x = np.array(var_x)
    return a / (1 + np.exp(-b * (var_x + c)))


# calculate statistic parameters
def fit_parameters(actual_y, fit_y):
    # find nan values and infinite values in predict y
    nb_nan = sum(np.isnan(fit_y))
    nb_inf = sum(np.isinf(fit_y))
    if nb_nan < 1 and nb_inf < 1:
        # calculate mean square error
        m_s_e = round(mean_squared_error(actual_y, fit_y), 3)
        # calculate coefficient of determination or R^2
        total_variance = sum(np.power(actual_y - np.mean(actual_y), 2))
        predict_variance = sum(np.power(fit_y - np.mean(actual_y), 2))
        r_square = round(predict_variance / total_variance, 3)
        return m_s_e, r_square
    else:
        return np.inf, 0


class FitModels:
    def __init__(self, y, x):
        # assert len of input x and y
        assert len(y) == len(x), 'Number of x and y should be equal'
        # initialize x, y and unknown_y
        self.y = np.round(y, 3)
        self.x = np.round(x, 3)
        self.unknown_y = None
        # get 20% interval for x 
        inv_x = (max(x) - min(x)) * 0.1
        if inv_x < 1:
            inv_x = 1
        self.x_axis = np.linspace(int(min(self.x) - inv_x), int(max(self.x) + inv_x), 50)
        self.y_axis = []
        # initialize fitting result with None or []
        self.simulate_y = []
        self.predict_x = None
        self.MSE = None
        self.R_square = None
        self.params = []
        self.function_name = None
        self.function_type = None
        self.reverse_function = None
        self.unable_predict = False

    def linear_regression(self):
        """
        # def linear function
        def simu_linear(var_x, a, b):
            var_x = np.array(var_x)
            return a + (b * var_x)
        """
        # get parameters by fitting real number
        params, pcov = curve_fit(simu_linear, self.x, self.y)
        # get round 2 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_linear(self.x, params[0], params[1])
        # generate regression curve data
        y_axis = simu_linear(self.x_axis, params[0], params[1])
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y={0}+({1}*x)".format(params[0], params[1])
        self.reverse_function = 'x = (y-{0})/{1}'.format(params[0], params[1])
        self.function_type = "linear"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def quadratic_regression(self):
        """
        # def quadratic function
        def simu_quadratic(var_x, a, b, c):
            var_x = np.array(var_x)
            return a + (b * var_x) + (c * var_x ** 2)
        """
        # get parameters by fitting real number
        params, pcov = curve_fit(simu_quadratic, self.x, self.y)
        # get round 2 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_quadratic(self.x, params[0], params[1], params[2])
        # generate serial predict y values
        y_axis = simu_quadratic(self.x_axis, params[0], params[1], params[2])
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y={0}+({1}*x)+({2}*x^2)".format(params[0],
                                                              params[1],
                                                              params[2],)
        self.reverse_function = ''
        self.function_type = "quadratic"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def polynomial_regression(self):
        """
        # def polynomial function at ^3
        def simu_poly(var_x, a, b, c, d):
            var_x = np.array(var_x)
            return a + (b * var_x) + (c * var_x ** 2) + (d * var_x ** 3)
        """

        # get parameters by fitting real number
        params, pcov = curve_fit(simu_poly, self.x, self.y)
        # get round 3 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_poly(self.x, params[0], params[1], params[2], params[3])
        # generate serial predict y values
        y_axis = simu_poly(self.x_axis, params[0], params[1], params[2], params[3])
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y={0}+({1}*x)+({2}*x^2)+({3}*x^3)".format(params[0],
                                                                        params[1],
                                                                        params[2],
                                                                        params[3])
        self.function_type = "poly"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def power_regression(self):
        """
        # def power function
        def simu_power(var_x, a, b, c):
            var_x = np.array(var_x)
            return a + b * np.power(var_x, c)
        :return:
        """

        # get parameters by fitting real number
        params, pcov = curve_fit(simu_power, self.x, self.y)
        # get round 2 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_power(self.x, params[0], params[1], params[2])
        # generate serial predict y values
        y_axis = simu_power(self.x_axis, params[0], params[1], params[2])
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y={0}+{1}*x^{2}".format(params[0],
                                                      params[1],
                                                      params[2],)
        self.reverse_function = ''
        self.function_type = "power"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def exponential_regression(self):
        """
        # def exponential function
        def simu_exponential(var_x, a, b):
            var_x = np.array(var_x)
            return a * np.exp(var_x) + b
        :return:
        """

        # get parameters by fitting real number
        params, pcov = curve_fit(simu_exponential, self.x, self.y)
        # get round 2 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_exponential(self.x, params[0], params[1])
        # generate serial predict y values
        y_axis = simu_exponential(self.x_axis, params[0], params[1])
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y = {0}*exp(x)+{1}".format(params[0],
                                                         params[1],)
        self.reverse_function = ''
        self.function_type = "exp"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def logarithmic_regression(self):
        """
        # def Logarithmic functions
        def simu_logarithmic(var_x, a, b):
            var_x = np.array(var_x)
            return a * np.log(var_x) + b
        :return:
        """

        # get parameters by fitting real number
        params, pcov = curve_fit(simu_logarithmic, self.x, self.y)
        # get round 2 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_logarithmic(self.x, params[0], params[1])
        # generate serial predict y values
        y_axis = simu_logarithmic(self.x_axis, params[0], params[1])
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y = {0}*In(x)+{1}".format(params[0],
                                                        params[1],)
        self.reverse_function = ''
        self.function_type = "log"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def sigmoid_regression(self):
        """
        # make simulation base on y_minus
        def simu_sigmoid(var_x, a, b, c):
            var_x = np.array(var_x)
            return a / (1 + np.exp(-b * (var_x + c)))
        :return:
        """

        # minus min of y ,reduce calculation
        min_y = np.min(self.y)
        y_minus = np.array(self.y) - min_y
        # get parameters by fitting real number
        params, pcov = curve_fit(simu_sigmoid, self.x, y_minus)
        # get round 3 of params
        params = np.round(params, 3)
        # get predict y value by simulation function
        simulate_y = simu_sigmoid(self.x, params[0], params[1], params[2]) + min_y
        # generate serial predict y values
        y_axis = simu_sigmoid(self.x_axis, params[0], params[1], params[2]) + min_y
        # get mean square error and r_square
        m_s_e, r_square = fit_parameters(self.y, simulate_y)
        # save records into self object
        self.function_name = "y={0}/(1+exp(-{1}*(x+{2})))+{3}".format(params[0], params[1], params[2], min_y)
        self.function_type = "sigmoid"
        self.simulate_y = np.round(simulate_y, 3)
        self.MSE = m_s_e
        self.R_square = r_square
        self.params = params
        self.y_axis = y_axis
        return self

    def all_regression(self):
        linear = FitModels(self.y, self.x).linear_regression()
        quadratic = FitModels(self.y, self.x).quadratic_regression()
        poly = FitModels(self.y, self.x).polynomial_regression()
        power = FitModels(self.y, self.x).power_regression()
        exp = FitModels(self.y, self.x).exponential_regression()
        log = FitModels(self.y, self.x).logarithmic_regression()
        sigmoid = FitModels(self.y, self.x).sigmoid_regression()
        mse_list = [linear.MSE, quadratic.MSE, poly.MSE, power.MSE, exp.MSE, log.MSE, sigmoid.MSE]
        print(mse_list)
        index_of_min = mse_list.index(min(mse_list))
        print(index_of_min)
        if index_of_min == 0:
            return linear
        elif index_of_min == 1:
            return quadratic
        elif index_of_min == 2:
            return poly
        elif index_of_min == 3:
            return power
        elif index_of_min == 4:
            return exp
        elif index_of_min == 5:
            return log
        elif index_of_min == 6:
            return sigmoid
        else:
            print("OUT OF function index:", index_of_min)
            raise ValueError

    def predict_unknown(self, unknown_y):
        # predict x base on input unknown y
        # unknown_y is a numpy array
        self.unknown_y = unknown_y
        if self.unknown_y:
            fit_function = self.function_type
            left_domain = min(self.x)-1
            right_domain = None
            x_range = [left_domain, right_domain]
            if fit_function == 'linear':
                reverse_function = inversefunc(simu_linear,
                                               args=(self.params[0], self.params[1]),
                                               accuracy=3,
                                               domain=x_range,
                                               )
            elif fit_function == 'quadratic':
                reverse_function = inversefunc(simu_quadratic,
                                               args=(self.params[0], self.params[1], self.params[2]),
                                               accuracy=3,
                                               domain=x_range,
                                               )
            elif fit_function == 'poly':
                reverse_function = inversefunc(simu_poly,
                                               args=(self.params[0], self.params[1], self.params[2], self.params[3]),
                                               accuracy=3,
                                               domain=x_range,
                                               )
            elif fit_function == 'power':
                reverse_function = inversefunc(simu_power,
                                               args=(self.params[0], self.params[1], self.params[2]),
                                               accuracy=3,
                                               domain=x_range,
                                               )
            elif fit_function == 'exp':
                reverse_function = inversefunc(simu_exponential,
                                               args=(self.params[0], self.params[1]),
                                               accuracy=3,
                                               domain=x_range,
                                               )
            elif fit_function == 'log':
                reverse_function = inversefunc(simu_logarithmic,
                                               args=(self.params[0], self.params[1]),
                                               accuracy=3,
                                               domain=x_range,
                                               )

            elif fit_function == 'sigmoid':
                reverse_function = inversefunc(simu_sigmoid,
                                               args=(self.params[0], self.params[1], self.params[2]),
                                               accuracy=3,
                                               domain=x_range,
                                               )
                try:
                    unknown_y = np.array(unknown_y) - np.min(self.y)
                    self.predict_x = np.round(reverse_function(unknown_y), 3)
                    return self
                except ValueError:
                    self.unable_predict = True
            else:
                print('Wrong type of function:', fit_function)
                raise TypeError
            try:
                self.predict_x = np.round(reverse_function(unknown_y), 3)
            except ValueError:
                self.unable_predict = True
        return self


def generate_result(fits, request):
    # set precision of 3 for y and predict_y
    # notice that np.round() don't work
    x = fits.x
    y = fits.y
    # name of x_axis
    x_axis_label = request.POST["x_axis"]
    # name of y_axis
    y_axis_label = request.POST["y_axis"]
    # type of maker 
    maker = request.POST["maker"]
    # color for maker
    maker_color = request.POST["marker_color"]
    # color for curve
    curve_color = request.POST["curve_color"]
    print("load request success")
    title = "Function: %s " % fits.function_name + "        R^2 : %0.3f" % fits.R_square
    # get 20% interval for x and y
    inv_x = (max(x) - min(x)) * 0.2
    inv_y = (max(y) - min(y)) * 0.2
    if inv_x < 1:
        inv_x = 0
    if inv_y < 1:
        inv_y = 0
    ##############

    p = figure(width=1000, height=600,
               x_range=[int(min(x) - inv_x), int(max(x) + inv_x)+1],
               y_range=[int(min(y) - inv_y), int(max(y) + inv_y)+1],
               x_axis_label=x_axis_label,
               y_axis_label=y_axis_label,
               title=title)

    p.title.text_font_size = "16pt"
    # add circle and line
    if maker == "1":
        p.circle(x, y, legend="Actual data", color=maker_color, line_color=None, size=12, alpha=0.8)
    elif maker == "2":
        p.triangle(x, y, legend="Actual data", color=maker_color, line_color=None, size=12, alpha=0.8)
    elif maker == "3":
        p.square(x, y, legend="Actual data", color=maker_color, line_color=None, size=12, alpha=0.8)
    elif maker == "4":
        p.diamond(x, y, legend="Actual data", color=maker_color, line_color=None, size=12, alpha=0.8)
    else:
        p.asterisk(x, y, legend="Actual data", color=maker_color, line_color=None, size=12, alpha=0.8)
    p.line(fits.x_axis, fits.y_axis, legend="Regression curve", line_color=curve_color, alpha=0.6)

    p.legend.location = 'top_left'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.axis_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font_size = "20pt"
    """
    # create standard data widgets
    standard = {'x': x, 'y': y}
    standard_source = ColumnDataSource(standard)
    standard_columns = [
        TableColumn(field="x", title=x_axis_label+' of Standard'),
        TableColumn(field="y", title=y_axis_label+' of Standard'),
    ]

    standard_table = DataTable(source=standard_source, columns=standard_columns, width=350, height=300)

    # create unknown data widgets
    unknown = {'x': predict_x, 'y': unknown_y}
    unknown_source = ColumnDataSource(unknown)
    unknown_columns = [
        TableColumn(field="x", title=x_axis_label + ' of Predict'),
        TableColumn(field="y", title=y_axis_label + ' of unknown'),
    ]

    unknown_table = DataTable(source=unknown_source, columns=unknown_columns, width=350, height=300)
    widgets = widgetbox(standard_table, unknown_table, width=400)
    # put the results in a row
    p = row(widgets, p)
    """
    the_script, the_div = components(p)
    return the_script, the_div


def test():
    x = [1, 2, 3, 4, 5, 6]
    y = [1, 4, 9, 15, 25, 36]
    unknown_y = [5, 7, 11]

    fits = FitModels(y, x)
    print("EMPTY RESULT \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          )

    fits = FitModels(y, x).linear_regression()
    fits.predict_unknown(unknown_y)
    print("linear fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).quadratic_regression()
    fits.predict_unknown(unknown_y)
    print("quadratic fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).polynomial_regression()
    fits.predict_unknown(unknown_y)
    print("polynomial fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).power_regression()
    fits.predict_unknown(unknown_y)
    print("power fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).exponential_regression()
    # fits.predict_unknown(unknown_y)
    print("exponential fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).logarithmic_regression()
    fits.predict_unknown(unknown_y)
    print("logarithmic fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).sigmoid_regression()
    # fits.predict_unknown(unknown_y)
    print("sigmoid fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )
    fits = FitModels(y, x).all_regression()
    fits.predict_unknown(unknown_y)
    print("all fits: \n",
          fits.function_name, '\n',
          fits.params, '\n',
          fits.MSE, '\n',
          fits.R_square, '\n',
          fits.simulate_y, '\n',
          fits.predict_x, '\n',
          )


if __name__ == "__main__":
    test()

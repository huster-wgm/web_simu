import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.resources import CDN
from bokeh.embed import file_html


class FitModels:
    def __init__(self, y, x):
        # assert len of input x and y
        assert len(y) == len(x), 'Number of x and y should be equal'
        # save it into self
        # get 20% interval for x 
        inv_x = (max(x) - min(x)) * 0.1
        if inv_x < 1:
            inv_x = 1
        self.y = y
        self.x = x
        self.predict_y = []
        self.MSE = None
        self.params = []
        self.function_name = None
        self.function_type = None
        self.reverse_function = None
        self.x_axis = np.linspace(int(min(self.x) - inv_x), int(max(self.x) + inv_x), 50)
        self.y_axis = []

    def linear_regression(self):
        # def linear function
        def simu_linear(var_x, a, b):
            var_x = np.array(var_x)
            return a + (b * var_x)

        # get parameters by fitting real number
        params, pcov = curve_fit(simu_linear, self.x, self.y)
        # get round 2 of params
        params = np.round(params, 2)
        # get predict y value by simulation function
        predict_y = simu_linear(self.x, params[0], params[1])
        # generate regression curve data
        y_axis = simu_linear(self.x_axis, params[0], params[1])

        # get mean square error of predict y and actual y
        m_s_e = mean_squared_error(self.y, predict_y)
        # save records into self object
        self.function_name = "y={0}+({1}*x)".format(params[0], params[1])
        self.reverse_function = 'x = (y-{0})/{1}'.format(params[0], params[1])
        self.function_type = "linear"
        self.predict_y = predict_y
        self.MSE = m_s_e
        self.params = params
        self.y_axis = y_axis
        return self

    def polynomial_regression(self):
        # def polynomial function at ^2
        def simu_poly_2(var_x, a, b, c):
            var_x = np.array(var_x)
            return a + (b * var_x) + (c * var_x ** 2)

        # def polynomial function at ^3
        def simu_poly_3(var_x, a, b, c, d):
            var_x = np.array(var_x)
            return a + (b * var_x) + (c * var_x ** 2) + (d * var_x ** 3)

        # get parameters by fitting real number
        params_2, pcov_2 = curve_fit(simu_poly_2, self.x, self.y)
        params_3, pcov_3 = curve_fit(simu_poly_3, self.x, self.y)
        # get round 2 of params
        params_2 = np.round(params_2, 2)
        params_3 = np.round(params_3, 2)
        # get predict y value by simulation function
        predict_y_2 = simu_poly_2(self.x, params_2[0], params_2[1], params_2[2])
        predict_y_3 = simu_poly_3(self.x, params_3[0], params_3[1], params_3[2], params_3[3])
        # generate serial predict y values 
        y_axis_2 = simu_poly_2(self.x_axis, params_2[0], params_2[1], params_2[2])
        y_axis_3 = simu_poly_3(self.x_axis, params_3[0], params_3[1], params_3[2], params_3[3])
        # get mean square error of predict y and actual y
        m_s_e_2 = mean_squared_error(self.y, predict_y_2)
        m_s_e_3 = mean_squared_error(self.y, predict_y_3)
        # choose the best fitting result
        if m_s_e_2 <= m_s_e_3:
            # choose power 2
            # save records into self object
            self.function_name = "y={0}+({1}*x)+({2}*x^2)".format(params_2[0],
                                                                  params_2[1],
                                                                  params_2[2])
            self.reverse_function = ''
            self.function_type = "poly_2"
            self.predict_y = predict_y_2
            self.MSE = m_s_e_2
            self.params = params_2
            self.y_axis = y_axis_2
        else:
            # choose power 3
            # save records into self object
            self.function_name = "y={0}+({1}*x)+({2}*x^2)+({3}*x^3)".format(params_3[0],
                                                                            params_3[1],
                                                                            params_3[2],
                                                                            params_3[3])
            self.function_type = "poly_3"
            self.predict_y = predict_y_3
            self.MSE = m_s_e_3
            self.params = params_3
            self.y_axis = y_axis_3
        return self

    def sigmoid_regression(self):
        # def sigmoid function
        min_y = np.round(np.min(self.y), 2)
        y_minus = np.array(self.y) - min_y

        # make simulation base on y_minus
        def simu_sigmoid(var_x, a, b, c):
            return a / (1 + np.exp(-b * (var_x + c)))

        # get parameters by fitting real number
        params, pcov = curve_fit(simu_sigmoid, self.x, y_minus)
        # get round 3 of params
        params = np.round(params, 2)
        # get predict y value by simulation function
        predict_y = simu_sigmoid(self.x, params[0], params[1], params[2]) + min_y
        # generate serial predict y values
        y_axis = simu_sigmoid(self.x_axis, params[0], params[1], params[2]) + min_y
        # get mean square error of predict y and actual y
        m_s_e = mean_squared_error(self.y, predict_y)
        # save records into self object
        self.function_name = "y={0}/(1+exp(-{1}*(x+{2})))+{3}".format(params[0], params[1], params[2], min_y)
        self.function_type = "sigmoid"
        self.predict_y = predict_y
        self.MSE = m_s_e
        params = np.insert(params, 3, min_y)
        self.params = params
        self.y_axis = y_axis
        return self

    def all_regression(self):
        fits = FitModels(self.y, self.x)
        linear_MSE = fits.linear_regression().MSE
        poly_MSE = fits.polynomial_regression().MSE
        sigmoid_MSE = fits.sigmoid_regression().MSE
        mse_list = [linear_MSE, poly_MSE, sigmoid_MSE]
        index_of_min = mse_list.index(min(mse_list))
        if index_of_min == 0:
            return fits.linear_regression
        elif index_of_min == 1:
            return fits.polynomial_regression()
        elif index_of_min == 2:
            return fits.sigmoid_regression()
        else:
            return 'Fitting errors'


def generate_result(fits, request):
    x = fits.x
    # set precision of 3 for y and pred_y
    # notice that np.round() don't work
    y = fits.y.tolist()
    y = [round(i, 3) for i in y]
    predict_y = fits.predict_y.tolist()
    predict_y = [round(j, 2) for j in predict_y]
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
    title = "Function: " + fits.function_name + "  MSE: %0.3f" % round(fits.MSE, 3)
    # get 20% interval for x and y
    inv_x = (max(x) - min(x)) * 0.2
    inv_y = (max(y) - min(y)) * 0.2
    if inv_x < 1:
        inv_x = 1
    if inv_y < 1:
        inv_y = 1
    ##############

    p = figure(width=800, height=600,
               x_range=[int(min(x) - inv_x), int(max(x) + inv_x)],
               y_range=[int(min(y) - inv_y), int(max(y) + inv_y)],
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
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.axis_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font_size = "20pt"

    # create widgets
    data = {'x': x, 'y': y, 'y_predict': predict_y}
    source = ColumnDataSource(data)
    columns = [
        TableColumn(field="x", title=x_axis_label),
        TableColumn(field="y", title=y_axis_label),
        TableColumn(field="y_predict", title="Predict_Y"),
    ]
    data_table = DataTable(source=source, columns=columns, width=300, height=500)

    widgets = widgetbox(data_table, width=350)
    # put the results in a row
    p = row(widgets, p)
    html = file_html(p, CDN, "result")
    return html


def test():
    x = [1, 2, 3, 4, 5, 6]
    y = [1, 4, 9, 15, 25, 36]

    fits = FitModels(y, x)
    print("EMPTY RESULT \n",
          fits.function_name,
          fits.params,
          fits.MSE,
          fits.predict_y, )

    linear = fits.linear_regression()
    print("linear \n",
          linear.function_name,
          linear.params,
          linear.MSE,
          linear.predict_y, )

    poly = fits.polynomial_regression()
    print("poly \n",
          poly.function_name,
          poly.params,
          poly.MSE,
          poly.predict_y, )

    sigmoid = fits.sigmoid_regression()
    print("sigmoid \n",
          sigmoid.function_name,
          sigmoid.params,
          sigmoid.MSE,
          sigmoid.predict_y, )

    all_three = fits.all_regression()
    print("all three \n",
          all_three.function_name,
          all_three.params,
          all_three.MSE,
          all_three.predict_y, )


if __name__ == "__main__":
    test()

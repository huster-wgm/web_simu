import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
from bokeh.plotting import figure,output_file,show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn

class fit_models():
    def __init__(self,y,x):
        # assert len of input x and y
        assert len(y)==len(x)
        # save it into self
        # get 20% interval for x 
        inv_x=(max(x)-min(x))*0.1
        if inv_x<1:
            inv_x=1
        self.y=y
        self.x=x
        self.pred_y=[]
        self.MSE=None
        self.params=[]
        self.function_name=None
        self.function_type=None
        self.x_axis=np.linspace(int(min(self.x)-inv_x), int(max(self.x)+inv_x), 50) 
        self.y_axis=[]
        
    def linear_regression(self):
        # def linear function
        def simu_linear(var_x,a,b):
            var_x=np.array(var_x)
            return a+(b*var_x)
        #get parameters by fitting real number
        params,pcov = curve_fit(simu_linear,self.x,self.y)
        # get round 2 of params
        params = np.round(params,2)
        # get predict y value by simulation function
        pred_y = simu_linear(self.x,params[0],params[1])
        # generate regression curve data
        y_axis = simu_linear(self.x_axis,params[0],params[1])
        
        # get mean squre error of pred_y and actual y
        MSE = mean_squared_error(self.y,pred_y)
        # save records into self object
        self.function_name="y={0}+({1}*x)".format(params[0],params[1])
        self.function_type="linear"
        self.pred_y=pred_y
        self.MSE=MSE
        self.params=params
        self.y_axis=y_axis
        return self

    def polynomial_regression(self):
        # def polynnomial function up to power 2
        def simu_poly_2(var_x,a,b,c):
            var_x=np.array(var_x)
            return a+(b*var_x)+(c*var_x**2)
        # def polynnomial function up to power 3
        def simu_poly_3(var_x,a,b,c,d):
            var_x=np.array(var_x)
            return a+(b*var_x)+(c*var_x**2)+(d*var_x**3)
        #get parameters by fitting real number
        params_2,pcov_2 =curve_fit(simu_poly_2,self.x,self.y)
        params_3,pcov_3 =curve_fit(simu_poly_3,self.x,self.y)
        # get round 2 of params
        params_2 = np.round(params_2,2)
        params_3 = np.round(params_3,2)
        # get predict y value by simulation function
        pred_y_2 = simu_poly_2(self.x,params_2[0],params_2[1],params_2[2])
        pred_y_3 = simu_poly_3(self.x,params_3[0],params_3[1],params_3[2],params_3[3])
        # generate serial predict y values 
        y_axis_2 = simu_poly_2(self.x_axis,params_2[0],params_2[1],params_2[2])
        y_axis_3 = simu_poly_3(self.x_axis,params_3[0],params_3[1],params_3[2],params_3[3])
        # get mean squre error of pred_y and actual y
        MSE_2 = mean_squared_error(self.y,pred_y_2)
        MSE_3 = mean_squared_error(self.y,pred_y_3)
        # choose the best fitting result
        if MSE_2 <= MSE_3:
            # choose power 2
            # save records into self object
            self.function_name="y={0}+({1}*x)+({2}*x^2)".format(params_2[0],
                                                    params_2[1],params_2[2])
            self.function_type="poly_2"                                        
            self.pred_y=pred_y_2
            self.MSE=MSE_2
            self.params=params_2
            self.y_axis=y_axis_2
        else:
            # choose power 3
            # save records into self object
            self.function_name="y={0}+({1}*x)+({2}*x^2)+({3}*x^3)".format(params_3[0],
                                            params_3[1],params_3[2],params_3[3])
            self.function_type="poly_3"
            self.pred_y=pred_y_3
            self.MSE=MSE_3
            self.params=params_3
            self.y_axis=y_axis_3
        return self
        
    def sigmoid_regression(self):
        # def sigmoid function
        min_y=np.round(np.min(self.y),2)
        y_minus=np.array(self.y)-min_y
        # make simulation base on y_minus
        def simu_simgoid(var_x,a,b,c):
            return a/(1+np.exp(-b*(var_x+c)))
        #get parameters by fitting real number
        params,pcov =curve_fit(simu_simgoid,self.x,y_minus)
        # get round 3 of params
        params = np.round(params,2)
        # get predict y value by simulation function
        pred_y = simu_simgoid(self.x,params[0],params[1],params[2])+min_y
        # generate serial predict y values
        y_axis = simu_simgoid(self.x_axis,params[0],params[1],params[2])+min_y
        # get mean squre error of pred_y and actual y
        MSE = mean_squared_error(self.y,pred_y)
        # save records into self object
        self.function_name="y={0}/(1+exp(-{1}*(x+{2})))+{3}".format(params[0],params[1],params[2],min_y)
        self.function_type="sigmoid"        
        self.pred_y=pred_y
        self.MSE=MSE
        params=np.insert(params,3,min_y)
        self.params=params
        self.y_axis=y_axis
        return self
        
    def all_regression(self):
        fits = fit_models(self.y,self.x)
        linear_MSE = fits.linear_regression().MSE
        poly_MSE = fits.polynomial_regression().MSE
        sigmoid_MSE = fits.sigmoid_regression().MSE
        mse_list=[linear_MSE,poly_MSE,sigmoid_MSE]
        index_of_min=mse_list.index(min(mse_list))
        if index_of_min==0:
            return fits.linear_regression()
        elif index_of_min==1:
            return fits.polynomial_regression()
        elif index_of_min==2:
            return fits.sigmoid_regression()
        else:
            raise ValueError  
        return 0    

def generate_result(fits, x_axis_label, y_axis_label):
    x=fits.x
    y=fits.y
    pred_y=fits.pred_y
    title="Function: "+fits.function_name+"  MSE: %0.3f"% round(fits.MSE,3)
    # get 20% interval for x and y
    inv_x=(max(x)-min(x))*0.2
    inv_y=(max(y)-min(y))*0.2
    if inv_x<1:
        inv_x=1
    if inv_y<1:
        inv_y=1
    ##############
    # create a losss curve plot
    output_file("result.html")
    p = figure(width=800, height=600,
               x_range=[int(min(x)-inv_x), int(max(x)+inv_x)],
               y_range=[int(min(y)-inv_y), int(max(y)+inv_y)],
               x_axis_label= x_axis_label,
               y_axis_label= y_axis_label,
               title=title)
    
    p.title.text_font_size = "16pt"
    # add circle and line
    p.circle(x, y, legend="Actual data", color="purple", line_color=None, size=12,alpha=0.8)
    p.line(fits.x_axis, fits.y_axis, legend="Regression curve",line_color="blue",alpha=0.6)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.axis_label_text_font_size = "20pt"
    p.yaxis.axis_label_text_font_size = "20pt"
    ####### create widgets
    
    data = dict(
            x=x,
            y=np.round(y,3),
            y_predict=np.round(pred_y,3),
        )
    source = ColumnDataSource(data)
    columns = [
            TableColumn(field="x", title=x_axis_label),
            TableColumn(field="y", title=y_axis_label),
            TableColumn(field="y_predict", title="Predict_Y"),
        ]
    data_table = DataTable(source=source, columns=columns, width=300, height=500)
    
    
    
    widgets=widgetbox(data_table, width=350)
    
    
    from bokeh.layouts import row
    # put the results in a row
    show(row(widgets, p))
    
    

def test():        
    x=[1,2,3,4,5,6]
    y=[1,4,9,15,25,36]
    
    fits=fit_models(y,x)
    print(  "EMPTY RESULT \n", 
            fits.function_name,
            fits.params,
            fits.MSE,
            fits.pred_y,)
            
    linear=fits.linear_regression()
    print(  "linear \n",
            linear.function_name,
            linear.params,
            linear.MSE,
            linear.pred_y,)
            
    poly=fits.polynomial_regression()
    print(  "poly \n",
            poly.function_name,
            poly.params,
            poly.MSE,
            poly.pred_y,)
            
    sigmoid=fits.sigmoid_regression()
    print(  "sigmoid \n",
            sigmoid.function_name,
            sigmoid.params,
            sigmoid.MSE,
            sigmoid.pred_y,)
            
    all_three=fits.all_regression()
    print(  "all three \n",
            all_three.function_name,
            all_three.params,
            all_three.MSE,
            all_three.pred_y,)        
        

if __name__=="__main__":
    test()
    
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

class fit_models():
    def __init__(self,y,x):
        # assert len of input x and y
        assert len(y)==len(x)
        # save it into self
        self.y=y
        self.x=x
        self.pred_y=[]
        self.MSE=None
        self.params=[]
        self.function_name=None

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
        # get mean squre error of pred_y and actual y
        MSE = mean_squared_error(self.y,pred_y)
        # save records into self object
        self.function_name="y={0}+({1}*x)".format(params[0],params[1])
        self.pred_y=pred_y
        self.MSE=MSE
        self.params=params

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
        # get mean squre error of pred_y and actual y
        MSE_2 = mean_squared_error(self.y,pred_y_2)
        MSE_3 = mean_squared_error(self.y,pred_y_3)
        # choose the best fitting result
        if MSE_2 <= MSE_3:
            # choose power 2
            # save records into self object
            self.function_name="y={0}+({1}*x)+({2}*x^2)".format(params_2[0],
                                                    params_2[1],params_2[2])
            self.pred_y=pred_y_2
            self.MSE=MSE_2
            self.params=params_2
        else:
            # choose power 3
            # save records into self object
            self.function_name="y={0}+({1}*x)+({2}*x^2)+({3}*x^3)".format(params_3[0],
                                            params_3[1],params_3[2],params_3[3])
            self.pred_y=pred_y_3
            self.MSE=MSE_3
            self.params=params_3

    def sigmoid_regression(self):
        self.function_name="sigmoid"
        # def sigmoid function
        min_y=np.min(self.y)
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
        # get mean squre error of pred_y and actual y
        MSE = mean_squared_error(self.y,pred_y)
        # save records into self object
        self.function_name="y={0}/(1+exp(-{1}*(x+{2})))+{3}".format(params[0],params[1],params[2],min_y)
        self.pred_y=pred_y
        self.MSE=MSE
        params=np.insert(params,3,min_y)
        self.params=params
        
def test():        
    x=[1,2,3,4,5,6]
    y=[1,4,9,15,25,36]
    
    fits=fit_models(y,x)
    print(  fits.function_name,
            fits.params,
            fits.MSE,
            fits.pred_y,)
            
    fits.linear_regression()
    print(  fits.function_name,
            fits.params,
            fits.MSE,
            fits.pred_y,)
            
    fits.polynomial_regression()
    print(  fits.function_name,
            fits.params,
            fits.MSE,
            fits.pred_y,)
            
    fits.sigmoid_regression()
    print(  fits.function_name,
            fits.params,
            fits.MSE,
            fits.pred_y,)
        

if __name__=="__main__":
    test()
    
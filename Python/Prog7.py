__author__ = 'Mohan Kandaraj'
import Tkinter
import sys
import tkFileDialog
from scipy.optimize import curve_fit
import numpy
import matplotlib.pyplot as pyplot

def linear_regression(data):
    """Compute Linear Regression for univariate model"""
    x_values = [x for x, y in data] #Get x values
    y_values = [y for x, y in data] #Get y values
    x_mean = sum(x_values) / len(x_values) #Compute mean value of x
    y_mean = sum(y_values) / len(y_values) #Compute mean value of y
    # Compute
    coefficient = sum([(x - x_mean) * (y-y_mean) for x,y in data]) / sum([(x - x_mean) ** 2 for x in x_values])
    intercept = y_mean - coefficient * x_mean  # Compute Intercept
    return((coefficient,intercept))

#Define function for linear model
def quad(x,a,b,c):
    """ Linear Equation """
    return a * x ** 2 + b * x + c

#Define function for quadratic
def lm(x,a,b):
    """ Linear Equation """
    return a * x + b


if __name__ == "__main__":
    """Main function to execute the program"""

    Tkinter.Tk().withdraw()
    try:
        file = tkFileDialog.askopenfile() # Ask user for the file and open the file in read mode
        if file is None: sys.exit()
        # Read Input, split input into lines, split fields in a line to a list and store as nested list
        brainandbody = [lines.split(",") for lines in file.read().splitlines()][1:]

        # Compute regression formula and print..
        regression =linear_regression([[float(brain),float(body)] for name,body,brain in brainandbody])
        print "Regression Model"
        print "bo = %s br + %s" % regression
        print "Regression Model after converting body weight to gram (i.e to same unit as brain)"
        print "bo = %s br + %s" % (regression[0]*1000,regression[1]*1000)

        brainandbody_n=numpy.array([[body,brain] for name,body,brain in brainandbody],float)
        coeff,covar=curve_fit(lm,brainandbody_n[:,1],brainandbody_n[:,0])
        print "Linear Regression Model using numpy Curve Fitting"
        print "bo = %s br + %s" % (coeff[0],coeff[1])
        print "\n"


        brain=[float(br) for name,bo,br in brainandbody]
        actual_body=[float(bo) for name,bo,br in brainandbody]
        linear_body=[lm(br,coeff[0],coeff[1]) for br in brain]

        import timeit
        setup="from __main__ import brainandbody,linear_regression"
        t=timeit.Timer("linear_regression([[float(brain),float(body)] for name,body,brain in brainandbody])",setup)
        setup="from __main__ import brainandbody_n,lm;from scipy.optimize import curve_fit"
        print "Time taken for manual linear Regression 5 loops  : %s" % (t.timeit(5))
        t=timeit.Timer("curve_fit(lm,brainandbody_n[:,1],brainandbody_n[:,0])",setup)
        print "Time taken for scipy curve fit Regression 5 loops: %s" % (t.timeit(5))
        print "\n"
        coeff,covar=curve_fit(quad,brainandbody_n[:,1],brainandbody_n[:,0])


        print "Quadratic Model using numpy Curve Fitting"
        print "bo = %s br^2 + %s br + %s" % (coeff[0],coeff[1],coeff[2])

        quad_body=[quad(br,coeff[0],coeff[1],coeff[2]) for br in brain]

        #Plot the data, linear and quadratic models
        dat,=pyplot.plot(brain,actual_body,"go",label="Actual")
        linear_line,=pyplot.plot(brain,linear_body,"b-",label="Linear")
        quad_line,=pyplot.plot(brain,quad_body,"ro",label="Quadratic")

        pyplot.legend(handles=[dat,linear_line,quad_line],loc=2)
        pyplot.title("Linear and Quadratic Fits")
        pyplot.show()
    except Exception, e:
        print "Error: " + str(e)
        sys.exit(e)
    finally:
        if file is not None:
            file.close()

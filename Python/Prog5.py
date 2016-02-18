__author__ = 'Mohan Kandaraj'
import Tkinter
import sys
import tkFileDialog

def linear_regression(data):
    """Compute Linear Regression for univariate model"""
    x_values = [x for x, y in data] #Get x values
    y_values = [y for x, y in data] #Get y values
    x_mean = sum(x_values) / len(x_values) #Compute mean value of x
    y_mean = sum(y_values) / len(y_values) #Compute mean value of y
    # Compute Coefficient
    coefficient = sum([(x - x_mean) * (y-y_mean) for x,y in data]) / sum([(x - x_mean) ** 2 for x in x_values])
    intercept = y_mean - coefficient * x_mean  # Compute Intercept
    return((coefficient,intercept))


def main():
    """Main function to execute the program"""
    Tkinter.Tk().withdraw()
    try:
        file = tkFileDialog.askopenfile() # Ask user for the file and open the file in read mode
        if file is None: sys.exit()
        # Read Input, split input into lines, split fields in a line to a list and store as nested list
        brainandbody = [lines.split(",") for lines in file.read().splitlines()][1:]
        # Compute regression formula and print..
        regression = linear_regression([[float(brain),float(body)] for name,body,brain in brainandbody])
        print "Regression Model"
        print "bo = %s br + %s" % regression
        print "Regression Model after converting body weight to gram (i.e to same unit as brain)"
        print "bo = %s br + %s" % (regression[0]*1000,regression[1]*1000)
    except Exception, e:
        print "Error: " + str(e)
        sys.exit(e)
    finally:
        if file is not None:
            file.close()


if __name__ == "__main__":
    main()
__author__ = 'Mohan Kandaraj'
import sys
import pandas as pd
import numpy as numpy
import Tkinter, tkFileDialog
import sys
import matplotlib.pyplot as pyplot
from scipy.optimize import curve_fit
from scipy import misc
import scipy.ndimage as ndimage
import skimage.filters as skif

if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO


def lm(x,a,b):
    """ Linear Equation """
    return a * x + b


def car_plot():
        #Ask user for the file(s)
        file=tkFileDialog.askopenfile(initialfile='cars.data.csv',title='Select File',filetypes=[('all','*'), ('csv','*.csv')])
        #Read file conente and replace =" with = so that we can parse the file properly
        if file is None: return
        #Column Names for the data since the file don't have column names
        colnames = ["buying_price", "maint_price", "doors","persons","lug_boot","safety","acceptability"]
        #Parse the file into data frame
        df=pd.read_csv(file,warn_bad_lines=True,names=colnames)
        BUYING_PRICE_VALUES = {'vhigh':4,'high':3,'med':2,'low':1}
        MAINT_PRICE_VALUES = {'vhigh':4,'high':3,'med':2,'low':1}
        DOORS_VALUES = {'1':1,'2':2,'3':3,'4':4,'5more':5}
        SAFETY_VALUES={'low':1,'med':2,'high':3}

        #Sub Plot for Buying Price
        pyplot.subplot(221)
        pyplot.xticks([1,2,3,4])
        pyplot.hist(df.buying_price.map(BUYING_PRICE_VALUES),4,rwidth=2,range=(0,5),align='mid', facecolor='g',alpha=.5)
        pyplot.title("Buying Price")
        pyplot.xlabel("1=low,  2=med  3=high  4=vhigh")
        pyplot.ylabel("Count")

        #Sub plot for maintenance Price
        pyplot.subplot(222)
        pyplot.xticks([1,2,3,4])
        pyplot.hist(df.maint_price.map(MAINT_PRICE_VALUES),4,range=(0,5), normed=False, facecolor='b',alpha=.3)
        pyplot.title("Maintenance Price")
        pyplot.xlabel("1=low,  2=med  3=high  4=vhigh")
        pyplot.ylabel("Count")

        #Subplot for safety
        pyplot.subplot(223)
        pyplot.xticks([1,2,3])
        pyplot.hist(df.safety.map(SAFETY_VALUES),3,range=(0,4), normed=False, facecolor='c',alpha=.6)
        pyplot.title("Safety")
        pyplot.xlabel("1=low,  2=med  3=high")
        pyplot.ylabel("Count")


        #Subplot for Doors
        pyplot.subplot(224)
        pyplot.xticks([1,2,3,4,5])
        pyplot.hist(df.doors.map(DOORS_VALUES),5,range=(0,6), normed=False, facecolor='y',alpha=.5)
        pyplot.title("Car Doors")
        pyplot.xlabel("Number of Doors")
        pyplot.ylabel("Count")

        #Add space between subplots
        pyplot.tight_layout(pad=1.75, h_pad=None, w_pad=None, rect=None)

        #Show the graph
        pyplot.show()

        return

def regression_plot():
    file = tkFileDialog.askopenfile(initialfile='brainandbody.csv',title='Select File',filetypes=[('all','*'), ('csv','*.csv')]) # Ask user for the file and open the file in read mode
    if file is None: return
    # Read Input, split input into lines, split fields in a line to a list and store as nested list
    brainandbody = [lines.split(",") for lines in file.read().splitlines()][1:]

    # Compute regression formula
    brainandbody_n=numpy.array([[body,brain] for name,body,brain in brainandbody],float)
    coeff,covar=curve_fit(lm,brainandbody_n[:,1],brainandbody_n[:,0])


    brain=[float(br) for name,bo,br in brainandbody]
    actual_body=[float(bo) for name,bo,br in brainandbody]
    linear_body=[lm(br,coeff[0],coeff[1]) for br in brain]





    #Plot the data, linear and quadratic models
    dat,=pyplot.plot(brain,actual_body,"go",label="Data")
    linear_line,=pyplot.plot(brain,linear_body,"b-",label="Linear Regression")
    pyplot.legend(handles=[dat,linear_line],loc=2)
    pyplot.title("Data and Linear Fit")
    pyplot.xlabel("Brain weight")
    pyplot.ylabel("Body Weight")
    pyplot.show()


def image_plot():
        file=tkFileDialog.askopenfilename(initialfile='objects.png',title='Select One or More Images',filetypes=[('all','*'), ('png image','*.png')])
        if file == "" : return
        #Load Image
        picture = misc.imread(str(file))
        #Apply Gaussian filter
        picture_filtered = ndimage.gaussian_filter(picture,4)
        #Find Threshold
        cutoff = skif.threshold_otsu(picture_filtered)
        #Detect objects
        labeled, n = ndimage.label(picture_filtered > cutoff)

        pyplot.imshow(labeled)

        #Find Object Centers
        centers = ndimage.center_of_mass(picture_filtered,labeled,range(0,n))

        #Plot Object Centers
        pyplot.scatter([x for y,x,z in centers],[y for y,x,z in centers],c='r',s=40)
        pyplot.title("Object Center")
        pyplot.show()


def http_plot():
    #Ask user for the file(s)
    file=tkFileDialog.askopenfile(initialfile='epa-http.txt',title='Select File',filetypes=[('all','*'), ('text','*.txt')])
    if file is None: return
    #Read file conente and replace =" with = so that we can parse the file properly
    filecontent=file.read().replace('="','=')

    #Create IO object for the cleansed data
    newfile=StringIO(filecontent)

    #Column Names for the data since the file don't have column names
    colnames=["host","date","request","httpcode","bytes"]

    #Parse the file into data frame
    df=pd.read_table(newfile,delim_whitespace=True,warn_bad_lines=True,names=colnames)

    #Create Hour Column from Date column
    df['hour']= df['date'].str.slice(4,6)
    #Create Day Column Date
    df['day']= df['date'].str.slice(1,3)

    #Plot number of request by
    pyplot.plot(df[['hour','request']].groupby(['hour'],as_index=False).count())
    pyplot.xlim((0,24))
    pyplot.title("Number of HTTP requests by hour")
    pyplot.xlabel("Hour")
    pyplot.ylabel("Number of HTTP Requests")
    pyplot.show()

if __name__ == "__main__":
    """Main function to execute the program"""
    Tkinter.Tk().withdraw()
    try:

        #Call function to Plot frequency of various car attributes
        car_plot()
        #Call function to plot regression line along with Data
        regression_plot()
        #Call function to show image and center of objects in the image
        image_plot()
        #Plot number of http request by hour
        http_plot()


    except Exception, e:
        print "Error: Terminating the program! " + str(e)
        sys.exit(e)
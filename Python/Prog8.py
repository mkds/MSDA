__author__ = 'Mohan Kandaraj'
import sys
from scipy import misc
import scipy.ndimage as ndimage
import skimage.filters as skif
import Tkinter, tkFileDialog

if __name__ == "__main__":
    """Main function to execute the program"""
    Tkinter.Tk().withdraw()
    try:
        #Ask user for the file(s)
        files=tkFileDialog.askopenfilenames(initialfile='*.png',title='Select One or More Images',filetypes=[('all','*'), ('png image','*.png')])
        for file in files:
            #Load Image
            picture = misc.imread(str(file))
            #Apply Gaussian filter
            picture_filtered = ndimage.gaussian_filter(picture, 4)
            #Find Threshold
            cutoff = skif.threshold_otsu(picture_filtered)
            #Detect objects
            labeled, n = ndimage.label(picture_filtered > cutoff)
            print "Number of objects in image %s  :  %s" % (file,n)
            #pylab.imshow(labeled)
            #pylab.show()

            #Find Object Centers
            centers = ndimage.center_of_mass(picture_filtered,labeled,range(0,n))
            print "Object Centers (Image %s):%s\n" % (file,centers)

    except Exception, e:
        print "Error: Terminating the program! " + str(e)
        sys.exit(e)
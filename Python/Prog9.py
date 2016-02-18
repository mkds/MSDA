__author__ = 'Mohan Kandaraj'
import sys
from scipy import misc
import pandas as pd
import Tkinter, tkFileDialog
import sys
import re
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO


if __name__ == "__main__":
    """Main function to execute the program"""
    Tkinter.Tk().withdraw()
    try:
        #Ask user for the file(s)
        file=tkFileDialog.askopenfile(initialfile='*.txt',title='Select File',filetypes=[('all','*'), ('text','*.txt')])
        #Read file conente and replace =" with = so that we can parse the file properly
        filecontent=file.read().replace('="','=')

        #Create IO object for the cleansed data
        newfile=StringIO(filecontent)

        #Column Names for the data since the file don't have column names
        colnames=["host","date","request","httpcode","bytes"]

        #Parse the file into data frame
        df=pd.read_table(newfile,delim_whitespace=True,warn_bad_lines=True,names=colnames)


        print "***Host or IP that made most requests***"
        print df[['host','request']].groupby(['host']).count().sort('request',ascending=False)[0:1]

        print "\n***Hostname or IP address that received the most total bytes from the ***"
        print df[['host','bytes']].groupby(['host'],as_index=False).sum().sort('bytes',ascending=False)[0:1]

        #Create Hour Column from Date column
        df['hour']= df['date'].str.slice(4,6)
        #Create Day Column Date
        df['day']= df['date'].str.slice(1,3)

        print "\n***Busiest Hour in terms of requests***"
        print df[['hour','day','request']].groupby(['hour','day']).count().sort('request',ascending=False)[0:1]

        #Capture gif file names from request string if present
        df['gif']=df['request'].str.extract(".*/(.*\.gif).*")

        print "\n***Which .gif image was downloaded the most during the day?***"
        print "\n***Most Downloaded .gif image on 29 ***"
        print df[df.day=='29'][['gif','day','request']].groupby(['gif','day']).count().sort('request',ascending=False).head(1)
        print "\n***Most Downloaded .gif image on 30 ***"
        print df[df.day=='30'][['gif','day','request']].groupby(['gif','day']).count().sort('request',ascending=False).head(1)

        print "\n***What HTTP reply codes were sent other than 200?***"
        print df[df.httpcode != 200].httpcode.unique()


    except Exception, e:
        print "Error: Terminating the program! " + str(e)
        sys.exit(e)
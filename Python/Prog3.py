__author__ = 'Mohan Kandaraj'

import sys
import re
import Tkinter
import tkFileDialog
import traceback
class CarEvaluation(object):
    """Class that ts CarEvaluation dataset"""

    #Define valid values for all attribute as keys of a dictionary with values as numerical representation of attributes
    _BUYING_PRICE_VALUES = {'vhigh':4,'high':3,'med':2,'low':1}
    _MAINT_PRICE_VALUES = {'vhigh':4,'high':3,'med':2,'low':1}
    _DOORS_VALUES = {'1':1,'2':2,'3':3,'4':4,'5more':5}
    _PERSONS_VALUES={'2':2,'4':4,'more':6}
    _LUG_BOOT_VALUES={'small':1,'med':2,'big':3}
    _SAFETY_VALUES={'low':1,'med':2,'high':3}
    _ACCEPTABILITY_VALUES={'unacc':1,'acc':2,'good':3,'vgood':4}

    #Set values for all attributes. As all the attributes are defined with setter method
    #      attribute value validation is done in the setter method
    def __init__(self, buying_price, maint_price, doors,persons,lug_boot,safety,acceptability):
        self.buying_price = buying_price
        self.maint_price = maint_price
        self.safety = safety
        self.doors = doors
        self.persons = persons
        self.lug_boot=lug_boot
        self.acceptability = acceptability

    @property
    def buying_price(self):
        return self._buying_price

    @buying_price.setter
    def buying_price(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._BUYING_PRICE_VALUES : raise InvalidValue("buying_price")
        self._buying_price=value

    @property
    def maint_price(self):
        return self._maint_price

    @maint_price.setter
    def maint_price(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._MAINT_PRICE_VALUES : raise InvalidValue("maint_price")
        self._maint_price=value

    @property
    def doors(self):
        return self._doors

    @doors.setter
    def doors(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._DOORS_VALUES : raise InvalidValue("door")
        self._doors=value

    @property
    def persons(self):
        return self._persons

    @persons.setter
    def persons(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._PERSONS_VALUES : raise InvalidValue("persons")
        self._persons=value

    
    @property
    def lug_boot(self):
        return self._lug_boot

    @lug_boot.setter
    def lug_boot(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._LUG_BOOT_VALUES : raise InvalidValue("lug_boot")
        self._lug_boot=value


    @property
    def safety(self):
        return self._safety

    @safety.setter
    def safety(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._SAFETY_VALUES : raise InvalidValue("safety")
        self._safety=value


    @property
    def acceptability(self):
        return self._acceptability

    @acceptability.setter
    def acceptability(self,value):
        #Raise exception for invalid values
        if value not in CarEvaluation._ACCEPTABILITY_VALUES : raise InvalidValue("acceptability")
        self._acceptability=value

    #Return integer value of the attribute by looking up for the value in values dictionary of that attribute
    def get_int_value(self,attribute_name):
        return getattr(self,"_"+attribute_name.upper()+"_VALUES")[getattr(self,attribute_name)]

    def __repr__(self):
        return ",".join([str(value) for value in [self.buying_price,self.maint_price,self.doors,self.persons,self.lug_boot,self.safety,self.acceptability]])

    def showEvaluation(self):
        print "The %s has a %s price and it's safety is rated a %s" % (self.name, self.price, self.safety)


class InvalidValue(Exception):
    """Exception for invalid attribute values"""
    def __init__(self,attribute_name):
        self.invalid_attribute = attribute_name

    def __repr__(self):
        return "Invalid value provided for e %s" % self.invalid_attribute

    def __str__(self):
        return self.__repr__()


def sort_by_attribute(list_carevaluation,attribute_name,desc=False):
    """Sort list of CarEvaluation by the attribute passed"""
    return sorted(list_carevaluation,key = lambda x: x.get_int_value(attribute_name),reverse=desc)


def main():
    """Main function to execute the program"""
    Tkinter.Tk().withdraw()
    try:
        #Ask user for the file and open the file in read mode
        file=tkFileDialog.askopenfile()

        try:
            #Read the file, split contents by lines, then split lines into words using "," as separator and
            #   use the words to create carEvaluation object
            carevaluation_list=[CarEvaluation(*lines.split(",")) for lines in file.read().splitlines()]
            process_records(carevaluation_list)
        except Exception, e:
            print "Error: Parsing file. Terminating the program! "  +  str(e)
            sys.exit(e)
        finally:
            file.close()
    except Exception, e:
        print "Error: Could not open the file to read. Terminating the program! " + str(e)
        sys.exit(e)

def process_records(carevaluation_list):
    """Do sort and filter operations on list of CarEvaluation"""

    #Function to convert list of CarEvaluation to records(strings) separated by newline
    car_lines = lambda car_list: "\n".join(`car_record` for car_record in car_list)

    print "\n *** Top 10 rows of the data sorted by 'safety' in descending order"
    print car_lines(sort_by_attribute(carevaluation_list,"safety",True)[:10])

    print "\n *** Bottom 15 rows of the data sorted by 'maint' in ascending order"
    print car_lines(sort_by_attribute(carevaluation_list,"maint_price")[-15:])

    #Filter criteria as regular expression. buying and maint: high or vhigh safety:high
    pattern_for_sort=re.compile(r'^(high|vhigh),(high|vhigh),(\d|\d\D+),(\D+|\d),\D+,high,\D+')
    #Filter records
    records_for_sort=[car_record for car_record in carevaluation_list if pattern_for_sort.match(`car_record`)]

    print "\n *** Rows that are high or vhigh in fields 'buying', 'maint', and 'safety', sorted by 'doors' in ascending order"
    print car_lines(sort_by_attribute(records_for_sort,"doors"))

    #Pattern for filtering records for saving file.  buying:vhigh maint:med doors:4 persons:4 or more
    pattern_for_save=re.compile(r'^vhigh,med,4,(4|more),\D+,\D+,\D+')
    records_to_save = car_lines([car_record for car_record in carevaluation_list if pattern_for_save.match(`car_record`)])
    try:
        write_file=tkFileDialog.asksaveasfile()
        write_file.write(records_to_save)
    except Exception, e:
        print "Error: Could not open the file to write. Terminating the program! " + str(e)
    finally :
        if write_file != None : write_file.close()



if __name__ == "__main__":
    main()
# 1. fill in this class
#   it will need to provide for what happens below in the
#	main, so you will at least need a constructor that takes the values as (Brand, Price, Safety Rating),
# 	a function called showEvaluation, and an attribute carCount
import sys
class CarEvaluation:
    'A simple class that represents a car evaluation'
    #all your logic here
    carCount = 0

    def __init__(self, name, price, safety):
        self.name = name
        self.price = price
        self.safety = safety
        CarEvaluation.carCount += 1

    def __repr__(self):
        return self.name

    def showEvaluation(self):
        print "The %s has a %s price and it's safety is rated a %s" % (self.name, self.price, self.safety)


#2. fill in this function
#   it takes a list of CarEvaluation objects for input and either "asc" or "des"
#   if it gets "asc" return a list of car names order by ascending price
# 	otherwise by descending price
def sortbyprice(listCarEvaluation, order):  #you fill in the rest

    listCarEvaluation.sort(key = lambda x: {"High":3,"Med":2,"Low":1}[x.price],reverse={"asc":False,"des":True}[order])
    return listCarEvaluation #return a value
    #return listCarEvaluation.sort(key = lambda x: {"High":3,"Med":2,"Low":1}[x.price])#return a value


#3. fill in this function
#   it takes a list for input of CarEvaluation objects and a value to search for
#	it returns true if the value is in the safety  attribute of an entry on the list,
#   otherwise false
def searchforsafety(a, b):  #you fill in the rest
    return b in [car.safety for car in a]  #return a value

# This is the main of the program.  Expected outputs are in comments after the function calls.
if __name__ == "__main__":
    eval1 = CarEvaluation("Ford", "High", 2)
    eval2 = CarEvaluation("GMC", "Med", 4)
    eval3 = CarEvaluation("Toyota", "Low", 3)

    print "Car Count = %d" % CarEvaluation.carCount  # Car Count = 3

    eval1.showEvaluation()  #The Ford has a High price and it's safety is rated a 2
    eval2.showEvaluation()  #The GMC has a Med price and it's safety is rated a 4
    eval3.showEvaluation()  #The Toyota has a Low price and it's safety is rated a 3

    L = [eval1, eval2, eval3]
    print sortbyprice(L, "asc");  #[Toyota, GMC, Ford]
    print sortbyprice(L, "des");  #[Ford, GMC, Toyota]
    print searchforsafety(L, 2);  #true
    print searchforsafety(L, 1);  #false

# Part II rewrite the main using introspection
    #Get current module
    this_module = sys.modules[__name__]
    eval4 = getattr(this_module,"CarEvaluation")("Ford","High",2)
    eval5 = getattr(this_module,"CarEvaluation")("GMC","Med",4)
    eval6 = getattr(this_module,"CarEvaluation")("Toyoto","Low",3)

    print "Car Count = %d" % getattr(getattr(this_module,"CarEvaluation"),"carCount")  # Car Count = 6
    getattr(eval4,"showEvaluation")()
    getattr(eval5,"showEvaluation")()
    getattr(eval6,"showEvaluation")()
    L1 = [eval4,eval5,eval6]
    print getattr(this_module,"sortbyprice")(L1,"asc") #[Toyota, GMC, Ford]
    print getattr(this_module,"sortbyprice")(L1,"des") #[Ford, GMC, Toyota]
    print getattr(this_module,"searchforsafety")(L1,2)#true
    print getattr(this_module,"searchforsafety")(L1,1) #false
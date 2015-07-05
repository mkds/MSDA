#12-Factorial loop
fact=1
for (i in 1:12){
  fact=fact*i
}
cat("12 Factorial = ",fact,"\n")
nvector=seq(20,50,5)
cat("Numeric vector: ",nvector,"\n")


#Function to solve Quadratic Equation
quadroots=function(coeff)
{
  rp1=-coeff[2]/(2*coeff[1])
  p=coeff[2]^2-4*coeff[1]*coeff[3]
  if (p > 0)
  {
    # Real Roots
    rp2=sqrt(p)/(2*coeff[1])
    return(c(rp1,rp2,1))
  }
  else
  {
    # Complex Roots
    rp2=sqrt(-p)/(2*coeff[1])
    return(c(rp1,rp2,-1))
  }
}

#Solve Quadratic Equation
#Get Input
inv=readline("Please enter coefficient (a,b,c) of quadratic equation ax^2+bx+c : ")
#Parse input and covert to numeric
coeff=as.vector(sapply(strsplit(inv," "),as.numeric))
#Check if input is valid
if (all(!is.na(coeff)) & length(coeff) ==3 & coeff[1]!=0){
  roots=quadroots(coeff)
  #roots[3]=1 means roots are real
  if (roots[3]==1){
    print(paste("Roots of the equation are",roots[1]+roots[2],roots[1]-roots[2]))
  }else {
    #Complex root
    print(paste0("Roots(Complex) of the equation are ",roots[1]," (+ or -) ",roots[2],"i"))
  }

} else {
  print("Invalid or Missing coefficients")
  
}



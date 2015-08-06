"""

Implementation of Ada Boosting algorithm and Real AdaBoosting algorithm

Input:
**************************
T (an integer number).
n (an integer number).
epsilon (a small real number)
x (a list of n real numbers. These are assumed to be in increasing order).
y (a list of n numbers, each one is either 1 or -1).
p (a list of n nonnegative numbers that sum up to 1).

Output: Real AdaBoosting
*****************************
1. The selected weak classifier: ht.
2. The G error value of ht : Gerror.
3. The weights ct+, ct-.
4. The probabilities normalization factor: Zt.
5. The probabilities after normalization: pi.
6. The values ft(xi) for each one of the examples.
7. The error of the boosted classifier: Et.
8. The bound on Et.
"""
import math
from test.support import temp_cwd

class adaboosting:
    ffun = []
    rfinal = []
    bound = 1
    bbound =1
    """Initiation of class variables"""
    def __init__(self,x,y,prob,t,eps,n):
        self.x=x
        self.y=y
        self.prob=prob
        self.t=t
        self.eps = float(eps)
        self.n = int(n)
        for i in range(0,int(n)):
            #adaboosting.ffun.append(0)# contains Ft value for AdaBoosting
            adaboosting.rfinal.append(0)# Contains ft value for Ral AdaBoosting
    """This function calculates the threshold array"""  
    def temp(self,temp):
        avg=(0+self.x[0])/2
        temp.append(avg)
        for i in range(0,len(self.x)-1):
            avg= (self.x[i]+self.x[i+1])/2
            temp.append(avg)
        avg= self.x[i+1]+ 0.1
        temp.append(avg)  
        return temp
    """This function calculates the hypothesis array for threshold less than value"""
    def lesshypo(self,temp_error,value):
        for i,sign in enumerate(self.y):
            if(value > self.x[i]):
                temp_error.append(1)
            else:
                temp_error.append(-1)
        return temp_error
    """This function calculates the error in hypothesis"""
    def errorcalc(self):
        error =0
        for i,va in enumerate(self.temp_error):
            if (va != y[i]):
                    #print(va, y[i])
                error=error+prob[i]
        return error    
    
    """This function implements F (f(x))function of real AdaBoosting algorithms
    Returns the error calculated as per f function
    """
    def realfinallistcalc(self):
        te = []
        for i,valu in  enumerate(adaboosting.rfinal):
            if(valu>0):
                te.append(1)
            else:
                te.append(-1)
        count_f=0
        for i,va in enumerate(te):
            if(va != y[i]):
                count_f =count_f+1
        return count_f
   
    """
    This Function calculate the output for Real AdaBoosting foe weak classifiers
    """       
        
    def realerror(self):        
        temp = []
        error_list = []
        list_error = []
        gvalue = []
        pvalue = []
        mark = []
        temp = self.temp(temp)
        #print (temp)
        for value in temp:
            temp_error=[]
            index ='Less than '+str(value)
            mark.append(index)
            self.temp_error = self.lesshypo(temp_error,value)
            list_error.append(self.temp_error)
            prposi =0
            prneg =0
            pwposi =0
            pwneg =0            
            gtemp =0            
            for i,va in enumerate(temp_error):
                if ( va == 1 and y[i] == 1):
                    prposi = prposi+prob[i]                
                elif(va == -1 and y[i] == -1):
                    prneg=prneg+prob[i]                
                elif(va == -1 and y[i] == +1):
                    pwposi=pwposi+prob[i]
                else:
                    pwneg=pwneg+prob[i]            
            gtemp = math.sqrt((prposi*pwneg))+math.sqrt((prneg*pwposi))
            pvalue.append((prposi,prneg,pwposi,pwneg))
            gvalue.append(gtemp)
        #print(gvalue)        
        print("      ")
        #print("Real Classifier (Real AdaBoosting)")
        min_val=min(gvalue)
        indx = gvalue.index(min_val)
        print("Weak Classifier" +mark[indx])
        print("G Error : " +str(min_val))
        
        tm = pvalue[indx]
        temp_com = list_error[indx]         
        ctpositive= 0.5*(math.log(((tm[0]+self.eps)/(tm[3]+self.eps))))
        ctneg = 0.5*(math.log((tm[2]+self.eps)/(tm[1]+self.eps)))
        print("Weights : "+str(ctpositive)+"and "+str(ctneg))
        zvalue = 2*(math.sqrt((tm[0]*tm[3]))+math.sqrt((tm[2]*tm[1])))
        print("Probablity Normalization Factor: "+str(zvalue))       
        for i,wt in enumerate(self.prob):
            if(temp_com[i]==1):
                inival = prob[i]
                prob[i]=(inival*math.exp(-1*y[i]*ctpositive))/zvalue
            else:
                inival = prob[i]
                prob[i]=(inival*math.exp(-1*y[i]*ctneg))/zvalue        
        print("Probablity after normalization: "+str(prob))        
        for i,val in enumerate(temp_com):
            if(val == 1):
                adaboosting.rfinal[i]= ctpositive+adaboosting.rfinal[i]
            else:
                adaboosting.rfinal[i]= ctneg+adaboosting.rfinal[i]        
        print("F(t) for each : "+str(adaboosting.rfinal))               
        adaboosting.bound = adaboosting.bound*zvalue      
        count_f = self.realfinallistcalc()        
        print("Et : "+str(count_f/int(self.n)))
        print("Bound on Et"+str(adaboosting.bound))

file_name = input("Enter the file name : ")
x = []
y = []
prob = []
with open(file_name) as f:
    for i, l in enumerate(f):
        if (i==0):
            (t,n,eps) = l.rstrip('\n').split(' ')
        if (i==1):
            l=l.split()
            if l:
                for j in l:
                    x.append(float(j))
        if (i==2):
            l=l.split()
            if l:
                for j in l:
                    y.append(int(j))
        if (i==3):
            l=l.split()
            if l:
                for j in l:
                    prob.append(float(j))

ada = adaboosting(x,y,prob,t,eps,n)
for i in range(0,int(t)):
    print(" ")
    print ("Iteration  "+ str(i))
    ada.realerror()
    #print("      ")

                    
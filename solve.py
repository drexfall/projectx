from math import *
from decimal import Decimal

class Matrix():
    def inverse(value):
        try:
            inverse = []

            for x in range(len(value)):
                row = []
                for y in range(len(value[x])): 
                    if x==y:
                        row.append(1.0)
                    else:
                        row.append(0.0)
                inverse.append(row)

            def convert_to_zero(val,inval):

                zero_val = list(val)
                inv_val  = list(inval)
                for p in range(len(val)):

                    val[p] = Decimal(eval(str(zero_val[p]-(zero_val[index_y]*value[index_x][p]))))
                    inval[p] = Decimal(eval(str(inv_val[p]-(zero_val[index_y]*inverse[index_x][p]))))
                    
                    
            for index_x,x in enumerate(value):
                for index_y,y in enumerate(x):
                    value[index_x][index_y] = Decimal(str(y))
                    inverse[index_x][index_y] = Decimal(str(inverse[index_x][index_y]))
            for index_x,x in enumerate(value):
                for index_y,y in enumerate(x):

                    if index_x == index_y:

                        for z in range(-1,-(1+len(x)),-1):

                            value[index_x][z] = Decimal(eval(str(Decimal(str(value[index_x][z])) / Decimal(str(y)))))
                            inverse[index_x][z] = Decimal(eval(str(Decimal(str(inverse[index_x][z]))/ Decimal(str(y)))))
                            
                        for t in range(len(x)):
                            if t != index_x:
                            
                                convert_to_zero(value[t],inverse[t])
                                
                                
            for x in range(len(value)):
                for y in range(len(value[x])):
                
                    value[x][y] = round(eval(str(value[x][y])),5)
                    inverse[x][y] = round(eval(str(inverse[x][y])),5)

            return inverse
        
        except:
                return "Inverse not possible"
            
    def transpose(value):

        transpose = []

        for x in range(len(value[0])):
            t_row = []
            
            for y in range(len(value)):
                t_row.append(value[y][x])
                
            transpose.append(t_row)
            
        return transpose

    def solve(value1, value2, operator):

        result = []

        if operator in ('+','-'):
            if len(value1) == len(value2) and len(value1[0]) == len(value2[0]):

                for index_x,x in enumerate(value1):
                    result_row = []
                    
                    for index_y,y in enumerate(x):
                        result_row.append(eval(str(y)+operator+str(value2[index_x][index_y])))

                    result.append(result_row)
                    
                return result
            
            else:
                return 'Matricies must be of the same dimensions!'
            
        elif operator == '*':
            if len(value1) == len(value2[0]):
                
                for i in range(len(value1)):
                    result_row = []
                    for x in range(len(value1)):
                        value = ''
                        
                        for y in range(len(value2)):
                            value+=(str(value1[i][index_y])+operator+str(value2[index_y][index_x])+'+')

                        result_row.append(eval(value.rstrip('+')))
                    result.append(result_row)
                        
                return result
            else:
                return 'Number of rows of first Matrix should be equal to number of columns in the second!'
        
class Basic():

    def __new__(cls,equation,rdval=1,base='e'):

        if equation == '':
            return '',''
        e2=[]
        e1=''
        c=0
        for x in equation:
            if x not in ['+','-','÷','x','^','e','π']:
                e1+=x
                
            else:
                e2.append(e1)
                if x=='÷':
                    e2.append('/')
                elif x=='x':
                    e2.append('*')
                elif x=='^':
                    e2.append('**')
                elif x=='π':
                    e2.append(str(pi))
                elif x=='e':
                    if equation[equation.index(x)-1]!='s':
                        e2.append(str(e))
                    else:
                        e2.append(e1+'e')
                        e2.remove('bas')
                else:
                    e2.append(x)
                e1=''
        e2+=[e1]
        
        if len(e2)==0:
            e2.append(equation)
        for y in e2:

            if len(y)==0:
                e2.remove(y)
        for x in e2:
            if x[:4] in ['sin(','cos(','tan('] or x[:5] in ['sinˉ(','cosˉ(','tanˉ(']:
                if rdval==1:
                    e2.insert(e2.index(x),x[:x.index('(')+1])
                
                    e2.insert(e2.index(x),x[x.index('(')+1:])
                    e2.remove(x)
                else:
                    try:
                        e2[e2.index(x)]=str(eval(x))
                    except:
                        pass
                
                
                x=x[4:]
        for x in e2:
            if x in ['sinˉ(','cosˉ(','tanˉ(']:
                e2.insert(e2.index(x),str('a'+x[:3]+'('))
                e2.remove(x)
            elif x[:4]=='log(':
                e2.insert(e2.index(x),str(x[:-1]+','+str(base)+')'))
                e2.remove(x)



        c=0

        for y in e2:

            if y[-1]=='!':

                e2.insert(e2.index(y),'factorial('+y[:-1]+')')
                e2.remove(y)
     
            elif rdval==1:
                if y in ['sin(','cos(','tan(']:
                    e2.insert(e2.index(y),str(y+'radians('))
                    e2.remove(y)
                    c+=1
                elif y in ['asin(','acos(','atan(']:
                    e2.insert(e2.index(y),str('degrees('+y))
                    e2.remove(y)
                    c+=1
                elif y[-c:] == ')'*c:
                    e2.insert(e2.index(y),str(y+')'*c))
                    e2.remove(y)
                    c=0
            try:
                if str(type(eval(y)))=="<class 'float'>":

                    e2[e2.index(y)]=str("Decimal('"+y+"')")
            except:
                pass

        
        for t in range(len(e2)):

            try:
                if ('sin' in e2[t]) or ('cos' in e2[t]) or ('tan' in e2[t]):
                    e2[t]=str(eval(str(e2[t]+e2[t+1])))
                    e2.remove(e2[t+1])

                    r=''
                    rc=0
                    for j in e2[t]:

                        if j==r:
                            rc+=1
                        r=j
                    if rc>=7:
                        e2[t]=str(round(eval(e2[t]),1))
            except:
                pass
        try:
            ans=str(eval(''.join(e2)))
            if "Decimal" in ans:
                ans=ans[:ans.index('(')+2]+ans[:ans.index("'")-1]
            return(ans,''.join(e2))
        except SyntaxError:
            return('Wrong Expression','')
        except ValueError:
            return("Domain's not right",'')
        except TypeError:
            return("Factorial of nothing? Seriously?",'')
        except ArithmeticError:
            return("That's bad math",'')
        except ZeroDivisionError:
            return("Can't divide by nothing!",'')
        except OverflowError:
            return("Too much for me!",'')

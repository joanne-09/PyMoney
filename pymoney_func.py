import datetime as date
import sys


# initialize category list
def initialCate():
    return ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 
            'income', ['salary', 'bonus']]


# initialize money and record if there is something
def initialize():
    try:
        with open('record.txt', 'r') as fh:
            record = fh.readlines()
            record[1:]=list(map(seq, record[1:]))
    except:
        with open('record.txt', 'w') as f:
            f.write('')
            record=[]

    # check if use program for the first time
    if len(record):
        money=int(record.pop(0))
        print("Welcome back!")
    else:
        try: money = int(input("How much money do you have? "))
        except:
            money=0
            print("Invalid value for money. Set to 0 by default.")
    
    return money, record


# function for turning each item in record into tuple
def seq(x):
    try:
        x=int(x)
        return str(x)
    except:
        return tuple(x.split())


# check if specific item is in category
def cateValid(item, cate):
    if item in cate:
        return True
    return False


# add new record
def add(rec, cate):
    try:
        addin=list(map(seq, input("Add some expense or income records with description and amount: ").split(', ')))
        if f'{cur_date.year}{cur_date.month}{cur_date.day}' not in rec:
            rec.append(f'{cur_date.year:04d}{cur_date.month:02d}{cur_date.day:02d}')
        for i in addin:
            if cateValid(i[0], cate):
                # modify money
                rec.append(i)
            else:
                print(f"{i[0]} not in category.")
    except ArithmeticError:
        print("Invalid value for money.\n"
              "Fail to add a record.")
    except:
        print("The format of a record should be like this: meal breakfast -50.\n"
              "Fail to add a record.")
    
    return rec


# view current record
def view(mon, rec, subcate):
    flag=(lambda x: x==11)(len(subcate))

    if flag:
        print("Here's your expense and income records: ")
    else:
        print(f"Here's your expense and income records under category \"{subcate[0]}\": ")
    
    print("Date     Category        Description          Amount\n"
          "======== =============== ==================== ======")
    
    storedate=''
    dateflag=1
    for i in rec:
        if type(i)==tuple:
            if i[0] in subcate:
                # check if if the first time to print date
                if dateflag:
                    print(storedate)
                    dateflag=0
                # print each item in list using join() to join items in tuple 
                print(f'         {i[0]:<15s} {i[1]:<20s} {i[2]:<6s}')
                mon += int(i[2])
        else:
            # if new date occur, set new date
            storedate=i
            dateflag=1

    print("======== =============== ==================== ======")
    if flag:
        print(f"Now you have {mon} dollars.")
    else:
        print(f"The total amount above is {mon}.")


# delete specific record
def delete(mon, rec):
    #try:
    tmp=input("Which record do you want to delete? ").split()
    if len(tmp!=2):
        print("Invalid format. Fail to delete a record.")
        return

    for i in range(len(rec)-1, -1, -1):
        if rec[i][0]==tmp[0] and rec[i][1]==tmp[1]:
            mon -= int(rec[i][1])
            rec.pop(i)
            return
    print(f"There's no record with {tmp[0]} {tmp[1]}. Fail to delete a record.")
    
    return mon, rec


# view all the category using recursion
def viewCate(cate, indent):
    for i in cate:
        if type(i)==str:
            print(' '*indent*2+f'- {i}')
        else:
            viewCate(i, indent+1)


# find subcategory of item in category
def findSubcate(item, cate):
    if type(cate) == list:
        for v in cate:
            p = findSubcate(item, v)
            if p == True:
                # if found, return the flatten list including itself
                # and its subcategories
                index = cate.index(v)
                return flatten(cate[index:index + 2])
            if p != False:
                # p is a list returned from flatten
                return p
    return cate == item


# flatten nested list
def flatten(ls):
    # return a flat list that contains all element in the nested list L
    # for example, flatten([1, 2, [3, [4], 5]]) returns [1, 2, 3, 4, 5]
    returnLs=[]
    for i in ls:
        if type(i)==list:
            returnLs+=flatten(i)
        else:
            returnLs.append(i)
    return returnLs


#save record to file
def save(mon, rec):
    with open('record.txt', 'w') as fh:
        fh.seek(0)
        fh.write(str(mon)+'\n')

        for i in rec:
            if type(i)==tuple:
                    fh.write(f'{i[0]} {i[1]} {i[2]}\n')
            else:
                fh.write(i+'\n')
    print("Bye~")


# main function
money, record = initialize()
category=initialCate()
flatcate=flatten(category)

cur_date=date.datetime.now()
while True:
    op=input("What do you want to do (add/view/delete/view categories/find/exit)? ")

    if op=='add':
        record=add(record, flatcate)
    
    elif op=='view':
        view(money, record, flatcate)
    
    elif op=='delete':
        money, record=delete(money, record)

    elif op=='view categories':
        viewCate(category, 0)
    
    elif op=='find':
        item=input("Which category do you want to find? ")
        sub=findSubcate(item, category)
        view(0, record, sub)

    elif op=='exit':
        save(money, record)
        break
    
    else:
        sys.stderr.write("Invalid command. Please try again.\n")

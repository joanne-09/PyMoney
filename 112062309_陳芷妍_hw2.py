import datetime as date
import sys


#initialize money and record if there is something
def initialize():
    try:
        with open('record.txt', 'r') as fh:
            category = fh.readlines()
            category[1:]=list(map(seq, category[1:]))
    except:
        with open('record.txt', 'w') as f:
            f.write('')
        category=[]
        

    # check if use program for the first time
    if len(category):
        money=int(category.pop(0))
        print("Welcome back!")
    else:
        try: money = int(input("How much money do you have? "))
        except:
            money=0
            print("Invalid value for money. Set to 0 by default.")
    
    return money, category


# function for turning each item in category into tuple
def seq(x) -> str:
    try:
        x=int(x)
        return str(x)
    except:
        return tuple(x.split())


# add new record
def add(mon, temp_c):
    try:
        addin=list(map(seq, input("Add some expense or income records with description and amount: ").split(', ')))
        if f'{cur_date.year}{cur_date.month}{cur_date.day}' not in temp_c:
            temp_c.append(f'{cur_date.year}{cur_date.month}{cur_date.day}')
        for i in addin:
            # modify money
            mon += int(i[1])
            temp_c.append(i)
    except ArithmeticError:
        print("Invalid value for money.\n"
              "Fail to add a record.")
    except:
        print("The format of a record should be like this: breakfast -50.\n"
              "Fail to add a record.")
    
    return mon, temp_c


# view current record
def view(mon, temp_c):
    print("Here's your expense and income records: ")
    print("Date     Description          Amount\n"
          "======== ==================== ======")
        
    for i in temp_c:
        if type(i)==tuple:
            # print each item in list using join() to join items in tuple 
            print(f'         {i[0]:<20s} {i[1]:<6s}')
        else:
            print(i)

    print("======== ==================== ======\n" 
         f"Now you have {mon} dollars.")


# delete specific record
def delete(mon, temp_c):
    try:
        tmp=input("Which record do you want to delete? ").split()
        for i in range(len(temp_c)-1, -1, -1):
            if temp_c[i][0]==tmp[0] and temp_c[i][1]==tmp[1]:
                mon -= int(temp_c[i][1])
                temp_c.pop(i)
                break
    except NameError:
        print(f"There's no record with {tmp[0]} {tmp[1]}. Fail to delete a record.")
    except:
        print("Invalid format. Fail to delete a record.")
    
    return mon, temp_c


#save record to file
def save(mon, temp_c):
    with open('record.txt', 'w') as fh:
        fh.seek(0)
        fh.write(str(mon)+'\n')

        for i in temp_c:
            if type(i)==tuple:
                    fh.write(f'{i[0]} {i[1]}\n')
            else:
                fh.write(i+'\n')
    print("Bye~")


# main function
money, category = initialize()

cur_date=date.datetime.now()
while True:
    op=input("What do you want to do (add/view/delete/exit)? ")

    if op=='add':
        money, category=add(money, category)
    
    elif op=='view':
        view(money, category)
    
    elif op=='delete':
        money, category=delete(money, category)

    elif op=='exit':
        save(money, category)
        break
    
    else:
        sys.stderr.write("Invalid command. Please try again.\n")

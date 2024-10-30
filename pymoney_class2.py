import datetime as date
import sys


def flatten(cate):
    # 1. Define the formal parameters so that this method
    #    can be called recursively.
    # 2. Recursively call self._flatten and return the flat list.
    # 3. (FYI) The method name starts with an underscore to indicate that
    #    it is not intended to be called outside the class.
    # 4. Alternatively, put flatten as an inner function of
    #    find_subcategories.
    
    returnLs=[]
    for i in cate:
        if type(i)==list:
            returnLs+=flatten(i)
        else: returnLs.append(i)
    return returnLs


class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        # 1. Read from 'records.txt' or prompt for initial amount of money.
        # 2. Initialize the attributes (self._records and self._initial_money)
        #    from the file or user input.
        try:
            with open('record.txt', 'r') as fh:
                self._records = fh.readlines()
                self._records[1:]=list(map(self.seq, self._records[1:]))
        except:
            with open('record.txt', 'w') as f:
                f.write('')
                self._records=[]

        # check if use program for the first time
        if len(self._records):
            self._initial_money=int(self._records.pop(0))
            print("Welcome back!")
        else:
            try: self._initial_money = int(input("How much money do you have? "))
            except:
                self._initial_money=0
                print("Invalid value for money. Set to 0 by default.")
        

    # function for turning each item in record into tuple
    def seq(self, x):
        try:
            x=int(x)
            return str(x)
        except:
            return tuple(x.split())


    def add(self, cate):
        # 1. Define the formal parameter so that a string input by the user
        #    representing a record can be passed in.
        # 2. Convert the string into a Record instance.
        # 3. Check if the category is valid. For this step, the predefined
        #    categories have to be passed in through the parameter.
        # 4. Add the Record into self._records if the category is valid.
        try:
            addin=list(map(self.seq, input("Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n").split(', ')))
            if f'{cur_date.year:04d}{cur_date.month:02d}{cur_date.day:02d}' not in self._records:
                self._records.append(f'{cur_date.year:04d}{cur_date.month:02d}{cur_date.day:02d}')
            for i in addin:
                if cate.is_category_valid(i[0]):
                    # check money
                    assert int(i[2])
                    self._records.append(i)
                else:
                    print(f"{i[0]} not in category.")
        except ValueError:
            print("Invalid value for money.\n"
                "Fail to add a record.")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

            print("The format of a record should be like this: meal breakfast -50.\n"
                "Fail to add a record.")


    def view(self):
        # 1. Print all the records and report the balance.
        print("Here's your expense and income records: ")      
        print("Date     Category        Description          Amount\n"
            "======== =============== ==================== ======")
        
        mon=self._initial_money
        storedate=''
        dateflag=1
        for i in self._records:
            if type(i)==tuple:
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
        print(f"Now you have {mon} dollars.")


    def delete(self):
        # 1. Define the formal parameter.
        # 2. Delete the specified record from self._records.
        tmp=input("Which record do you want to delete? ").split()
        if len(tmp) !=3:
            print("Invalid format. Fail to delete a record.")
            return

        for i in range(len(self._records)-1, -1, -1):
            if type(self._records[i])==tuple and self._records[i][0]==tmp[0] and self._records[i][1]==tmp[1] and self._records[i][2]==tmp[2]:
                self._records.pop(i)
                print("Successfully deleted.")
                return
        print(f"There's no record with {tmp[0]} {tmp[1]} {tmp[2]}. Fail to delete a record.")
        

    def find(self, subcate):
        # 1. Define the formal parameter to accept a non-nested list
        #    (returned from find_subcategories)
        # 2. Print the records whose category is in the list passed in
        #    and report the total amount of money of the listed records.
        print(f"Here's your expense and income records under category \"{subcate[0]}\": ")      
        print("Date     Category        Description          Amount\n"
            "======== =============== ==================== ======")
        
        mon=0
        storedate=''
        dateflag=1
        for i in self._records:
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
        print(f"Now you have {mon} dollars.")
    

    def save(self):
        # 1. Write the initial money and all the records to 'records.txt'.
        with open('record.txt', 'w') as fh:
            fh.seek(0)
            fh.write(str(self._initial_money)+'\n')

            for i in self._records:
                if type(i)==tuple:
                        fh.write(f'{i[0]} {i[1]} {i[2]}\n')
                else:
                    fh.write(i+'\n')
        print("Bye~")


class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        # 1. Initialize self._categories as a nested list.
        self._categories=['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 
                          'income', ['salary', 'bonus']]


    def view(self):
        # 1. Define the formal parameters so that this method
        #    can be called recursively.
        # 2. Recursively print the categories with indentation.
        # 3. Alternatively, define an inner function to do the recursion.
        iniCate=self._categories
        def viewCur(cate, indent=0):
            for i in cate:
                if type(i)==str:
                    print(' '*indent*2+f'- {i}')
                else:
                    viewCur(i, indent+1)
        
        viewCur(iniCate)


    def is_category_valid(self, item):
        # 1. Define the formal parameters so that a category name can be
        #    passed in and the method can be called recursively.
        # 2. Recursively check if the category name is in self._categories.
        # 3. Alternatively, define an inner function to do the recursion.
        flat=flatten(self._categories)
        if item in flat:
            return 1
        return 0


    def findSubcate(self, item):
        # 1. Define the formal parameters so that a category name can be
        #    passed in and the method can be called recursively.
        # 2. Recursively find the target category and call the
        #    self._flatten method to get the subcategories into a flat list.
        # 3. Alternatively, define an inner function to do the recursion.
        iniCate=self._categories
        def findSubGen(item, cate, found=False):
            if type(cate) == list:
                for index, child in enumerate(cate):
                    yield from findSubGen(item, child, found)
                    if child==item and index+1<len(cate) \
                        and type(cate[index+1])==list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from findSubGen(item, cate[index+1], True)
            else:
                if cate == item or found:
                    yield cate
        
        ret=findSubGen(item,iniCate)
        return ret


categories = Categories()
records = Records()
cur_date=date.datetime.now()

while True:
    op = input('\nWhat do you want to do (add/view/delete/view categories/find/exit)? ')

    if op=='add':
        records.add(categories)

    elif op=='view':
        records.view()

    elif op=='delete':
        records.delete()

    elif op=='view categories':
        categories.view()

    elif op=='find':
        category = input('Which category do you want to find? ')
        target_categories = categories.findSubcate(category)
        records.find(list(target_categories))

    elif op=='exit':
        records.save()
        break

    else:
        sys.stderr.write('Invalid command. Try again.\n')
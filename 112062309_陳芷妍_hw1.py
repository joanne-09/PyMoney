money = int(input("How much money do you have? "))
category, amount = input("Add an expense or income record with description and amount: ").split()
amount = int(amount)
print(f"Now you have {money+amount} dollars.")

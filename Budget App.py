class Category:
    
    '''Initialise data members'''
    def __init__(self, description):
        # Description
        self.description = description
        # List of descriptions and amount
        self.ledger = []
        # Initial Balance
        self.__balance = 0.0

    '''String output of ledger'''
    def __repr__(self):
        # Centered header
        header = self.description.center(30, "*") + "\n"
        # Append ledger items to string
        ledger = ""
        
        for item in self.ledger:
            # Left align description + max 23 spaces
            line_description = "{:<23}".format(item["description"])
            # Right align amount, 2dp, + max 7 spaces
            line_amount = "{:>7.2f}".format(item["amount"])
            # Truncate ledger description and amount to 23 and 7 characters respectively
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return header + ledger + total

    '''Take in deposit'''
    def deposit(self, amount, description=""):
        # Append ledger list with amt and descr
        self.ledger.append({"amount": amount, "description": description})
        # Add to balance
        self.__balance += amount

    '''Similar to above'''
    def withdraw(self, amount, description=""):
        # If balance >= amount, remove from ledger list, adjust balance, return True
        if self.__balance - amount >= 0:
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.__balance -= amount
            return True
        else:
            return False

    '''Get balance'''
    def get_balance(self):
        return self.__balance

    '''Transfer funds from one category to another'''
    def transfer(self, amount, category_instance):
        # If category exists, withdraw amount and deposit in (new) category
        if self.withdraw(amount, "Transfer to {}".format(category_instance.description)):
            category_instance.deposit(amount, "Transfer from {}".format(self.description))
            return True
        else:
            return False

    '''Check funds'''
    def check_funds(self, amount):
        if self.__balance >= amount:
            return True
        else:
            return False


def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.description, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")

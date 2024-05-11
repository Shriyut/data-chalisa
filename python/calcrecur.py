def addition(num1, num2):
    return float(num1) + float(num2)


def subtract(num1, num2):
    return float(num1) - float(num2)


def multiply(num1, num2):
    return float(num1) * float(num2)


def divide(num1, num2):
    if float(num2) == 0.0:
        raise ArithmeticError("Division by 0 is not supported")
    return float(num1) / float(num2)


def calculate(num1, num2, operation):
    if (operation == "+"):
        print(addition(num1, num2))
    if (operation == "-"):
        print(subtract(num1, num2))
    if (operation == "*"):
        print(multiply(num1, num2))
    if (operation == "/"):
        print(divide(num1, num2))


def executor():
    userInput = input("Enter Y to continue or N to exit")

    if userInput == "Y" or userInput == "y":
        num1 = input("First number")
        num2 = input("Second number")
        operation = input("Operation")
        calculate(num1, num2, operation)
        executor()
    elif userInput == "N" or userInput == "n":
        print("graceful exit")
    else:
        print("Invalid input provided please press Y or N")
        executor()


def main():
    print("//////////////CALCULATOR//////////////")
    # calculate()
    executor()


if __name__ == "__main__":
    main()

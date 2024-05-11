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


def main():
    print("//////////////Calculator//////////////")
    num1 = input("Enter first number")
    num2 = input("Enter second number")
    operation = input("Enter operation type")
    if operation == "+":
        print(addition(num1, num2))
    elif operation == "-":
        print(subtract(num1, num2))
    elif operation == "*":
        print(multiply(num1, num2))
    elif operation == "/":
        print(divide(num1, num2))
    else:
        print("Invalid operation")


if __name__ == "__main__":
    main()

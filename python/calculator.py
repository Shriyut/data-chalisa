
def main():
    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")
    operation = input("Enter operation type: ")

    result = ""
    try:
        if operation == "+" or operation == "ADD":
            result = float(num1)+float(num2)
        elif operation == "-" or operation == "SUBTRACT":
            result = float(num1) - float(num2)
        elif operation == "/" or operation == "DIVIDE":
            result = float(num1)/float(num2)
        elif operation == "*" or operation == "MULTIPLY":
            result = float(num1) * float(num2)
        else:
            print("Enter a valid operation i.e. add, subtract, multiply, divide")
    except Exception as e:
        print("Error while executing "+str(e))
    finally:
        print(result)


if __name__=="__main__":
     main()

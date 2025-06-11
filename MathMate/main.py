class MathMate:
    def __init__(self):
        self.name = "MathMate"
        print(f"Welcome to {self.name} - Your personal math assistant!")

    def menu(self):
        print("\nChoose an operation:")
        print("1. Add numbers")
        print("2. Subtract numbers")
        print("3. Multiply numbers")
        print("4. Divide numbers")
        print("5. Exit")

    def add(self):
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = num1 + num2
            print(f"The result is: {result}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def subtract(self):
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = num1 - num2
            print(f"The result is: {result}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def multiply(self):
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = num1 * num2
            print(f"The result is: {result}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def divide(self):
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            if num2 == 0:
                print("Cannot divide by zero!")
            else:
                result = num1 / num2
                print(f"The result is: {result}")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def run(self):
        while True:
            self.menu()
            choice = input("Enter your choice (1-5): ")
            if choice == '1':
                self.add()
            elif choice == '2':
                self.subtract()
            elif choice == '3':
                self.multiply()
            elif choice == '4':
                self.divide()
            elif choice == '5':
                print(f"Thank you for using {self.name}. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")

# Main program
if __name__ == "__main__":
    math_mate = MathMate()
    math_mate.run()

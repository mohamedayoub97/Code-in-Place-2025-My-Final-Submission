class QuantumCalc:
    def __init__(self):
        self.running = True

    def start(self):
        print("Welcome to QuantumCalc! A Physics Console for all your calculations!")
        print("Type 'exit' to quit anytime.")
        while self.running:
            self.display_menu()

    def display_menu(self):
        print("\nSelect a calculation or option:")
        print("1. Force (F = ma)")
        print("2. Kinetic Energy (KE = 0.5 * m * v^2)")
        print("3. Work (W = F * d)")
        print("4. Potential Energy (PE = m * g * h)")
        print("5. Learn about Famous Physicists")
        print("6. Exit")
        
        choice = input("Enter choice: ")

        if choice == '1':
            self.calculate_force()
        elif choice == '2':
            self.calculate_kinetic_energy()
        elif choice == '3':
            self.calculate_work()
        elif choice == '4':
            self.calculate_potential_energy()
        elif choice == '5':
            self.learn_about_physicists()
        elif choice == '6' or choice.lower() == 'exit':
            self.running = False
            print("Exiting QuantumCalc. Stay curious!")
        else:
            print("Invalid choice. Try again.")

    def calculate_force(self):
        try:
            mass = float(input("Enter mass (in kg): "))
            acceleration = float(input("Enter acceleration (in m/s^2): "))
            force = mass * acceleration
            print(f"Force = {force} N")
        except ValueError:
            print("Invalid input! Please enter numeric values.")

    def calculate_kinetic_energy(self):
        try:
            mass = float(input("Enter mass (in kg): "))
            velocity = float(input("Enter velocity (in m/s): "))
            kinetic_energy = 0.5 * mass * velocity ** 2
            print(f"Kinetic Energy = {kinetic_energy} J")
        except ValueError:
            print("Invalid input! Please enter numeric values.")

    def calculate_work(self):
        try:
            force = float(input("Enter force (in N): "))
            distance = float(input("Enter distance (in meters): "))
            work = force * distance
            print(f"Work = {work} J")
        except ValueError:
            print("Invalid input! Please enter numeric values.")

    def calculate_potential_energy(self):
        try:
            mass = float(input("Enter mass (in kg): "))
            height = float(input("Enter height (in meters): "))
            gravity = 9.81  # Acceleration due to gravity in m/s^2
            potential_energy = mass * gravity * height
            print(f"Potential Energy = {potential_energy} J")
        except ValueError:
            print("Invalid input! Please enter numeric values.")

    def learn_about_physicists(self):
        print("\nChoose a famous physicist to learn about:")
        print("1. Albert Einstein")
        print("2. Isaac Newton")
        print("3. Marie Curie")
        print("4. Nikola Tesla")
        print("5. Galileo Galilei")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            self.einstein_bio()
        elif choice == '2':
            self.newton_bio()
        elif choice == '3':
            self.curie_bio()
        elif choice == '4':
            self.tesla_bio()
        elif choice == '5':
            self.galileo_bio()
        else:
            print("Invalid choice. Try again.")

    def einstein_bio(self):
        print("\nAlbert Einstein (1879–1955):")
        print("A theoretical physicist, best known for the theory of relativity, which revolutionized our understanding of space, time, and gravity.")
        print("He won the Nobel Prize in Physics in 1921 for his explanation of the photoelectric effect, and his equation E=mc² is one of the most famous equations in physics.")
        print("Einstein's work led to the development of quantum mechanics, and his ideas continue to influence modern physics today.")

    def newton_bio(self):
        print("\nIsaac Newton (1642–1727):")
        print("An English mathematician, astronomer, and physicist, widely recognized as one of the most influential scientists in history.")
        print("He is best known for formulating the laws of motion and universal gravitation, which laid the foundation for classical mechanics.")
        print("His work in optics, calculus, and the formulation of his 'Principia Mathematica' marked a major milestone in scientific thought.")

    def curie_bio(self):
        print("\nMarie Curie (1867–1934):")
        print("A pioneering physicist and chemist, Curie was the first woman to win a Nobel Prize, and the only woman to win Nobel Prizes in two different fields: Physics (1903) and Chemistry (1911).")
        print("She is best known for her discovery of the elements radium and polonium, and her work on radioactivity, which has had a lasting impact on both science and medicine.")
        print("Curie’s research helped develop radiation therapy for cancer treatment and opened doors for further studies in nuclear physics.")

    def tesla_bio(self):
        print("\nNikola Tesla (1856–1943):")
        print("A Serbian-American inventor, electrical engineer, mechanical engineer, and futurist, known for his contributions to the development of alternating current (AC) electrical systems.")
        print("Tesla’s innovations include the Tesla coil, induction motor, and the development of wireless transmission of energy, influencing modern electrical engineering.")
        print("His work laid the foundation for much of today's electrical power generation and distribution technology.")

    def galileo_bio(self):
        print("\nGalileo Galilei (1564–1642):")
        print("An Italian astronomer, physicist, and engineer, known for his advancements in observational astronomy and the development of the scientific method.")
        print("Galileo made groundbreaking improvements to the telescope, discovered Jupiter’s moons, and supported the heliocentric model of the solar system, challenging long-held views of the time.")
        print("His work in mechanics, motion, and astronomy paved the way for the scientific revolution.")

if __name__ == "__main__":
    quantum_calc = QuantumCalc()
    quantum_calc.start()

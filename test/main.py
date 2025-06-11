import random
import textwrap

# Store detailed bios of famous physicists
physicists = {
    "Albert Einstein": {
        "bio": """Albert Einstein (1879–1955) was a theoretical physicist best known for developing the theory of relativity,
which revolutionized our understanding of space, time, and gravity. His equation E=mc², expressing the equivalence of
mass and energy, is one of the most famous formulas in physics. He received the Nobel Prize in 1921 for his work on the
photoelectric effect, which laid the foundation for quantum theory.""",
        "quote": "Imagination is more important than knowledge.",
        "famous_work": "Theory of Relativity",
        "equation": "E = mc²"
    },
    "Isaac Newton": {
        "bio": """Sir Isaac Newton (1643–1727) was an English physicist and mathematician who laid the foundations of classical mechanics
with his laws of motion and universal gravitation. He also made significant contributions to optics and invented calculus
(independently of Leibniz). His book 'Philosophiæ Naturalis Principia Mathematica' is a cornerstone of physics.""",
        "quote": "If I have seen further it is by standing on the shoulders of giants.",
        "famous_work": "Laws of Motion & Universal Gravitation",
        "equation": "F = ma"
    },
    "Marie Curie": {
        "bio": """Marie Curie (1867–1934) was a pioneering physicist and chemist who conducted groundbreaking research on radioactivity.
She was the first woman to win a Nobel Prize and the only person to win Nobel Prizes in two different scientific fields
(Physics and Chemistry). Her work led to the development of X-ray machines and advanced the understanding of atomic structure.""",
        "quote": "Nothing in life is to be feared, it is only to be understood.",
        "famous_work": "Radioactivity",
        "equation": "Discovery of Polonium and Radium"
    },
    "Stephen Hawking": {
        "bio": """Stephen Hawking (1942–2018) was a British theoretical physicist known for his work on black holes and cosmology.
He proposed that black holes emit radiation (now called Hawking Radiation), changing how we view them fundamentally.
His book 'A Brief History of Time' brought complex physics to a general audience and became a bestseller.""",
        "quote": "Intelligence is the ability to adapt to change.",
        "famous_work": "Hawking Radiation & Black Hole Thermodynamics",
        "equation": "S = k * A / (4 * l_p²)"
    }
}

def wrap_text(text):
    return textwrap.fill(text, width=80)

def show_menu():
    print("\n🌌 Welcome to CosmoScope – The Universe in Numbers 🌌")
    print("Explore the minds that shaped the universe.")
    print("\nOptions:")
    print("1. View list of famous physicists")
    print("2. Learn about a specific physicist")
    print("3. Get a random physics fact")
    print("4. Exit")

def list_physicists():
    print("\n👨‍🔬 Available Physicists:")
    for name in physicists:
        print(f"- {name}")

def show_physicist(name):
    if name in physicists:
        data = physicists[name]
        print(f"\n📘 {name} – {data['famous_work']}")
        print("\n🧬 Biography:")
        print(wrap_text(data["bio"]))
        print("\n💬 Famous Quote:")
        print(f'"{data["quote"]}"')
        print("\n🔬 Signature Equation or Discovery:")
        print(f"{data['equation']}")
    else:
        print("Physicist not found. Please enter a correct name from the list.")

def random_fact():
    name = random.choice(list(physicists.keys()))
    data = physicists[name]
    print(f"\n🔭 Random Physics Spotlight: {name}")
    print(f"📚 Did you know? {wrap_text(data['bio'].split('.')[0] + '.')}")

def cosmoscope():
    while True:
        show_menu()
        choice = input("\nChoose an option (1-4): ")
        if choice == "1":
            list_physicists()
        elif choice == "2":
            name = input("Enter the full name of the physicist: ")
            show_physicist(name)
        elif choice == "3":
            random_fact()
        elif choice == "4":
            print("\n🌠 Thank you for exploring the cosmos with CosmoScope!")
            break
        else:
            print("Invalid choice. Please select from 1 to 4.")

if __name__ == "__main__":
    cosmoscope()

def main_menu():
  print("\n--- Bromine Synthesis Calculator ---")
  print("Select a synthesis method:")
  print("1. Oxidation with Chlorine (Cl₂)")
  print("2. Oxidation with Sulfuric Acid and MnO₂")
  print("3. Exit")
  return input("Enter your choice (1-3): ")

def calculate_chlorine_method():
  print("\n--- Bromine Production Using Chlorine ---")
  try:
      moles_nabr = float(input("Enter the amount of NaBr (moles): "))
      print("\nReaction: 2 NaBr + Cl₂ → Br₂ + 2 NaCl")

      # Stoichiometry
      moles_br2 = moles_nabr / 2  # 2 moles of NaBr produce 1 mole of Br2
      moles_cl2 = moles_br2       # 1 mole of Cl2 is needed for 1 mole of Br2

      print(f"To produce {moles_br2:.2f} moles of bromine (Br₂):")
      print(f"- You need {moles_cl2:.2f} moles of chlorine (Cl₂).")
  except ValueError:
      print("Invalid input. Please enter a numerical value.")

def calculate_sulfuric_acid_method():
  print("\n--- Bromine Production Using MnO₂ and H₂SO₄ ---")
  try:
      moles_nabr = float(input("Enter the amount of NaBr (moles): "))
      print("\nReaction: 2 NaBr + MnO₂ + 3 H₂SO₄ → Br₂ + MnSO₄ + Na₂SO₄ + 2 H₂O")

      # Stoichiometry
      moles_br2 = moles_nabr / 2  # 2 moles of NaBr produce 1 mole of Br2
      moles_mno2 = moles_br2      # 1 mole of MnO2 for 1 mole of Br2
      moles_h2so4 = moles_br2 * 3 # 3 moles of H2SO4 for 1 mole of Br2

      print(f"To produce {moles_br2:.2f} moles of bromine (Br₂):")
      print(f"- You need {moles_mno2:.2f} moles of manganese dioxide (MnO₂).")
      print(f"- You need {moles_h2so4:.2f} moles of sulfuric acid (H₂SO₄).")
  except ValueError:
      print("Invalid input. Please enter a numerical value.")

def main():
  while True:
      choice = main_menu()
      if choice == "1":
          calculate_chlorine_method()
      elif choice == "2":
          calculate_sulfuric_acid_method()
      elif choice == "3":
          print("Exiting the calculator. Goodbye!")
          break
      else:
          print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
  main()

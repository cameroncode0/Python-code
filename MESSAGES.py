def print_messages(count, message1, message2, save_to_file):
    output = []
    for i in range(1, count + 1):
        output.append(f"{i}. {message1}")
        output.append(f"{i}. {message2}")

    if save_to_file:
        with open("messages_output.txt", "w") as file:
            file.write("\n".join(output))
        print("Messages saved to 'messages_output.txt'.")
    else:
        print("\n".join(output))

def main():
    print("Welcome to the Custom Message Printer!")
    try:
        count = int(input("Enter the number of times to print the messages: "))
        message1 = input("Enter the first message: ")
        message2 = input("Enter the second message: ")
        save_option = input("Would you like to save the output to a file? (yes/no): ").strip().lower()
        save_to_file = save_option == "yes"

        print_messages(count, message1, message2, save_to_file)
    except ValueError:
        print("Invalid input. Please enter a numerical value for the count.")

if __name__ == "__main__":
    main()

from chatbot import get_property_response

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = get_property_response(question)

    print("\nAI:")
    print(answer)
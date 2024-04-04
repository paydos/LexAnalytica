from model import ExpertAgent


def main():
    agent = ExpertAgent(api_key="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", model_name="gpt-4-turbo-preview")
    
    while True:
        user_input = input("You: ")  # Get input from the user

        agent.chat(user_input)

if __name__ == "__main__":
    main()

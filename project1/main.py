# imports a high-level framework that allows us to build AI apps
from langchain_core.messages import HumanMessage
# allows us to use the OpenAI API to generate text
from langchain_openai import ChatOpenAI
#  allows us to create tools that the AI can use
from langchain.tools import tool
# allows us to create agents that can use tools to solve problems
from langgraph.prebuilt import create_react_agent
# allows us to load environment variables from a .env file
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Decorator to define a tool that the AI can use
@tool
def calculator(a: float, b: float) -> float:
    """A simple calculator that adds two numbers."""
    print("The calculator has been called.")  # Print a message indicating the calculation being performed
    return f"The sum of {a} and {b} is {a + b}."


def main():
    model = ChatOpenAI(temperature=0)  # Create an instance of the OpenAI chat model with a temperature of 0 (no randomness)

    tools = [calculator]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm your AI assistant. Type 'exit' to quit.")
    print("How can I assist you today?")


    while True:
        user_input = input("You: ").strip() # .strinp() removes any leading or trailing whitespace from the user's input
        
        # Check if the user wants to exit the program
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        print("\nAssistant:", end="")  # Print "Assistant:" without the default newline at the end

        # Stream the response from the agent executor and print it in real-time (types word by word)
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            # Check if the chunk contains an "agent" key and if it has "messages"
            if "agent" in chunk and "messages" in chunk["agent"]:
                # Loop through each message in the agent's messages and print its content
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()  



if __name__ == "__main__":
    main()
# Run commands in terminal:
# uv add langgraph langchain python-dotenv langchain-openai
# uv run main.py
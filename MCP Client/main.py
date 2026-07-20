from agent import Agent

agent = Agent()

while True:
    question = input("You: ")
    print()
    print("Assistant:")
    print(agent.chat(question))
    print()
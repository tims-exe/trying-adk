import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner 
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_sync

load_dotenv()

# initialize persistent session storage
db_url = "sqlite:///./agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# define initial state
initial_state = {
    "user_name": "Tim",
    "reminders": [],
}


async def main_async():
    APP_NAME = "Memory Agent"
    USER_ID = "tims"

    # session management : find or create
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # if there is an existing session, use it, else create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session {SESSION_ID}")

    else:
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state = initial_state,
        )
        SESSION_ID = new_session.id 
        print(f"Created new session : {SESSION_ID}")


    # agent runner setup
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )


    # interactive conversation loop
    print("\nWelcome to Memory Agent Chat !")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation\n")

    while True:
        user_input = input("You : ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation, Your data has been saved")
            break
        
        # process the user query through the agent
        await call_agent_sync(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())
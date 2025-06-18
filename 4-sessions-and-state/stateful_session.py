import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Tim",
    "user_preference": """
    I like to play Football and Basketball.
    My favourite food is Pizza.
    My favourite anime is Attack on Titan.
    Loves to code
    """
}


APP_NAME = "Tim Bot"
USER_ID = "tims"
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

print("CREATED NEW SESSION:")
print(f"\tSession ID : {SESSION_ID}")


runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)


new_message = types.Content(
    role="user",
    parts=[types.Part(text="What is Tim's favourite Anime")]
)


for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)

print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key} : {value}")


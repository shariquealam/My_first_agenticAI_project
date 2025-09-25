import asyncio
import os

from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from framework.agentFactory import AgentFactory

os.environ[
    "OPENAI_API_KEY"] = ""


async def main():
    model_client = OpenAIChatCompletionClient( model="gpt-4o" )
    factory = AgentFactory( model_client )
    read_sheet_id = "d/1xCWlivIgST8-XbH3Gi3OD9HjimdSB-F_gpEnz0l4p7Y"
    write_sheet_id = "d/1AXPYRnZoQX0HCKx92eOgI6bdIO0M6b7JD4nUHadctZc"


    google_sheet_agent = factory.create_google_sheet_agent(system_message="You are a Google Sheets agent. You can read and write data to spreadsheets.")


    # Example read
    google_read_sheet_agent = google_sheet_agent.step(f"""
        You are an google Sheet Reader.

        Your task:
        1. Open google sheet, sheet_id = {read_sheet_id}
        2. Extract all the test cases.
        3. Pass these test cases to the playwrite agent for execution.
        When ready, write: "TEST_DATA_READY", Playwrite Agent should proceed next"
    """)



    playwrite_agent = factory.create_playwrite_agent(system_message=("""
                You are a Playwright automation expert.ONLY proceed when Google Sheet Read Agent has completed testing

                Your task:
                1. Wait for Google Sheet Read Agent to complete with "TEST_DATA_READY" message
                2. Take the test cases from Google Sheet Read Agent and execute each test cases one by one
                3. When the execution is complete, create a message "EXECUTION_COMPLETED"
                Google Sheet Write Agent should proceed next"
                """))




    google_write_sheet_agent = google_sheet_agent.step(f"""
            You are an google Sheet writer.

            Your task:
            1. Wait for Playwrite Agent to complete with "EXECUTION_COMPLETED" message.
            2. Write the test execution result in the sheetID = {write_sheet_id}
            2. Create a google sheet adding the test execution result in the given Sheet ID.
        """)



    team = RoundRobinGroupChat( participants=[google_read_sheet_agent, playwrite_agent, google_write_sheet_agent],
                                termination_condition=TextMentionTermination( "REGISTRATION PROCESS COMPLETE" ) )

    task_result = await Console( team.run_stream( task="Execute Sequential Google search Process:\n\n"

                                                       "STEP 1 - GoogleSheetReadAgent (FIRST):\n"
                                                       "Get all the test cases from the given google sheet and pass to PlaywriteAgent\n\n"

                                                       "STEP 2 - PlaywriteAgent:\n"
                                                       "Execute all the test cases received from GoogleSheetReadAgent.\n\n"

                                                       "STEP 3 - GoogleSheetWriteAgent:\n"
                                                       "Once the execution is completed, updated the given google sheet with the test result.\n\n"

                                                       "Each agent should complete their work fully before the next agent begins. "
                                                       "Pass data clearly between agents using the specified formats." ) )
    final_message = task_result.messages[-1]
    final_message.content





asyncio.run( main() )

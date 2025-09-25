from openai import OpenAI
from autogen_agentchat.agents import AssistantAgent

from framework.mcp_config import McpConfig
from framework.googleOperation import GoogleOperation


class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client
        self.mcp_config = McpConfig()
        self.google_operation = GoogleOperation()

    def create_database_agent(self, system_message):
        database_agent = AssistantAgent( name="DatabaseAgent", model_client=self.model_client,
                                         workbench=self.mcp_config.get_mysql_workbench(),
                                         system_message=system_message )
        return database_agent

    def create_api_agent(self,system_message):
        rest_api_workbench = self.mcp_config.get_rest_api_workbench()
        file_system_workbench = self.mcp_config.get_filesystem_workbench()

        api_agent = AssistantAgent(name="APIAgent",model_client=self.model_client,
                                   workbench=[rest_api_workbench, file_system_workbench],

                                   system_message=system_message)
        return api_agent

    def create_playwrite_agent(self, system_message):
        playwrite_workbench = self.mcp_config.get_playwrite_workbench()
        playwrite_agent = AssistantAgent(name="PlaywriteAgent", model_client=self.model_client,
                                        workbench=playwrite_workbench,
                                        system_message=system_message)
        return playwrite_agent

    def create_excel_agent(self, system_message=None):
        """Create an Excel agent with custom system message"""
        excel_workbench = self.mcp_config.get_excel_workbench()

        return AssistantAgent(
            name="ExcelAgent",
            model_client=self.model_client,
            workbench=excel_workbench,
            system_message=system_message
        )


    def google_sheet_agent(self, prompt, sheet_id):
        # Ask LLM what to do
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI agent that manages Google Sheets."},
                {"role": "user", "content": prompt}
            ]
        )
        action = response.choices[0].message.content
        # action = response["choices"][0]["message"]["content"]

        # Example: parse LLM output (could be JSON or structured text)
        if "read" in action:
            # return self.google_operation.read_sheet(sheet_id, "Sheet1!A1:C5")
            return self.google_operation.read_sheet(sheet_id)
        elif "write" in action:
            # return self.google_operation.write_sheet(sheet_id, "Sheet1!A2", [["AI wrote this"]])
            return self.google_operation.write_sheet(sheet_id, [["AI wrote this"]])
        else:
            return "No valid action"


    ## Google Sheet Read Agent ###
    # def google_sheet_agent(self,system_message=None):
    #     return AssistantAgent(
    #         name="GoogleSheetAgent",
    #         model_client=self.model_client,
    #         system_message=system_message
    #     )



        # action = response["choices"][0]["message"]["content"]
        #
        # # Example: parse LLM output (could be JSON or structured text)
        # if "read" in action:
        #     return self.google_operation.read_sheet(sheet_id, "Sheet1!A1:C5")
        # elif "write" in action:
        #     return self.google_operation.write_sheet(sheet_id, "Sheet1!A2", [["AI wrote this"]])
        # else:
        #     return "No valid action"



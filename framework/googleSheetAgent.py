# from autogen import AssistantAgent
from autogen import AssistantAgent
# from autogen_agentchat.agents import AssistantAgent

from googleOperation import read_sheet, write_sheet

class GoogleSheetAgent(AssistantAgent):
    def __init__(self, name, sheet_id, **kwargs):
        super().__init__(name=name, **kwargs)
        self.sheet_id = sheet_id

    def handle_message(self, message):
        content = message["content"].lower()

        if "read" in content:
            return {"content": str(read_sheet(self.sheet_id, "Sheet1!A1:C10"))}

        if "write" in content:
            write_sheet(self.sheet_id, "Sheet1!A2", [["AI Agent", "Wrote this!"]])
            return {"content": "✅ Data written to Google Sheet."}

        return {"content": "I only support 'read' or 'write' operations."}

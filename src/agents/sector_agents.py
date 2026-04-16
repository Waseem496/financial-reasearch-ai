class BaseAgent:
    def get_context(self):
        return ""

class ITAgent(BaseAgent):
    def get_context(self):
        return "Focus on IT services, software companies, AI trends, outsourcing, cloud."

class PharmaAgent(BaseAgent):
    def get_context(self):
        return "Focus on pharma companies, drug pipelines, R&D, regulations, approvals."
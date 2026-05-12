from __future__ import annotations


class BaseAgent:
    name = 'general'

    def run(self, payload: dict) -> dict:
        return {'message': 'task completed', 'payload': payload}


class ResearchAgent(BaseAgent):
    name = 'research'

    def run(self, payload: dict) -> dict:
        topic = payload.get('topic', 'unknown')
        return {'summary': f'researched topic: {topic}'}


class AnalysisAgent(BaseAgent):
    name = 'analysis'

    def run(self, payload: dict) -> dict:
        return {'analysis': 'completed', 'input_keys': list(payload.keys())}


class ReportingAgent(BaseAgent):
    name = 'reporting'

    def run(self, payload: dict) -> dict:
        return {'report': 'generated', 'sections': payload.get('sections', [])}


AGENTS = {
    'general': BaseAgent(),
    'research': ResearchAgent(),
    'analysis': AnalysisAgent(),
    'reporting': ReportingAgent(),
}


def get_agent(name: str) -> BaseAgent:
    return AGENTS.get(name, AGENTS['general'])

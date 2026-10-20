"""Learner workspace. Keep the runtime and transport boundaries unchanged."""
from lab.contracts import HarnessError


class StudentPlanner:
    evidence_label = "student_scripted_planner"

    async def propose(self, request, timeout):
        """Return {"proposal": <proposal object>, "metadata": {...}}.

        request contains ticket, catalog, observations, and output_schema.
        Begin by returning one lookup proposal. On the next call inspect the
        observation and propose a supported completion. Do not call a tool here.
        This exercise is deterministic Python; label it as such.
        """
        raise HarnessError("student_incomplete", "Implement StudentPlanner.propose after predicting the trace.")

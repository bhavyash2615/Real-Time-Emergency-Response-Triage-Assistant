import json


class ContextBuilder:

    def __init__(self):
        pass

    def build_context(self, current_issue, pruned_history, protocols):
        """
        Build optimized context for reasoning
        """

        context = {}

        # -------------------------
        # Patient Context
        # -------------------------
        context["patient"] = {
            "age": pruned_history.get("age"),
            "gender": pruned_history.get("gender"),
            "diagnoses": pruned_history.get("relevant_diagnoses", []),
            "medications": pruned_history.get("relevant_medications", [])
        }

        # -------------------------
        # Current Issue
        # -------------------------
        context["current_issue"] = current_issue

        # -------------------------
        # Protocol Context
        # -------------------------
        protocol_context = []

        for p in protocols:

            protocol_context.append({
                "disease": p.get("disease"),
                "triage_level": p.get("triage_level"),
                "key_symptoms": p.get("symptoms", [])[:5],
                "medication": p.get("medication", [])[:3],
                "steps": p.get("steps", [])[:5]
            })

        context["protocols"] = protocol_context

        return context


    def compress_context(self, context):
        """
        Simple scaledown-style compression
        Remove unnecessary verbosity
        """

        compressed = json.dumps(context)

        return compressed

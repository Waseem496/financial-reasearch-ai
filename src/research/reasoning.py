class ResearchReasoner:

    def should_continue(self, step_number: int, max_steps: int = 8) -> bool:
        return step_number < max_steps


    def refine_query(self, query: str, previous_results: list):

        if not previous_results:
            return query + " latest data 2024 2025"

        last = previous_results[-1].lower()

        if "growth" in last:
            return query + " CAGR growth rate data"

        if "ai" in last:
            return query + " AI adoption impact statistics"

        if "risk" in last:
            return query + " risks challenges analysis"

        return query + " financial analysis"


    def generate_followups(self, base_query: str, insights: list, context: str):
        """
        🔥 CORE INTELLIGENCE: Generate next research directions
        """

        followups = []

        for insight in insights:

            text = insight.lower()

            if "growth" in text or "increase" in text:
                followups.append(f"{base_query} growth drivers and CAGR analysis")

            if "decline" in text or "risk" in text or "challenge" in text:
                followups.append(f"{base_query} risk factors and challenges")

            if "ai" in text or "automation" in text:
                followups.append(f"{base_query} AI impact and future opportunities")

            if "market" in text:
                followups.append(f"{base_query} market size forecast and trends")

            if "company" in text or "tcs" in text or "infosys" in text:
                followups.append(f"{base_query} company comparison financial performance")

        # fallback (important)
        if not followups:
            followups.append(f"{base_query} future outlook 2025")

        return list(set(followups))[:2]
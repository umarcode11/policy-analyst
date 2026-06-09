# Custom Tool: Claim Confidence Scorer
# This tool takes a claim and evidence snippets and scores
# how well the evidence supports or contradicts the claim.

def score_claim_confidence(claim: str, evidence: str) -> str:
    """
    Custom-built tool that scores how well evidence supports a claim.
    Returns a confidence level: HIGH, MEDIUM, LOW, or CONTRADICTED.
    This is the custom tool built for the Policy Analyst project.
    """

    if not claim or not evidence:
        return "SCORE: UNKNOWN | Reason: Missing claim or evidence."

    claim_lower = claim.lower()
    evidence_lower = evidence.lower()

    # Keywords that suggest strong support
    support_keywords = [
        "confirmed", "verified", "approved", "increased", "achieved",
        "successfully", "report shows", "data shows", "according to",
        "official", "announced", "signed", "passed", "launched"
    ]

    # Keywords that suggest contradiction
    contradict_keywords = [
        "denied", "false", "incorrect", "disputed", "rejected",
        "contradicts", "no evidence", "misleading", "fake", "unverified",
        "failed", "not true", "debunked", "questioned"
    ]

    # Keywords that suggest uncertainty
    uncertain_keywords = [
        "unclear", "alleged", "reportedly", "unconfirmed", "rumored",
        "sources say", "possibly", "may have", "could be", "not yet"
    ]

    support_score = sum(1 for kw in support_keywords if kw in evidence_lower)
    contradict_score = sum(1 for kw in contradict_keywords if kw in evidence_lower)
    uncertain_score = sum(1 for kw in uncertain_keywords if kw in evidence_lower)

    # Determine verdict
    if contradict_score >= 2:
        verdict = "CONTRADICTED"
        reason = f"Evidence contains {contradict_score} contradiction signal(s)."
    elif support_score >= 3:
        verdict = "HIGH CONFIDENCE"
        reason = f"Evidence contains {support_score} strong support signal(s)."
    elif support_score >= 1 and contradict_score == 0:
        verdict = "MEDIUM CONFIDENCE"
        reason = f"Evidence shows partial support with {support_score} signal(s)."
    elif uncertain_score >= 1:
        verdict = "LOW CONFIDENCE"
        reason = f"Evidence is uncertain with {uncertain_score} uncertainty signal(s)."
    else:
        verdict = "LOW CONFIDENCE"
        reason = "Evidence does not clearly support or contradict the claim."

    return (
        f"CLAIM: {claim}\n"
        f"SCORE: {verdict}\n"
        f"REASON: {reason}\n"
        f"SUPPORT SIGNALS: {support_score} | "
        f"CONTRADICTION SIGNALS: {contradict_score} | "
        f"UNCERTAINTY SIGNALS: {uncertain_score}"
    )
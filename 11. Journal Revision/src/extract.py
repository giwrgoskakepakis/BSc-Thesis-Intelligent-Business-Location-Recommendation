import json, re
from preferences import PREFERENCE_TERMS

KNOWN_TERMS = set(PREFERENCE_TERMS)   # the only valid outputs

TERM_DEFINITIONS = """
    - central: close to the city centre / downtown / the heart of town
    - peripheral: far from the centre — outskirts, outer villages, countryside, rural, "off the beaten track"
    - coastal: near the sea, coast, beach, waterfront, or port
    - near_university: near the university / campus / the student quarter
    - large_area: a large, spread-out, sparsely-built district with room for a big land footprint (a big plot or yard). NOT a roomy shop interior.
"""

PROMPT_TEMPLATE = """
    You extract LOCATION preferences from an entrepreneur's query about where to open a business.

    The ONLY valid preference terms are:
    {definitions}

    Rules:
    - Output ONLY a JSON array of the applicable terms, e.g. ["peripheral"] or ["central","coastal"].
    - Use ONLY terms from the list above. Never invent terms.
    - If the query expresses no location preference, output [].
    - Ignore the type of business itself ("a clothing shop near campus" -> ["near_university"]).
    - Map indirect phrasings to the right term ("off the beaten track" -> peripheral; "by the sea" -> coastal).

    Query: {query}
    JSON:
"""

def _parse_terms(raw):
    """Pull a flat JSON array out of the model's text and validate it."""
    m = re.search(r'\[[^\[\]]*\]', raw)          # first flat [...] group
    if not m:
        return set()
    try:
        terms = json.loads(m.group(0))
    except json.JSONDecodeError:
        return set()
    return {t for t in terms if t in KNOWN_TERMS}  # validation: drop anything not in the vocabulary

def make_extractor(call_llm):
    """call_llm(prompt:str)->str. Returns an extract_constraints(query) function."""
    def extract_constraints(query):
        if not query:
            return {'hard': set(), 'soft': set()}
        raw = call_llm(PROMPT_TEMPLATE.format(definitions=TERM_DEFINITIONS, query=query))
        return {'hard': _parse_terms(raw), 'soft': set()}
    return extract_constraints
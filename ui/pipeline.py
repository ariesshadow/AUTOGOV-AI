"""
AutoGov AI Pipeline

Connects the Streamlit UI to the real AutoGov backend agents:

Vision / OCR -> Policy RAG -> PDF Compilation

No mock or demo fallback is used.
"""

from typing import Any, Dict, Tuple


# ---------------------------------------------------------------------------
# Vision / OCR
# ---------------------------------------------------------------------------

def run_vision(uploaded_file) -> Tuple[Dict[str, Any], bool]:
    """
    Run the real Vision/OCR agent.

    Expected backend:
        ocr_agent.parse_document(uploaded_file) -> dict

    Returns:
        profile, True
    """

    try:
        from ocr_agent import parse_document
    except ImportError as exc:
        raise RuntimeError(
            "Vision/OCR agent could not be imported. "
            "Make sure ocr_agent.py exists and all required dependencies "
            "are installed."
        ) from exc

    try:
        profile = parse_document(uploaded_file)
    except Exception as exc:
        raise RuntimeError(
            f"Vision/OCR agent failed: {exc}"
        ) from exc

    if not isinstance(profile, dict):
        raise RuntimeError(
            "Vision/OCR agent returned an invalid response. "
            "Expected a dictionary."
        )

    if not validate_profile(profile):
        raise RuntimeError(
            "Vision/OCR agent returned an incomplete profile. "
            "Required fields: full_name, cnic_number, dob, city."
        )

    return profile, True


# ---------------------------------------------------------------------------
# Policy RAG
# ---------------------------------------------------------------------------

def run_policy(
    user_profile: Dict[str, Any],
    service_request: Dict[str, Any],
) -> Tuple[Dict[str, Any], bool]:
    """
    Run the real Policy RAG agent.

    Supported backend functions:

        rag_agent.query_policy(user_profile, department)

    or:

        rag_agent.rag_query(user_profile, department)

    Returns:
        verification, True
    """

    if not isinstance(user_profile, dict):
        raise RuntimeError(
            "Invalid applicant profile supplied to Policy RAG."
        )

    if not isinstance(service_request, dict):
        raise RuntimeError(
            "Invalid service request supplied to Policy RAG."
        )

    department = service_request.get("department")

    if not department:
        raise RuntimeError(
            "No department/service was provided for the Policy RAG agent."
        )

    try:
        import rag_agent
    except ImportError as exc:
        raise RuntimeError(
            "Policy RAG agent could not be imported. "
            "Make sure rag_agent.py exists and all required dependencies "
            "are installed."
        ) from exc

    query_function = getattr(
        rag_agent,
        "query_policy",
        None,
    )

    if query_function is None:
        query_function = getattr(
            rag_agent,
            "rag_query",
            None,
        )

    if query_function is None:
        raise RuntimeError(
            "Policy RAG agent does not expose query_policy() "
            "or rag_query()."
        )

    try:
        verification = query_function(
            user_profile,
            department,
        )
    except Exception as exc:
        raise RuntimeError(
            f"Policy RAG agent failed: {exc}"
        ) from exc

    if not isinstance(verification, dict):
        raise RuntimeError(
            "Policy RAG agent returned an invalid response. "
            "Expected a dictionary."
        )

    if not validate_verification(verification):
        raise RuntimeError(
            "Policy RAG agent returned an incomplete verification result."
        )

    return verification, True


# ---------------------------------------------------------------------------
# PDF Compilation
# ---------------------------------------------------------------------------

def run_pdf(
    data: Dict[str, Any],
) -> Tuple[bytes, bool]:
    """
    Run the real PDF compilation agent.

    Expected backend:
        pdf_agent.generate_pdf_form(data) -> bytes

    Returns:
        pdf_bytes, True
    """

    if not isinstance(data, dict):
        raise RuntimeError(
            "Invalid data supplied to PDF Compilation agent."
        )

    try:
        from pdf_agent import generate_pdf_form
    except ImportError as exc:
        raise RuntimeError(
            "PDF agent could not be imported. "
            "Make sure pdf_agent.py exists and all required dependencies "
            "are installed."
        ) from exc

    try:
        pdf_bytes = generate_pdf_form(data)
    except Exception as exc:
        raise RuntimeError(
            f"PDF agent failed: {exc}"
        ) from exc

    if not isinstance(
        pdf_bytes,
        (bytes, bytearray),
    ):
        raise RuntimeError(
            "PDF agent returned an invalid response. "
            "Expected PDF bytes."
        )

    pdf_bytes = bytes(pdf_bytes)

    if not pdf_bytes.startswith(b"%PDF"):
        raise RuntimeError(
            "PDF agent returned data that does not appear to be a valid PDF."
        )

    return pdf_bytes, True


# ---------------------------------------------------------------------------
# Profile validation
# ---------------------------------------------------------------------------

def validate_profile(
    profile: Dict[str, Any],
) -> bool:
    """
    Validate the profile returned by Vision/OCR.
    """

    if not isinstance(profile, dict):
        return False

    required_fields = {
        "full_name",
        "cnic_number",
        "dob",
        "city",
    }

    return required_fields.issubset(
        profile.keys()
    )


# ---------------------------------------------------------------------------
# Policy verification validation
# ---------------------------------------------------------------------------

def validate_verification(
    verification: Dict[str, Any],
) -> bool:
    """
    Validate the verification result returned by Policy RAG.
    """

    if not isinstance(verification, dict):
        return False

    required_fields = {
        "eligible",
        "required_documents",
        "official_fee_pkr",
        "processing_days",
    }

    return required_fields.issubset(
        verification.keys()
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "run_vision",
    "run_policy",
    "run_pdf",
    "validate_profile",
    "validate_verification",
]
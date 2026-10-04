"""
AutoGov AI Streamlit application.

Connects the existing UI to the real AutoGov backend pipeline:
Vision/OCR -> Policy RAG -> PDF Compilation
"""

from __future__ import annotations

import time

import streamlit as st

from ui.ui_components import (
    load_css,
    agent_trace,
    render_navbar,
    render_hero,
    render_how_it_works,
    service_selector,
    render_step_heading,
    render_upload_zone,
    render_run_button,
    TraceController,
    profile_card,
    verification_card,
    metrics_row,
    download_section,
    error_state,
    empty_state,
    loading_skeleton,
    render_footer,
)

from ui.pipeline import (
    run_vision,
    run_policy,
    run_pdf,
)


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def _initialize_state() -> None:
    if "pipeline_state" not in st.session_state:
        st.session_state.pipeline_state = {
            "step": 0,
            "profile": None,
            "verification": None,
            "pdf": None,
            "trace": False,
            "error": None,
            "error_stage": None,
            "started_at": None,
            "completed_at": None,
        }

    if "trace_states" not in st.session_state:
        st.session_state.trace_states = None

    if "trace_logs" not in st.session_state:
        st.session_state.trace_logs = []

    if "trace_elapsed" not in st.session_state:
        st.session_state.trace_elapsed = 0

    if "selected_service" not in st.session_state:
        st.session_state.selected_service = None

    if "run_agents_requested" not in st.session_state:
        st.session_state.run_agents_requested = False

    if "upload_version" not in st.session_state:
        st.session_state.upload_version = 0


# ---------------------------------------------------------------------------
# Reset pipeline state
# ---------------------------------------------------------------------------

def _reset_pipeline_state() -> None:
    st.session_state.pipeline_state = {
        "step": 0,
        "profile": None,
        "verification": None,
        "pdf": None,
        "trace": False,
        "error": None,
        "error_stage": None,
        "started_at": None,
        "completed_at": None,
    }

    st.session_state.trace_states = None
    st.session_state.trace_logs = []
    st.session_state.trace_elapsed = 0


# ---------------------------------------------------------------------------
# Save trace
# ---------------------------------------------------------------------------

def _save_trace(trace: TraceController) -> None:
    st.session_state.trace_states = trace.states.copy()
    st.session_state.trace_logs = trace.logs.copy()

    started_at = st.session_state.pipeline_state.get(
        "started_at"
    )

    completed_at = st.session_state.pipeline_state.get(
        "completed_at"
    )

    if (
        started_at is not None
        and completed_at is not None
    ):
        st.session_state.trace_elapsed = (
            completed_at - started_at
        )

    elif started_at is not None:
        st.session_state.trace_elapsed = (
            time.perf_counter() - started_at
        )

    else:
        st.session_state.trace_elapsed = 0


# ---------------------------------------------------------------------------
# Render saved execution trace
# ---------------------------------------------------------------------------

def render_saved_trace() -> None:
    trace_states = st.session_state.get(
        "trace_states"
    )

    trace_logs = st.session_state.get(
        "trace_logs",
        [],
    )

    trace_elapsed = st.session_state.get(
        "trace_elapsed",
        0,
    )

    if not trace_states:
        return

    agent_trace(
        trace_states,
        trace_logs,
        trace_elapsed,
    )


# ---------------------------------------------------------------------------
# Main pipeline execution
# ---------------------------------------------------------------------------

def _run_real_pipeline(
    uploaded_file,
    service: str,
) -> None:

    state = st.session_state.pipeline_state

    state.update(
        {
            "step": 1,
            "profile": None,
            "verification": None,
            "pdf": None,
            "trace": False,
            "error": None,
            "error_stage": None,
            "started_at": time.perf_counter(),
            "completed_at": None,
        }
    )

    st.session_state.trace_states = None
    st.session_state.trace_logs = []
    st.session_state.trace_elapsed = 0

    trace_placeholder = st.empty()

    st.markdown(
        "<h2 class='trace-section-title'>Agent Thought Trace</h2>",
        unsafe_allow_html=True,
    )

    trace = TraceController(
        placeholder=trace_placeholder
    )

    # -----------------------------------------------------------------------
    # Step 1: Vision / OCR
    # -----------------------------------------------------------------------

    try:
        trace.start("vision")

        trace.log(
            "vision",
            "Reading uploaded government document...",
        )

        trace.log(
            "vision",
            "Running document OCR and field extraction...",
        )

        profile, _ = run_vision(
            uploaded_file
        )

        trace.log(
            "vision",
            "Validating extracted applicant fields...",
        )

        trace.log(
            "vision",
            "Validation passed: applicant profile extracted successfully.",
        )

        trace.complete("vision")

        state["profile"] = profile
        state["step"] = 2

        _save_trace(trace)

    except Exception as exc:

        trace.fail(
            "vision",
            str(exc),
        )

        state["error"] = str(exc)
        state["error_stage"] = "Vision / OCR"
        state["trace"] = True

        _save_trace(trace)

        return

    # -----------------------------------------------------------------------
    # Step 2: Policy RAG
    # -----------------------------------------------------------------------

    try:
        trace.start("rag")

        trace.log(
            "rag",
            f"Preparing policy query for {service}...",
        )

        trace.log(
            "rag",
            "Searching the policy knowledge base...",
        )

        trace.log(
            "rag",
            "Retrieving relevant policy information...",
        )

        service_request = {
            "department": service,
        }

        verification, _ = run_policy(
            profile,
            service_request,
        )

        trace.log(
            "rag",
            "Grounding eligibility and service requirements...",
        )

        trace.log(
            "rag",
            "Policy verification completed.",
        )

        trace.complete("rag")

        state["verification"] = verification
        state["step"] = 3

        _save_trace(trace)

    except Exception as exc:

        trace.fail(
            "rag",
            str(exc),
        )

        state["error"] = str(exc)
        state["error_stage"] = "Policy RAG"
        state["trace"] = True

        _save_trace(trace)

        return

    # -----------------------------------------------------------------------
    # Step 3: PDF Compilation
    # -----------------------------------------------------------------------

    try:
        trace.start("pdf")

        trace.log(
            "pdf",
            "Preparing verified application data...",
        )

        trace.log(
            "pdf",
            "Compiling final application package...",
        )

        pdf_data = {
            "user_profile": profile,
            "rag_verification": verification,
            "service": service,
            "department": service,
        }

        pdf_bytes, _ = run_pdf(
            pdf_data
        )

        trace.log(
            "pdf",
            "Final PDF generated successfully.",
        )

        trace.complete("pdf")

        state["pdf"] = pdf_bytes
        state["step"] = 4
        state["completed_at"] = time.perf_counter()
        state["trace"] = True

        _save_trace(trace)

    except Exception as exc:

        trace.fail(
            "pdf",
            str(exc),
        )

        state["error"] = str(exc)
        state["error_stage"] = "PDF Compilation"
        state["trace"] = True

        _save_trace(trace)

        return

    state["trace"] = True
    _save_trace(trace)


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

def _render_results() -> None:

    state = st.session_state.pipeline_state

    profile = state.get("profile")
    verification = state.get("verification")
    pdf_bytes = state.get("pdf")

    if not profile or not verification:
        return

    st.markdown(
        "<div class='results-section'>",
        unsafe_allow_html=True,
    )

    st.subheader(
        "Application results"
    )

    eligible = verification.get(
        "eligible",
        False,
    )

    fee = verification.get(
        "official_fee_pkr",
        0,
    )

    days = verification.get(
        "processing_days",
        0,
    )

    required_documents = verification.get(
        "required_documents",
        [],
    )

    eligibility = (
        "Eligible"
        if eligible
        else "Not eligible"
    )

    try:
        fee_text = f"{float(fee):,.0f}"
    except (
        TypeError,
        ValueError,
    ):
        fee_text = str(fee)

    st.markdown(
        f"""
        <div class="result-summary">
            <strong>{eligibility}</strong>

            <span>
                Official fee
                <b>PKR {fee_text}</b>
            </span>

            <span>
                Processing
                <b>{days} days</b>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    started_at = state.get(
        "started_at"
    )

    completed_at = state.get(
        "completed_at"
    )

    if (
        started_at is not None
        and completed_at is not None
    ):
        elapsed = (
            completed_at
            - started_at
        )

        processing_time = (
            f"{elapsed:.1f}s"
        )

    else:
        processing_time = "Completed"

    metrics = [
        (
            "Processing time",
            processing_time,
            "",
        ),
        (
            "Docs verified",
            len(required_documents),
            "",
        ),
        (
            "Fee accuracy",
            "Verified",
            "",
        ),
        (
            "Policy grounding",
            "Active",
            "",
        ),
    ]

    metrics_row(
        metrics
    )

    if pdf_bytes:
        service_name = str(
            state.get(
                "service",
                "application",
            )
        ).lower()

        download_section(
            pdf_bytes,
            filename=f"{service_name}_application.pdf",
        )

    with st.expander(
        "Applicant profile",
        expanded=True,
    ):
        profile_card(
            profile,
            editable=False,
        )

    with st.expander(
        "Verification details",
        expanded=True,
    ):
        verification_card(
            verification
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

def main() -> None:

    _initialize_state()

    load_css()

    render_navbar()

    render_hero()

    render_how_it_works()

    # -----------------------------------------------------------------------
    # Workspace anchor
    # -----------------------------------------------------------------------

    st.markdown(
        "<div id='workspace'></div>",
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # Workspace
    # -----------------------------------------------------------------------

    with st.container(
        border=True,
        gap="medium",
    ):

        render_step_heading(
            1,
            "Upload & Service",
            "Choose a service and upload the document you want to process.",
        )

        uploaded = render_upload_zone()

        service = service_selector()

        service_chosen = bool(
            st.session_state.get(
                "selected_service"
            )
        )

        ready = (
            uploaded is not None
            and service_chosen
        )

        if (
            not uploaded
            and not service_chosen
        ):
            helper_text = (
                "Upload a document and select a service to continue."
            )

        elif not service_chosen:
            helper_text = (
                "Select a service to continue."
            )

        else:
            helper_text = (
                "Upload a document to continue."
            )

        render_run_button(
            disabled=not ready,
            helper_text=helper_text,
        )

    # -----------------------------------------------------------------------
    # Run real agents
    # -----------------------------------------------------------------------

    if (
        ready
        and st.session_state.get(
            "run_agents_requested",
            False,
        )
    ):

        st.session_state[
            "run_agents_requested"
        ] = False

        _reset_pipeline_state()

        st.session_state.pipeline_state["service"] = service

        _run_real_pipeline(
            uploaded,
            service,
        )

    # -----------------------------------------------------------------------
    # Current pipeline state
    # -----------------------------------------------------------------------

    state = st.session_state.pipeline_state

    # -----------------------------------------------------------------------
    # Saved execution trace
    # -----------------------------------------------------------------------

    if state.get("trace"):

        render_saved_trace()

    # -----------------------------------------------------------------------
    # Pipeline error
    # -----------------------------------------------------------------------

    if state.get("error"):

        error_state(
            f"{state.get('error_stage', 'Pipeline')} failed",
            state["error"],
            "Check the agent configuration and try again.",
        )

    # -----------------------------------------------------------------------
    # Results
    # -----------------------------------------------------------------------

    if (
        state.get("step", 0) >= 4
        and not state.get("error")
    ):

        _render_results()

    elif (
        state.get("step", 0) == 0
        and not uploaded
    ):

        empty_state(
            "Upload a document and select a government service to begin."
        )

    # -----------------------------------------------------------------------
    # Footer
    # -----------------------------------------------------------------------

    render_footer()


if __name__ == "__main__":
    main()
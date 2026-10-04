from __future__ import annotations

import html
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import streamlit as st


# ---------------------------------------------------------------------------
# CSS loader
# ---------------------------------------------------------------------------

def load_css(path: str = "styles.css") -> None:
    css_path = Path(__file__).parent / path

    if not css_path.is_file():
        raise FileNotFoundError(f"CSS file not found: {css_path}")

    css = css_path.read_text(encoding="utf-8")
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Navbar
# ---------------------------------------------------------------------------

def render_navbar() -> None:
    st.markdown(
        """
        <header class="nav-bar" id="top">
            <a class="nav-brand" href="#top" aria-label="AutoGov AI home">
                <svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true">
                    <defs>
                        <linearGradient
                            id="brand-gradient"
                            x1="0"
                            y1="0"
                            x2="1"
                            y2="1"
                        >
                            <stop stop-color="var(--primary)"/>
                            <stop offset="1" stop-color="var(--accent)"/>
                        </linearGradient>
                    </defs>

                    <path
                        d="M20 3.5 34 9v9.4c0 8.2-5.7 14.7-14 18.1C11.7 33.1 6 26.6 6 18.4V9l14-5.5Z"
                        fill="url(#brand-gradient)"
                    />

                    <path
                        d="m13.5 20.2 4.2 4.1 8.8-9"
                        fill="none"
                        stroke="var(--bg)"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2.6"
                    />
                </svg>

                <span>AutoGov AI</span>
            </a>

            <nav class="nav-links" aria-label="Main navigation">
                <a href="#how-it-works">How it works</a>
                <a href="#workspace">Workspace</a>
            </nav>

            <div class="nav-actions">
                <span class="online-status">
                    <span class="pulse-dot"></span>
                    3 Agents Online
                </span>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------

def render_hero() -> None:
    st.markdown(
        """
        <div class="hero-eyebrow eyebrow gradient-text">
            MULTI-AGENT GOVTECH
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.1, 0.9],
        gap="large",
        vertical_alignment="center",
    )

    with left:
        st.markdown(
            """
            <div class="hero-copy">
                <h1>
                    Government services, with a clearer way forward.
                </h1>

                <p class="hero-description">
                    Move from document to application with grounded guidance
                    at every step.
                </p>

                <div class="hero-actions">
                    <a class="button-gradient" href="#workspace">
                        Go to Workspace
                        <span aria-hidden="true">→</span>
                    </a>

                    <a class="button-quiet" href="#how-it-works">
                        How it works
                        <span aria-hidden="true">↘</span>
                    </a>
                </div>

                <div class="trust-row">
                    <span class="trust-pill">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 3 20 6v5.5c0 4.7-3.3 8.2-8 9.8-4.7-1.6-8-5.1-8-9.8V6l8-3Z"/>
                            <path d="m8.5 12 2.2 2.2 4.8-5"/>
                        </svg>
                        Grounded policy retrieval
                    </span>

                    <span class="trust-pill">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M4 7h16v13H4zM8 7V4h8v3M8 12h8M8 16h5"/>
                        </svg>
                        FBR · NADRA · Passport
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="pipeline-card">
                <div class="pipeline-topline">
                    <span>AGENT PIPELINE</span>

                    <span class="pipeline-live">
                        <i></i>
                        READY
                    </span>
                </div>

                <div class="pipeline-flow">

                    <div class="pipeline-node">
                        <span class="pipeline-icon vision-icon">
                            <svg viewBox="0 0 24 24">
                                <path d="M2.5 12s3.3-6 9.5-6 9.5 6 9.5 6-3.3 6-9.5 6-9.5-6-9.5-6Z"/>
                                <circle cx="12" cy="12" r="2.5"/>
                            </svg>
                        </span>

                        <strong>Vision</strong>
                        <small>Document fields</small>
                    </div>

                    <div class="pipeline-connector">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>

                    <div class="pipeline-node">
                        <span class="pipeline-icon rag-icon">
                            <svg viewBox="0 0 24 24">
                                <path d="M12 3v3m0 12v3M3 12h3m12 0h3M5.6 5.6l2.1 2.1m8.6 8.6 2.1 2.1m0-12.8-2.1 2.1m-8.6 8.6-2.1 2.1"/>
                                <circle cx="12" cy="12" r="4.2"/>
                                <path d="m10.5 12 1.1 1.1 2-2.2"/>
                            </svg>
                        </span>

                        <strong>Policy RAG</strong>
                        <small>Official sources</small>
                    </div>

                    <div class="pipeline-connector">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>

                    <div class="pipeline-node">
                        <span class="pipeline-icon pdf-icon">
                            <svg viewBox="0 0 24 24">
                                <path d="M6 3h8l4 4v14H6zM14 3v5h5M9 13h6m-6 3h6"/>
                            </svg>
                        </span>

                        <strong>PDF Action</strong>
                        <small>Application output</small>
                    </div>

                </div>

                <div class="pipeline-foot">
                    <span>VISION → RAG → PDF</span>
                    <span>3 STEPS</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# How it works
# ---------------------------------------------------------------------------

def render_how_it_works() -> None:
    st.markdown(
        """
        <section class="how-section" id="how-it-works">
            <div class="section-kicker eyebrow gradient-text">
                A clearer path through every form
            </div>

            <h2>How it works</h2>

            <div class="how-grid">

                <article class="how-card">
                    <span class="how-number">01</span>

                    <span class="how-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M2.5 12s3.3-6 9.5-6 9.5 6 9.5 6-3.3 6-9.5 6-9.5-6-9.5-6Z"/>
                            <circle cx="12" cy="12" r="2.5"/>
                        </svg>
                    </span>

                    <h3>Vision / OCR</h3>
                    <p>Extract fields from your documents.</p>
                </article>

                <article class="how-card">
                    <span class="how-number">02</span>

                    <span class="how-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M12 3v3m0 12v3M3 12h3m12 0h3M5.6 5.6l2.1 2.1m8.6 8.6 2.1 2.1m0-12.8-2.1 2.1m-8.6 8.6-2.1 2.1"/>
                            <circle cx="12" cy="12" r="4.2"/>
                            <path d="m10.5 12 1.1 1.1 2-2.2"/>
                        </svg>
                    </span>

                    <h3>Policy RAG</h3>
                    <p>Verify details against official policy.</p>
                </article>

                <article class="how-card">
                    <span class="how-number">03</span>

                    <span class="how-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M6 3h8l4 4v14H6zM14 3v5h5M9 13h6m-6 3h6"/>
                        </svg>
                    </span>

                    <h3>PDF Action</h3>
                    <p>Prepare a complete application PDF.</p>
                </article>

            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Service selector
# ---------------------------------------------------------------------------

def service_selector() -> str:
    services = {
        "FBR": {
            "title": "FBR NTN Registration",
            "description": "Register for your tax number.",
            "meta": "NTN · Filer status",
            "icon": """
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3" y="7" width="18" height="14" rx="2"/>
                    <path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m-13 5h18m-12 0v2h6v-2"/>
                </svg>
            """,
        },
        "NADRA": {
            "title": "NADRA CNIC Renewal",
            "description": "Renew or update your CNIC.",
            "meta": "CNIC · Identity",
            "icon": """
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <rect x="3" y="5" width="18" height="14" rx="2"/>
                    <circle cx="8.5" cy="11" r="2"/>
                    <path d="M5.5 16a3 3 0 0 1 6 0m3-6h4m-4 4h4"/>
                </svg>
            """,
        },
        "PASSPORT": {
            "title": "Passport Renewal",
            "description": "Renew your travel document.",
            "meta": "Passport · Travel",
            "icon": """
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M5 3h14v18H5zM8 3v18m4-13 1.2 2.4 2.8.4-2 2 .5 2.8-2.5-1.3-2.5 1.3.5-2.8-2-2 2.8-.4L12 8Z"/>
                </svg>
            """,
        },
    }

    st.markdown(
        "<h3 class='service-heading'>Select a service</h3>",
        unsafe_allow_html=True,
    )

    columns = st.columns(
        3,
        gap="small",
        vertical_alignment="top",
    )

    selected = st.session_state.get("selected_service")

    if selected not in services:
        selected = None

    for column, (key, service) in zip(columns, services.items()):
        with column:

            selected_class = (
                " selected"
                if selected == key
                else ""
            )

            check_badge = (
                "<span class='service-check' aria-label='Selected'>✓</span>"
                if selected == key
                else ""
            )

            st.markdown(
                f"""
                <article class="service-card{selected_class}">
                    <span class="service-icon">
                        {service["icon"]}
                    </span>

                    <h4>{html.escape(service["title"])}</h4>

                    <p>{html.escape(service["description"])}</p>

                    <span class="service-meta">
                        {html.escape(service["meta"])}
                    </span>

                    {check_badge}
                </article>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                service["title"],
                key=f"service_option_{key}",
                help=f"Select {service['title']}",
                width="stretch",
            ):
                st.session_state["selected_service"] = key
                st.rerun()

    return selected or ""


# ---------------------------------------------------------------------------
# Step heading
# ---------------------------------------------------------------------------

def render_step_heading(
    step_num: int,
    title: str,
    subtitle: str = "",
) -> None:
    subtitle_html = (
        f"<p class='step-subtitle'>{html.escape(subtitle)}</p>"
        if subtitle
        else ""
    )

    st.markdown(
        f"""
        <div class="step-header workspace-step">
            <div class="eyebrow gradient-text">
                STEP {step_num} OF 3
            </div>

            <div class="step-title-row">
                <span class="step-badge">
                    {step_num:02d}
                </span>

                <h2>{html.escape(title)}</h2>
            </div>

            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Upload zone
# ---------------------------------------------------------------------------

def render_upload_zone() -> Any:
    upload_version = st.session_state.get(
        "upload_version",
        0,
    )

    upload_key = (
        f"document_upload_{upload_version}"
    )

    st.markdown(
        """
        <div class="upload-instructions">
            <svg viewBox="0 0 48 48" aria-hidden="true">
                <path d="M24 31V8m0 0-8 8m8-8 8 8M9 28v10a3 3 0 0 0 3 3h24a3 3 0 0 0 3-3V28"/>
            </svg>

            <strong>
                Upload your CNIC / government document
            </strong>

            <span>
                PNG, JPG or PDF · max 200MB
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload your CNIC / government document",
        type=[
            "png",
            "jpg",
            "jpeg",
            "pdf",
        ],
        label_visibility="collapsed",
        key=upload_key,
    )

    if uploaded is None:
        return None

    size = uploaded.size

    if size >= 1024 * 1024:
        size_label = f"{size / (1024 * 1024):.1f} MB"
    else:
        size_label = f"{size / 1024:.1f} KB"

    safe_name = html.escape(
        uploaded.name
    )

    preview_col, remove_col = st.columns(
        [3.8, 1.2],
        gap="small",
        vertical_alignment="center",
    )

    with preview_col:
        st.markdown(
            f"""
            <div class="upload-preview">
                <span class="upload-file-icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M6 3h8l4 4v14H6zM14 3v5h5M9 13h6m-6 3h6"/>
                    </svg>
                </span>

                <span class="upload-file-details">
                    <strong>{safe_name}</strong>

                    <small>
                        {size_label} · Ready to analyze
                    </small>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with remove_col:
        if st.button(
            "Remove",
            key="remove_uploaded_document",
            help="Remove uploaded document",
            width="stretch",
        ):
            st.session_state["upload_version"] = (
                upload_version + 1
            )

            st.rerun()

    return uploaded


# ---------------------------------------------------------------------------
# Run button
# ---------------------------------------------------------------------------

def render_run_button(
    disabled: bool,
    helper_text: str = "",
) -> None:

    clicked = st.button(
        "Run AutoGov Agents",
        key="run_autogov_agents",
        type="primary",
        disabled=disabled,
        width="stretch",
    )

    if clicked:
        st.session_state["run_agents_requested"] = True

    if disabled and helper_text:
        st.markdown(
            f"""
            <p class="action-helper">
                {html.escape(helper_text)}
            </p>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Agent trace
# ---------------------------------------------------------------------------

def _trace_html(
    states: Dict[str, str],
    logs: List[str],
    elapsed: float,
    target: int,
) -> str:

    html_output = (
        "<div class='agent-trace'>"
        "<div class='timeline'>"
    )

    order = [
        "vision",
        "rag",
        "pdf",
    ]

    titles = {
        "vision": "Vision / OCR Agent",
        "rag": "Policy RAG Agent",
        "pdf": "PDF Action Agent",
    }

    for agent in order:

        state = states.get(
            agent,
            "idle",
        )

        safe_state = (
            state
            if state in {
                "idle",
                "active",
                "done",
                "error",
                "pending",
            }
            else "idle"
        )

        html_output += f"""
        <div class='timeline-step {safe_state}'>
            <div class='dot'></div>
            <div>{titles[agent]}</div>
        </div>
        """

    html_output += "</div>"

    html_output += (
        "<div class='terminal-log'>"
    )

    for timestamp, line in logs:

        safe_line = html.escape(
            line
        )

        if (
            line.startswith("[")
            and "]" in line
        ):
            tag, message = line.split(
                "]",
                1,
            )

            agent = html.escape(
                tag[1:]
            )

            message = html.escape(
                message.strip()
            )

            html_output += (
                "<div class='terminal-line'>"
                f"<span class='timestamp'>{html.escape(timestamp)}</span>"
                f"<span class='agent'>[{agent}]</span>"
                f"<span class='msg'>{message}</span>"
                "</div>"
            )

        else:
            html_output += (
                "<div class='terminal-line'>"
                f"{safe_line}"
                "</div>"
            )

    html_output += """
        <div class='terminal-line'>
            <span class='timestamp'></span>
            <span class='agent'></span>
            <span class='msg'>|</span>
        </div>
    """

    html_output += "</div>"

    if target <= 0:
        percent = 100
    else:
        percent = min(
            elapsed / target,
            1.0,
        ) * 100

    if percent < 75:
        bar_color = "var(--primary)"
    elif percent < 90:
        bar_color = "var(--warning)"
    else:
        bar_color = "var(--danger)"

    html_output += f"""
        <div class='trace-progress'>
            <div class='trace-progress-track'>
                <div
                    class='trace-progress-fill'
                    style='width:{percent}%;background:{bar_color};'
                ></div>
            </div>

            <small class='trace-elapsed'>
                Elapsed {int(elapsed)}s / {target}s
            </small>
        </div>
    """

    html_output += "</div>"

    return html_output


def agent_trace(
    states: Dict[str, str],
    logs: List[str],
    elapsed: float,
    target: int = 120,
) -> None:

    trace_html = _trace_html(
        states,
        logs,
        elapsed,
        target,
    )

    st.markdown(
        trace_html,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Trace controller
# ---------------------------------------------------------------------------

class TraceController:
    def __init__(
        self,
        placeholder: Any,
    ):
        self.placeholder = placeholder
        self.start_time = time.perf_counter()

        self.states = {
            "vision": "idle",
            "rag": "pending",
            "pdf": "pending",
        }

        self.logs: List[
            tuple[str, str]
        ] = []

    def _render(self) -> None:
        elapsed = (
            time.perf_counter()
            - self.start_time
        )

        with self.placeholder.container():

            agent_trace(
                self.states,
                self.logs,
                elapsed,
            )

    def _store_state(self) -> None:
        st.session_state[
            "trace_states"
        ] = self.states.copy()

        st.session_state[
            "trace_logs"
        ] = list(self.logs)

        st.session_state[
            "trace_elapsed"
        ] = (
            time.perf_counter()
            - self.start_time
        )

    def start(
        self,
        agent: str,
    ) -> None:

        self.states[agent] = "active"

        self._store_state()
        self._render()

    def log(
        self,
        agent: str,
        message: str,
    ) -> None:

        timestamp = time.strftime(
            "%H:%M:%S"
        )

        self.logs.append(
            (
                timestamp,
                f"[{agent.upper()}] {message}",
            )
        )

        self._store_state()
        self._render()

    def complete(
        self,
        agent: str,
    ) -> None:

        self.states[agent] = "done"

        self._store_state()
        self._render()

    def fail(
        self,
        agent: str,
        error_msg: str,
    ) -> None:

        timestamp = time.strftime(
            "%H:%M:%S"
        )

        self.states[agent] = "error"

        self.logs.append(
            (
                timestamp,
                f"[{agent.upper()}] Error: {error_msg}",
            )
        )

        self._store_state()
        self._render()


# ---------------------------------------------------------------------------
# Persisted trace renderer
# ---------------------------------------------------------------------------

def render_saved_trace() -> None:
    states = st.session_state.get(
        "trace_states"
    )

    logs = st.session_state.get(
        "trace_logs"
    )

    elapsed = st.session_state.get(
        "trace_elapsed",
        0,
    )

    if not states:
        return

    st.markdown(
        "<h2 class='trace-section-title'>"
        "Agent Thought Trace"
        "</h2>",
        unsafe_allow_html=True,
    )

    agent_trace(
        states,
        logs or [],
        elapsed,
    )


# ---------------------------------------------------------------------------
# Profile card
# ---------------------------------------------------------------------------

def profile_card(
    user_profile: Dict[str, Any],
    confidences: Optional[
        Dict[str, str]
    ] = None,
    editable: bool = True,
) -> Dict[str, Any]:

    st.subheader(
        "Applicant profile"
    )

    cols = st.columns(2)

    new = user_profile.copy()

    with cols[0]:

        new["full_name"] = st.text_input(
            "Full name",
            value=str(
                user_profile.get(
                    "full_name",
                    "",
                )
            ),
            disabled=not editable,
        )

        new["cnic_number"] = st.text_input(
            "CNIC number",
            value=str(
                user_profile.get(
                    "cnic_number",
                    "",
                )
            ),
            disabled=not editable,
        )

    with cols[1]:

        dob = user_profile.get(
            "dob",
            "2000-01-01",
        )

        new["dob"] = st.date_input(
            "Date of birth",
            value=dob,
            disabled=not editable,
        )

        new["city"] = st.text_input(
            "City",
            value=str(
                user_profile.get(
                    "city",
                    "",
                )
            ),
            disabled=not editable,
        )

    if confidences:

        badges = []

        for field, level in confidences.items():

            if level == "high":
                cls = "success"
            elif level == "medium":
                cls = "warn"
            else:
                cls = "error"

            badges.append(
                f"<span class='badge {cls}'>"
                f"{html.escape(field)}: "
                f"{html.escape(level.title())}"
                f"</span>"
            )

        st.markdown(
            "".join(badges),
            unsafe_allow_html=True,
        )

    return new


# ---------------------------------------------------------------------------
# Verification card
# ---------------------------------------------------------------------------

def verification_card(
    rag_verification: Dict[str, Any],
) -> None:

    st.subheader(
        "Verification result"
    )

    eligible = rag_verification.get(
        "eligible",
        False,
    )

    fee = rag_verification.get(
        "official_fee_pkr",
        0,
    )

    days = rag_verification.get(
        "processing_days",
        "-",
    )

    docs = rag_verification.get(
        "required_documents",
        [],
    )

    if eligible:
        badge = (
            "<span class='badge success'>"
            "Eligible"
            "</span>"
        )
    else:
        badge = (
            "<span class='badge error'>"
            "Not eligible"
            "</span>"
        )

    st.markdown(
        badge,
        unsafe_allow_html=True,
    )

    try:
        fee_text = f"{float(fee):,.0f}"
    except (
        TypeError,
        ValueError,
    ):
        fee_text = html.escape(
            str(fee)
        )

    st.markdown(
        f"**Official fee:** PKR {fee_text}"
    )

    st.markdown(
        f"**Processing time:** "
        f"{html.escape(str(days))} day(s)"
    )

    st.markdown(
        "**Required documents**"
    )

    for index, doc in enumerate(docs):

        st.checkbox(
            str(doc),
            value=False,
            disabled=True,
            key=f"required_doc_{index}_{hash(str(doc))}",
        )

    sources = rag_verification.get(
        "sources",
        [],
    )

    if sources:

        with st.expander(
            "Sources (policy snippets)"
        ):

            for src in sources:

                source_name = html.escape(
                    str(
                        src.get(
                            "source",
                            "",
                        )
                    )
                )

                snippet = html.escape(
                    str(
                        src.get(
                            "snippet",
                            "",
                        )
                    )
                )

                st.markdown(
                    f"*`{source_name}`*: "
                    f"{snippet}"
                )


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def metric_card(
    label: str,
    value: Any,
    hint: str = "",
) -> None:

    st.markdown(
        f"""
        <div class='metric-card'>
            <div style='font-size:0.9rem;color:var(--muted);'>
                {html.escape(str(label))}
            </div>

            <div style='font-size:1.4rem;font-weight:600;color:var(--text);'>
                {html.escape(str(value))}
            </div>

            <div style='font-size:0.75rem;color:var(--muted);'>
                {html.escape(str(hint))}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrics_row(
    metrics: List[
        tuple[str, Any, str]
    ],
) -> None:

    if not metrics:
        return

    cols = st.columns(
        len(metrics)
    )

    for col, (
        label,
        value,
        hint,
    ) in zip(
        cols,
        metrics,
    ):

        with col:

            metric_card(
                label,
                value,
                hint,
            )


# ---------------------------------------------------------------------------
# Download section
# ---------------------------------------------------------------------------

def download_section(
    pdf_bytes: bytes,
    filename: str = "application.pdf",
) -> None:

    st.markdown(
        "<h3 class='section-title'>"
        "Download your application"
        "</h3>",
        unsafe_allow_html=True,
    )

    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        width="stretch",
    )


# ---------------------------------------------------------------------------
# Edge states
# ---------------------------------------------------------------------------

def error_state(
    title: str,
    msg: str,
    action_hint: str,
) -> None:

    st.error(
        f"**{title}**\n"
        f"{msg}\n"
        f"*Hint:* {action_hint}"
    )


def not_found_state() -> None:

    st.warning(
        "Information not found in official policy data — "
        "we never guess fees or requirements."
    )


def empty_state(
    msg: str,
) -> None:

    st.info(msg)


def loading_skeleton() -> None:

    st.markdown(
        """
        <div
            class="trace-loading"
            role="status"
            aria-label="Preparing agent trace"
        >
            <div class="trace-loading-title">
                <span class="skeleton-block skeleton-icon"></span>
                <span class="skeleton-block skeleton-title"></span>
            </div>

            <div class="trace-loading-step">
                <span class="skeleton-block skeleton-dot"></span>
                <span class="skeleton-block skeleton-line"></span>
            </div>

            <div class="trace-loading-step">
                <span class="skeleton-block skeleton-dot"></span>
                <span class="skeleton-block skeleton-line short"></span>
            </div>

            <div class="trace-loading-step">
                <span class="skeleton-block skeleton-dot"></span>
                <span class="skeleton-block skeleton-line medium"></span>
            </div>

            <div class="skeleton-block skeleton-log"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

def render_footer() -> None:

    st.markdown(
        """
        <div class='footer' id=''>
            Built by Om e Kalsoom, Khadija Ejaz,
            Khadija Shafique Hussain, Areeba Memon,
            Hania Ghaffar
            <br/>
            Built for HEC-NCEAC & PEC Generative & Agentic AI
            Training – Cohort 11
        </div>
        """,
        unsafe_allow_html=True,
    )
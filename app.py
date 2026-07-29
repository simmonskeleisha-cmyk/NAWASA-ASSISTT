"""
NAWASA Customer Portal & Chatbot - Streamlit rewrite

Design direction: "Tide & Gauge" — a Caribbean water utility should feel like
the sea and the meter it measures, not a generic SaaS dashboard. Deep ocean
gradient hero with a wave divider, segmented "tide gauge" navigation, and
digital-meter typography (JetBrains Mono) for every number a customer would
actually read off a real gauge: bill totals, meter readings, leak deltas.

Run with:
    pip install -r requirements.txt
    streamlit run app.py
"""

import streamlit as st
from datetime import date, datetime, timedelta

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------

st.set_page_config(
    page_title="NAWASA Customer Portal",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
# Deep Ocean   #0B3D59  - primary dark / hero base
# Reef Teal    #0F7173  - secondary / gradient end
# Aqua Glow    #4FD1C5  - signature accent, active states, meter glow
# Sand         #F5EFE0  - warm off-white section background
# Coral Alert  #FF6B5B  - urgency / outage severity
# Ink          #10242E  - body text

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #10242E; }
    h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.01em; }
    .mono { font-family: 'JetBrains Mono', monospace; }

    .block-container { padding-top: 0 !important; padding-bottom: 3rem; max-width: 1100px; }
    header[data-testid="stHeader"] { background: transparent; }

    /* ---------- Hero ---------- */
    .hero-wrap {
        margin: -1rem -100vw 0 -100vw; padding: 0 100vw;
        background: linear-gradient(120deg, #0B3D59 0%, #0F7173 100%);
        position: relative; overflow: hidden;
    }
    .hero-inner { max-width: 1100px; margin: 0 auto; padding: 2rem 1rem 4.5rem 1rem; position: relative; z-index: 2; }
    .hero-eyebrow {
        display:inline-flex; align-items:center; gap:6px;
        color:#4FD1C5; font-family:'JetBrains Mono', monospace; font-size:0.72rem;
        letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.75rem;
    }
    .hero-title { color:#fff; font-size:2.6rem; font-weight:700; margin:0 0 0.4rem 0; line-height:1.05; }
    .hero-sub { color:#CFEAE8; font-size:1.02rem; max-width:520px; margin:0; }
    .hero-wave { position:absolute; bottom:-1px; left:0; width:100%; line-height:0; z-index:1; }

    div[data-testid="stPopover"] button {
        background: rgba(255,255,255,0.12) !important; color:#fff !important;
        border:1px solid rgba(255,255,255,0.35) !important; border-radius:999px !important;
        font-family:'JetBrains Mono', monospace !important;
    }
    div[data-testid="stPopover"] button:hover { background: rgba(255,255,255,0.22) !important; }

    /* ---------- Segmented "tide gauge" nav ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background:#EAF3F1; padding:5px; border-radius:999px;
        margin-top: -2.6rem; position:relative; z-index:3; width:fit-content;
    }
    .stTabs [data-baseweb="tab"] {
        height:auto; padding:9px 16px; border-radius:999px; background:transparent;
        font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:#0B3D59;
    }
    .stTabs [aria-selected="true"] {
        background:#0B3D59 !important; color:#fff !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display:none; }
    .stTabs [data-baseweb="tab-border"] { display:none; }

    /* ---------- Cards ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important; border:1px solid #E7EEEC !important;
        box-shadow: 0 1px 2px rgba(11,61,89,0.04);
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 6px 18px rgba(11,61,89,0.08); transform: translateY(-1px);
    }

    /* ---------- Meter-style readouts ---------- */
    .gauge {
        background:#0B3D59; border-radius:12px; padding:1.1rem 1.3rem;
        display:inline-block; min-width:220px;
    }
    .gauge-label { color:#8FC7C3; font-family:'JetBrains Mono',monospace; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.08em; }
    .gauge-value { color:#4FD1C5; font-family:'JetBrains Mono',monospace; font-size:2.1rem; font-weight:700; text-shadow:0 0 18px rgba(79,209,197,0.45); }
    .gauge-unit { color:#CFEAE8; font-family:'JetBrains Mono',monospace; font-size:0.95rem; }

    /* ---------- Severity chips ---------- */
    .chip { display:inline-block; padding:3px 11px; border-radius:999px; font-size:0.72rem; font-family:'JetBrains Mono',monospace; }
    .chip-low { background:#EAF3F1; color:#0F7173; }
    .chip-medium { background:#FFF1E0; color:#B4610A; }
    .chip-high { background:#FFE3DE; color:#C4402C; }
    .chip-emergency { background:#FF6B5B; color:#fff; }

    /* ---------- Buttons ---------- */
    .stButton>button[kind="primary"] {
        background:#0B3D59 !important; border:none !important; border-radius:8px !important;
        font-weight:600;
    }
    .stButton>button[kind="primary"]:hover { background:#0F7173 !important; }

    /* ---------- Footer ---------- */
    .footer-wrap {
        margin: 3rem -100vw 0 -100vw; padding: 0 100vw;
        background:#0B3D59; color:#CFEAE8;
    }
    .footer-inner { max-width:1100px; margin:0 auto; padding:1.6rem 1rem; text-align:center; font-size:0.82rem; }

    .section-eyebrow {
        font-family:'JetBrains Mono', monospace; font-size:0.72rem; letter-spacing:0.08em;
        text-transform:uppercase; color:#0F7173; margin-bottom:0.15rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

SECTION_LABELS = ["Ask", "Report", "Bill", "Meter", "Policy", "Schedule", "Offices", "Values"]

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------

def init_state():
    defaults = {
        "chat_history": [
            {
                "role": "assistant",
                "content": "Hi, I'm the NAWASA Assistant. Ask me about outages, "
                           "your bill, meter readings, or reconnection times.",
            }
        ],
        "unread_notifications": 3,
        "notifications": [
            {"title": "Scheduled maintenance", "body": "Water supply interruption in Kingstown, Fri 6am-2pm."},
            {"title": "Outage resolved", "body": "Burst pipe on Grenville St. has been repaired."},
            {"title": "Bill reminder", "body": "Your July statement is ready to view."},
        ],
        "outage_reports": [],
        "maintenance_requests": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_state()

# --------------------------------------------------------------------------
# Hero + notifications
# --------------------------------------------------------------------------

WAVE_SVG = """
<div class="hero-wave">
<svg viewBox="0 0 1440 90" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style="width:100%;height:70px;display:block;">
<path fill="#ffffff" d="M0,32 C240,80 480,0 720,24 C960,48 1200,88 1440,40 L1440,90 L0,90 Z"></path>
</svg>
</div>
"""


def render_notifications():
    st.markdown("**Notifications**")
    if not st.session_state.notifications:
        st.caption("You're all caught up.")
    for n in st.session_state.notifications:
        with st.container(border=True):
            st.markdown(f"**{n['title']}**")
            st.caption(n["body"])
    if st.button("Clear all", use_container_width=True):
        st.session_state.unread_notifications = 0
        st.session_state.notifications = []
        st.rerun()


def render_hero():
    st.markdown('<div class="hero-wrap"><div class="hero-inner">', unsafe_allow_html=True)
    left, right = st.columns([5, 1])
    with left:
        st.markdown(
            '<div class="hero-eyebrow">● Live · Kingstown, St. Vincent</div>'
            '<h1 class="hero-title">NAWASA Customer Portal</h1>'
            '<p class="hero-sub">Report outages, estimate your bill, read your meter, '
            'and reach a real branch office — all from one place.</p>',
            unsafe_allow_html=True,
        )
    with right:
        st.write("")
        st.write("")
        with st.popover(f"🔔 {st.session_state.unread_notifications}"):
            render_notifications()
    st.markdown('</div>' + WAVE_SVG + '</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Chat
# --------------------------------------------------------------------------

def get_bot_reply(user_msg: str) -> str:
    """Simple keyword router placeholder — swap this out for a real LLM call."""
    msg = user_msg.lower()
    if any(w in msg for w in ["outage", "burst", "no water", "leak"]):
        return "Sorry about that. Open the **Report** tab to log the location and issue so a crew can be dispatched."
    if any(w in msg for w in ["bill", "cost", "estimate", "how much"]):
        return "Head to the **Bill** tab to estimate your monthly total from your usage in cubic meters."
    if any(w in msg for w in ["disconnect", "reconnect", "cut off"]):
        return "Reconnections are typically processed within 24-48 hours of payment. See the **Policy** tab for details."
    if any(w in msg for w in ["office", "branch", "hours", "location"]):
        return "Check the **Offices** tab for addresses and opening hours nearest you."
    if any(w in msg for w in ["meter", "read"]):
        return "The **Meter** tab walks you through reading your meter and spotting a possible leak."
    return "I can help with outages, billing, meter readings, disconnections, and office hours — what would you like to know?"


def render_chat_section():
    st.markdown('<div class="section-eyebrow">24/7 Assistant</div>', unsafe_allow_html=True)
    st.markdown("### Ask about your service")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Type your question…")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        reply = get_bot_reply(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()


# --------------------------------------------------------------------------
# Outage / burst pipe reporting
# --------------------------------------------------------------------------

def render_outage_section():
    st.markdown('<div class="section-eyebrow">Rapid Response</div>', unsafe_allow_html=True)
    st.markdown("### Report an outage or burst pipe")
    st.caption("The more precise the location, the faster a crew can find it.")

    with st.form("outage_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            issue_type = st.selectbox("Issue type", ["No water supply", "Burst pipe", "Low pressure", "Discolored water", "Other"])
            location = st.text_input("Location / nearest landmark")
        with col2:
            severity = st.select_slider("Severity", ["Low", "Medium", "High", "Emergency"])
            contact = st.text_input("Contact number")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Submit report", type="primary")

    if submitted:
        if not location or not contact:
            st.error("Add a location and contact number so a crew can reach you.")
        else:
            st.session_state.outage_reports.append({
                "type": issue_type, "location": location, "severity": severity,
                "contact": contact, "description": description,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            st.success("Report submitted. Crews are dispatched by severity.")

    if st.session_state.outage_reports:
        with st.expander(f"Your submitted reports ({len(st.session_state.outage_reports)})"):
            for r in reversed(st.session_state.outage_reports):
                chip_class = f"chip-{r['severity'].lower()}"
                st.markdown(
                    f"**{r['type']}** at {r['location']} "
                    f'<span class="chip {chip_class}">{r["severity"]}</span> '
                    f'<span class="mono" style="color:#7A8B92;font-size:0.78rem;">· {r["time"]}</span>',
                    unsafe_allow_html=True,
                )


# --------------------------------------------------------------------------
# Bill estimator
# --------------------------------------------------------------------------

RATE_TIERS = [
    (0, 10, 3.50),
    (10, 20, 5.00),
    (20, 40, 7.25),
    (40, float("inf"), 9.75),
]
BASE_CHARGE = 15.00


def estimate_bill(usage_m3: float) -> float:
    total = BASE_CHARGE
    remaining = usage_m3
    for low, high, rate in RATE_TIERS:
        band = min(remaining, high - low)
        if band <= 0:
            continue
        total += band * rate
        remaining -= band
        if remaining <= 0:
            break
    return round(total, 2)


def render_bill_estimator():
    st.markdown('<div class="section-eyebrow">Estimate</div>', unsafe_allow_html=True)
    st.markdown("### Monthly water bill")
    st.caption("Based on cubic meters (m³) consumed, tiered by usage band.")

    usage = st.slider("Estimated monthly usage (m³)", 0, 100, 15)
    est = estimate_bill(usage)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(
            f'<div class="gauge"><div class="gauge-label">Estimated bill</div>'
            f'<div class="gauge-value">${est:,.2f}</div>'
            f'<div class="gauge-unit">XCD / month</div></div>',
            unsafe_allow_html=True,
        )
        st.caption(f"Includes a base charge of ${BASE_CHARGE:.2f}, plus tiered consumption rates.")
    with col2:
        with st.container(border=True):
            st.markdown("**Rate tiers**")
            for low, high, rate in RATE_TIERS:
                label = f"{low}–{int(high)} m³" if high != float("inf") else f"{low}+ m³"
                st.markdown(f'<span class="mono">{label}: ${rate:.2f}/m³</span>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Meter reading & leak detection guide
# --------------------------------------------------------------------------

def render_meter_reading_guide():
    st.markdown('<div class="section-eyebrow">Read Your Meter</div>', unsafe_allow_html=True)
    st.markdown("### Meter & leak guide")

    with st.expander("How to read your meter", expanded=True):
        st.markdown(
            "1. Locate your meter box, usually near the property boundary.\n"
            "2. Lift the lid and clean off any dirt or debris.\n"
            "3. Record the black (odometer-style) digits, left to right.\n"
            "4. Compare against last month's reading to see your usage."
        )

    with st.expander("Simple leak check"):
        st.markdown(
            "1. Turn off every tap and appliance that uses water.\n"
            "2. Note the exact meter reading.\n"
            "3. Wait 1–2 hours without using any water.\n"
            "4. Check the meter again — any movement suggests a leak."
        )
        c1, c2 = st.columns(2)
        with c1:
            r1 = st.number_input("Reading before waiting (m³)", min_value=0.0, step=0.001, format="%.3f")
        with c2:
            r2 = st.number_input("Reading after waiting (m³)", min_value=0.0, step=0.001, format="%.3f")
        if st.button("Check for a leak"):
            diff = r2 - r1
            st.markdown(
                f'<div class="gauge"><div class="gauge-label">Meter delta</div>'
                f'<div class="gauge-value">{diff:+.3f}</div>'
                f'<div class="gauge-unit">m³</div></div>',
                unsafe_allow_html=True,
            )
            if diff > 0:
                st.warning("Movement detected with no water in use — you likely have a leak. Report it in the Report tab.")
            else:
                st.success("No movement detected. No leak indicated by this test.")


# --------------------------------------------------------------------------
# Disconnection policy
# --------------------------------------------------------------------------

def render_disconnection_guide():
    st.markdown('<div class="section-eyebrow">Know Your Terms</div>', unsafe_allow_html=True)
    st.markdown("### Disconnection & reconnection")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**When disconnection may occur**")
            st.markdown(
                "- Overdue balance beyond the grace period\n"
                "- Unresolved billing disputes without a payment arrangement\n"
                "- Unauthorized connection or tampering"
            )
    with col2:
        with st.container(border=True):
            st.markdown("**Reconnection timeline**")
            st.markdown(
                "- Processed within **24–48 hours** of full payment or an approved plan.\n"
                "- Emergency reconnection may be expedited for medical or safety reasons — contact your branch office."
            )


# --------------------------------------------------------------------------
# Maintenance scheduler
# --------------------------------------------------------------------------

def render_maintenance_scheduler():
    st.markdown('<div class="section-eyebrow">Book a Visit</div>', unsafe_allow_html=True)
    st.markdown("### Schedule maintenance")

    with st.form("maintenance_form", clear_on_submit=True):
        service = st.selectbox("Service needed", ["New connection", "Meter replacement", "Pipe repair", "Water quality test", "Other"])
        preferred_date = st.date_input("Preferred date", min_value=date.today(), value=date.today() + timedelta(days=2))
        address = st.text_input("Service address")
        notes = st.text_area("Additional notes (optional)")
        submitted = st.form_submit_button("Request service", type="primary")

    if submitted:
        if not address:
            st.error("Add a service address so we can route a technician.")
        else:
            st.session_state.maintenance_requests.append({
                "service": service, "date": preferred_date.strftime("%Y-%m-%d"),
                "address": address, "notes": notes,
            })
            st.success(f"Service request submitted for {preferred_date.strftime('%B %d, %Y')}.")

    if st.session_state.maintenance_requests:
        with st.expander(f"Your service requests ({len(st.session_state.maintenance_requests)})"):
            for r in reversed(st.session_state.maintenance_requests):
                st.markdown(f"**{r['service']}** at {r['address']} — <span class='mono'>{r['date']}</span>", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Branch office locator
# --------------------------------------------------------------------------

OFFICES = [
    {"name": "Kingstown Head Office", "hours": "Mon–Fri 8:00am–4:00pm", "phone": "(784) 456-1111"},
    {"name": "Georgetown Branch", "hours": "Mon–Fri 8:30am–3:30pm", "phone": "(784) 456-2222"},
    {"name": "Barrouallie Branch", "hours": "Mon–Fri 8:30am–3:30pm", "phone": "(784) 456-3333"},
    {"name": "Chateaubelair Branch", "hours": "Mon–Fri 8:30am–3:30pm", "phone": "(784) 456-4444"},
]


def render_office_locator():
    st.markdown('<div class="section-eyebrow">Find Us</div>', unsafe_allow_html=True)
    st.markdown("### Branch offices")
    cols = st.columns(2)
    for i, office in enumerate(OFFICES):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{office['name']}**")
                st.markdown(f'<span class="mono" style="color:#7A8B92;font-size:0.85rem;">🕒 {office["hours"]}</span>', unsafe_allow_html=True)
                st.markdown(f'<span class="mono" style="color:#7A8B92;font-size:0.85rem;">📞 {office["phone"]}</span>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Core values
# --------------------------------------------------------------------------

CORE_VALUES = [
    ("Integrity", "Acting honestly and transparently in every customer interaction."),
    ("Reliability", "Delivering safe, consistent water service across every community."),
    ("Responsiveness", "Acting quickly on outages, requests, and customer concerns."),
    ("Sustainability", "Protecting water resources for future generations."),
]


def render_core_values():
    st.markdown('<div class="section-eyebrow">What Guides Us</div>', unsafe_allow_html=True)
    st.markdown("### Core values")
    cols = st.columns(len(CORE_VALUES))
    for col, (title, desc) in zip(cols, CORE_VALUES):
        with col:
            with st.container(border=True):
                st.markdown(f"**{title}**")
                st.caption(desc)


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------

def render_footer():
    st.markdown(
        f'<div class="footer-wrap"><div class="footer-inner">'
        f'© {datetime.now().year} NAWASA — National Water & Sewerage Authority. '
        f'For emergencies, use the Report tab.</div></div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------
# App layout
# --------------------------------------------------------------------------

render_hero()

tabs = st.tabs(SECTION_LABELS)
with tabs[0]:
    render_chat_section()
with tabs[1]:
    render_outage_section()
with tabs[2]:
    render_bill_estimator()
with tabs[3]:
    render_meter_reading_guide()
with tabs[4]:
    render_disconnection_guide()
with tabs[5]:
    render_maintenance_scheduler()
with tabs[6]:
    render_office_locator()
with tabs[7]:
    render_core_values()

render_footer()

"""
NAWASA Customer Portal & AI Assistant
Merged Version
- Original Tide & Gauge UI
- Gemini AI Chatbot
- Grenada Version
"""

import os
import streamlit as st

from datetime import date, datetime, timedelta

from google import genai
from google.genai import types

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="NAWASA Customer Portal",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# GEMINI MODEL
# ---------------------------------------------------------

MODEL_NAME = "gemini-3.1-flash-lite"

SYSTEM_INSTRUCTION = """
You are NAWASA Assist, the official customer assistant for
Grenada's National Water & Sewerage Authority.

Answer ONLY questions relating to NAWASA.

If information is unknown reply:

"I am sorry, I do not have that information."

Facts:

• NAWASA stands for National Water & Sewerage Authority.

• NAWASA serves Grenada,
Carriacou,
and Petite Martinique.

• Mission:
To provide clean, safe and reliable drinking water and
efficient sewage services.

• Motto:
Committed to Meeting Customers' Needs.

• Email:
communications@nawasa.gd

• WhatsApp:
405-5245
459-6064
405-9143

• Main Office:
The Carenage
St. George's
Grenada

• Office Hours
Monday-Friday
8:00 AM - 4:00 PM

• Cash Office
7:30 AM - 3:00 PM

• Customers can request:

- New connection
- Meter replacement
- Change of name
- Change of mailing address
- Disconnection
- Reconnection

• High water usage may be caused by leaks.

• To detect leaks:

Turn off all taps.

Wait 1-2 hours.

If the meter moves,
there is likely a leak.

Stay polite,
professional,
and concise.
"""

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Gemini Setup")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.get("api_key", "")
    )

    if api_key:
        st.session_state.api_key = api_key

    st.divider()

    if st.button("Reset Conversation"):

        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
        st.session_state.pop("client", None)
        st.session_state.pop("chat_api_key", None)

        st.rerun()

# ---------------------------------------------------------
# INITIALIZE GEMINI
# ---------------------------------------------------------

api_key = st.session_state.get("api_key", "").strip()

if api_key:

    if (
        "chat" not in st.session_state
        or st.session_state.get("chat_api_key") != api_key
    ):

        os.environ["GEMINI_API_KEY"] = api_key

        st.session_state.client = genai.Client()

        st.session_state.chat = (
            st.session_state.client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                ),
            )
        )

        st.session_state.chat_api_key = api_key

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

html,
body,
[class*="css"]{
font-family:'Inter',sans-serif;
color:#10242E;
}

h1,h2,h3,h4{
font-family:'Space Grotesk',sans-serif!important;
}

.mono{
font-family:'JetBrains Mono',monospace;
}

.block-container{
padding-top:0!important;
padding-bottom:3rem;
max-width:1100px;
}

header[data-testid="stHeader"]{
background:transparent;
}

/* Hero */

.hero-wrap{

margin:-1rem -100vw 0 -100vw;
padding:0 100vw;

background:linear-gradient(
120deg,
#0B3D59 0%,
#0F7173 100%
);

position:relative;
overflow:hidden;

}

.hero-inner{

max-width:1100px;

margin:auto;

padding:2rem 1rem 4.5rem;

}

.hero-eyebrow{

display:inline-flex;

gap:6px;

color:#4FD1C5;

font-family:'JetBrains Mono';

font-size:.72rem;

letter-spacing:.08em;

text-transform:uppercase;

}

.hero-title{

color:white;

font-size:2.6rem;

font-weight:700;

margin-top:.5rem;

}

.hero-sub{

color:#CFEAE8;

font-size:1rem;

max-width:520px;

}

/* Tabs */

.stTabs [data-baseweb="tab-list"]{

gap:4px;

background:#EAF3F1;

padding:5px;

border-radius:999px;

margin-top:-2.5rem;

}

.stTabs [data-baseweb="tab"]{

font-family:'JetBrains Mono';

border-radius:999px;

padding:10px 16px;

}

.stTabs [aria-selected="true"]{

background:#0B3D59!important;

color:white!important;

}

.stTabs [data-baseweb="tab-highlight"]{

display:none;

}

</style>
""",
unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

def init_state():

    defaults = {

        "chat_history":[
            {
                "role":"assistant",
                "content":"Welcome to NAWASA Customer Services. How may I help you today?"
            }
        ],

        "notifications":[

            {
                "title":"Scheduled Maintenance",
                "body":"Water interruption in St. George's Friday 6AM-2PM."
            },

            {
                "title":"Bill Reminder",
                "body":"Your latest statement is available."
            }

        ],

        "unread_notifications":2,

        "outage_reports":[],

        "maintenance_requests":[],

        "messages":[]
    }

    for k,v in defaults.items():

        if k not in st.session_state:

            st.session_state[k]=v

init_state()
# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

WAVE_SVG = """
<div class="hero-wave">
<svg
viewBox="0 0 1440 90"
xmlns="http://www.w3.org/2000/svg"
preserveAspectRatio="none"
style="width:100%;height:70px;display:block;">

<path
fill="#ffffff"
d="M0,32 C240,80 480,0 720,24 C960,48 1200,88 1440,40
L1440,90
L0,90Z"/>

</svg>
</div>
"""


def render_notifications():

    st.markdown("### Notifications")

    if not st.session_state.notifications:

        st.success("You're all caught up!")

    else:

        for notice in st.session_state.notifications:

            with st.container(border=True):

                st.markdown(f"**{notice['title']}**")

                st.caption(notice["body"])

    if st.button("Clear Notifications"):

        st.session_state.notifications = []

        st.session_state.unread_notifications = 0

        st.rerun()


def render_hero():

    st.markdown(
        '<div class="hero-wrap"><div class="hero-inner">',
        unsafe_allow_html=True
    )

    left,right = st.columns([5,1])

    with left:

        st.markdown(

        """
<div class="hero-eyebrow">
● Live · Grenada
</div>

<h1 class="hero-title">
NAWASA Customer Portal
</h1>

<p class="hero-sub">

Report outages,

estimate your bill,

check your meter,

schedule maintenance,

or chat with our AI assistant.

</p>

        """,

        unsafe_allow_html=True

        )

    with right:

        st.write("")
        st.write("")

        with st.popover(
            f"🔔 {st.session_state.unread_notifications}"
        ):

            render_notifications()

    st.markdown(

        "</div>"+WAVE_SVG+"</div>",

        unsafe_allow_html=True

    )


# ---------------------------------------------------------
# GEMINI CHAT
# ---------------------------------------------------------

def ask_gemini(prompt):

    api_key = st.session_state.get("api_key","").strip()

    if not api_key:

        return (
            "Please enter your Gemini API key in the sidebar "
            "before chatting."
        )

    try:

        response = (
            st.session_state.chat.send_message(prompt)
        )

        return response.text

    except Exception as e:

        return f"Error: {e}"


# ---------------------------------------------------------
# CHAT TAB
# ---------------------------------------------------------

def render_chat_section():

    st.markdown(
        '<div class="section-eyebrow">24/7 AI Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "### Ask NAWASA anything"
    )

    if len(st.session_state.chat_history)==0:

        st.session_state.chat_history.append(

            {
                "role":"assistant",

                "content":
                "Welcome to NAWASA Customer Services. "
                "How may I help you today?"
            }

        )

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    prompt = st.chat_input(
        "Ask NAWASA anything..."
    )

    if prompt:

        st.session_state.chat_history.append(

            {
                "role":"user",
                "content":prompt
            }

        )

        with st.chat_message("user"):

            st.write(prompt)

        with st.chat_message("assistant"):

            with st.spinner(
                "NAWASA Assistant is thinking..."
            ):

                reply = ask_gemini(prompt)

                st.write(reply)

        st.session_state.chat_history.append(

            {
                "role":"assistant",
                "content":reply
            }

        )

        st.rerun()
        # ---------------------------------------------------------
# REPORT OUTAGE
# ---------------------------------------------------------

def render_outage_section():

    st.markdown(
        '<div class="section-eyebrow">Rapid Response</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Report an outage or burst pipe")

    st.caption(
        "Provide as much information as possible so a NAWASA crew "
        "can locate the problem quickly."
    )

    with st.form("outage_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:

            issue_type = st.selectbox(

                "Issue Type",

                [
                    "No Water Supply",
                    "Burst Pipe",
                    "Low Water Pressure",
                    "Discoloured Water",
                    "Water Leak",
                    "Other"
                ]
            )

            location = st.text_input(
                "Location / Landmark"
            )

        with col2:

            severity = st.select_slider(

                "Severity",

                options=[
                    "Low",
                    "Medium",
                    "High",
                    "Emergency"
                ],

                value="Medium"
            )

            contact = st.text_input(
                "Contact Number"
            )

        description = st.text_area(
            "Describe the problem"
        )

        submitted = st.form_submit_button(

            "Submit Report",

            type="primary"
        )

    if submitted:

        if not location:

            st.error(
                "Please provide the location."
            )

        elif not contact:

            st.error(
                "Please provide a contact number."
            )

        else:

            report = {

                "issue": issue_type,

                "location": location,

                "severity": severity,

                "contact": contact,

                "description": description,

                "time": datetime.now().strftime(
                    "%d %B %Y %I:%M %p"
                )

            }

            st.session_state.outage_reports.append(report)

            st.success(
                "✅ Your report has been submitted successfully."
            )

    # -------------------------------------------------

    if st.session_state.outage_reports:

        st.markdown("---")

        st.markdown("### Submitted Reports")

        for report in reversed(
            st.session_state.outage_reports
        ):

            with st.container(border=True):

                severity = report["severity"]

                if severity == "Low":
                    chip = "🟢"

                elif severity == "Medium":
                    chip = "🟡"

                elif severity == "High":
                    chip = "🟠"

                else:
                    chip = "🔴"

                st.markdown(
                    f"### {chip} {report['issue']}"
                )

                st.write(
                    f"**Location:** {report['location']}"
                )

                st.write(
                    f"**Severity:** {report['severity']}"
                )

                st.write(
                    f"**Contact:** {report['contact']}"
                )

                if report["description"]:

                    st.write(
                        f"**Description:** {report['description']}"
                    )

                st.caption(
                    f"Submitted: {report['time']}"
                )

    else:

        st.info(
            "No outage reports have been submitted yet."
        )
        # ---------------------------------------------------------
# BILL ESTIMATOR
# ---------------------------------------------------------

BASE_CHARGE = 15.00

RATE_TIERS = [

    (0,10,3.50),

    (10,20,5.00),

    (20,40,7.25),

    (40,float("inf"),9.75)

]


def estimate_bill(usage):

    total = BASE_CHARGE

    remaining = usage

    for low, high, rate in RATE_TIERS:

        amount = min(remaining, high-low)

        if amount <= 0:
            continue

        total += amount * rate

        remaining -= amount

        if remaining <= 0:
            break

    return round(total,2)


# ---------------------------------------------------------
# BILL TAB
# ---------------------------------------------------------

def render_bill_estimator():

    st.markdown(
        '<div class="section-eyebrow">Estimate</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Monthly Water Bill")

    st.caption(
        "Estimate your monthly bill based on your water usage."
    )

    usage = st.slider(

        "Estimated Monthly Usage (m³)",

        min_value=0,

        max_value=100,

        value=15

    )

    bill = estimate_bill(usage)

    left,right = st.columns([1,1])

    with left:

        st.markdown(

            f"""
<div class="gauge">

<div class="gauge-label">

Estimated Bill

</div>

<div class="gauge-value">

${bill:.2f}

</div>

<div class="gauge-unit">

XCD

</div>

</div>
            """,

            unsafe_allow_html=True

        )

        st.caption(

            f"Includes a base charge of ${BASE_CHARGE:.2f}"

        )

    with right:

        with st.container(border=True):

            st.markdown("### Current Rate Tiers")

            for low,high,rate in RATE_TIERS:

                if high == float("inf"):

                    label = f"{low}+ m³"

                else:

                    label = f"{low}-{int(high)} m³"

                st.write(
                    f"{label}  •  ${rate:.2f} per m³"
                )


# ---------------------------------------------------------
# METER GUIDE
# ---------------------------------------------------------

def render_meter_reading_guide():

    st.markdown(
        '<div class="section-eyebrow">Meter Reading</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Read Your Water Meter")

    with st.expander(
        "How to Read Your Meter",
        expanded=True
    ):

        st.markdown("""

1. Locate the water meter.

2. Lift the meter cover.

3. Read the black numbers from left to right.

4. Ignore the red digits.

5. Record the reading.

6. Compare it with your previous reading to calculate usage.

""")

    with st.expander(
        "Leak Detection"
    ):

        st.markdown("""

Turn off:

- All taps

- Washing machines

- Toilets

- Outdoor hoses

Wait approximately two hours.

Read the meter again.

If the reading changes without using water,

there is likely a leak.

""")

        col1,col2 = st.columns(2)

        with col1:

            before = st.number_input(

                "Reading Before",

                min_value=0.0,

                format="%.3f"

            )

        with col2:

            after = st.number_input(

                "Reading After",

                min_value=0.0,

                format="%.3f"

            )

        if st.button("Check Meter"):

            difference = after-before

            st.markdown(

                f"""
<div class="gauge">

<div class="gauge-label">

Meter Difference

</div>

<div class="gauge-value">

{difference:.3f}

</div>

<div class="gauge-unit">

m³

</div>

</div>
                """,

                unsafe_allow_html=True

            )

            if difference > 0:

                st.warning(
                    "Possible leak detected. Please report it using the Report tab."
                )

            else:

                st.success(
                    "No leak detected from this test."
                )
                # ---------------------------------------------------------
# DISCONNECTION POLICY
# ---------------------------------------------------------

def render_disconnection_guide():

    st.markdown(
        '<div class="section-eyebrow">Customer Policy</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Disconnection & Reconnection")

    left,right = st.columns(2)

    with left:

        with st.container(border=True):

            st.markdown("#### Water Service May Be Disconnected For")

            st.markdown("""

- Customer request

- Non-payment of arrears

- Illegal meter tampering

- Water wastage or abuse

- Unauthorized connections

""")

    with right:

        with st.container(border=True):

            st.markdown("#### Reconnection")

            st.markdown("""

• After outstanding balances are paid.

• Once reconnection requirements are satisfied.

• Processing normally begins after payment is confirmed.

For additional assistance contact the nearest NAWASA office.

""")

# ---------------------------------------------------------
# MAINTENANCE REQUEST
# ---------------------------------------------------------

def render_maintenance_scheduler():

    st.markdown(
        '<div class="section-eyebrow">Maintenance</div>',
        unsafe_allow_html=True
    )

    st.markdown("### Schedule Maintenance")

    with st.form("maintenance_form", clear_on_submit=True):

        service = st.selectbox(

            "Service Required",

            [

                "New Water Connection",

                "Pipe Repair",

                "Meter Replacement",

                "Water Quality Test",

                "Inspection",

                "Other"

            ]

        )

        preferred_date = st.date_input(

            "Preferred Date",

            min_value=date.today(),

            value=date.today()+timedelta(days=3)

        )

        address = st.text_input("Service Address")

        notes = st.text_area("Additional Notes")

        submit = st.form_submit_button(

            "Submit Request",

            type="primary"

        )

    if submit:

        if not address:

            st.error("Please enter the service address.")

        else:

            st.session_state.maintenance_requests.append({

                "service":service,

                "date":preferred_date,

                "address":address,

                "notes":notes

            })

            st.success(
                "Maintenance request submitted successfully."
            )

    if st.session_state.maintenance_requests:

        st.markdown("---")

        st.markdown("### Submitted Requests")

        for request in reversed(

            st.session_state.maintenance_requests

        ):

            with st.container(border=True):

                st.markdown(
                    f"**{request['service']}**"
                )

                st.write(request["address"])

                st.caption(request["date"])

# ---------------------------------------------------------
# GRENADA OFFICES
# ---------------------------------------------------------

OFFICES = [

    {

        "name":"Head Office",

        "location":"The Carenage, St. George's",

        "phone":"(473) 440-2302",

        "hours":"Mon-Fri 8:00 AM - 4:00 PM"

    },

    {

        "name":"Grenville Office",

        "location":"Grenville",

        "phone":"(473) 442-7240",

        "hours":"Mon-Fri 8:00 AM - 4:00 PM"

    },

    {

        "name":"Gouyave Office",

        "location":"Gouyave",

        "phone":"(473) 444-7224",

        "hours":"Mon-Fri 8:00 AM - 4:00 PM"

    },

    {

        "name":"Grand Anse Office",

        "location":"Grand Anse",

        "phone":"(473) 444-1005",

        "hours":"Mon-Fri 8:00 AM - 4:00 PM"

    }

]

def render_office_locator():

    st.markdown(

        '<div class="section-eyebrow">Office Locator</div>',

        unsafe_allow_html=True

    )

    st.markdown("### NAWASA Offices")

    cols = st.columns(2)

    for i, office in enumerate(OFFICES):

        with cols[i % 2]:

            with st.container(border=True):

                st.markdown(f"### {office['name']}")

                st.write(office["location"])

                st.write(f"☎ {office['phone']}")

                st.caption(office["hours"])

# ---------------------------------------------------------
# CORE VALUES
# ---------------------------------------------------------

VALUES = [

    (

        "Excellence",

        "Delivering quality service to every customer."

    ),

    (

        "Accountability",

        "Being responsible to customers and stakeholders."

    ),

    (

        "Innovation",

        "Improving operations through creativity."

    ),

    (

        "Community",

        "Supporting Grenada through reliable water services."

    )

]

def render_core_values():

    st.markdown(

        '<div class="section-eyebrow">Core Values</div>',

        unsafe_allow_html=True

    )

    st.markdown("### What Guides Us")

    cols = st.columns(4)

    for col,(title,text) in zip(cols,VALUES):

        with col:

            with st.container(border=True):

                st.markdown(f"### {title}")

                st.caption(text)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

def render_footer():

    st.markdown("""

<hr>

<center>

<b>NAWASA Grenada</b><br>

National Water & Sewerage Authority<br>

Committed to Meeting Customers' Needs

</center>

""",

    unsafe_allow_html=True

)

# ---------------------------------------------------------
# APP LAYOUT
# ---------------------------------------------------------

render_hero()

tabs = st.tabs([

    "Ask",

    "Report",

    "Bill",

    "Meter",

    "Policy",

    "Schedule",

    "Offices",

    "Values"

])

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

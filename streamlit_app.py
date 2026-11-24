import streamlit as st

st.set_page_config(page_title="FinAssist AI", page_icon="💳", layout="wide")

TEXT = {
    "English": {
        "tagline": "Simple financial learning and government-scheme discovery",
        "profile": "My Profile", "schemes": "Find Schemes", "assistant": "Ask FinAssist",
        "learn": "Financial Learning", "roadmap": "My Roadmap", "fraud": "Fraud Safety",
        "name": "First name (optional)", "age": "Age", "state": "State / UT",
        "occupation": "Occupation", "income": "Approx. annual household income (₹)",
        "bank": "Do you have a bank or post-office savings account?",
        "farmer": "Does your family own cultivable agricultural land?",
        "tax": "Are you currently / previously an income-tax payer?",
        "save": "Save profile", "saved": "Profile saved for this session.",
        "question": "Ask a question", "send": "Ask", "language": "Language",
        "voice": "Voice question (optional)", "transcribe": "Transcribe audio",
        "profile_needed": "Complete and save your profile first to see scheme matches.",
    },
    "हिन्दी": {
        "tagline": "आसान वित्तीय जानकारी और सरकारी योजनाओं की खोज",
        "profile": "मेरी प्रोफ़ाइल", "schemes": "योजनाएँ खोजें", "assistant": "FinAssist से पूछें",
        "learn": "वित्तीय शिक्षा", "roadmap": "मेरी योजना", "fraud": "धोखाधड़ी से सुरक्षा",
        "name": "पहला नाम (वैकल्पिक)", "age": "आयु", "state": "राज्य / केंद्र शासित प्रदेश",
        "occupation": "व्यवसाय", "income": "परिवार की अनुमानित वार्षिक आय (₹)",
        "bank": "क्या आपके पास बैंक या डाकघर का बचत खाता है?",
        "farmer": "क्या आपके परिवार के पास खेती योग्य भूमि है?",
        "tax": "क्या आप वर्तमान में या पहले आयकरदाता रहे हैं?",
        "save": "प्रोफ़ाइल सेव करें", "saved": "प्रोफ़ाइल इस सत्र के लिए सेव हो गई।",
        "question": "अपना प्रश्न पूछें", "send": "पूछें", "language": "भाषा",
        "voice": "आवाज़ में प्रश्न (वैकल्पिक)", "transcribe": "ऑडियो को टेक्स्ट में बदलें",
        "profile_needed": "योजनाएँ देखने के लिए पहले अपनी प्रोफ़ाइल भरकर सेव करें।",
    }
}

def save_profile(p):
    # Streamlit session state keeps demo data only for the active session.
    st.session_state["finassist_profile"] = p

def latest_profile():
    return st.session_state.get("finassist_profile")

SCHEMES = [
    {
        "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
        "summary": "A one-year renewable life-insurance scheme offered through participating banks/post offices.",
        "rule": lambda p: 18 <= p["age"] <= 50 and p["bank"],
        "eligibility": "Individual participating bank/post-office account holders aged 18–50, subject to scheme conditions and consent.",
        "docs": "Ask the participating bank/post office for its current enrolment form and KYC requirements.",
        "url": "https://jansuraksha.gov.in/"
    },
    {
        "name": "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
        "summary": "A one-year renewable accident-insurance scheme through participating banks/post offices.",
        "rule": lambda p: 18 <= p["age"] <= 70 and p["bank"],
        "eligibility": "Individual participating bank/post-office account holders aged 18–70, subject to scheme conditions and consent.",
        "docs": "Ask the participating bank/post office for its current enrolment form and KYC requirements.",
        "url": "https://jansuraksha.gov.in/"
    },
    {
        "name": "Atal Pension Yojana (APY)",
        "summary": "A pension scheme for eligible subscribers, administered through banks and post offices.",
        "rule": lambda p: 18 <= p["age"] <= 40 and p["bank"] and not p["tax"],
        "eligibility": "Indian citizens aged 18–40 with a savings account; a person who is or has been an income-tax payer is not eligible to join a new APY account.",
        "docs": "Contact your bank/post office for current enrolment and KYC requirements.",
        "url": "https://pfrda.org.in/web/pfrda/w/faqs/atal-pension-yojana"
    },
    {
        "name": "PM-KISAN Samman Nidhi",
        "summary": "Income support for eligible landholding farmer families, subject to exclusions and government verification.",
        "rule": lambda p: p["farmer"],
        "eligibility": "For eligible landholding farmer families with cultivable land, subject to official exclusions, land-record checks and State/UT verification.",
        "docs": "Land records, bank details and identity/KYC documents may be required; confirm the exact list on the official portal.",
        "url": "https://pmkisan.gov.in/"
    },
]

def answer_question(q, lang):
    ql = q.lower()
    hindi = lang == "हिन्दी"
    if any(w in ql for w in ["upi", "pin", "otp", "scam", "fraud", "फ्रॉड", "ओटीपी", "धोख"]):
        return ("सुरक्षा: अपना OTP, UPI PIN, पासवर्ड या स्क्रीन-शेयरिंग एक्सेस किसी को न दें। पैसे प्राप्त करने के लिए UPI PIN डालने की आवश्यकता नहीं होती। संदेह होने पर भुगतान रोकें और अपने बैंक के आधिकारिक नंबर/ऐप से संपर्क करें।"
                if hindi else
                "Safety: Never share your OTP, UPI PIN, password or screen-sharing access. You do not need to enter a UPI PIN to receive money. If something seems suspicious, stop the transaction and contact your bank through its official app or number.")
    if any(w in ql for w in ["savings", "बचत", "save money"]):
        return ("बचत की शुरुआत छोटी, नियमित राशि से करें। जरूरी खर्च लिखें, आय और खर्च की तुलना करें और आपातकालीन जरूरतों के लिए धीरे-धीरे अलग राशि रखें।"
                if hindi else
                "Start with a small, regular saving habit. Track essential expenses, compare income with spending, and gradually build money for unexpected needs. Choose regulated institutions and understand fees and withdrawal rules.")
    if any(w in ql for w in ["loan", "लोन", "कर्ज"]):
        return ("ऋण लेने से पहले ब्याज दर, कुल भुगतान, EMI, प्रोसेसिंग फीस, देरी का शुल्क और समय से पहले भुगतान की शर्तें समझें। केवल EMI नहीं, कुल लागत की तुलना करें।"
                if hindi else
                "Before taking a loan, understand the interest rate, total repayment, EMI, processing fee, late charges and prepayment terms. Compare the total cost, not just the EMI.")
    if any(w in ql for w in ["insurance", "बीमा"]):
        return ("बीमा जोखिम से सुरक्षा देता है। पॉलिसी में क्या शामिल है, क्या शामिल नहीं है, प्रीमियम, अवधि और क्लेम प्रक्रिया ध्यान से पढ़ें।"
                if hindi else
                "Insurance helps manage specific risks. Read what is covered and excluded, the premium, policy term, waiting periods (if any), and claim process before choosing.")
    if any(w in ql for w in ["bank", "बैंक", "account", "खाता"]):
        return ("बैंक खाता पैसे जमा करने, भुगतान पाने और डिजिटल लेन-देन में मदद करता है। न्यूनतम बैलेंस, शुल्क, नामांकन और शिकायत प्रक्रिया समझें।"
                if hindi else
                "A bank account can help you store money, receive payments and make transactions. Check minimum-balance rules, fees, nominee details and the bank's complaint process.")
    if any(w in ql for w in ["apy", "atal pension", "पेंशन"]):
        return ("Atal Pension Yojana में नए नामांकन के लिए आयु 18–40 वर्ष, बचत खाता और आयकरदाता न होना जैसी शर्तें हैं। आधिकारिक PFRDA जानकारी और बैंक से पुष्टि करें।"
                if hindi else
                "Atal Pension Yojana generally requires the applicant to be 18–40, have a savings account, and not be an income-tax payer (for new enrolment). Confirm current terms with PFRDA or your bank.")
    return ("मैं सामान्य वित्तीय जानकारी दे सकता/सकती हूँ। अपना प्रश्न बचत, बैंकिंग, ऋण, बीमा, पेंशन, सरकारी योजना या धोखाधड़ी से सुरक्षा के बारे में थोड़ा स्पष्ट लिखें।"
            if hindi else
            "I can explain general financial topics. Try asking about savings, banking, loans, insurance, pensions, government schemes or fraud prevention. This demo is educational and does not provide personalized investment or legal advice.")

st.markdown("""
<style>
.main {background-color:#f6f8fc;}
.block-container {padding-top:1.6rem;}
.hero {padding:1.4rem 1.6rem;border-radius:18px;background:linear-gradient(115deg,#102a56,#2364a8);color:white;margin-bottom:1rem;}
.hero h1 {color:white;margin:0;}
.small-note {font-size:0.88rem;color:#586579;}
div[data-testid="stMetric"] {background:white;padding:14px;border-radius:12px;border:1px solid #e8edf5;}
</style>
""", unsafe_allow_html=True)

lang = st.sidebar.selectbox("Language / भाषा", ["English", "हिन्दी"])
t = TEXT[lang]
st.sidebar.title("💳 FinAssist AI")
page = st.sidebar.radio("Navigate", [t["profile"], t["schemes"], t["assistant"], t["learn"], t["roadmap"], t["fraud"]])
st.sidebar.caption("Prototype • India")
st.markdown(f'<div class="hero"><h1>💳 FinAssist AI</h1><p>{t["tagline"]}</p></div>', unsafe_allow_html=True)

profile = latest_profile()

if page == t["profile"]:
    st.subheader(t["profile"])
    st.info("Demo privacy: use fictional/sample details only. Profile data stays in the active session. Do not enter Aadhaar, account numbers, passwords, OTPs or other sensitive identifiers.")
    defaults = profile or {}
    with st.form("profile_form"):
        name = st.text_input(t["name"], value=defaults.get("name") or "")
        age = st.number_input(t["age"], min_value=0, max_value=110, value=int(defaults.get("age") or 25))
        state = st.selectbox(t["state"], ["Delhi","Uttar Pradesh","Bihar","Rajasthan","Madhya Pradesh","Maharashtra","West Bengal","Tamil Nadu","Karnataka","Other"])
        occupation = st.selectbox(t["occupation"], ["Salaried","Self-employed","Agriculture","Student","Homemaker","Unemployed","Other"])
        income = st.number_input(t["income"], min_value=0, max_value=100000000, value=int(defaults.get("income") or 200000), step=10000)
        bank = st.checkbox(t["bank"], value=bool(defaults.get("bank", True)))
        farmer = st.checkbox(t["farmer"], value=bool(defaults.get("farmer", False)))
        tax = st.checkbox(t["tax"], value=bool(defaults.get("tax", False)))
        submitted = st.form_submit_button(t["save"], type="primary")
        if submitted:
            save_profile({"name":name,"age":int(age),"state":state,"occupation":occupation,
                          "income":float(income),"bank":bank,"farmer":farmer,"tax":tax})
            st.success(t["saved"])
            st.rerun()
    if profile:
        st.caption("The profile is kept only for this active session and is used for the eligibility demonstration.")

elif page == t["schemes"]:
    st.subheader(t["schemes"])
    if not profile:
        st.warning(t["profile_needed"])
    else:
        st.write(f"Profile: age {profile['age']} • {profile['occupation']} • {profile['state']}")
        matches = [s for s in SCHEMES if s["rule"](profile)]
        st.metric("Potential matches", len(matches))
        if not matches:
            st.info("No match found in this small demo catalogue. This does not mean you are ineligible for all schemes.")
        for s in matches:
            with st.expander("✅ " + s["name"], expanded=True):
                st.write(s["summary"])
                st.markdown("**Preliminary eligibility**")
                st.write(s["eligibility"])
                st.markdown("**Documents / next step**")
                st.write(s["docs"])
                st.link_button("Open official scheme website", s["url"])
        st.warning("These are preliminary rule-based matches, not an official eligibility decision. Scheme rules and required documents can change. Verify with the official portal or relevant department.")

elif page == t["assistant"]:
    st.subheader(t["assistant"])
    st.caption("Ask in English or Hindi. The built-in assistant uses a small set of educational responses.")
    if "chat" not in st.session_state:
        st.session_state.chat = []
    for item in st.session_state.chat:
        with st.chat_message(item["role"]):
            st.write(item["content"])
    q = st.chat_input(t["question"])
    if q:
        a = answer_question(q, lang)
        st.session_state.chat.append({"role":"user","content":q})
        st.session_state.chat.append({"role":"assistant","content":a})
        st.rerun()
    st.divider()
    st.markdown("**Voice input (optional)**")
    audio = st.audio_input(t["voice"])
    if audio:
        st.audio(audio)
        st.info("Audio recording captured. This deployable baseline provides typed chat; speech-to-text can be connected as a separate service.")

elif page == t["learn"]:
    st.subheader(t["learn"])
    topics = {
        "Savings / बचत": "A savings account stores money with a regulated bank. Compare interest, fees, access and minimum-balance conditions.",
        "Insurance / बीमा": "Insurance transfers specified financial risks under a contract. Check exclusions, premium, coverage, waiting periods and claim requirements.",
        "Loans / ऋण": "A loan must be repaid. Compare annual interest, total repayment, processing charges, late fees and prepayment rules.",
        "Pension / पेंशन": "A pension can provide income in later life. Eligibility, contribution amounts and benefits depend on the scheme.",
        "Digital banking / डिजिटल बैंकिंग": "Use official bank apps, strong device security and transaction alerts. Never share OTPs or UPI PINs."
    }
    for title, body in topics.items():
        with st.expander(title):
            st.write(body)

elif page == t["roadmap"]:
    st.subheader(t["roadmap"])
    if not profile:
        st.warning(t["profile_needed"])
    else:
        st.write("A simple educational roadmap based on the profile. It is not an investment recommendation.")
        steps = [
            "List essential monthly expenses and regular income.",
            "Check that your bank contact details and nominee information are up to date.",
            "Build a small emergency reserve gradually, according to what is affordable.",
            "Understand the risks, fees and conditions before signing up for a financial product.",
            "Check government scheme eligibility through official portals and keep documents current.",
            "Review the plan every 3–6 months or after a major change in circumstances."
        ]
        for i, step in enumerate(steps, 1):
            st.checkbox(f"{i}. {step}", key=f"roadmap_{i}")
        st.caption("Avoid borrowing or investing based only on an app suggestion. Ask a trusted, qualified adviser when needed.")

elif page == t["fraud"]:
    st.subheader(t["fraud"])
    st.error("Never share OTP, UPI PIN, CVV, passwords or screen-sharing access.")
    items = [
        ("Fake KYC update", "Do not click unknown links or install remote-access apps. Contact your bank using its official app or website."),
        ("UPI collect request", "Read the request carefully. A UPI PIN authorizes a payment; it is not needed to receive money."),
        ("Impersonation calls", "Banks and government departments should not ask you to disclose your PIN or OTP over a call."),
        ("Too-good-to-be-true offers", "Verify scheme announcements on official government domains. Do not pay an agent to guarantee benefits."),
        ("Suspicious transaction", "Contact your bank immediately through official channels. In India, report cyber financial fraud through the national cybercrime helpline 1930 or cybercrime.gov.in.")
    ]
    for title, body in items:
        with st.expander(title):
            st.write(body)
    st.markdown("Official cybercrime portal: https://cybercrime.gov.in/")

st.divider()
st.caption("FinAssist AI is an educational prototype. It is not affiliated with the Government of India, does not submit applications or process payments, and does not make official eligibility decisions. Profile data remains in the active session; verify current information with the relevant department.")

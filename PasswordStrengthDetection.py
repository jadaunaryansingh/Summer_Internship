import streamlit as st
import re
st.set_page_config(
    page_title="Password Strength Checker",
    page_icon="🔐",
    layout="centered"
)
st.markdown("""
    <style>
        .main-container {
            background-color: #f8f9fa;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .strength-box {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.8rem;
            border-radius: 10px;
            margin-top: 10px;
        }
        .weak { background-color: #ffcccc; color: #a30000; }
        .medium { background-color: #fff3cd; color: #856404; }
        .strong { background-color: #d4edda; color: #155724; }
        .suggestion {
            font-size: 0.95rem;
            margin-left: 1rem;
            margin-top: 5px;
        }
        .footer {
            font-size: 0.85rem;
            color: #888;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("## 🔐 Password Strength Checker")
st.write("Enter a password to check its strength and get improvement tips.")
def check_strength(password):
    length = len(password)
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    score = sum([has_lower, has_upper, has_digit, has_special])
    suggestions = []

    if length < 8:
        suggestions.append("➤ Make it longer (at least 8 characters).")
    if not has_lower:
        suggestions.append("➤ Add lowercase letters (a–z).")
    if not has_upper:
        suggestions.append("➤ Add uppercase letters (A–Z).")
    if not has_digit:
        suggestions.append("➤ Include numbers (0–9).")
    if not has_special:
        suggestions.append("➤ Use special characters (!@#$%^&* etc).")

    if length < 6 or score < 2:
        return "Weak", score, suggestions
    elif score == 2 and length >= 6:
        return "Medium", score, suggestions
    elif score >= 3 and length >= 8:
        return "Strong", score, ["✅ Great job! Just avoid common words."]
    else:
        return "Medium", score, suggestions
password = st.text_input("🔑 Enter your password:", type="password")
if password:
    strength, score, tips = check_strength(password)

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    if strength == "Weak":
        st.markdown(f'<div class="strength-box weak">❌ Weak Password</div>', unsafe_allow_html=True)
    elif strength == "Medium":
        st.markdown(f'<div class="strength-box medium">⚠ Medium Password</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="strength-box strong">✅ Strong Password</div>', unsafe_allow_html=True)
    st.markdown("### 🔢 Strength Meter")
    st.progress(min(score / 4, 1.0))
    st.markdown("### 💡 Suggestions to Improve:")
    for tip in tips:
        st.markdown(f'<div class="suggestion">{tip}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">🔒 Your password is never stored or shared. All checks happen locally in your browser.</div>', unsafe_allow_html=True)
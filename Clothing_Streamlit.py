import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="StyleMe – AI Fashion Recommender", layout="wide")
# --- CUSTOM STYLING ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(-45deg, #d4fc79, #96e6a1, #a1c4fd, #c2e9fb);
            background-size: 400% 400%;
            animation: gradientBG 20s ease infinite;
            color: #2C3E50;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .main-title {
            font-size: 56px;
            font-weight: bold;
            color: #1B1464;
            text-align: center;
            margin-top: 20px;
        }

        .subtitle {
            font-size: 22px;
            text-align: center;
            color: #2C3E50;
            margin-bottom: 40px;
        }

        .stButton>button {
            background-color: #6C5CE7;
            color: white;
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-size: 18px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #4834d4;
            color: #f1f2f6;
        }

        .footer {
            text-align: center;
            color: #7F8C8D;
            font-size: 14px;
            margin-top: 50px;
        }
    </style>
    <div class="main-title">👗 StyleMe</div>
    <div class="subtitle">Your AI-powered clothing stylist for the perfect fit, every time.</div>
""", unsafe_allow_html=True)

# --- AI BODY SHAPE DETECTION FUNCTION ---
def detect_body_shape(image_bytes):
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)
        if not results.pose_landmarks:
            return "Could not detect full body"
        landmarks = results.pose_landmarks.landmark
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        shoulder_width = abs(left_shoulder.x - right_shoulder.x)
        hip_width = abs(left_hip.x - right_hip.x)
        ratio = shoulder_width / hip_width if hip_width != 0 else 0
        if ratio > 1.2:
            return "Inverted Triangle"
        elif ratio < 0.8:
            return "Pear"
        elif 0.9 <= ratio <= 1.1:
            return "Hourglass"
        else:
            return "Rectangle"

# --- SUGGESTIONS DATA (including Oval and Trapezoid for Male) ---
suggestions = {
    "Pear": {
        "Casual": ["A-line dresses", "Structured tops", "Wide-leg jeans"],
        "Formal": ["Blazers with shoulder pads", "Fit and flare dresses"],
        "Party": ["Off-shoulder tops", "Statement necklaces"],
        "Ethnic": ["Anarkali suits", "Lehengas with heavy dupattas"]
    },
    "Hourglass": {
        "Casual": ["Wrap tops", "High-waisted jeans", "Belted dresses"],
        "Formal": ["Bodycon dresses", "Tailored suits"],
        "Party": ["Sheath dresses", "Mermaid gowns"],
        "Ethnic": ["Sarees with detailed blouses", "Lehenga with fitted choli"]
    },
    "Rectangle": {
        "Casual": ["Peplum tops & skirts", "Layered outfits"],
        "Formal": ["Blazers with structure", "Wrap blouses"],
        "Party": ["Ruffle dresses", "A-line mini dresses"],
        "Ethnic": ["Layered kurtis", "Empire-waist anarkalis"]
    },
    "Triangle": {
        "Casual": ["Boat neck tops", "Flared jeans"],
        "Formal": ["Detailed jackets", "High-neck blouses"],
        "Party": ["One-shoulder dresses", "Tulle skirts"],
        "Ethnic": ["Kurtis with embroidered necklines", "Angrakha style kurtas"]
    },
    "Inverted Triangle": {
        "Casual": ["V-neck tops", "Flowy skirts"],
        "Formal": ["Minimal shoulder detailing", "High-waist pants"],
        "Party": ["Fit-and-flare dresses", "Wrap jumpsuits"],
        "Ethnic": ["Paneled kurtis", "Patiala suits"]
    },
    # New male body types
    "Oval": {
        "Casual": ["Loose fit T-shirts", "Straight-leg jeans", "Layered jackets"],
        "Formal": ["Single-breasted suits", "Shirt with vertical stripes"],
        "Party": ["V-neck sweaters", "Dark slim jeans"],
        "Ethnic": ["Kurta with straight cuts", "Nehru jackets"]
    },
    "Trapezoid": {
        "Casual": ["Fitted polo shirts", "Slim chinos", "Bomber jackets"],
        "Formal": ["Double-breasted blazers", "Tailored trousers"],
        "Party": ["Textured blazers", "Monochrome outfits"],
        "Ethnic": ["Bandhgala jackets", "Pathani suits"]
    }
}

# --- FEATURED LOOKS DATA (including Oval and Trapezoid for Male) ---
featured_looks = {
    "Female": {
        "Pear": {
            "Casual": [
                {
                    "title": "Structured Denim Jacket",
                    "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246",
                    "price": 2499,
                    "price_str": "₹2,499",
                    "link": "https://www.amazon.in/"
                },
                {
                    "title": "A-line Summer Dress",
                    "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c",
                    "price": 1999,
                    "price_str": "₹1,999",
                    "link": "https://www.amazon.in/"
                }
            ],
            "Formal": [
                {
                    "title": "Tailored Blazer Dress",
                    "image": "https://images.unsplash.com/photo-1600180758890-6eec4a07ef9d",
                    "price": 3499,
                    "price_str": "₹3,499",
                    "link": "https://www.amazon.in/"
                }
            ]
        },
        "Hourglass": {
            "Party": [
                {
                    "title": "Mermaid Sequin Gown",
                    "image": "https://images.unsplash.com/photo-1520975686471-a96b039eaa1c",
                    "price": 4799,
                    "price_str": "₹4,799",
                    "link": "https://www.amazon.in/"
                }
            ]
        }
    },
    "Male": {
        "Rectangle": {
            "Casual": [
                {
                    "title": "Slim Fit Denim Jacket",
                    "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f",
                    "price": 2999,
                    "price_str": "₹2,999",
                    "link": "https://www.amazon.in/"
                },
                {
                    "title": "Chino Pants",
                    "image": "https://images.unsplash.com/photo-1521334884684-d80222895322",
                    "price": 1799,
                    "price_str": "₹1,799",
                    "link": "https://www.amazon.in/"
                }
            ],
            "Formal": [
                {
                    "title": "Tailored Suit",
                    "image": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91",
                    "price": 5999,
                    "price_str": "₹5,999",
                    "link": "https://www.amazon.in/"
                }
            ]
        },
        "Inverted Triangle": {
            "Party": [
                {
                    "title": "Leather Jacket",
                    "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c",
                    "price": 3999,
                    "price_str": "₹3,999",
                    "link": "https://www.amazon.in/"
                }
            ]
        },
        "Oval": {
            "Casual": [
                {
                    "title": "Loose Fit Graphic T-Shirt",
                    "image": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91",
                    "price": 1599,
                    "price_str": "₹1,599",
                    "link": "https://www.amazon.in/"
                },
                {
                    "title": "Straight Leg Jeans",
                    "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f",
                    "price": 2499,
                    "price_str": "₹2,499",
                    "link": "https://www.amazon.in/"
                }
            ],
            "Formal": [
                {
                    "title": "Single-Breasted Suit",
                    "image": "https://images.unsplash.com/photo-1521334884684-d80222895322",
                    "price": 5499,
                    "price_str": "₹5,499",
                    "link": "https://www.amazon.in/"
                }
            ]
        },
        "Trapezoid": {
            "Party": [
                {
                    "title": "Textured Blazer",
                    "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c",
                    "price": 4599,
                    "price_str": "₹4,599",
                    "link": "https://www.amazon.in/"
                }
            ],
            "Formal": [
                {
                    "title": "Double-Breasted Blazer",
                    "image": "https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb",
                    "price": 4999,
                    "price_str": "₹4,999",
                    "link": "https://www.amazon.in/"
                }
            ]
        }
    }
}

# --- BODY TYPES BY GENDER ---
body_types_by_gender = {
    "Female": ["Pear", "Rectangle", "Hourglass", "Triangle", "Inverted Triangle"],
    "Male": ["Rectangle", "Inverted Triangle", "Triangle", "Oval", "Trapezoid"],
    "Other": ["Pear", "Rectangle", "Hourglass", "Triangle", "Inverted Triangle", "Oval", "Trapezoid"]
}

# --- FORM SECTION ---
with st.container():
    st.markdown("### 📋 Enter Your AI-Assisted Style Profile")
    uploaded_image = st.file_uploader("📸 Upload a full-body image (AI will analyze your body type)", type=["jpg", "jpeg", "png"])

    # Put gender selector outside form for immediate update on body type options
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    body_type_options = body_types_by_gender.get(gender, body_types_by_gender["Other"])

    with st.form("style_form"):
        col2, col3 = st.columns([2, 2])
        with col2:
            body_type = st.selectbox("Your Guess Body Type (AI will refine it)", body_type_options)
        with col3:
            style = st.selectbox("Style", ["Casual", "Formal", "Party", "Ethnic"])

        col4, col5 = st.columns(2)
        with col4:
            size = st.selectbox("Size", ["S", "M", "L", "XL", "XXL"])
        with col5:
            budget = st.slider("Budget (₹)", 500, 10000, step=500)

        submitted = st.form_submit_button("✨ Get AI Recommendations")

# --- AI DETECTION LOGIC ---
if uploaded_image is not None:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    with st.spinner("🧐 AI is analyzing your body shape..."):
        detected_shape = detect_body_shape(uploaded_image)
        if detected_shape and detected_shape in suggestions:
            st.success(f"🧠 AI Detected Body Type: {detected_shape}")
            body_type = detected_shape
        else:
            st.warning("AI couldn't confidently detect your body shape. Please try another image.")

# --- RECOMMENDATION DISPLAY ---
if submitted:
    st.markdown("## 💼 AI-Powered Outfit Suggestions")
    st.success(f"For your {body_type} body type and {style} style, under ₹{budget}, here are AI-curated picks:")

    items = suggestions.get(body_type, {}).get(style, [])
    if items:
        for item in items:
            st.markdown(f"- ✅ {item}")
    else:
        st.warning("No AI suggestions available for this selection yet.")

    # --- AI-Driven Featured Looks ---
    st.markdown("### 👗 AI-Matched Featured Looks")
    gender_looks = featured_looks.get(gender, {})
    body_looks = gender_looks.get(body_type, {})
    style_looks = body_looks.get(style, [])

    filtered_looks = [look for look in style_looks if look["price"] <= budget]

    if filtered_looks:
        cols = st.columns(len(filtered_looks))
        for col, look in zip(cols, filtered_looks):
            with col:
                st.image(look["image"], use_column_width=True)
                st.caption(f"{look['title']} - {look['price_str']}")
                st.markdown(f"[🛒 Buy Now]({look['link']})")
    else:
        st.info("✨ More featured looks coming soon for this body type, style, and budget!")

    st.markdown("---")
    st.info("🎯 AI Tip: Use accessories and layering to accentuate your body shape effectively!")

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        © 2025 StyleMe Inc. | Fashion by AI, Styled by You.
    </div>
""", unsafe_allow_html=True)
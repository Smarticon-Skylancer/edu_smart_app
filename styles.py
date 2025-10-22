import streamlit as st

def inject_css(role=None):
    """
    Inject CSS styles. Role can be 'student', 'admin', or None (for login/signup).
    """

    # Default (login/register) colors
    primary_color = "#2563eb"   # Blue
    hover_color = "#5670c5"
    sidebar_bg = "#1f2937"

    if role == "Admin":
        primary_color = "#16a34a"   # Green
        hover_color = "#78AEB8"
        sidebar_bg = "#064e3b"

    st.markdown(
        f"""
        <style>
        /* General app background */
        .stApp {{
            background-color: #8BBDC6;
            color: #111827;
            font-family: "Segoe UI", Tahoma, sans-serif;
            display : block;
        }}

        /* Headings */
        h1, h2, h3 {{
            color: #1f2937;
            font-weight: 600;
            text-align: center;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            color: #f9fafb;
        }}
        section[data-testid="stSidebar"] * {{
            color: #f9fafb !important;
        }}

        /* Centered card for login/signup */
        .centered-card {{
            max-width: 400px;
            margin: 5% auto; /* center vertically & horizontally */
            padding: 2rem;
            background: #ADD8E6;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput input {{
            background-color: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            border-radius: 8px;
        }}

        /* Buttons */
        .stButton button {{
            width: 40%;
            background-color: {primary_color};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 500;
            transition: background 0.3s ease;
            display : block;
            margin: 0 auto;
        }}
        .stButton button:hover {{
            background-color: {hover_color};
        }}

        /* Tables */
        .stDataFrame {{
            background-color: white;
            border-radius: 8px;
            padding: 8px;
        }}

        /* Messages */
        .stAlert error{{
            border-radius: 8px;
            background-color: red;
        }}
        /* Registration title */
        .register-title{{
           font-size : 40px;
           color : #00000;
           font-family : ; 
           text-align : center;
        }}
        /* Admin title */
        .admin-title{{
           font-size : 40px;
           color : #00000;
           font-family : Arial-black; 
           text-align : center;
            
        }}
        /* Welcome Message */
        .welcome_message{{
           font-size : 65px;
           color : #00000;
           font-family : Tahoma; 
           font-weight : bolder;
           text-align : center;
           
           
           
            
        }}
        .sub-title{{
            font-size: 30px;
        }}
        .stAlert success{{
            border-radius: 8px;
            background-color: #008000;
        }}
        .cgpa-success {{
            background-color: #16a34a; /* green */
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            font-weight: bolder;
            font-size: 23px;
            }}
        .labels{{
            font-size : 22px;
            font-family : Tahoma;
            text-align : right;
        }}
        /* Card container */
.user-info-card {{
    background-color: #ffffff; /* white background */
    border-radius: 15px;       /* rounded corners */
    padding: 20px;
    margin:  0 auto;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* soft shadow */
    max-width: 500px;
}}

/* Card title */
.user-info-card h2 {{
    color: #2c3e50; /* dark blue-gray */
    margin-bottom: 15px;
    font-size: 40px;
    text-align: center;
}}

/* Info text */
.user-info-card p {{
    margin: 8px 0;
    font-size: 20px;
    color: #34495e;
}}

/* Highlight labels */
.user-info-card strong {{
    color: #27ae60; /* green highlight */
}}
.user-info-card hr {{
    border: none;
    height: 2px;
    background-color: #87ceeb; 
    margin: 10px 0;
    
}}
.event-card {{
    background-color: #f7f7f7;
    border-radius: 15px;       /* rounded corners */
    padding: 20px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); /* soft shadow */
    max-width: 100%;
}}
/* Card title */
.event-card h2 {{
    color: #2c3e50; /* dark blue-gray */
    margin-bottom: 15px;
    font-size: 40px;
    text-align: center;
}}

/* Info text */
.event-card p {{
    margin: 8px 0;
    font-size: 20px;
    color: #34495e;
}}

/* Highlight labels */
.event-card strong {{
    color: blue; /* green highlight */
}}
.event-card hr {{
    border: none;
    height: 2px;
    background-color: #87ceeb; 
    margin: 10px 0;
    
}}
.message-card{{
    background-color: #f7f7f7;
    border-radius: 5%;
    width:40%;
    margin-bottom:3%;
    text-align: left;
    font-family:Tahoma;
    margin-left:50%;
}}

        
        
        </style>
        """,
        unsafe_allow_html=True,
    )

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import anthropic
import base64
from io import BytesIO

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="GlowGuard Pro — Advanced Skincare Intelligence",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  
  .main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 3rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
  }
  .main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,183,197,0.15) 0%, transparent 60%);
    border-radius: 50%;
  }
  .main-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    color: white;
    margin: 0;
    letter-spacing: -1px;
  }
  .main-header p {
    color: rgba(255,255,255,0.7);
    font-size: 1.1rem;
    margin-top: 0.5rem;
  }
  .badge {
    display: inline-block;
    background: rgba(255,183,197,0.2);
    color: #ffb7c5;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    font-weight: 500;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,183,197,0.3);
  }

  .status-safe {
    background: #d4edda; color: #155724;
    padding: 12px 20px; border-radius: 10px;
    font-weight: 600; font-size: 1.1rem;
    border-left: 4px solid #28a745;
  }
  .status-caution {
    background: #fff3cd; color: #856404;
    padding: 12px 20px; border-radius: 10px;
    font-weight: 600; font-size: 1.1rem;
    border-left: 4px solid #ffc107;
  }
  .status-danger {
    background: #f8d7da; color: #721c24;
    padding: 12px 20px; border-radius: 10px;
    font-weight: 600; font-size: 1.1rem;
    border-left: 4px solid #dc3545;
  }
  .status-must {
    background: #cce5ff; color: #004085;
    padding: 12px 20px; border-radius: 10px;
    font-weight: 600; font-size: 1.1rem;
    border-left: 4px solid #004085;
  }

  .insight-card {
    background: #f8f9ff;
    border: 1px solid #e8eaf6;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
  }
  .metric-card {
    text-align: center;
    padding: 1.2rem;
    background: white;
    border-radius: 12px;
    border: 1px solid #eee;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .cycle-day {
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 0.5rem;
  }
  .day-exfol { background: #fff3e0; border: 2px solid #ff9800; }
  .day-retinol { background: #ede7f6; border: 2px solid #7e57c2; }
  .day-recovery { background: #e8f5e9; border: 2px solid #4caf50; }

  .product-card {
    background: white;
    border: 1px solid #eee;
    border-radius: 14px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: transform 0.2s;
  }
  .scan-result-box {
    background: linear-gradient(135deg, #667eea11, #764ba211);
    border: 1px solid #e8eaf6;
    border-radius: 14px;
    padding: 1.5rem;
  }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv("skincare_rules.csv")
    df.columns = df.columns.str.replace('_', ' ').str.title()
    df = df.apply(lambda x: x.map(lambda y: str(y).replace('_', ' ').title() if isinstance(y, str) else y))
    return df

df = load_data()
semua_bahan_raw = pd.concat([df['Bahan 1'], df['Bahan 2']]).unique()
semua_bahan = sorted([b for b in semua_bahan_raw if b.lower() != 'all active'])

# ============================================================
# SIDEBAR NAVIGASI
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
      <span style="font-size: 2rem;">🧪</span>
      <h2 style="font-family:'DM Serif Display',serif; margin:0.3rem 0;">GlowGuard Pro</h2>
      <p style="color: #888; font-size: 0.8rem;">Advanced Skincare Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio("Navigation", [
        "🏠 Home",
        "👤 Skin Profile Quiz",
        "🧪 Ingredient Analyzer",
        "🔄 Skin Cycling Planner",
        "💡 Product Recommendations",
        "📸 AI Face Scan",
        "📊 My Dashboard"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.caption("Data by Aqeela · Powered by Claude AI")
    st.caption("Expert System + Claude Vision")

# ============================================================
# PAGE: HOME
# ============================================================
if "🏠 Home" in menu:
    st.markdown("""
    <div class="main-header">
      <div class="badge">ADVANCED SKINCARE INTELLIGENCE SYSTEM</div>
      <h1>GlowGuard Pro</h1>
      <p>Dermatology-grade analysis — from ingredient safety checks to live AI face scanning. Built on a knowledge-based expert system and Claude AI.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="insight-card">
          <h3>🧪 35+ Ingredients</h3>
          <p style="color:#666">Mapped interaction rules for all major actives — retinol, vitamin C, AHAs, peptides, and more.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="insight-card">
          <h3>🤖 Claude AI Powered</h3>
          <p style="color:#666">Face scan analysis and personalized advice powered by Anthropic's Claude Vision API.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="insight-card">
          <h3>📊 Evidence-Based</h3>
          <p style="color:#666">Built on dermatological literature and clinical chemistry — not just influencer advice.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### How GlowGuard works")
    steps = ["Build your skin profile", "Analyze your ingredients", "Get your cycling plan", "Discover curated products", "AI scan your face"]
    cols = st.columns(5)
    for i, (col, step) in enumerate(zip(cols, steps)):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding: 1rem;">
              <div style="width:40px;height:40px;border-radius:50%;background:#1a1a2e;color:white;
                          font-weight:700;font-size:1.1rem;margin:0 auto 0.5rem;
                          display:flex;align-items:center;justify-content:center;">{i+1}</div>
              <p style="font-size:0.8rem;color:#555;">{step}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# PAGE: SKIN PROFILE QUIZ
# ============================================================
elif "👤 Skin Profile Quiz" in menu:
    st.title("👤 Build Your Skin Profile")
    st.write("Answer these questions to unlock personalized recommendations across all features.")

    with st.form("skin_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            skin_type = st.selectbox("Skin type", ["Oily", "Dry", "Combination", "Normal", "Sensitive"])
            skin_age = st.selectbox("Age range", ["Under 20", "20–25", "25–30", "30–35", "35–40", "40+"])
            climate = st.selectbox("Climate / environment", ["Tropical / humid (Indonesia)", "Dry / hot", "Temperate", "Cold"])
        with col2:
            concerns = st.multiselect("Main concerns (select all)", [
                "Acne / breakouts", "Hyperpigmentation / dark spots", "Wrinkles / anti-aging",
                "Redness / rosacea", "Dehydration", "Large pores", "Dullness / uneven tone",
                "Milia / texture", "Oiliness / sebum"
            ])
            current_actives = st.multiselect("Actives you currently use", [
                "Retinol", "Vitamin C", "AHA / BHA", "Niacinamide", "Benzoyl Peroxide",
                "Peptides", "Hyaluronic Acid", "Ceramide", "Centella Asiatica", "Zinc"
            ])
        
        sensitivity = st.slider("Skin sensitivity level", 1, 10, 5, help="1 = very tolerant, 10 = extremely sensitive")
        budget = st.select_slider("Monthly skincare budget (IDR)", 
                                  options=["< 200rb", "200rb–500rb", "500rb–1jt", "1jt–2jt", "> 2jt"])
        submitted = st.form_submit_button("🔍 Generate My Skin Profile", type="primary", use_container_width=True)

    if submitted:
        st.session_state['profile'] = {
            'skin_type': skin_type,
            'concerns': concerns,
            'actives': current_actives,
            'sensitivity': sensitivity,
            'budget': budget,
            'age': skin_age,
            'climate': climate
        }
        
        st.success("✅ Profile saved! Navigate to other pages for personalized recommendations.")
        st.markdown("### Your Skin Analysis")

        # Radar chart untuk skin profile
        categories = ['Hydration need', 'Barrier health', 'Sebum level', 'Sensitivity', 'Active tolerance']
        
        # Heuristic scores based on skin type
        scores_map = {
            "Oily": [40, 70, 90, 30, 75],
            "Dry": [90, 40, 10, 60, 50],
            "Combination": [60, 55, 65, 50, 65],
            "Normal": [60, 80, 50, 30, 80],
            "Sensitive": [70, 30, 40, 95, 20]
        }
        scores = scores_map.get(skin_type, [60, 60, 60, 60, 60])
        if sensitivity > 7:
            scores[3] = min(100, scores[3] + 20)

        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.2)',
            line=dict(color='#667eea', width=2),
            marker=dict(size=6)
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=350,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Recommendations
        st.markdown("### 💡 Key Recommendations")
        if "Acne / breakouts" in concerns and "Hyperpigmentation / dark spots" in concerns:
            st.info("🎯 **Primary Goal:** Treat acne first, then address pigmentation. Niacinamide is your best friend — it tackles both simultaneously.")
        if sensitivity > 7:
            st.warning("⚠️ **High Sensitivity Detected:** Avoid layering more than 2 actives. Focus on barrier repair before introducing retinol or exfoliants.")
        if skin_type == "Oily" and "Acne / breakouts" in concerns:
            st.info("🧴 **For Oily + Acne Skin:** Salicylic acid (BHA) is preferred over AHAs — it penetrates oil-filled pores. Pair with niacinamide for sebum control.")


# ============================================================
# PAGE: INGREDIENT ANALYZER
# ============================================================
elif "🧪 Ingredient Analyzer" in menu:
    st.title("🧪 Chemical Interaction Analyzer")
    st.write("Analyze the safety of combining two skincare actives — with deep chemical insights and charts.")

    col1, col2 = st.columns(2)
    with col1:
        bahan_a = st.selectbox("Bahan Aktif 1 (Ingredient A)", semua_bahan, key="ba")
    with col2:
        bahan_b = st.selectbox("Bahan Aktif 2 (Ingredient B)", semua_bahan, key="bb", index=1)

    if st.button("🔬 Analyze Interaction", type="primary", use_container_width=True):
        if bahan_a == bahan_b:
            st.info("💡 Same ingredient selected. Monitor for over-concentration, not interaction risk.")
        else:
            match = df[
                ((df['Bahan 1'] == bahan_a) & ((df['Bahan 2'] == bahan_b) | (df['Bahan 2'] == 'All Active'))) |
                ((df['Bahan 1'] == bahan_b) & ((df['Bahan 2'] == bahan_a) | (df['Bahan 2'] == 'All Active'))) |
                (((df['Bahan 1'] == 'All Active') | (df['Bahan 2'] == 'All Active')) &
                 ((df['Bahan 1'] == bahan_a) | (df['Bahan 2'] == bahan_b) | (df['Bahan 1'] == bahan_b) | (df['Bahan 2'] == bahan_a)))
            ]

            if not match.empty:
                data = match.iloc[0]
                status = data['Status'].upper()

                # Status badge
                status_class = {
                    "AMAN": "status-safe", "WAJIB": "status-must",
                    "HATI-HATI": "status-caution", "JANGAN": "status-danger",
                    "HATI Hati": "status-caution"
                }
                status_emoji = {"AMAN": "✅", "WAJIB": "🛡️", "HATI-HATI": "⚠️", "JANGAN": "🚨"}
                css_class = next((v for k, v in status_class.items() if k in status.upper()), "status-caution")
                emoji = next((v for k, v in status_emoji.items() if k in status.upper()), "⚠️")

                st.markdown(f'<div class="{css_class}">{emoji} STATUS: {status}</div>', unsafe_allow_html=True)
                st.markdown("")

                # Metrics row
                c1, c2, c3, c4 = st.columns(4)
                risk_colors = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                with c1:
                    risk = data.get('Irritation Risk', 'N/A')
                    st.metric("Irritation Risk", f"{risk_colors.get(risk.title(), '⚪')} {risk.title()}")
                with c2:
                    st.metric("Interaction Type", data.get('Interaction Type', 'N/A').title())
                with c3:
                    st.metric("pH — A", data.get('Ph 1', 'N/A'))
                with c4:
                    st.metric("pH — B", data.get('Ph 2', 'N/A'))

                # Risk chart
                st.markdown("### 📊 Risk Breakdown")
                irritation_score = {"Low": 15, "Medium": 55, "High": 90}.get(data.get('Irritation Risk', 'Low').title(), 50)
                
                fig = go.Figure()
                metrics = ['Irritation Risk', 'Barrier Damage', 'pH Clash', 'Efficacy Loss']
                
                # Heuristic risk values based on status
                if "JANGAN" in status.upper():
                    values = [irritation_score, 80, 70, 75]
                    bar_color = '#dc3545'
                elif "HATI" in status.upper():
                    values = [irritation_score, 45, 40, 35]
                    bar_color = '#ffc107'
                elif "WAJIB" in status.upper():
                    values = [10, 5, 5, 0]
                    bar_color = '#007bff'
                else:
                    values = [10, 10, 15, 5]
                    bar_color = '#28a745'

                fig.add_trace(go.Bar(
                    x=metrics, y=values,
                    marker_color=[bar_color] * 4,
                    text=[f"{v}%" for v in values],
                    textposition='outside'
                ))
                fig.update_layout(
                    yaxis=dict(range=[0, 110], title="Risk Level (%)"),
                    showlegend=False,
                    height=280,
                    margin=dict(l=0, r=0, t=10, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)

                # Explanation
                with st.expander("📝 Detailed Dermatological Explanation", expanded=True):
                    st.markdown(f"**Summary:** {data.get('Explanation', 'No explanation available.')}")
                    st.markdown("---")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"""
                        **{data.get('Bahan 1', 'Ingredient A')}**
                        - Category: {data.get('Kategori 1', 'N/A')}
                        - Strength: {data.get('Strength 1', 'N/A')}
                        - pH: {data.get('Ph 1', 'N/A')}
                        """)
                    with col_b:
                        st.markdown(f"""
                        **{data.get('Bahan 2', 'Ingredient B')}**
                        - Category: {data.get('Kategori 2', 'N/A')}
                        - Strength: {data.get('Strength 2', 'N/A')}
                        - pH: {data.get('Ph 2', 'N/A')}
                        """)

                # Safe alternatives suggestion
                if "JANGAN" in status.upper():
                    st.error("🚨 This combination should NEVER be used together. Use on alternate nights only.")
                    st.markdown("**Safe alternatives for the same goal:**")
                    st.markdown("- Replace one active with a gentler version (e.g., PHAs instead of AHAs)")
                    st.markdown("- Use Centella Asiatica or Niacinamide as a buffer ingredient")
            else:
                st.warning("🤷‍♀️ Combination not yet in our database. Always patch test first.")

    # Heatmap semua kombinasi
    st.markdown("---")
    st.markdown("### 🗺️ Full Interaction Heatmap")
    with st.expander("View interaction matrix for all mapped combinations"):
        pivot_data = {}
        key_ingredients = ['Retinol', 'Vitamin C', 'Aha Bha', 'Niacinamide', 'Hyaluronic Acid', 
                           'Salicylic Acid', 'Benzoyl Peroxide', 'Ceramide', 'Peptide']
        
        label_map = {"AMAN": 2, "WAJIB": 3, "HATI-HATI": 1, "HATI HATI": 1, "JANGAN": 0}
        matrix = []
        
        for b1 in key_ingredients:
            row = []
            for b2 in key_ingredients:
                if b1 == b2:
                    row.append(2)
                else:
                    m = df[((df['Bahan 1']==b1)&(df['Bahan 2']==b2))|((df['Bahan 1']==b2)&(df['Bahan 2']==b1))]
                    if not m.empty:
                        s = m.iloc[0]['Status'].upper().strip()
                        row.append(label_map.get(s, 2))
                    else:
                        row.append(-1)
            matrix.append(row)

        short_names = [b.split()[0] for b in key_ingredients]
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=short_names,
            y=short_names,
            colorscale=[
                [0, '#dc3545'], [0.25, '#dc3545'],
                [0.26, '#ffc107'], [0.5, '#ffc107'],
                [0.51, '#28a745'], [0.75, '#28a745'],
                [0.76, '#007bff'], [1, '#007bff']
            ],
            zmin=0, zmax=3,
            text=[['JANGAN' if v==0 else 'HATI2' if v==1 else 'AMAN' if v==2 else 'WAJIB' if v==3 else '?' for v in row] for row in matrix],
            texttemplate="%{text}",
            textfont=dict(size=9),
            showscale=True,
            colorbar=dict(tickvals=[0,1,2,3], ticktext=['JANGAN','HATI2','AMAN','WAJIB'])
        ))
        fig.update_layout(height=420, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE: SKIN CYCLING PLANNER
# ============================================================
elif "🔄 Skin Cycling Planner" in menu:
    st.title("🔄 Skin Cycling Planner")
    st.write("A science-backed rotating routine to maximize results and minimize irritation.")

    st.info("💡 **What is skin cycling?** A method popularized by dermatologists where you rotate actives across nights to give skin recovery time between harsh ingredients.")

    col1, col2 = st.columns([2, 1])
    with col1:
        skin_t = st.selectbox("Your skin type", ["Oily", "Dry", "Combination", "Sensitive", "Normal"])
        concerns_c = st.multiselect("Key concerns", ["Acne", "Pigmentation", "Aging / wrinkles", "Redness", "Texture"])
    with col2:
        tolerance = st.radio("Retinol experience", ["Beginner", "Intermediate", "Advanced"])
        cycle_len = st.radio("Cycle length", ["4-night (standard)", "6-night (sensitive)"])

    if st.button("🗓️ Generate My Skin Cycling Plan", type="primary", use_container_width=True):
        
        st.markdown("### Your Personalized Skin Cycling Plan")

        # Define cycle based on profile
        is_sensitive = skin_t == "Sensitive" or tolerance == "Beginner"
        retinol_strength = {"Beginner": "0.025%", "Intermediate": "0.1%", "Advanced": "0.3%"}[tolerance]
        
        nights = 6 if "6-night" in cycle_len else 4
        
        if nights == 4:
            plan = [
                {
                    "night": 1, "type": "Exfoliation Night", "color": "day-exfol",
                    "products": ["AHA 10% / BHA 2% toner", "Hyaluronic Acid serum", "Barrier moisturizer"],
                    "tip": "Apply exfoliant first, wait 15 mins before layering."
                },
                {
                    "night": 2, "type": "Retinol Night", "color": "day-retinol",
                    "products": [f"Retinol {retinol_strength}", "Niacinamide serum", "Ceramide moisturizer"],
                    "tip": "Sandwich retinol: moisturizer → retinol → moisturizer if beginner."
                },
                {
                    "night": 3, "type": "Recovery Night 1", "color": "day-recovery",
                    "products": ["Centella Asiatica toner", "Panthenol serum", "Ceramide + Hyaluronic cream"],
                    "tip": "No actives tonight. Focus entirely on barrier repair."
                },
                {
                    "night": 4, "type": "Recovery Night 2", "color": "day-recovery",
                    "products": ["Hyaluronic Acid serum", "Niacinamide (optional)", "Heavy occlusive moisturizer"],
                    "tip": "This is your skin's recharge night. Go simple."
                }
            ]
        else:
            plan = [
                {"night": 1, "type": "Exfoliation Night", "color": "day-exfol",
                 "products": ["AHA toner", "HA serum", "Moisturizer"], "tip": "Gentle chemical exfoliation only."},
                {"night": 2, "type": "Recovery Night", "color": "day-recovery",
                 "products": ["Centella", "Ceramide", "Hyaluronic cream"], "tip": "Repair and soothe."},
                {"night": 3, "type": "Retinol Night", "color": "day-retinol",
                 "products": [f"Retinol {retinol_strength}", "Niacinamide", "Ceramide"], "tip": "Low and slow."},
                {"night": 4, "type": "Recovery Night", "color": "day-recovery",
                 "products": ["HA serum", "Barrier cream"], "tip": "Full rest night."},
                {"night": 5, "type": "Retinol Night", "color": "day-retinol",
                 "products": [f"Retinol {retinol_strength}", "Peptide serum", "Ceramide"], "tip": "2nd retinol session."},
                {"night": 6, "type": "Recovery Night", "color": "day-recovery",
                 "products": ["Centella", "Niacinamide", "Occlusive moisturizer"], "tip": "Barrier lock."},
            ]

        cols = st.columns(len(plan))
        for col, day in zip(cols, plan):
            with col:
                st.markdown(f"""
                <div class="cycle-day {day['color']}">
                  <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.1em;color:#555;">NIGHT {day['night']}</div>
                  <div style="font-weight:700;font-size:0.9rem;margin:6px 0;">{day['type']}</div>
                  {"".join(f'<div style="font-size:0.75rem;margin:3px 0;color:#444;">• {p}</div>' for p in day['products'])}
                </div>
                """, unsafe_allow_html=True)
                st.caption(day['tip'])

        # AM routine
        st.markdown("---")
        st.markdown("### ☀️ AM Routine (Every Day — Non-Negotiable)")
        am_steps = [
            ("1", "Cleanser", "Low-pH gel/foam cleanser", "#e3f2fd"),
            ("2", "Vitamin C", "L-AA 10–15% or derivative", "#fff9c4"),
            ("3", "Niacinamide", "5–10% serum", "#e8f5e9"),
            ("4", "Moisturizer", "Lightweight gel or lotion", "#f3e5f5"),
            ("5", "SPF 50+", "MANDATORY — PA++++ preferred", "#ffebee"),
        ]
        cols = st.columns(5)
        for col, (num, name, desc, bg) in zip(cols, am_steps):
            with col:
                st.markdown(f"""
                <div style="background:{bg};border-radius:10px;padding:0.8rem;text-align:center;">
                  <div style="font-size:1.3rem;font-weight:800;color:#333;">{num}</div>
                  <div style="font-weight:600;font-size:0.85rem;">{name}</div>
                  <div style="font-size:0.75rem;color:#666;margin-top:4px;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        # Cycle visualization
        st.markdown("---")
        st.markdown("### 📈 What to Expect Over 4 Weeks")
        weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
        skin_health = [45, 58, 70, 82]
        irritation = [30, 20, 12, 5]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks, y=skin_health, mode='lines+markers', name='Skin Health',
                                  line=dict(color='#28a745', width=3), marker=dict(size=10)))
        fig.add_trace(go.Scatter(x=weeks, y=irritation, mode='lines+markers', name='Irritation Level',
                                  line=dict(color='#dc3545', width=3), marker=dict(size=10)))
        fig.update_layout(height=250, legend=dict(orientation="h"), 
                          yaxis_title="Score (%)", margin=dict(l=0,r=0,t=10,b=0),
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE: PRODUCT RECOMMENDATIONS
# ============================================================
elif "💡 Product Recommendations" in menu:
    st.title("💡 Product Recommendations")
    st.write("Curated skincare products matched to your skin profile — with ingredients, prices (IDR), and ratings.")

    col1, col2, col3 = st.columns(3)
    with col1:
        filter_skin = st.multiselect("Skin type", ["Oily", "Dry", "Combination", "Sensitive"], default=["Combination"])
    with col2:
        filter_concern = st.multiselect("Concern", ["Acne", "Pigmentation", "Hydration", "Anti-aging", "Barrier repair"])
    with col3:
        filter_budget = st.select_slider("Max price (IDR)", ["< 100rb", "< 300rb", "< 500rb", "< 1jt", "Semua"], value="< 500rb")

    # Static product database — extendable via API/CSV
    products = [
        {
            "name": "Niacinamide 10% + Zinc 1%",
            "brand": "The Ordinary",
            "price": 120000,
            "rating": 4.7,
            "skin_types": ["Oily", "Combination", "Acne"],
            "concerns": ["Acne", "Pigmentation"],
            "ingredients": ["Niacinamide 10%", "Zinc PCA 1%", "Pentylene Glycol"],
            "ph": "6.5",
            "emoji": "🧴",
            "why": "Dual-action: reduces sebum + fades dark spots simultaneously."
        },
        {
            "name": "Vitamin C Suspension 23%",
            "brand": "The Ordinary",
            "price": 155000,
            "rating": 4.5,
            "skin_types": ["Normal", "Combination"],
            "concerns": ["Pigmentation", "Anti-aging"],
            "ingredients": ["L-Ascorbic Acid 23%", "HPTA 2%", "Squalane"],
            "ph": "3.5",
            "emoji": "✨",
            "why": "High-potency Vitamin C for stubborn pigmentation and brightness."
        },
        {
            "name": "Hyaluronic Acid 2% + B5",
            "brand": "The Ordinary",
            "price": 130000,
            "rating": 4.8,
            "skin_types": ["Dry", "Sensitive", "Combination", "Oily", "Normal"],
            "concerns": ["Hydration", "Barrier repair"],
            "ingredients": ["Hyaluronic Acid 2%", "Vitamin B5", "Arginine"],
            "ph": "Neutral",
            "emoji": "💧",
            "why": "Universal hydrator — safe with all actives and all skin types."
        },
        {
            "name": "AHA 30% + BHA 2% Peeling Solution",
            "brand": "The Ordinary",
            "price": 175000,
            "rating": 4.3,
            "skin_types": ["Oily", "Combination"],
            "concerns": ["Acne", "Pigmentation", "Texture"],
            "ingredients": ["Glycolic Acid 30%", "Salicylic Acid 2%", "Aloe Vera"],
            "ph": "3.5",
            "emoji": "🔬",
            "why": "10-minute weekly mask. DO NOT combine with retinol night."
        },
        {
            "name": "Cica Cream",
            "brand": "Some By Mi",
            "price": 220000,
            "rating": 4.6,
            "skin_types": ["Sensitive", "Dry", "Combination"],
            "concerns": ["Barrier repair", "Hydration", "Acne"],
            "ingredients": ["Centella Asiatica Extract", "Madecassoside", "Tea Tree Oil", "Ceramide"],
            "ph": "Neutral",
            "emoji": "🌿",
            "why": "Ideal recovery cream — perfect for cycling rest nights."
        },
        {
            "name": "Retinol 0.5% in Squalane",
            "brand": "The Ordinary",
            "price": 195000,
            "rating": 4.5,
            "skin_types": ["Normal", "Combination", "Oily"],
            "concerns": ["Anti-aging", "Acne", "Pigmentation"],
            "ingredients": ["Retinol 0.5%", "Squalane", "BHT"],
            "ph": "Neutral",
            "emoji": "⭐",
            "why": "Mid-strength retinol in a non-irritating squalane base. Great first retinol."
        },
        {
            "name": "Sunscreen Mild Airy Finish SPF50+",
            "brand": "Azarine",
            "price": 80000,
            "rating": 4.9,
            "skin_types": ["Oily", "Combination", "Sensitive"],
            "concerns": ["Acne", "Pigmentation"],
            "ingredients": ["Zinc Oxide", "Ethylhexyl Methoxycinnamate", "Centella Extract"],
            "ph": "Neutral",
            "emoji": "🛡️",
            "why": "Local brand, budget-friendly, PA++++, non-greasy. A must-have."
        },
        {
            "name": "CICA Barrier Capsule Serum",
            "brand": "Mugungwha",
            "price": 260000,
            "rating": 4.4,
            "skin_types": ["Sensitive", "Dry"],
            "concerns": ["Barrier repair", "Hydration"],
            "ingredients": ["Ceramide NP", "Ceramide EOP", "Panthenol", "Centella"],
            "ph": "Neutral",
            "emoji": "💊",
            "why": "Premium ceramide blend — best for compromised barrier recovery."
        },
    ]

    shown = 0
    for p in products:
        show = True
        if filter_concern and not any(c in p['concerns'] for c in filter_concern):
            show = False
        if filter_budget != "Semua":
            max_price = int(filter_budget.replace("< ", "").replace("rb", "000").replace("jt", "000000"))
            if p['price'] > max_price:
                show = False
        
        if show:
            shown += 1
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(f"<div style='font-size:3rem;text-align:center;padding:1rem;'>{p['emoji']}</div>", 
                           unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{p['name']}** — *{p['brand']}*")
                st.markdown(f"💰 Rp {p['price']:,} · ⭐ {p['rating']} · pH {p['ph']}")
                st.markdown(f"**Ingredients:** {', '.join(p['ingredients'])}")
                st.markdown(f"*{p['why']}*")
                tag_html = "".join(f'<span style="background:#e8f5e9;color:#2e7d32;padding:2px 10px;border-radius:12px;font-size:0.75rem;margin-right:4px;">{t}</span>' for t in p['concerns'])
                st.markdown(tag_html, unsafe_allow_html=True)
            st.markdown("---")

    if shown == 0:
        st.warning("No products match your current filters. Try broadening your selection.")

    st.caption(f"Showing {shown} of {len(products)} products in our database.")


# ============================================================
# PAGE: AI FACE SCAN
# ============================================================
elif "📸 AI Face Scan" in menu:
    st.title("📸 AI Face Scan — Powered by Claude Vision")
    st.write("Upload a selfie and Claude AI will analyze your skin concerns, barrier health, and recommend a routine.")

    st.warning("⚠️ **Privacy note:** Your photo is sent directly to Anthropic's Claude API for analysis and is NOT stored by GlowGuard.")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload your selfie", 
            type=["jpg", "jpeg", "png"],
            help="Best results: no filter, good natural lighting, front-facing, no heavy makeup"
        )
        
        if uploaded_file:
            st.image(uploaded_file, caption="Your photo", use_column_width=True)

        extra_context = st.text_area(
            "Any additional context? (optional)",
            placeholder="e.g. I've been breaking out for 2 weeks, I use retinol twice a week, my skin feels tight in the morning..."
        )

        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            help="Your key is used only for this request and never stored."
        )

    with col2:
        st.markdown("""
        ### What Claude analyzes:
        - 🔍 **Visible skin type** (oily zones, dry patches)
        - 🎯 **Skin concerns** (hyperpigmentation, redness, texture, acne)
        - 🛡️ **Barrier assessment** (signs of dehydration or damage)
        - 💊 **Ingredient recommendations** based on visible needs
        - 🗓️ **Starter routine** tailored to what it sees
        - ⚠️ **Warnings** about visible sensitivities
        
        ---
        **Tips for best results:**
        - Use natural daylight, not artificial light
        - No filter, no heavy foundation
        - Front-facing, neutral expression
        - Clean skin preferred (but not required)
        """)

        if uploaded_file and api_key:
            if st.button("🔍 Analyze My Skin with AI", type="primary", use_container_width=True):
                with st.spinner("Claude is analyzing your skin..."):
                    try:
                        image_bytes = uploaded_file.read()
                        encoded = base64.b64encode(image_bytes).decode("utf-8")
                        media_type = uploaded_file.type or "image/jpeg"

                        client = anthropic.Anthropic(api_key=api_key)
                        
                        prompt = f"""You are a world-class dermatologist and skincare formulation expert. 
                        Analyze this person's face and skin carefully.
                        
                        Additional context from user: {extra_context if extra_context else 'None provided.'}
                        
                        Provide a structured analysis with these sections:
                        
                        ## 🔍 Skin Type Assessment
                        What skin type do they appear to have? Note oily zones, dry patches, combination areas.
                        
                        ## 🎯 Visible Skin Concerns
                        List any concerns you can see: hyperpigmentation, acne/breakouts, redness, texture issues, 
                        enlarged pores, dehydration lines, dark circles, uneven skin tone, etc.
                        
                        ## 🛡️ Barrier Health
                        Signs of barrier damage or compromise? Dehydration? Sensitivity indicators?
                        
                        ## 💊 Recommended Actives
                        List 3-5 specific ingredients this person should prioritize and why, ordered by priority.
                        
                        ## 🗓️ Starter Routine (AM + PM)
                        Simple, actionable AM and PM routine based on what you see.
                        
                        ## ⚠️ Ingredients to Avoid
                        What should this person avoid or introduce slowly?
                        
                        ## 📊 Confidence Note
                        Be transparent about what you can and cannot determine from a photo alone.
                        
                        Be specific, actionable, and compassionate. Avoid vague statements."""

                        response = client.messages.create(
                            model="claude-opus-4-5",
                            max_tokens=1500,
                            messages=[{
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": media_type,
                                            "data": encoded
                                        }
                                    },
                                    {"type": "text", "text": prompt}
                                ]
                            }]
                        )

                        analysis = response.content[0].text
                        
                        st.markdown("---")
                        st.markdown("### 🧬 Claude's Skin Analysis")
                        st.markdown(f"""
                        <div class="scan-result-box">
                        {analysis}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("✅ Analysis complete! Navigate to the Ingredient Analyzer or Skin Cycling Planner to act on these insights.")

                    except anthropic.AuthenticationError:
                        st.error("❌ Invalid API key. Please check your Anthropic API key.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        elif uploaded_file and not api_key:
            st.info("👆 Enter your Anthropic API key above to run the AI analysis.")
        elif not uploaded_file:
            st.info("👆 Upload a photo on the left to get started.")


# ============================================================
# PAGE: MY DASHBOARD
# ============================================================
elif "📊 My Dashboard" in menu:
    st.title("📊 My Skincare Dashboard")
    
    profile = st.session_state.get('profile', None)
    
    if not profile:
        st.info("Complete the Skin Profile Quiz first to see your personalized dashboard.")
        st.stop()

    # Header metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Skin Type", profile.get('skin_type', '—'))
    with col2:
        st.metric("Actives in Use", len(profile.get('actives', [])))
    with col3:
        st.metric("Key Concerns", len(profile.get('concerns', [])))
    with col4:
        sensitivity = profile.get('sensitivity', 5)
        level = "High" if sensitivity > 7 else "Moderate" if sensitivity > 4 else "Low"
        st.metric("Sensitivity", level)

    st.markdown("---")

    # Conflict checker
    st.markdown("### ⚡ Active Ingredient Conflict Check")
    actives = profile.get('actives', [])
    
    if len(actives) < 2:
        st.info("Add more actives in your profile to see conflict analysis.")
    else:
        conflicts = []
        safe_pairs = []
        
        for i in range(len(actives)):
            for j in range(i+1, len(actives)):
                a, b = actives[i], actives[j]
                a_clean = a.replace(' / ', ' ').title()
                b_clean = b.replace(' / ', ' ').title()
                
                m = df[
                    ((df['Bahan 1'].str.contains(a_clean.split()[0], case=False, na=False)) & 
                     (df['Bahan 2'].str.contains(b_clean.split()[0], case=False, na=False))) |
                    ((df['Bahan 1'].str.contains(b_clean.split()[0], case=False, na=False)) & 
                     (df['Bahan 2'].str.contains(a_clean.split()[0], case=False, na=False)))
                ]
                
                if not m.empty:
                    status = m.iloc[0]['Status'].upper()
                    if "JANGAN" in status:
                        conflicts.append((a, b, m.iloc[0].get('Explanation', '')))
                    else:
                        safe_pairs.append((a, b, status))

        if conflicts:
            st.error(f"🚨 **{len(conflicts)} dangerous combination(s) detected in your routine!**")
            for a, b, exp in conflicts:
                st.markdown(f"- ❌ **{a}** + **{b}**: {exp}")
        
        if safe_pairs:
            with st.expander(f"✅ {len(safe_pairs)} safe combinations"):
                for a, b, s in safe_pairs:
                    st.markdown(f"- ✅ **{a}** + **{b}** → {s}")

    # Skin concern distribution
    concerns = profile.get('concerns', [])
    if concerns:
        st.markdown("---")
        st.markdown("### 🎯 Your Concern Profile")
        concern_priority = {
            "Acne / breakouts": 5, "Hyperpigmentation / dark spots": 4,
            "Wrinkles / anti-aging": 3, "Redness / rosacea": 4,
            "Dehydration": 3, "Large pores": 2, "Dullness / uneven tone": 3,
            "Milia / texture": 2, "Oiliness / sebum": 3
        }
        concern_scores = [concern_priority.get(c, 3) for c in concerns]
        
        fig = go.Figure(go.Bar(
            x=concerns,
            y=concern_scores,
            marker_color=['#dc3545' if s==5 else '#ffc107' if s==4 else '#28a745' for s in concern_scores],
            text=['High priority' if s==5 else 'Medium' if s==4 else 'Lower' for s in concern_scores],
            textposition='outside'
        ))
        fig.update_layout(
            yaxis=dict(title="Priority Level", range=[0, 7]),
            height=280, showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=10,b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
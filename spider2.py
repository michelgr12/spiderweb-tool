import streamlit as st
import plotly.graph_objects as go

# Invoerdata
categories = {
    "Mensen": ["kennis jongerenparticipatie", "participatief proces", "samenwerken jongeren"],
    "Organisatie": ["governance", "cultuur", "werkprocessen"],
    "Partners": ["netwerk", "afspraken & randvoorwaarden", "kwaliteit werk"],
    "Jongeren": ["verbinding", "diverse manieren", "in staat stellen"],
}

niveau_mapping = {
    "start": 1,
    "basis": 2,
    "gevorderd": 3,
    "expert": 4
}

kleurenschema = ["#7768bf", "#cf4aef", "#170341", "#2d0c81", "#282340",
                 "#f8a6c3", "#cfc5ff", "#efbffa", "#f0eced"]

st.set_page_config(layout="wide")
st.title("🕸️ Spiderweb-diagram Generator")

titel = st.text_input("Titel voor het diagram", "Mijn Spiderweb")

# Input per parameter
st.markdown("### Vul per parameter het niveau in:")
input_niveaus = {}
col1, col2 = st.columns(2)

with col1:
    for cat in ["Mensen", "Organisatie"]:
        st.subheader(cat)
        for param in categories[cat]:
            keuze = st.selectbox(f"{param}", niveau_mapping.keys(), key=param)
            input_niveaus[param] = niveau_mapping[keuze]

with col2:
    for cat in ["Jongeren", "Partners"]:
        st.subheader(cat)
        for param in categories[cat]:
            keuze = st.selectbox(f"{param}", niveau_mapping.keys(), key=param)
            input_niveaus[param] = niveau_mapping[keuze]

# Hoekverdeling per kwadrant
kwadrant_hoeken = {
    "Mensen": [45, 60, 75],
    "Organisatie": [315, 330, 345],
    "Partners": [225, 240, 255],
    "Jongeren": [135, 120, 105]
}

theta = []
r = []
labels = []

for cat, hoeken in kwadrant_hoeken.items():
    for param, hoek in zip(categories[cat], hoeken):
        theta.append(hoek)
        r.append(input_niveaus[param])
        labels.append(param)

# Cirkel sluiten
theta.append(theta[0])
r.append(r[0])
labels.append(labels[0])

# Plot maken
fig = go.Figure()

# Achtergrondkleur (kleurverloop per ring)
for val in [1, 2, 3, 4]:
    fig.add_trace(go.Scatterpolar(
        r=[val] * len(theta),
        theta=theta,
        fill='toself',
        mode='lines',
        line_color='rgba(200,200,255,0.08)',
        showlegend=False,
        hoverinfo='skip'
    ))

# Resultaten plotten
fig.add_trace(go.Scatterpolar(
    r=r,
    theta=theta,
    mode='lines+markers',
    fill='toself',
    line_color=kleurenschema[0],
    name='Niveau',
    marker=dict(size=8)
))

# Layout
fig.update_layout(
    title=dict(text=titel, x=0.5, xanchor='center'),
    polar=dict(
        angularaxis=dict(
            tickmode='array',
            tickvals=theta[:-1],
            ticktext=labels[:-1],
            tickfont=dict(size=11)
        ),
        radialaxis=dict(
            visible=True,
            range=[0, 4],
            tickvals=[1, 2, 3, 4],
            ticktext=["Start", "Basis", "Gevorderd", "Expert"],
            tickfont=dict(size=12, color='black'),
            tickangle=0
        )
    ),
    showlegend=False,
    width=1200,
    height=800,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=100)
)

# Annotaties: kwadrantnamen (wit), binnen/buitenwereld
fig.update_layout(
    annotations=[
        dict(text="Jongeren", x=0.15, y=0.85, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="white")),
        dict(text="Mensen", x=0.85, y=0.85, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="white")),
        dict(text="Partners", x=0.15, y=0.15, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="white")),
        dict(text="Organisatie", x=0.85, y=0.15, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="white")),
        dict(text="Buitenwereld", x=0.03, y=0.5, xref="paper", yref="paper",
             showarrow=False, font=dict(size=14, color="black")),
        dict(text="Binnenwereld", x=0.97, y=0.5, xref="paper", yref="paper",
             showarrow=False, font=dict(size=14, color="black")),
    ],
    shapes=[
        # Verticale lijn (binnen/buiten)
        dict(
            type="line", x0=0.5, y0=0.3, x1=0.5, y1=0.7,
            xref='paper', yref='paper',
            line=dict(color="gray", width=1.5, dash="dot")
        ),
        # Horizontale lijn
        dict(
            type="line", x0=0.3, y0=0.5, x1=0.7, y1=0.5,
            xref='paper', yref='paper',
            line=dict(color="gray", width=1.5, dash="dot")
        )
    ]
)

# Teken het figuur
st.plotly_chart(fig, use_container_width=True)

# Download als PNG
img_bytes = fig.to_image(format="png", width=1200, height=800, scale=1)
st.download_button(
    label="📥 Download als PNG",
    data=img_bytes,
    file_name="spiderweb.png",
    mime="image/png"
)

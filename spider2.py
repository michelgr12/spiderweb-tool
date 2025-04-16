import streamlit as st
import plotly.graph_objects as go

# Data
parameters = [
    ("Jongeren", "verbinding"),
    ("Jongeren", "diverse manieren"),
    ("Jongeren", "in staat stellen"),
    ("Mensen", "kennis jongerenparticipatie"),
    ("Mensen", "participatief proces"),
    ("Mensen", "samenwerken jongeren"),
    ("Organisatie", "governance"),
    ("Organisatie", "cultuur"),
    ("Organisatie", "werkprocessen"),
    ("Partners", "netwerk"),
    ("Partners", "afspraken & randvoorwaarden"),
    ("Partners", "kwaliteit werk")
]

niveau_mapping = {
    "start": 1,
    "basis": 2,
    "gevorderd": 3,
    "expert": 4
}

kleurenschema = ["#7768bf"]

st.set_page_config(layout="wide")
st.title("🕸️ Spiderweb-diagram Generator")

titel = st.text_input("Titel voor het diagram", "Mijn Spiderweb")

# Input
st.markdown("### Vul per parameter het niveau in:")
input_niveaus = {}
for cat, param in parameters:
    keuze = st.selectbox(f"{param} ({cat})", niveau_mapping.keys(), key=param)
    input_niveaus[param] = niveau_mapping[keuze]

# Verdeling: 12 hoeken gelijkmatig over 360°
angles = [i * 30 + 15 for i in range(len(parameters))]
r = [input_niveaus[param] for (_, param) in parameters]
labels = [param for (_, param) in parameters]

# Sluit de cirkel
r.append(r[0])
angles.append(angles[0])
labels.append(labels[0])

# Plot
fig = go.Figure()

# Kleurverloop-ringen
for val in [1, 2, 3, 4]:
    fig.add_trace(go.Scatterpolar(
        r=[val] * len(angles),
        theta=angles,
        fill='toself',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        fillcolor='rgba(200, 200, 255, 0.08)',
        showlegend=False,
        hoverinfo='skip'
    ))

# Spiderweb
fig.add_trace(go.Scatterpolar(
    r=r,
    theta=angles,
    mode='lines+markers',
    fill='toself',
    line_color=kleurenschema[0],
    marker=dict(size=8)
))

# Layout
fig.update_layout(
    title=dict(text=titel, x=0.5, xanchor='center', font=dict(color='black')),
    polar=dict(
        angularaxis=dict(
            tickmode='array',
            tickvals=angles[:-1],
            ticktext=labels[:-1],
            tickfont=dict(size=12, color='black')
        ),
        radialaxis=dict(
            visible=True,
            range=[0, 4],
            tickvals=[1, 2, 3, 4],
            ticktext=["Start", "Basis", "Gevorderd", "Expert"],
            tickfont=dict(size=13, color='black'),
        )
    ),
    showlegend=False,
    width=1200,
    height=800,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(t=100)
)

# Annotaties: kwadrantnamen en binnen/buitenwereld
fig.update_layout(
    annotations=[
        dict(text="Jongeren", x=0.3, y=0.95, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="black")),
        dict(text="Mensen", x=0.85, y=0.85, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="black")),
        dict(text="Organisatie", x=0.85, y=0.15, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="black")),
        dict(text="Partners", x=0.15, y=0.15, xref="paper", yref="paper",
             showarrow=False, font=dict(size=18, color="black")),
        dict(text="Buitenwereld", x=0.04, y=0.5, xref="paper", yref="paper",
             showarrow=False, font=dict(size=14, color="black")),
        dict(text="Binnenwereld", x=0.96, y=0.5, xref="paper", yref="paper",
             showarrow=False, font=dict(size=14, color="black")),
    ],
    shapes=[
        # Verticale lijn (lang)
        dict(
            type="line", x0=0.5, y0=0.1, x1=0.5, y1=0.9,
            xref='paper', yref='paper',
            line=dict(color="gray", width=1.5, dash="dot")
        ),
        # Horizontale lijn (lang)
        dict(
            type="line", x0=0.1, y0=0.5, x1=0.9, y1=0.5,
            xref='paper', yref='paper',
            line=dict(color="gray", width=1.5, dash="dot")
        )
    ]
)

# Teken
st.plotly_chart(fig, use_container_width=True)

# Download PNG
img_bytes = fig.to_image(format="png", width=1200, height=800, scale=1)
st.download_button(
    label="📥 Download als PNG",
    data=img_bytes,
    file_name="spiderweb.png",
    mime="image/png"
)

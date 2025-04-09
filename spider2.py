import streamlit as st
import plotly.graph_objects as go

# Parameters en indeling
categories = {
    "Mensen": ["kennis jongerenparticipatie", "participatief proces", "samenwerken jongeren"],
    "Organisatie": ["governance", "cultuur", "werkprocessen"],
    "Jongeren": ["verbinding", "diverse manieren", "in staat stellen"],
    "Partners": ["netwerk", "afspraken & randvoorwaarden", "kwaliteit werk"]
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

# Titel invoer
titel = st.text_input("Titel voor het diagram", "Mijn Spiderweb")

# Invoer per parameter
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

# Chart genereren
if st.button("Genereer spiderweb"):
    labels = list(input_niveaus.keys())
    waarden = list(input_niveaus.values())
    waarden.append(waarden[0])
    labels.append(labels[0])

    fig = go.Figure()

    # Achtergrondkleurverloop per ring
    for r in [1, 2, 3, 4]:
        fig.add_trace(go.Scatterpolar(
            r=[r] * len(labels),
            theta=labels,
            fill='toself',
            mode='lines',
            line_color='rgba(200,200,255,0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))

    # Spiderweb
    fig.add_trace(go.Scatterpolar(
        r=waarden,
        theta=labels,
        fill='toself',
        name='Niveau',
        line_color=kleurenschema[0],
        marker=dict(size=8)
    ))

    # Layout en assen
    fig.update_layout(
        title=dict(text=titel, x=0.5, xanchor='center'),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 4],
                tickvals=[1, 2, 3, 4],
                ticktext=["Start", "Basis", "Gevorderd", "Expert"],
                tickfont=dict(size=12)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        width=1200,
        height=800,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=100)
    )

    # Annotaties + kwadrantlijnen
    fig.update_layout(
        annotations=[
            dict(text="Buitenwereld", x=0.02, y=0.5, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=16)),
            dict(text="Binnenwereld", x=0.98, y=0.5, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=16)),
            dict(text="Jongeren", x=0.2, y=0.85, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=18, color="#7768bf")),
            dict(text="Mensen", x=0.8, y=0.85, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=18, color="#cf4aef")),
            dict(text="Partners", x=0.2, y=0.1, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=18, color="#170341")),
            dict(text="Organisatie", x=0.8, y=0.1, xref="paper", yref="paper",
                 showarrow=False, font=dict(size=18, color="#2d0c81")),
        ],
        shapes=[
            dict(  # verticale lijn midden (scheiding binnen/buiten)
                type="line",
                x0=0.5, y0=0, x1=0.5, y1=1,
                xref='paper', yref='paper',
                line=dict(color="gray", width=2, dash="dot")
            ),
            dict(  # diagonale kwadrantlijn 1
                type="line", x0=0, y0=0, x1=1, y1=1,
                xref='paper', yref='paper',
                line=dict(color="lightgray", width=1, dash="dot")
            ),
            dict(  # diagonale kwadrantlijn 2
                type="line", x0=1, y0=0, x1=0, y1=1,
                xref='paper', yref='paper',
                line=dict(color="lightgray", width=1, dash="dot")
            )
        ]
    )

    # Plot weergeven
    st.plotly_chart(fig, use_container_width=True)

    # PNG-export
    img_bytes = fig.to_image(format="png", width=1200, height=800, scale=1)
    st.download_button(
        label="📥 Download als PNG",
        data=img_bytes,
        file_name="spiderweb.png",
        mime="image/png"
    )
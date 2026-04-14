from __future__ import annotations
import plotly.graph_objects as go


def make_interactive_1h_plot(
    nmr_result: dict,
    smiles: str,
    show_integrals: bool = True,
):
    ppm_axis = nmr_result["ppm_axis"]
    spectrum = nmr_result["spectrum"]
    peaks = nmr_result["peaks"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ppm_axis,
            y=spectrum,
            mode="lines",
            name="¹H NMR",
            hovertemplate="δ = %{x:.2f} ppm<br>Intensity = %{y:.2f}<extra></extra>",
        )
    )

    # Unsichtbare Marker für Peak-Hover
    peak_x = [p["shift"] for p in peaks]
    peak_y = []
    for x in peak_x:
        idx = min(range(len(ppm_axis)), key=lambda i: abs(ppm_axis[i] - x))
        peak_y.append(float(spectrum[idx]))

    peak_text = [
        f"{p['shift']:.2f} ppm<br>{p['mult_str']}, {p['n_h']}H"
        for p in peaks
    ]

    if show_integrals:
        fig.add_trace(
            go.Scatter(
                x=peak_x,
                y=peak_y,
                mode="markers",
                name="Peaks",
                marker=dict(size=8, opacity=0.0),
                text=peak_text,
                hovertemplate="%{text}<extra></extra>",
                showlegend=False,
            )
        )

    # NMR-typischer Bereich
    x_left = 12.5
    x_right = -0.3

    y_max = max(float(spectrum.max()) if len(spectrum) else 1.0, 1.0)

    
    if show_integrals:
        fig.update_layout(
            title=f"Simulated ¹H-NMR Spectrum — {smiles}",
            xaxis_title="Chemical Shift δ (ppm)",
            yaxis_title="Proton Number (rel. Intensity)",
            template="simple_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )
    else:
        fig.update_layout(
            title=f"Simulated ¹H-NMR Spectrum",
            xaxis_title="Chemical Shift δ (ppm)",
            yaxis_title="Proton Number (rel. Intensity)",
            template="plotly_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )    

    # X-Achse: invertiert, begrenzt und nur horizontal navigierbar
    fig.update_xaxes(
        range=[x_left, x_right],
        autorange=False,
        minallowed=x_right,
        maxallowed=x_left,
        fixedrange=False,
        showgrid=True,
        zeroline=False,
        title_text="Chemical Shift (δ, ppm)",
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    # Y-Achse fixieren, damit Scroll/Zoom nur horizontal wirkt
    fig.update_yaxes(
        range=[0, y_max * 1.08],
        autorange=False,
        fixedrange=True,
        showgrid=True,
        zeroline=False,
        title_text="Relative Intensity",
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    fig.update_layout(
    margin=dict(l=70, r=30, t=50, b=70),
    )

    return fig

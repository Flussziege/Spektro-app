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
            hovertemplate="δ = %{x:.2f} ppm<br>Intensität = %{y:.2f}<extra></extra>",
        )
    )


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

    fig.update_layout(
        title=f"Simuliertes ¹H-NMR-Spektrum — {smiles}",
        xaxis_title="Chemical Shift δ (ppm)",
        yaxis_title="Protonenzahl (rel. Intensität)",
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
    )

    # Y-Achse fixieren, damit Scroll/Zoom nur horizontal wirkt
    fig.update_yaxes(
        range=[0, y_max * 1.08],
        autorange=False,
        fixedrange=True,
        showgrid=True,
        zeroline=False,
    )

    return fig

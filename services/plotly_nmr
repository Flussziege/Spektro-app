from __future__ import annotations
import plotly.graph_objects as go


def make_interactive_1h_plot(nmr_result: dict, smiles: str, show_integrals: bool = True):
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

    # Peak-Labels als Hover-Marker
    peak_x = [p["shift"] for p in peaks]
    peak_y = []
    for x in peak_x:
        idx = min(range(len(ppm_axis)), key=lambda i: abs(ppm_axis[i] - x))
        peak_y.append(spectrum[idx])

    peak_text = [
        f"{p['shift']:.2f} ppm<br>{p['mult_str']}, {p['n_h']}H"
        for p in peaks
    ]

    fig.add_trace(
        go.Scatter(
            x=peak_x,
            y=peak_y,
            mode="markers",
            name="Peaks",
            marker=dict(size=7),
            text=peak_text,
            hovertemplate="%{text}<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"Simuliertes ¹H-NMR-Spektrum — {smiles}",
        xaxis_title="Chemical Shift δ (ppm)",
        yaxis_title="Protonenzahl (rel. Intensität)",
        dragmode="pan",
        template="plotly_white",
        height=500,
        margin=dict(l=30, r=30, t=60, b=30),
    )

    # NMR-typisch invertierte ppm-Achse
    fig.update_xaxes(
        autorange="reversed",
        showgrid=True,
        zeroline=False,
    )
    fig.update_yaxes(
        showgrid=True,
        zeroline=False,
    )

    return fig

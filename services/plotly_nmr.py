from __future__ import annotations
import plotly.graph_objects as go
import numpy as np


def add_baseline_noise(y, noise_level: float = 0.003, seed: int | None = 42):
    y = np.asarray(y, dtype=float)

    rng = np.random.default_rng(seed)
    noise = rng.normal(0, noise_level, size=len(y))

    baseline = np.clip(noise, 0, None)
    return y + baseline


def make_interactive_1h_plot(
    nmr_result: dict,
    smiles: str,
    show_integrals: bool = True,
    theme_mode: str = "light",
    **kwargs,
):
    ppm_axis = nmr_result["ppm_axis"]
    spectrum = np.asarray(nmr_result["spectrum"], dtype=float)
    peaks = nmr_result["peaks"]

    fig = go.Figure()

    # leichtes Rauschen für 1H
    y_plot = add_baseline_noise(spectrum, noise_level=0.003, seed=42)

    fig.add_trace(
        go.Scatter(
            x=ppm_axis,
            y=y_plot,
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
        peak_y.append(float(y_plot[idx]))

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

    y_max = max(float(y_plot.max()) if len(y_plot) else 1.0, 1.0)

    if show_integrals:
        fig.update_layout(
            title=f"Simulated ¹H-NMR Spectrum — {smiles}",
            xaxis_title="Chemical Shift δ (ppm)",
            yaxis_title="Proton Number (rel. Intensity)",
            template="simple_white",
            height=520,
            margin=dict(l=70, r=30, t=50, b=70),
            dragmode="pan",
            hovermode="x unified",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font=dict(color="#E5E7EB"),
        )
    else:
        fig.update_layout(
            title="Simulated ¹H-NMR Spectrum",
            xaxis_title="Chemical Shift δ (ppm)",
            yaxis_title="Proton Number (rel. Intensity)",
            template="plotly_white",
            height=520,
            margin=dict(l=70, r=30, t=50, b=70),
            dragmode="pan",
            hovermode="x unified",
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font=dict(color="#E5E7EB"),
        )

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
        gridcolor="#334155",
        linecolor="#94A3B8",
        tickfont=dict(color="#E5E7EB"),
        title_font=dict(color="#E5E7EB"),
        )


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
        gridcolor="#334155",
        linecolor="#94A3B8",
        tickfont=dict(color="#E5E7EB"),
        title_font=dict(color="#E5E7EB"),
    )

    if theme_mode == "dark":
        fig.update_layout(
            paper_bgcolor="#0F172A",
            plot_bgcolor="#0F172A",
            font=dict(color="#E5E7EB"),
        )
        fig.update_xaxes(
            gridcolor="#334155",
            linecolor="#94A3B8",
            tickfont=dict(color="#E5E7EB"),
            title_font=dict(color="#E5E7EB"),
        )
        fig.update_yaxes(
            gridcolor="#334155",
            linecolor="#94A3B8",
            tickfont=dict(color="#E5E7EB"),
            title_font=dict(color="#E5E7EB"),
        )
    else:
        fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#111827"),
        )
        fig.update_xaxes(
            gridcolor="#E5E7EB",
            linecolor="#94A3B8",
            tickfont=dict(color="#111827"),
            title_font=dict(color="#111827"),
        )
        fig.update_yaxes(
            gridcolor="#E5E7EB",
            linecolor="#94A3B8",
            tickfont=dict(color="#111827"),
            title_font=dict(color="#111827"),
        )


    return fig
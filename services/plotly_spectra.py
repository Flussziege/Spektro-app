from __future__ import annotations
import plotly.graph_objects as go
import numpy as np


def add_baseline_noise(y, noise_level: float = 0.006, seed: int | None = 42):
    y = np.asarray(y, dtype=float)

    rng = np.random.default_rng(seed)
    noise = rng.normal(0, noise_level, size=len(y))

    baseline = np.clip(noise, 0, None)
    return y + baseline
def def make_interactive_13c_plot(
        spec_result: dict,
        smiles: str,
        show_integrals: bool = True,
        theme_mode: str = "light",
    ):
    x = np.asarray(spec_result["wns"], dtype=float)
    y = np.asarray(spec_result["spectrum"], dtype=float)
    freqs = spec_result.get("frequencies", [])
    intens = spec_result.get("intensities", [])

    # leichtes 13C-Rauschen
    y_plot = add_baseline_noise(y, noise_level=0.006, seed=42)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_plot,
            mode="lines",
            name="¹³C NMR",
            hovertemplate="δ = %{x:.2f} ppm<br>Intensity = %{y:.2f}<extra></extra>",
        )
    )

    if len(freqs) > 0:
        peak_y = []
        for f in freqs:
            idx = min(range(len(x)), key=lambda i: abs(x[i] - f))
            peak_y.append(float(y_plot[idx]))

        peak_text = [
            f"{float(f):.1f} ppm<br>rel. Intensity: {float(i):.2f}"
            for f, i in zip(freqs, intens)
        ]

        if show_integrals:
            fig.add_trace(
                go.Scatter(
                    x=list(freqs),
                    y=peak_y,
                    mode="markers",
                    marker=dict(size=8, opacity=0.0),
                    text=peak_text,
                    hovertemplate="%{text}<extra></extra>",
                    showlegend=False,
                )
            )

    if show_integrals:
        fig.update_layout(
            title=f"Simulated ¹³C-NMR Spectrum — {smiles}",
            xaxis_title="Chemical Shift (δ, ppm)",
            yaxis_title="Relative Intensity",
            template="plotly_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )
    else:
        fig.update_layout(
            title="Simulated ¹³C-NMR Spectrum",
            xaxis_title="Chemical Shift (δ, ppm)",
            yaxis_title="Relative Intensity",
            template="plotly_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )

    fig.update_xaxes(
        range=[230, -10],
        autorange=False,
        minallowed=-10,
        maxallowed=230,
        fixedrange=False,
        showgrid=True,
        zeroline=False,
    )

    fig.update_yaxes(
        fixedrange=True,
        showgrid=True,
        zeroline=False,
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

def make_interactive_ir_plot(ir_result: dict, smiles: str, show_integrals: bool = True, theme_mode: str = "light"):
    x = ir_result["wns"]
    y = ir_result["spectrum"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="IR",
            hovertemplate="%{x:.0f} cm⁻¹<br>Intensity = %{y:.2f}<extra></extra>",
        )
    )

    if show_integrals:
        fig.update_layout(
            title=f"Simulated IR Spectrum — {smiles}",
            xaxis_title="Wavenumber (cm⁻¹)",
            yaxis_title="Intensity (rel.)",
            template="plotly_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )
    else: 
        fig.update_layout(
            title=f"Simulated IR Spectrum",
            xaxis_title="Wavenumber (cm⁻¹)",
            yaxis_title="Intensity (rel.)",
            template="plotly_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )

    # IR klassisch: hohe Wellenzahl links
    fig.update_xaxes(
        autorange="reversed",
        fixedrange=False,
        showgrid=True,
        zeroline=False,
        minallowed=500,
        maxallowed=4000,
    )

    fig.update_yaxes(
        fixedrange=True,
        showgrid=True,
        zeroline=False,
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

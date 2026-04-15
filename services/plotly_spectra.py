from __future__ import annotations

import numpy as np
import plotly.graph_objects as go


def add_baseline_noise(y, noise_level: float = 0.006, seed: int | None = 42):
    y = np.asarray(y, dtype=float)

    rng = np.random.default_rng(seed)
    noise = rng.normal(0, noise_level, size=len(y))

    baseline = np.clip(noise, 0, None)
    return y + baseline


def _apply_spectrum_theme(fig: go.Figure, theme_mode: str = "light") -> go.Figure:
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


def make_interactive_1h_plot(
    nmr_result: dict,
    smiles: str,
    show_integrals: bool = True,
    theme_mode: str = "light",
    **kwargs,
):
    ppm_axis = np.asarray(nmr_result["ppm_axis"], dtype=float)
    spectrum = np.asarray(nmr_result["spectrum"], dtype=float)
    peaks = nmr_result.get("peaks", [])

    fig = go.Figure()

    y_plot = add_baseline_noise(spectrum, noise_level=0.003, seed=42)
    y_max = max(float(y_plot.max()) if len(y_plot) else 1.0, 1.0)

    fig.add_trace(
        go.Scatter(
            x=ppm_axis,
            y=y_plot,
            mode="lines",
            name="¹H NMR",
            hovertemplate="δ = %{x:.2f} ppm<br>Intensity = %{y:.2f}<extra></extra>",
        )
    )

    if len(peaks) > 0 and show_integrals:
        peak_x = [float(p["shift"]) for p in peaks]
        peak_y = []
        for x in peak_x:
            idx = min(range(len(ppm_axis)), key=lambda i: abs(ppm_axis[i] - x))
            peak_y.append(float(y_plot[idx]))

        peak_text = [
            f"{float(p['shift']):.2f} ppm<br>{p['mult_str']}, {p['n_h']}H"
            for p in peaks
        ]

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

    fig.update_layout(
        title=f"Simulated ¹H-NMR Spectrum — {smiles}" if show_integrals else "Simulated ¹H-NMR Spectrum",
        xaxis_title="Chemical Shift (δ, ppm)",
        yaxis_title="Relative Intensity",
        template="plotly_white" if theme_mode != "dark" else "simple_white",
        height=520,
        margin=dict(l=70, r=30, t=50, b=70),
        dragmode="zoom",
        hovermode="x unified",
        uirevision="1h-spectrum",
    )

    fig.update_xaxes(
        range=[12.5, -0.3],
        autorange=False,
        minallowed=-0.3,
        maxallowed=12.5,
        fixedrange=False,
        showgrid=True,
        zeroline=False,
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    fig.update_yaxes(
        range=[0, y_max * 1.08],
        autorange=False,
        fixedrange=True,
        showgrid=True,
        zeroline=False,
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    return _apply_spectrum_theme(fig, theme_mode)


def make_interactive_13c_plot(
    spec_result: dict,
    smiles: str,
    show_integrals: bool = True,
    theme_mode: str = "light",
):
    x = np.asarray(spec_result["wns"], dtype=float)
    y = np.asarray(spec_result["spectrum"], dtype=float)
    freqs = spec_result.get("frequencies", [])
    intens = spec_result.get("intensities", [])

    y_plot = add_baseline_noise(y, noise_level=0.006, seed=42)
    y_max = max(float(y_plot.max()) if len(y_plot) else 1.0, 1.0)

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

    if len(freqs) > 0 and show_integrals:
        peak_y = []
        for f in freqs:
            idx = min(range(len(x)), key=lambda i: abs(x[i] - f))
            peak_y.append(float(y_plot[idx]))

        peak_text = [
            f"{float(f):.1f} ppm<br>rel. Intensity: {float(i):.2f}"
            for f, i in zip(freqs, intens)
        ]

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

    fig.update_layout(
        title=f"Simulated ¹³C-NMR Spectrum — {smiles}" if show_integrals else "Simulated ¹³C-NMR Spectrum",
        xaxis_title="Chemical Shift (δ, ppm)",
        yaxis_title="Relative Intensity",
        template="plotly_white",
        height=520,
        margin=dict(l=30, r=30, t=60, b=30),
        dragmode="zoom",
        hovermode="x unified",
        uirevision="13c-spectrum",
    )

    fig.update_xaxes(
        range=[230, -10],
        autorange=False,
        minallowed=-10,
        maxallowed=230,
        fixedrange=False,
        showgrid=True,
        zeroline=False,
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    fig.update_yaxes(
        range=[0, y_max * 1.05],
        autorange=False,
        fixedrange=True,
        showgrid=True,
        zeroline=False,
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    return _apply_spectrum_theme(fig, theme_mode)


def make_interactive_ir_plot(
    ir_result: dict,
    smiles: str,
    show_integrals: bool = True,
    theme_mode: str = "light",
):
    x = np.asarray(ir_result["wns"], dtype=float)
    y = np.asarray(ir_result["spectrum"], dtype=float)

    y_max = max(float(y.max()) if len(y) else 1.0, 1.0)

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

    fig.update_layout(
        title=f"Simulated IR Spectrum — {smiles}" if show_integrals else "Simulated IR Spectrum",
        xaxis_title="Wavenumber (cm⁻¹)",
        yaxis_title="Intensity (rel.)",
        template="plotly_white",
        height=520,
        margin=dict(l=30, r=30, t=60, b=30),
        dragmode="zoom",
        hovermode="x unified",
        uirevision="ir-spectrum",
    )

    fig.update_xaxes(
        autorange="reversed",
        fixedrange=False,
        showgrid=True,
        zeroline=False,
        minallowed=500,
        maxallowed=4000,
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    fig.update_yaxes(
        range=[0, y_max * 1.05],
        autorange=False,
        fixedrange=True,
        showgrid=True,
        zeroline=False,
        automargin=True,
        showline=True,
        mirror=False,
        ticks="outside",
    )

    return _apply_spectrum_theme(fig, theme_mode)
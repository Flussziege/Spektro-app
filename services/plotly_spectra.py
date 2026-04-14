from __future__ import annotations
import plotly.graph_objects as go


def make_interactive_13c_plot(spec_result: dict, smiles: str, show_integrals: bool = True):
    x = spec_result["wns"]
    y = spec_result["spectrum"]
    freqs = spec_result.get("frequencies", [])
    intens = spec_result.get("intensities", [])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="¹³C NMR",
            hovertemplate="δ = %{x:.2f} ppm<br>Intensity = %{y:.2f}<extra></extra>",
        )
    )

    if len(freqs) > 0:
        peak_y = []
        for f in freqs:
            idx = min(range(len(x)), key=lambda i: abs(x[i] - f))
            peak_y.append(float(y[idx]))

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
            xaxis_title="Chemical Shift δ (ppm)",
            yaxis_title="Intensity (rel.)",
            template="plotly_white",
            height=520,
            margin=dict(l=30, r=30, t=60, b=30),
            dragmode="pan",
            hovermode="x unified",
        )
    else:
        fig.update_layout(
            title=f"Simulated ¹³C-NMR Spectrum",
            xaxis_title="Chemical Shift δ (ppm)",
            yaxis_title="Intensity (rel.)",
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

    return fig


def make_interactive_ir_plot(ir_result: dict, smiles: str, show_integrals: bool = True):
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

    return fig

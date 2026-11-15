"""
PhysicsX Lab - UI Theme & Style Engine
Provides consistent cyberpunk/modern dark ed-tech styling and Plotly chart themes.
"""

import streamlit as st


def apply_custom_theme():
    """Injects high-end, responsive dark CSS into any Streamlit page."""
    st.markdown(
        """
        <style>
        /* Global font smoothing & theme variables */
        :root {
            --bg-primary: #0b0f19;
            --bg-secondary: #111827;
            --card-bg: rgba(22, 30, 49, 0.7);
            --card-border: rgba(99, 102, 241, 0.2);
            --accent-cyan: #00f0ff;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }

        /* Glassmorphism Card Style */
        .px-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(12px);
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .px-card:hover {
            border-color: rgba(0, 240, 255, 0.4);
            box-shadow: 0 15px 30px -5px rgba(0, 240, 255, 0.1);
            transform: translateY(-2px);
        }

        /* Gradient Headline */
        .px-gradient-text {
            background: linear-gradient(135deg, #00f0ff 0%, #6366f1 50%, #d946ef 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        /* Glowing Badge */
        .px-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 14px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            background: rgba(0, 240, 255, 0.1);
            color: #00f0ff;
            border: 1px solid rgba(0, 240, 255, 0.3);
            margin-bottom: 12px;
        }

        .px-badge-success {
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
            border-color: rgba(16, 185, 129, 0.3);
        }

        .px-badge-purple {
            background: rgba(139, 92, 246, 0.1);
            color: #c084fc;
            border-color: rgba(139, 92, 246, 0.3);
        }

        /* Enhanced Metrics */
        [data-testid="stMetric"] {
            background: rgba(22, 30, 49, 0.6);
            border: 1px solid rgba(99, 102, 241, 0.15);
            padding: 14px 18px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            border-color: rgba(0, 240, 255, 0.3);
            background: rgba(22, 30, 49, 0.85);
        }
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }
        [data-testid="stMetricValue"] {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        /* Buttons Enhancement */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
            border: 1px solid rgba(99, 102, 241, 0.25);
        }
        .stButton > button:hover {
            border-color: #00f0ff;
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.25);
            transform: translateY(-1px);
        }

        /* Form container border */
        [data-testid="stForm"] {
            border-radius: 16px;
            border: 1px solid rgba(99, 102, 241, 0.2);
            background: rgba(22, 30, 49, 0.4);
            padding: 24px;
        }

        /* Question palette grid buttons */
        .palette-btn {
            padding: 4px !important;
            font-size: 11px !important;
        }

        /* Custom scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0b0f19;
        }
        ::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, subtitle: str, icon: str = "⚛️", badge: str = "PhysicsX Lab"):
    """Renders a visually striking page hero header with badge and gradient typography."""
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div class="px-badge">
                <span>{icon}</span>
                <span>{badge}</span>
            </div>
            <h1 class="px-gradient-text" style="font-size: 2.4rem; margin: 0 0 8px 0; line-height: 1.2;">
                {icon} {title}
            </h1>
            <p style="color: #94a3b8; font-size: 1.05rem; margin: 0; max-width: 800px; line-height: 1.5;">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_plotly_layout(title: str = "", x_title: str = "", y_title: str = "", height: int = 440):
    """Returns a sleek, dark-mode configured Plotly layout dict."""
    return dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(color="#f8fafc", size=15),
            x=0.02,
            y=0.96,
        ),
        xaxis=dict(
            title=dict(text=x_title, font=dict(color="#94a3b8", size=13)),
            tickfont=dict(color="#94a3b8", size=11),
            gridcolor="rgba(255, 255, 255, 0.07)",
            zerolinecolor="rgba(255, 255, 255, 0.2)",
            showgrid=True,
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color="#94a3b8", size=13)),
            tickfont=dict(color="#94a3b8", size=11),
            gridcolor="rgba(255, 255, 255, 0.07)",
            zerolinecolor="rgba(255, 255, 255, 0.2)",
            showgrid=True,
        ),
        plot_bgcolor="rgba(15, 23, 42, 0.6)",
        paper_bgcolor="rgba(15, 23, 42, 0)",
        legend=dict(
            font=dict(color="#cbd5e1", size=11),
            bgcolor="rgba(15, 23, 42, 0.8)",
            bordercolor="rgba(99, 102, 241, 0.2)",
            borderwidth=1,
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        margin=dict(l=55, r=25, t=50, b=50),
        height=height,
        hovermode="x unified",
    )

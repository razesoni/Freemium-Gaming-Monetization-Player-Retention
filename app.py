import json
import io
import pandas as pd
from flask import Flask, render_template, request, jsonify, Response
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_raw_data, clean_game_data, filter_gaming_dataset
from src.monetization import calculate_arpu, segment_revenue_contribution, genre_monetization_depth
from src.player_analysis import calculate_correlation_matrix

app = Flask(__name__)

# --- Load & Clean Data on Startup ---
try:
    RAW_DF = load_raw_data()
    PAYING_DF, F2P_DF = clean_game_data(RAW_DF)
    BASE_DF = pd.concat([PAYING_DF, F2P_DF], ignore_index=True)
except Exception as e:
    print(f"Dataset load error: {e}")
    # Minimal fallback schema
    BASE_DF = pd.DataFrame(columns=[
        "UserID", "Age", "Gender", "Country", "Device", "GameGenre",
        "SessionCount", "AverageSessionLength", "SpendingSegment",
        "InAppPurchaseAmount", "FirstPurchaseDaysAfterInstall", "PaymentMethod", "LastPurchaseDate"
    ])

def style_plotly_chart(fig: go.Figure) -> go.Figure:
    """Applies high-contrast dark & neon gaming styling."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F3F4F6", family="sans-serif", size=12),
        margin=dict(l=25, r=25, t=45, b=25),
        legend=dict(
            font=dict(color="#F3F4F6"),
            bgcolor="rgba(17, 24, 39, 0.7)",
            bordercolor="rgba(255, 255, 255, 0.15)",
            borderwidth=1
        )
    )
    fig.update_xaxes(
        tickfont=dict(color="#D1D5DB"),
        title_font=dict(color="#F9FAFB"),
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.08)",
        zeroline=False
    )
    fig.update_yaxes(
        tickfont=dict(color="#D1D5DB"),
        title_font=dict(color="#F9FAFB"),
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.08)",
        zeroline=False
    )
    return fig

def generate_analytics_payload(df: pd.DataFrame):
    paying_cohort = df[df["InAppPurchaseAmount"] > 0]
    f2p_cohort = df[(df["InAppPurchaseAmount"].isna()) | (df["InAppPurchaseAmount"] == 0)]
    
    total_rev = paying_cohort["InAppPurchaseAmount"].sum() if not paying_cohort.empty else 0.0
    paying_users = paying_cohort["UserID"].nunique() if not paying_cohort.empty else 0
    f2p_users = f2p_cohort["UserID"].nunique() if not f2p_cohort.empty else 0
    arppu = (total_rev / paying_users) if paying_users > 0 else 0.0

    kpis = {
        "total_revenue": f"${total_rev:,.2f}",
        "paying_users": f"{paying_users:,}",
        "f2p_users": f"{f2p_users:,}",
        "arppu": f"${arppu:.2f}"
    }

    charts = {}

    if not paying_cohort.empty:
        # --- TAB 1: Monetization & Pareto Concentration ---
        seg_summary = segment_revenue_contribution(paying_cohort)
        
        # 1. Revenue Pareto Doughnut
        fig_pareto = px.pie(
            seg_summary, values="TotalRevenue", names="SpendingSegment", hole=0.45,
            color="SpendingSegment",
            color_discrete_map={"Whale": "#FF6B00", "Dolphin": "#3B82F6", "Minnow": "#10B981"}
        )
        fig_pareto.update_traces(textposition="inside", textinfo="percent+label")
        charts["fig_pareto"] = json.loads(style_plotly_chart(fig_pareto).to_json())

        # 2. Total Revenue by Genre
        genre_rev = paying_cohort.groupby("GameGenre")["InAppPurchaseAmount"].sum().reset_index().sort_values(by="InAppPurchaseAmount", ascending=False)
        fig_genre_rev = px.bar(
            genre_rev, x="InAppPurchaseAmount", y="GameGenre", orientation="h",
            color="InAppPurchaseAmount", color_continuous_scale="Inferno"
        )
        fig_genre_rev.update_layout(yaxis=dict(autorange="reversed"))
        charts["fig_genre_rev"] = json.loads(style_plotly_chart(fig_genre_rev).to_json())

        # 3. Genre Depth (Whale vs Dolphin vs Minnow average spend)
        depth_df = genre_monetization_depth(paying_cohort)
        fig_depth = px.bar(
            depth_df, x="GameGenre", y=[c for c in ["Whale", "Dolphin", "Minnow"] if c in depth_df.columns],
            barmode="group", color_discrete_map={"Whale": "#FF6B00", "Dolphin": "#38BDF8", "Minnow": "#4ADE80"}
        )
        fig_depth.update_layout(xaxis_tickangle=-35)
        charts["fig_depth"] = json.loads(style_plotly_chart(fig_depth).to_json())

        # --- TAB 2: Engagement vs Monetization Correlation ---
        # 4. Correlation Heatmap
        corr = calculate_correlation_matrix(paying_cohort)
        if not corr.empty:
            fig_corr = px.imshow(
                corr, text_auto=True, aspect="auto",
                color_continuous_scale="Viridis"
            )
            charts["fig_corr"] = json.loads(style_plotly_chart(fig_corr).to_json())

        # 5. Session Count vs IAP Amount Scatter
        fig_scatter = px.scatter(
            paying_cohort, x="SessionCount", y="InAppPurchaseAmount",
            color="SpendingSegment", hover_data=["Age", "GameGenre"],
            color_discrete_map={"Whale": "#FF6B00", "Dolphin": "#38BDF8", "Minnow": "#10B981"}
        )
        charts["fig_scatter"] = json.loads(style_plotly_chart(fig_scatter).to_json())

        # 6. Average Session Length Distribution
        fig_session_box = px.box(
            paying_cohort, x="SpendingSegment", y="AverageSessionLength",
            color="SpendingSegment", color_discrete_map={"Whale": "#FF6B00", "Dolphin": "#38BDF8", "Minnow": "#10B981"}
        )
        charts["fig_session_box"] = json.loads(style_plotly_chart(fig_session_box).to_json())

        # --- TAB 3: Cohort & Demographics ---
        # 7. Device ARPU Split
        device_df = paying_cohort.groupby("Device").agg(
            Revenue=("InAppPurchaseAmount", "sum"),
            Users=("UserID", "nunique")
        ).reset_index()
        device_df["ARPU"] = (device_df["Revenue"] / device_df["Users"]).round(2)
        fig_device = px.bar(
            device_df, x="Device", y="ARPU", color="Device",
            color_discrete_map={"iOS": "#38BDF8", "Android": "#10B981", "Other": "#9CA3AF"}
        )
        charts["fig_device"] = json.loads(style_plotly_chart(fig_device).to_json())

        # 8. Top Countries by Player Volume
        country_df = df["Country"].value_counts().head(10).reset_index()
        country_df.columns = ["Country", "Players"]
        fig_country = px.bar(
            country_df, x="Country", y="Players", color="Players",
            color_continuous_scale="Teal"
        )
        fig_country.update_layout(xaxis_tickangle=-35)
        charts["fig_country"] = json.loads(style_plotly_chart(fig_country).to_json())

        # 9. Days to First Purchase (Latency)
        latency_df = paying_cohort["FirstPurchaseDaysAfterInstall"].dropna()
        fig_latency = px.histogram(
            latency_df, nbins=30, color_discrete_sequence=["#FF6B00"]
        )
        charts["fig_latency"] = json.loads(style_plotly_chart(fig_latency).to_json())

    # Raw table sample preview
    cols = [
        col for col in [
            "UserID", "Age", "Gender", "Country", "Device", "GameGenre",
            "SessionCount", "AverageSessionLength", "SpendingSegment",
            "InAppPurchaseAmount", "FirstPurchaseDaysAfterInstall", "PaymentMethod"
        ] if col in df.columns
    ]
    table_data = df[cols].head(50).to_dict(orient="records")

    return {
        "kpis": kpis,
        "charts": charts,
        "table_cols": cols,
        "table_data": table_data,
        "empty": df.empty
    }

@app.route("/")
def index():
    genres = sorted(BASE_DF["GameGenre"].dropna().unique())
    segments = ["Whale", "Dolphin", "Minnow"]
    devices = sorted(BASE_DF["Device"].dropna().unique())
    countries = sorted(BASE_DF["Country"].dropna().unique())

    return render_template(
        "index.html",
        genres=genres,
        segments=segments,
        devices=devices,
        countries=countries
    )

@app.route("/api/filter", methods=["POST"])
def api_filter():
    data = request.get_json() or {}
    filtered_df = filter_gaming_dataset(
        df=BASE_DF,
        genres=data.get("genres"),
        segments=data.get("segments"),
        devices=data.get("devices"),
        countries=data.get("countries")
    )
    return jsonify(generate_analytics_payload(filtered_df))

@app.route("/api/download-csv", methods=["POST"])
def download_csv():
    data = request.get_json() or {}
    filtered_df = filter_gaming_dataset(
        df=BASE_DF,
        genres=data.get("genres"),
        segments=data.get("segments"),
        devices=data.get("devices"),
        countries=data.get("countries")
    )
    output = io.StringIO()
    filtered_df.to_csv(output, index=False)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=freemium_game_analytics.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
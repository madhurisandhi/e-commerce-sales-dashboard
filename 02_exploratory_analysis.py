import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ─────────────────────────────────────────────
# E-Commerce Sales Dashboard
# Script 02: Exploratory Data Analysis (EDA)
# ─────────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="Blues_d")
os.makedirs("outputs/figures", exist_ok=True)


def load_clean_data():
    """Load cleaned data or generate sample."""
    try:
        return pd.read_csv("data/cleaned/sales_clean.csv", parse_dates=["order_date"])
    except FileNotFoundError:
        from notebooks.data_cleaning import generate_sample_data, clean_data
        return clean_data(generate_sample_data(800))


def plot_monthly_revenue(df):
    monthly = df.groupby(["year", "month_name", "month"])["sales"].sum().reset_index()
    monthly = monthly.sort_values(["year", "month"])

    fig, ax = plt.subplots(figsize=(12, 5))
    for year, grp in monthly.groupby("year"):
        ax.plot(grp["month"], grp["sales"], marker="o", linewidth=2, label=str(year))

    ax.set_title("Monthly Revenue Trend by Year", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales ($)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    ax.legend(title="Year")
    plt.tight_layout()
    plt.savefig("outputs/figures/monthly_revenue.png", dpi=150)
    print("Saved: monthly_revenue.png")
    plt.show()


def plot_category_performance(df):
    cat = df.groupby("category").agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        orders=("order_id", "count")
    ).reset_index().sort_values("total_sales", ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Sales by category
    sns.barplot(data=cat, x="total_sales", y="category", palette="Blues_d", ax=axes[0])
    axes[0].set_title("Revenue by Category", fontweight="bold")
    axes[0].set_xlabel("Total Sales ($)")
    axes[0].set_ylabel("")
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # Profit margin by category
    cat["margin"] = (cat["total_profit"] / cat["total_sales"] * 100).round(1)
    sns.barplot(data=cat, x="margin", y="category", palette="Greens_d", ax=axes[1])
    axes[1].set_title("Profit Margin % by Category", fontweight="bold")
    axes[1].set_xlabel("Profit Margin (%)")
    axes[1].set_ylabel("")

    plt.suptitle("Category Performance Overview", fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig("outputs/figures/category_performance.png", dpi=150)
    print("Saved: category_performance.png")
    plt.show()


def plot_regional_heatmap(df):
    pivot = df.pivot_table(values="sales", index="region", columns="quarter", aggfunc="sum")

    fig, ax = plt.subplots(figsize=(11, 4))
    sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="YlOrRd",
                linewidths=0.5, ax=ax, cbar_kws={"label": "Sales ($)"})
    ax.set_title("Regional Sales by Quarter ($)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Region")
    plt.tight_layout()
    plt.savefig("outputs/figures/regional_heatmap.png", dpi=150)
    print("Saved: regional_heatmap.png")
    plt.show()


def plot_rfm_segments(df):
    """Simple RFM segmentation visualisation."""
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("customer_id").agg(
        recency=("order_date", lambda x: (snapshot_date - x.max()).days),
        frequency=("order_id", "count"),
        monetary=("sales", "sum")
    ).reset_index()

    # Score 1–4
    rfm["R"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1])
    rfm["F"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
    rfm["M"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4])
    rfm["RFM"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)

    def segment(row):
        score = int(row["R"]) + int(row["F"]) + int(row["M"])
        if score >= 10: return "Champions"
        elif score >= 7: return "Loyal"
        elif score >= 5: return "At-Risk"
        else: return "Lost"

    rfm["Segment"] = rfm.apply(segment, axis=1)

    seg_counts = rfm["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]

    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#2E74B5", "#70AD47", "#FFC000", "#FF0000"]
    sns.barplot(data=seg_counts, x="Segment", y="Count",
                palette=colors[:len(seg_counts)], ax=ax)
    ax.set_title("Customer Segments (RFM Analysis)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Segment")
    ax.set_ylabel("Number of Customers")
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}", (p.get_x() + p.get_width() / 2, p.get_height() + 0.5),
                    ha="center", fontsize=11)
    plt.tight_layout()
    plt.savefig("outputs/figures/rfm_segments.png", dpi=150)
    print("Saved: rfm_segments.png")
    plt.show()
    return rfm


def summary_stats(df):
    print("\n" + "=" * 50)
    print("SUMMARY STATISTICS")
    print("=" * 50)
    print(f"Total Revenue:      ${df['sales'].sum():>12,.2f}")
    print(f"Total Profit:       ${df['profit'].sum():>12,.2f}")
    print(f"Overall Margin:     {df['profit'].sum() / df['sales'].sum() * 100:>11.1f}%")
    print(f"Avg Order Value:    ${df['sales'].mean():>12,.2f}")
    print(f"Total Orders:       {df['order_id'].nunique():>12,}")
    print(f"Unique Customers:   {df['customer_id'].nunique():>12,}")
    print(f"Date Range:         {df['order_date'].min().date()} → {df['order_date'].max().date()}")


if __name__ == "__main__":
    print("=" * 50)
    print("E-Commerce EDA")
    print("=" * 50)
    df = load_clean_data()
    summary_stats(df)
    plot_monthly_revenue(df)
    plot_category_performance(df)
    plot_regional_heatmap(df)
    rfm = plot_rfm_segments(df)
    print("\nRFM Segment Distribution:")
    print(rfm["Segment"].value_counts().to_string())

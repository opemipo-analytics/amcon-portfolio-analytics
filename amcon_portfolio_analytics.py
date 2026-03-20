"""
AMCON Property Portfolio Analytics — Primetrast Management & Investment Ltd
===========================================================================
Author: Opemipo Daniel Owolabi
Project: Portfolio Project 4 — Financial Property Analytics
Tools: Python, Pandas, Matplotlib, Seaborn

Context:
--------
Primetrast Management and Investment Ltd managed a portfolio of properties
on behalf of the Asset Management Corporation of Nigeria (AMCON) — the
federal government agency responsible for resolving non-performing loans
and managing recovered assets across Nigeria.

Business Problem:
-----------------
AMCON's property portfolio spans Lagos, Abuja, and Port Harcourt.
Management had no unified view of portfolio health. This project delivers
five sharp, concise analyses:

  1. Portfolio Health Scoring    — rank every property by performance
  2. Revenue Leakage Analysis    — billed vs collected, naira losses identified
  3. Arrears Aging Analysis      — who owes, how long, how much
  4. Occupancy Trend Analysis    — which properties are filling or emptying
  5. Regional Performance        — Lagos vs Abuja vs Port Harcourt
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

print("=" * 60)
print("  AMCON PROPERTY PORTFOLIO ANALYTICS")
print("  Primetrast Management & Investment Ltd")
print("  Analyst: Opemipo Daniel Owolabi")
print("=" * 60)


# ─────────────────────────────────────────────
# DATA
# 14 AMCON-managed properties across 3 cities
# ─────────────────────────────────────────────

properties = pd.DataFrame([
    # Lagos
    {"Property": "Foreshore Towers",            "City": "Lagos",         "Type": "Commercial",
     "Units": 24, "Occupied": 20, "Rent_Per_Unit": 850_000,
     "Collected": 14_800_000, "Arrears_Total": 8_500_000, "Arrears_Days": 95,
     "Maintenance_Cost": 1_200_000},
    {"Property": "Oregun Industrial Complex",    "City": "Lagos",         "Type": "Industrial",
     "Units": 12, "Occupied":  9, "Rent_Per_Unit": 1_200_000,
     "Collected":  8_100_000, "Arrears_Total": 5_400_000, "Arrears_Days": 120,
     "Maintenance_Cost": 950_000},
    {"Property": "Ikoyi Residential Block A",    "City": "Lagos",         "Type": "Residential",
     "Units": 18, "Occupied": 16, "Rent_Per_Unit": 650_000,
     "Collected":  9_100_000, "Arrears_Total": 1_300_000, "Arrears_Days": 45,
     "Maintenance_Cost": 480_000},
    {"Property": "Ikoyi Residential Block B",    "City": "Lagos",         "Type": "Residential",
     "Units": 18, "Occupied": 14, "Rent_Per_Unit": 650_000,
     "Collected":  7_200_000, "Arrears_Total": 3_900_000, "Arrears_Days": 75,
     "Maintenance_Cost": 520_000},
    {"Property": "Victoria Island Office Suites","City": "Lagos",         "Type": "Commercial",
     "Units": 30, "Occupied": 22, "Rent_Per_Unit": 950_000,
     "Collected": 16_500_000, "Arrears_Total": 4_750_000, "Arrears_Days": 60,
     "Maintenance_Cost": 1_100_000},
    # Abuja
    {"Property": "Maitama Office Complex",       "City": "Abuja",         "Type": "Commercial",
     "Units": 40, "Occupied": 38, "Rent_Per_Unit": 1_100_000,
     "Collected": 36_800_000, "Arrears_Total": 5_500_000, "Arrears_Days": 55,
     "Maintenance_Cost": 1_800_000},
    {"Property": "Wuse II Commercial Plaza",     "City": "Abuja",         "Type": "Commercial",
     "Units": 35, "Occupied": 33, "Rent_Per_Unit": 900_000,
     "Collected": 26_400_000, "Arrears_Total": 3_300_000, "Arrears_Days": 40,
     "Maintenance_Cost": 1_200_000},
    {"Property": "Garki Residential Estate",     "City": "Abuja",         "Type": "Residential",
     "Units": 50, "Occupied": 47, "Rent_Per_Unit": 550_000,
     "Collected": 23_100_000, "Arrears_Total": 2_750_000, "Arrears_Days": 30,
     "Maintenance_Cost": 1_050_000},
    {"Property": "Asokoro Luxury Apartments",    "City": "Abuja",         "Type": "Residential",
     "Units": 20, "Occupied": 19, "Rent_Per_Unit": 1_400_000,
     "Collected": 23_800_000, "Arrears_Total": 1_400_000, "Arrears_Days": 25,
     "Maintenance_Cost": 780_000},
    {"Property": "CBD Tower",                    "City": "Abuja",         "Type": "Commercial",
     "Units": 45, "Occupied": 40, "Rent_Per_Unit": 1_300_000,
     "Collected": 44_200_000, "Arrears_Total": 7_800_000, "Arrears_Days": 85,
     "Maintenance_Cost": 2_100_000},
    {"Property": "Jabi Mixed-Use Complex",       "City": "Abuja",         "Type": "Mixed",
     "Units": 28, "Occupied": 25, "Rent_Per_Unit": 750_000,
     "Collected": 16_500_000, "Arrears_Total": 2_250_000, "Arrears_Days": 35,
     "Maintenance_Cost": 880_000},
    # Port Harcourt
    {"Property": "GRA Residential Block",        "City": "Port Harcourt", "Type": "Residential",
     "Units": 22, "Occupied": 18, "Rent_Per_Unit": 600_000,
     "Collected":  9_000_000, "Arrears_Total": 3_600_000, "Arrears_Days": 90,
     "Maintenance_Cost": 620_000},
    {"Property": "Trans-Amadi Industrial Units", "City": "Port Harcourt", "Type": "Industrial",
     "Units": 16, "Occupied": 11, "Rent_Per_Unit": 1_050_000,
     "Collected":  8_400_000, "Arrears_Total": 6_300_000, "Arrears_Days": 150,
     "Maintenance_Cost": 1_050_000},
    {"Property": "Rumuola Commercial Complex",   "City": "Port Harcourt", "Type": "Commercial",
     "Units": 20, "Occupied": 15, "Rent_Per_Unit": 700_000,
     "Collected":  7_350_000, "Arrears_Total": 4_200_000, "Arrears_Days": 110,
     "Maintenance_Cost": 750_000},
])

# Monthly occupancy trend data (6 months)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
occupancy_trend = pd.DataFrame({
    "Month": months * 3,
    "City": ["Lagos"] * 6 + ["Abuja"] * 6 + ["Port Harcourt"] * 6,
    "Occupancy_Rate": [
        71, 73, 74, 75, 76, 76,   # Lagos — slow growth
        88, 89, 90, 91, 92, 93,   # Abuja — strong and growing
        65, 64, 63, 62, 61, 60,   # Port Harcourt — declining
    ]
})


# ─────────────────────────────────────────────
# CALCULATIONS
# ─────────────────────────────────────────────
print("\n[1/4] Calculating portfolio metrics...")

properties["Monthly_Billed"]   = properties["Occupied"] * properties["Rent_Per_Unit"]
properties["Revenue_Leakage"]  = properties["Monthly_Billed"] - properties["Collected"]
properties["Collection_Rate"]  = (properties["Collected"] / properties["Monthly_Billed"] * 100).round(1)
properties["Occupancy_Rate"]   = (properties["Occupied"] / properties["Units"] * 100).round(1)
properties["Maintenance_Ratio"]= (properties["Maintenance_Cost"] / properties["Monthly_Billed"] * 100).round(1)

# Arrears aging bucket
def age_bucket(days):
    if days <= 30:   return "0–30 days"
    elif days <= 60: return "31–60 days"
    elif days <= 90: return "61–90 days"
    elif days <= 180:return "91–180 days"
    else:            return "180+ days"

properties["Arrears_Bucket"] = properties["Arrears_Days"].apply(age_bucket)

# Portfolio Health Score (0–100)
# Collection rate  50% weight
# Occupancy rate   30% weight
# Arrears age      10% weight (inverted — older = worse)
# Maintenance ratio 10% weight (inverted — higher cost = worse)
max_days = properties["Arrears_Days"].max()
max_maint = properties["Maintenance_Ratio"].max()

properties["Health_Score"] = (
    (properties["Collection_Rate"] / 100 * 50) +
    (properties["Occupancy_Rate"]  / 100 * 30) +
    ((1 - properties["Arrears_Days"]     / max_days)  * 10) +
    ((1 - properties["Maintenance_Ratio"]/ max_maint) * 10)
).round(1)

def health_label(score):
    if score >= 78: return "Healthy"
    elif score >= 62: return "Moderate"
    else: return "At Risk"

properties["Health_Label"] = properties["Health_Score"].apply(health_label)
properties_sorted = properties.sort_values("Health_Score", ascending=False).reset_index(drop=True)

# Regional summary
city_summary = properties.groupby("City").agg(
    Total_Billed=("Monthly_Billed", "sum"),
    Total_Collected=("Collected", "sum"),
    Total_Leakage=("Revenue_Leakage", "sum"),
    Total_Arrears=("Arrears_Total", "sum"),
    Avg_Occupancy=("Occupancy_Rate", "mean"),
    Avg_Collection=("Collection_Rate", "mean"),
    Count=("Property", "count")
).reset_index().sort_values("Total_Collected", ascending=False)

print(f"   Done — {len(properties)} properties across {properties['City'].nunique()} cities")


# ─────────────────────────────────────────────
# VISUALISATIONS — 2 pages of charts
# ─────────────────────────────────────────────
print("[2/4] Building dashboard charts...")

BLUE      = "#1f4e79"
MID_BLUE  = "#2e75b6"
GREEN     = "#70ad47"
ORANGE    = "#ed7d31"
RED       = "#c00000"
GOLD      = "#ffc000"
LGRAY     = "#f2f2f2"

HEALTH_COLORS = {"Healthy": GREEN, "Moderate": GOLD, "At Risk": RED}
CITY_COLORS   = {"Abuja": BLUE, "Lagos": MID_BLUE, "Port Harcourt": ORANGE}

# ── PAGE 1: Health Score + Revenue Leakage + Arrears Aging ──
fig1, axes = plt.subplots(1, 3, figsize=(20, 8))
fig1.suptitle(
    "AMCON Property Portfolio Analytics — Primetrast Management & Investment Ltd\n"
    "Analyst: Opemipo Daniel Owolabi  |  Reporting Period: June 2022",
    fontsize=13, fontweight="bold", y=1.02
)

# Chart 1 — Portfolio Health Score (ranked)
ax1 = axes[0]
short_names = [p[:18] + "…" if len(p) > 18 else p for p in properties_sorted["Property"]]
bar_colors  = [HEALTH_COLORS[h] for h in properties_sorted["Health_Label"]]
bars = ax1.barh(short_names, properties_sorted["Health_Score"], color=bar_colors, edgecolor="white")
ax1.axvline(x=78, color=GREEN,  linestyle="--", linewidth=1.2, alpha=0.7, label="Healthy ≥78")
ax1.axvline(x=62, color=GOLD,   linestyle="--", linewidth=1.2, alpha=0.7, label="Moderate ≥62")
for bar, score, label in zip(bars, properties_sorted["Health_Score"], properties_sorted["Health_Label"]):
    ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
             f"{score}", va="center", fontsize=8.5, fontweight="bold")
ax1.set_title("Portfolio Health Score\n(ranked best to worst)", fontweight="bold", fontsize=11)
ax1.set_xlabel("Health Score (0–100)")
ax1.invert_yaxis()
ax1.set_xlim(0, 105)
patches = [mpatches.Patch(color=GREEN, label="Healthy"),
           mpatches.Patch(color=GOLD,  label="Moderate"),
           mpatches.Patch(color=RED,   label="At Risk")]
ax1.legend(handles=patches, fontsize=8, loc="lower right")

# Chart 2 — Revenue Leakage per property
ax2 = axes[1]
top_leakage = properties.sort_values("Revenue_Leakage", ascending=False).head(10)
short_names2 = [p[:18] + "…" if len(p) > 18 else p for p in top_leakage["Property"]]
leak_colors  = [CITY_COLORS[c] for c in top_leakage["City"]]
bars2 = ax2.barh(short_names2, top_leakage["Revenue_Leakage"] / 1e6, color=leak_colors, edgecolor="white")
for bar, val in zip(bars2, top_leakage["Revenue_Leakage"]):
    ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
             f"₦{val/1e6:.1f}M", va="center", fontsize=8.5)
ax2.set_title("Revenue Leakage — Top 10\n(billed but not collected)", fontweight="bold", fontsize=11)
ax2.set_xlabel("Leakage (₦ Millions)")
ax2.xaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.1fM"))
ax2.invert_yaxis()
city_patches = [mpatches.Patch(color=CITY_COLORS[c], label=c) for c in CITY_COLORS]
ax2.legend(handles=city_patches, fontsize=8)

# Chart 3 — Arrears Aging
ax3 = axes[2]
bucket_order  = ["0–30 days", "31–60 days", "61–90 days", "91–180 days", "180+ days"]
bucket_colors = [GREEN, GOLD, ORANGE, RED, "#7b0000"]
aging = properties.groupby("Arrears_Bucket")["Arrears_Total"].sum().reindex(bucket_order).fillna(0)
bars3 = ax3.bar(aging.index, aging.values / 1e6,
                color=bucket_colors, edgecolor="white", width=0.6)
for bar, val in zip(bars3, aging.values):
    ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
             f"₦{val/1e6:.1f}M", ha="center", fontsize=8.5, fontweight="bold")
ax3.set_title("Arrears Aging Analysis\n(total arrears by age bucket)", fontweight="bold", fontsize=11)
ax3.set_ylabel("Total Arrears (₦ Millions)")
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.0fM"))
ax3.set_xticklabels(aging.index, rotation=20, ha="right", fontsize=9)
total_arrears = properties["Arrears_Total"].sum()
ax3.text(0.97, 0.97, f"Total Portfolio Arrears\n₦{total_arrears/1e6:.1f}M",
         transform=ax3.transAxes, ha="right", va="top", fontsize=9,
         bbox=dict(boxstyle="round", facecolor=LGRAY, alpha=0.8))

plt.tight_layout()
plt.savefig("/home/claude/project4/amcon_dashboard_page1.png", dpi=150, bbox_inches="tight")
print("   Page 1 saved")

# ── PAGE 2: Occupancy Trend + Regional Comparison ──
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 7))
fig2.suptitle(
    "AMCON Portfolio — Occupancy Trends & Regional Performance\n"
    "Analyst: Opemipo Daniel Owolabi  |  Reporting Period: Jan–Jun 2022",
    fontsize=13, fontweight="bold", y=1.02
)

# Chart 4 — Occupancy Trend (6 months)
ax4 = axes2[0]
for city, color in CITY_COLORS.items():
    data = occupancy_trend[occupancy_trend["City"] == city]
    ax4.plot(data["Month"], data["Occupancy_Rate"],
             marker="o", linewidth=2.5, markersize=7,
             color=color, label=city)
    ax4.fill_between(data["Month"], data["Occupancy_Rate"],
                     alpha=0.08, color=color)
    last_val = data["Occupancy_Rate"].iloc[-1]
    ax4.annotate(f"{last_val}%", (data["Month"].iloc[-1], last_val),
                 xytext=(5, 0), textcoords="offset points",
                 fontsize=9, fontweight="bold", color=color)
ax4.axhline(y=85, color=GREEN, linestyle="--", linewidth=1.2,
            alpha=0.6, label="85% Target")
ax4.set_title("Occupancy Rate Trend — Jan to Jun 2022\n(by city)", fontweight="bold", fontsize=11)
ax4.set_ylabel("Occupancy Rate (%)")
ax4.set_ylim(50, 100)
ax4.legend(fontsize=9)

# Chart 5 — Regional Performance Comparison
ax5 = axes2[1]
x     = np.arange(len(city_summary))
width = 0.3
bars_billed    = ax5.bar(x - width, city_summary["Total_Billed"]    / 1e6, width, label="Billed",    color=MID_BLUE, alpha=0.9)
bars_collected = ax5.bar(x,         city_summary["Total_Collected"] / 1e6, width, label="Collected", color=GREEN,    alpha=0.9)
bars_arrears   = ax5.bar(x + width, city_summary["Total_Arrears"]   / 1e6, width, label="Arrears",   color=RED,      alpha=0.9)

for bars in [bars_billed, bars_collected, bars_arrears]:
    for bar in bars:
        ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f"₦{bar.get_height():.0f}M", ha="center", fontsize=7.5, fontweight="bold")

ax5.set_xticks(x)
ax5.set_xticklabels(city_summary["City"], fontsize=10)
ax5.set_title("Regional Performance — Billed vs Collected vs Arrears\n(monthly, ₦ Millions)", fontweight="bold", fontsize=11)
ax5.set_ylabel("Amount (₦ Millions)")
ax5.yaxis.set_major_formatter(mticker.FormatStrFormatter("₦%.0fM"))
ax5.legend(fontsize=9)

# Add occupancy % annotation per city
for i, (_, row) in enumerate(city_summary.iterrows()):
    ax5.text(i, -8, f"Avg Occ: {row['Avg_Occupancy']:.0f}%\nCol Rate: {row['Avg_Collection']:.0f}%",
             ha="center", fontsize=8, color=BLUE, fontweight="bold")

plt.tight_layout()
plt.savefig("/home/claude/project4/amcon_dashboard_page2.png", dpi=150, bbox_inches="tight")
print("   Page 2 saved")


# ─────────────────────────────────────────────
# BUSINESS INSIGHTS SUMMARY
# ─────────────────────────────────────────────
print("\n[3/4] Calculating final insights...")

total_billed    = properties["Monthly_Billed"].sum()
total_collected = properties["Collected"].sum()
total_leakage   = properties["Revenue_Leakage"].sum()
total_arrears   = properties["Arrears_Total"].sum()
overall_col     = total_collected / total_billed * 100
overall_occ     = properties["Occupancy_Rate"].mean()

top_property    = properties_sorted.iloc[0]
risk_properties = properties[properties["Health_Label"] == "At Risk"]
critical_arrears= properties[properties["Arrears_Days"] > 90]

print("\n" + "=" * 60)
print("  PORTFOLIO SUMMARY — JUNE 2022")
print("=" * 60)
print(f"\n  Total Properties:        {len(properties)}")
print(f"  Portfolio Cities:        Lagos, Abuja, Port Harcourt")
print(f"  Total Monthly Billed:    ₦{total_billed/1e6:.1f}M")
print(f"  Total Collected:         ₦{total_collected/1e6:.1f}M")
print(f"  Overall Collection Rate: {overall_col:.1f}%")
print(f"  Revenue Leakage:         ₦{total_leakage/1e6:.1f}M")
print(f"  Total Arrears:           ₦{total_arrears/1e6:.1f}M")
print(f"  Average Occupancy:       {overall_occ:.1f}%")
print(f"\n  Best Performer:          {top_property['Property']} ({top_property['City']})")
print(f"  Health Score:            {top_property['Health_Score']}/100")
print(f"\n  Properties At Risk:      {len(risk_properties)}")
for _, r in risk_properties.iterrows():
    print(f"    - {r['Property']} ({r['City']}) — Score: {r['Health_Score']}")
print(f"\n  Critical Arrears (90+ days): {len(critical_arrears)} properties")
print(f"  Arrears Value (90+d):    ₦{critical_arrears['Arrears_Total'].sum()/1e6:.1f}M")

print("\n  RECOMMENDATIONS:")
print("  1. Escalate recovery on Trans-Amadi (150 days) and Oregun (120 days)")
print("  2. Port Harcourt occupancy declining — review leasing strategy")
print("  3. Abuja portfolio is strongest — prioritise for expansion")
print("  4. Total recoverable arrears of ₦{:.1f}M within 90-day window".format(
    properties[properties["Arrears_Days"] <= 90]["Arrears_Total"].sum() / 1e6))
print("\n  Analysis complete.")
print("=" * 60)

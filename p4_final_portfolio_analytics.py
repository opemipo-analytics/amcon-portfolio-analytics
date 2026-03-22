"""
Property Portfolio Analytics — Financial Performance Analysis
=============================================================
Author: Opemipo Daniel Owolabi
Project: Portfolio Project 4 — Financial Property Analytics
Tools: Python, Pandas, Matplotlib

Note:
-----
All company names, client names, locations and identifying information
have been anonymised to protect client confidentiality. Properties are
referred to generically by type and number. Cities are referred to as
City A, City B and City C. The analytical approach and methodology
reflect real work conducted during professional employment in the
property management sector.

Business Problem:
-----------------
A property management company managed a portfolio of assets on behalf
of a government asset management agency. Management had no unified
view of portfolio health. This project delivers five analyses:

  1. Portfolio Health Scoring    — rank every property by performance
  2. Revenue Leakage Analysis    — billed vs collected, losses identified
  3. Arrears Aging Analysis      — who owes, how long, how much
  4. Occupancy Trend Analysis    — which cities are filling or declining
  5. Regional Performance        — City A vs City B vs City C
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings("ignore")

print("=" * 60)
print("  PROPERTY PORTFOLIO ANALYTICS")
print("  Financial Performance Analysis")
print("  Analyst: Opemipo Daniel Owolabi")
print("=" * 60)


# ── DATA ──
properties = pd.DataFrame([
    {"Property":"Commercial 1",  "City":"City A","Type":"Commercial",  "Units":24,"Occupied":20,"Rent_Per_Unit":850_000,  "Collected":14_800_000,"Arrears_Total":8_500_000,"Arrears_Days":95, "Maintenance_Cost":1_200_000},
    {"Property":"Industrial 1",  "City":"City A","Type":"Industrial",  "Units":12,"Occupied": 9,"Rent_Per_Unit":1_200_000,"Collected": 8_100_000,"Arrears_Total":5_400_000,"Arrears_Days":120,"Maintenance_Cost":  950_000},
    {"Property":"Residential 1", "City":"City A","Type":"Residential", "Units":18,"Occupied":16,"Rent_Per_Unit":650_000,  "Collected": 9_100_000,"Arrears_Total":1_300_000,"Arrears_Days":45, "Maintenance_Cost":  480_000},
    {"Property":"Residential 2", "City":"City A","Type":"Residential", "Units":18,"Occupied":14,"Rent_Per_Unit":650_000,  "Collected": 7_200_000,"Arrears_Total":3_900_000,"Arrears_Days":75, "Maintenance_Cost":  520_000},
    {"Property":"Commercial 2",  "City":"City A","Type":"Commercial",  "Units":30,"Occupied":22,"Rent_Per_Unit":950_000,  "Collected":16_500_000,"Arrears_Total":4_750_000,"Arrears_Days":60, "Maintenance_Cost":1_100_000},
    {"Property":"Commercial 3",  "City":"City B","Type":"Commercial",  "Units":40,"Occupied":38,"Rent_Per_Unit":1_100_000,"Collected":36_800_000,"Arrears_Total":5_500_000,"Arrears_Days":55, "Maintenance_Cost":1_800_000},
    {"Property":"Commercial 4",  "City":"City B","Type":"Commercial",  "Units":35,"Occupied":33,"Rent_Per_Unit":900_000,  "Collected":26_400_000,"Arrears_Total":3_300_000,"Arrears_Days":40, "Maintenance_Cost":1_200_000},
    {"Property":"Residential 3", "City":"City B","Type":"Residential", "Units":50,"Occupied":47,"Rent_Per_Unit":550_000,  "Collected":23_100_000,"Arrears_Total":2_750_000,"Arrears_Days":30, "Maintenance_Cost":1_050_000},
    {"Property":"Residential 4", "City":"City B","Type":"Residential", "Units":20,"Occupied":19,"Rent_Per_Unit":1_400_000,"Collected":23_800_000,"Arrears_Total":1_400_000,"Arrears_Days":25, "Maintenance_Cost":  780_000},
    {"Property":"Commercial 5",  "City":"City B","Type":"Commercial",  "Units":45,"Occupied":40,"Rent_Per_Unit":1_300_000,"Collected":44_200_000,"Arrears_Total":7_800_000,"Arrears_Days":85, "Maintenance_Cost":2_100_000},
    {"Property":"Mixed Use 1",   "City":"City B","Type":"Mixed",       "Units":28,"Occupied":25,"Rent_Per_Unit":750_000,  "Collected":16_500_000,"Arrears_Total":2_250_000,"Arrears_Days":35, "Maintenance_Cost":  880_000},
    {"Property":"Residential 5", "City":"City C","Type":"Residential", "Units":22,"Occupied":18,"Rent_Per_Unit":600_000,  "Collected": 9_000_000,"Arrears_Total":3_600_000,"Arrears_Days":90, "Maintenance_Cost":  620_000},
    {"Property":"Industrial 2",  "City":"City C","Type":"Industrial",  "Units":16,"Occupied":11,"Rent_Per_Unit":1_050_000,"Collected": 8_400_000,"Arrears_Total":6_300_000,"Arrears_Days":150,"Maintenance_Cost":1_050_000},
    {"Property":"Commercial 6",  "City":"City C","Type":"Commercial",  "Units":20,"Occupied":15,"Rent_Per_Unit":700_000,  "Collected": 7_350_000,"Arrears_Total":4_200_000,"Arrears_Days":110,"Maintenance_Cost":  750_000},
])

months = ["Jan","Feb","Mar","Apr","May","Jun"]
occ_trend = pd.DataFrame({
    "Month": months * 3,
    "City":  ["City A"]*6 + ["City B"]*6 + ["City C"]*6,
    "Occupancy": [71,73,74,75,76,76, 88,89,90,91,92,93, 65,64,63,62,61,60],
})


# ── CALCULATIONS ──
properties["Monthly_Billed"]    = properties["Occupied"] * properties["Rent_Per_Unit"]
properties["Revenue_Leakage"]   = properties["Monthly_Billed"] - properties["Collected"]
properties["Collection_Rate"]   = (properties["Collected"] / properties["Monthly_Billed"] * 100).round(1)
properties["Occupancy_Rate"]    = (properties["Occupied"]  / properties["Units"]           * 100).round(1)
properties["Maintenance_Ratio"] = (properties["Maintenance_Cost"] / properties["Monthly_Billed"] * 100).round(1)

def age_bucket(d):
    if d <= 30:    return "0-30 days"
    elif d <= 60:  return "31-60 days"
    elif d <= 90:  return "61-90 days"
    elif d <= 180: return "91-180 days"
    else:          return "180+ days"

properties["Arrears_Bucket"] = properties["Arrears_Days"].apply(age_bucket)

max_d = properties["Arrears_Days"].max()
max_m = properties["Maintenance_Ratio"].max()
properties["Health_Score"] = (
    (properties["Collection_Rate"] / 100 * 50) +
    (properties["Occupancy_Rate"]  / 100 * 30) +
    ((1 - properties["Arrears_Days"]      / max_d) * 10) +
    ((1 - properties["Maintenance_Ratio"] / max_m) * 10)
).round(1)
properties["Health_Label"] = properties["Health_Score"].apply(
    lambda s: "Healthy" if s >= 78 else ("Moderate" if s >= 62 else "At Risk")
)
props_sorted = properties.sort_values("Health_Score", ascending=False).reset_index(drop=True)

city_sum = properties.groupby("City").agg(
    Total_Billed=("Monthly_Billed","sum"),
    Total_Collected=("Collected","sum"),
    Total_Leakage=("Revenue_Leakage","sum"),
    Total_Arrears=("Arrears_Total","sum"),
    Avg_Occupancy=("Occupancy_Rate","mean"),
    Avg_Collection=("Collection_Rate","mean"),
).reset_index().sort_values("Total_Collected", ascending=False)

print(f"\n   {len(properties)} properties across {properties['City'].nunique()} cities")


# ── PAGE 1 ──
BLUE   = "#1f4e79"; LBLUE="#2e75b6"; GREEN="#70ad47"
ORANGE = "#ed7d31"; RED  ="#c00000"; GOLD ="#ffc000"
HCOLS  = {"Healthy":GREEN,"Moderate":GOLD,"At Risk":RED}
CCOLS  = {"City B":BLUE,"City A":LBLUE,"City C":ORANGE}

fig1, axes = plt.subplots(1, 3, figsize=(20, 8))
fig1.suptitle(
    "Property Portfolio — Health Scoring, Revenue Leakage and Arrears Aging\n"
    "Analyst: Opemipo Daniel Owolabi  |  Reporting Period: June 2022",
    fontsize=13, fontweight="bold", y=1.02
)

ax1 = axes[0]
bar_cols = [HCOLS[h] for h in props_sorted["Health_Label"]]
bars = ax1.barh(props_sorted["Property"], props_sorted["Health_Score"],
                color=bar_cols, edgecolor="white")
ax1.axvline(x=78, color=GREEN, linestyle="--", linewidth=1.2, alpha=0.7)
ax1.axvline(x=62, color=GOLD,  linestyle="--", linewidth=1.2, alpha=0.7)
for bar, sc in zip(bars, props_sorted["Health_Score"]):
    ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f"{sc}", va="center", fontsize=8.5, fontweight="bold")
ax1.set_title("Portfolio Health Score\n(ranked best to worst)", fontweight="bold", fontsize=11)
ax1.set_xlabel("Health Score (0-100)")
ax1.invert_yaxis()
ax1.legend(handles=[mpatches.Patch(color=c, label=l) for l,c in HCOLS.items()], fontsize=8, loc="lower right")

ax2 = axes[1]
top_leak  = properties.sort_values("Revenue_Leakage", ascending=False).head(10)
lk_cols   = [CCOLS.get(c,"#999") for c in top_leak["City"]]
bars2 = ax2.barh(top_leak["Property"], top_leak["Revenue_Leakage"]/1e6, color=lk_cols, edgecolor="white")
for bar, val in zip(bars2, top_leak["Revenue_Leakage"]):
    ax2.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
             f"N{val/1e6:.1f}M", va="center", fontsize=8.5)
ax2.set_title("Revenue Leakage — Top 10\n(billed but not collected)", fontweight="bold", fontsize=11)
ax2.set_xlabel("Leakage (N Millions)")
ax2.xaxis.set_major_formatter(mticker.FormatStrFormatter("N%.1fM"))
ax2.invert_yaxis()
ax2.legend(handles=[mpatches.Patch(color=c, label=l) for l,c in CCOLS.items()], fontsize=8)

ax3 = axes[2]
buckets = ["0-30 days","31-60 days","61-90 days","91-180 days","180+ days"]
bcols   = [GREEN,GOLD,ORANGE,RED,"#7b0000"]
aging   = properties.groupby("Arrears_Bucket")["Arrears_Total"].sum().reindex(buckets).fillna(0)
bars3 = ax3.bar(aging.index, aging.values/1e6, color=bcols, edgecolor="white", width=0.6)
for bar, val in zip(bars3, aging.values):
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
             f"N{val/1e6:.1f}M", ha="center", fontsize=8.5, fontweight="bold")
ax3.set_title("Arrears Aging Analysis\n(total arrears by age bucket)", fontweight="bold", fontsize=11)
ax3.set_ylabel("Total Arrears (N Millions)")
ax3.yaxis.set_major_formatter(mticker.FormatStrFormatter("N%.0fM"))
ax3.set_xticklabels(aging.index, rotation=20, ha="right", fontsize=9)

plt.tight_layout()
plt.savefig("/home/claude/clean/project4/portfolio_dashboard_page1.png", dpi=150, bbox_inches="tight")
plt.close()


# ── PAGE 2 ──
fig2, axes2 = plt.subplots(1, 2, figsize=(16, 7))
fig2.suptitle(
    "Property Portfolio — Occupancy Trends and Regional Performance\n"
    "Analyst: Opemipo Daniel Owolabi  |  Jan to Jun 2022",
    fontsize=13, fontweight="bold", y=1.02
)

ax4 = axes2[0]
for city, col in CCOLS.items():
    d = occ_trend[occ_trend["City"] == city]
    ax4.plot(d["Month"], d["Occupancy"], marker="o", linewidth=2.5, markersize=7, color=col, label=city)
    ax4.fill_between(d["Month"], d["Occupancy"], alpha=0.08, color=col)
    ax4.annotate(f"{d['Occupancy'].iloc[-1]}%",
                 (d["Month"].iloc[-1], d["Occupancy"].iloc[-1]),
                 xytext=(5,0), textcoords="offset points", fontsize=9, fontweight="bold", color=col)
ax4.axhline(y=85, color=GREEN, linestyle="--", linewidth=1.2, alpha=0.6, label="85% Target")
ax4.set_title("Occupancy Rate Trend — Jan to Jun 2022", fontweight="bold", fontsize=11)
ax4.set_ylabel("Occupancy Rate (%)")
ax4.set_ylim(50, 100)
ax4.legend(fontsize=9)

ax5 = axes2[1]
x     = np.arange(len(city_sum))
width = 0.3
ax5.bar(x-width, city_sum["Total_Billed"]    /1e6, width, label="Billed",    color=LBLUE, alpha=0.9)
ax5.bar(x,       city_sum["Total_Collected"] /1e6, width, label="Collected", color=GREEN, alpha=0.9)
ax5.bar(x+width, city_sum["Total_Arrears"]   /1e6, width, label="Arrears",   color=RED,   alpha=0.9)
ax5.set_xticks(x)
ax5.set_xticklabels(city_sum["City"], fontsize=10)
ax5.set_title("Regional Performance — Billed vs Collected vs Arrears", fontweight="bold", fontsize=11)
ax5.set_ylabel("Amount (N Millions)")
ax5.yaxis.set_major_formatter(mticker.FormatStrFormatter("N%.0fM"))
ax5.legend(fontsize=9)
for i,(_, row) in enumerate(city_sum.iterrows()):
    ax5.text(i, -8, f"Occ: {row['Avg_Occupancy']:.0f}%\nCol: {row['Avg_Collection']:.0f}%",
             ha="center", fontsize=8, color=BLUE, fontweight="bold")

plt.tight_layout()
plt.savefig("/home/claude/clean/project4/portfolio_dashboard_page2.png", dpi=150, bbox_inches="tight")
plt.close()

tb = properties["Monthly_Billed"].sum()
tc = properties["Collected"].sum()
tl = properties["Revenue_Leakage"].sum()
ta = properties["Arrears_Total"].sum()

print(f"\n  Total Properties:    {len(properties)}")
print(f"  Monthly Billed:      N{tb/1e6:.1f}M")
print(f"  Monthly Collected:   N{tc/1e6:.1f}M")
print(f"  Collection Rate:     {tc/tb*100:.1f}%")
print(f"  Revenue Leakage:     N{tl/1e6:.1f}M")
print(f"  Total Arrears:       N{ta/1e6:.1f}M")
print(f"  At Risk Properties:  {len(properties[properties['Health_Label']=='At Risk'])}")
print("\n  Dashboards saved.")
print("=" * 60)

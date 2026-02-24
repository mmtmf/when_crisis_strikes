import os
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# ============================================================
# Style: grayscale-friendly + Times New Roman (single-column)
# ============================================================
mpl.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
})

SINGLE_COL_IN = 3.35  # ~85mm

# ============================================================
# Paths (EDIT THESE)
# ============================================================
DATA_PATH = r"C:\Users\au546005\OneDrive - Aarhus universitet\Documents\PhD\when_crisis_strikes_project\data\Kodeark_3.xlsm"
RESULTS_DIR = r"C:\Users\au546005\OneDrive - Aarhus universitet\Documents\PhD\when_crisis_strikes_project\results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def out(name: str, ext: str = "png") -> str:
    return os.path.join(RESULTS_DIR, f"{name}.{ext}")

# ============================================================
# English display labels (Danish -> English) used in ALL figures
# ============================================================
LABELS_EN = {
    # Affect
    "Frygt": "Fear",
    "Sårbarhed": "Vulnerability",
    "Sorg": "Grief",
    "Savn": "Longing",
    "Bebrejdelse": "Blame",
    "Splittelse": "Division",
    "Trøst": "Consolation",

    # Exhortation / social-ethical
    "Modstandskraft (resiliens)": "Resilience",
    "Sammenhængskraft": "Social cohesion",
    "Opdragelse": "Moral formation",
    "Forsoning": "Reconciliation",

    # Identity repertoire
    "Kirke": "The Church",
    "Nationen": "Nation",
    "Militær": "Military",
    "Kongehus": "Monarchy",
    "Lokalmiljø": "Local community",
    '"Globalmiljø"': "Global community",

    # Text centrality
    "Tekst i centrum": "Text central",
    "Tekst i periferi": "Text peripheral",

    # Theology
    "Teodicé-problematik": "Theodicy",
    "Synd": "Sin",
    "Frelse": "Salvation",
    "Tro": "Faith",
    "Vantro": "Unbelief",
    "Vantro/manglende tro": "Unbelief",
    "Korsfæstelse/offer/opstandelse": "Christ-event",
    "Kærlighed": "Love",
    "Næstekærlighed": "Neighbour-love",

    # If present in sheet
    "Tilstand": "State/condition",

    # Enemy / solidarity repertoire
    "Ekstern modstander": "External enemy",
    "Samfundsmæssig transformation": "Societal transformation",
}

def lab(code: str) -> str:
    return LABELS_EN.get(code, code)

# ============================================================
# Helpers
# ============================================================
def normalize_code(s: str) -> str:
    return str(s).strip()

def assert_codes_exist(tidy: pd.DataFrame, codes: list[str]) -> None:
    have = set(tidy["code"].dropna().unique())
    missing = [c for c in codes if c not in have]
    if missing:
        raise ValueError(
            "Missing codes in tidy['code']:\n"
            f"{missing}\n\n"
            "Tip: print(sorted(tidy['code'].unique())) to inspect available labels."
        )

# ============================================================
# Load + Tidy from Excel ('Udregninger 2')
# ============================================================
def load_tidy_from_udregninger2(xlsm_path: str, sheet: str = "Udregninger 2") -> pd.DataFrame:
    raw = pd.read_excel(xlsm_path, sheet_name=sheet, header=None)

    # Data rows begin at row index 4 (row 3 contains headers)
    data = raw.iloc[4:].copy()
    data = data.rename(columns={0: "code"})
    data["code"] = data["code"].map(normalize_code)
    data = data[~data["code"].str.lower().isin(["nan", ""])]
    data = data.reset_index(drop=True)

    blocks = [
        {"crisis": "Schleswigian Wars", "w": 89.0,  "col_named_n": 1,  "col_named_p": 2,  "col_base_n": 3,  "col_base_p": 4,  "col_rd": 5},
        {"crisis": "Occupation",        "w": 103.0, "col_named_n": 25, "col_named_p": 26, "col_base_n": 27, "col_base_p": 28, "col_rd": 29},
        {"crisis": "COVID-19",          "w": 103.0, "col_named_n": 49, "col_named_p": 50, "col_base_n": 51, "col_base_p": 52, "col_rd": 53},
    ]

    tidy_parts = []
    for b in blocks:
        tmp = pd.DataFrame({
            "code": data["code"],
            "crisis": b["crisis"],
            "n_crisis_code": pd.to_numeric(data[b["col_named_n"]], errors="coerce"),
            "p_crisis": pd.to_numeric(data[b["col_named_p"]], errors="coerce"),
            "n_base_code": pd.to_numeric(data[b["col_base_n"]], errors="coerce"),
            "p_base": pd.to_numeric(data[b["col_base_p"]], errors="coerce"),
            "rd": pd.to_numeric(data[b["col_rd"]], errors="coerce"),
        })
        tmp["delta_pp"] = (tmp["p_crisis"] - tmp["p_base"]) * 100.0
        tidy_parts.append(tmp)

    tidy = pd.concat(tidy_parts, ignore_index=True)

    # ----------------------------
    # Pooled corpus (vectorized weighted means; no groupby.apply)
    # ----------------------------
    crisis_weights = {b["crisis"]: b["w"] for b in blocks}

    tmpw = tidy.copy()
    tmpw["w"] = tmpw["crisis"].map(crisis_weights).astype(float)

    tmpw["p_crisis_w"] = tmpw["p_crisis"] * tmpw["w"]
    tmpw["p_base_w"] = tmpw["p_base"] * tmpw["w"]

    pooled = tmpw.groupby("code", as_index=False).agg(
        w=("w", "sum"),
        p_crisis_w=("p_crisis_w", "sum"),
        p_base_w=("p_base_w", "sum"),
    )

    pooled["p_crisis"] = pooled["p_crisis_w"] / pooled["w"]
    pooled["p_base"] = pooled["p_base_w"] / pooled["w"]
    pooled["crisis"] = "Pooled"
    pooled["delta_pp"] = (pooled["p_crisis"] - pooled["p_base"]) * 100.0
    pooled = pooled[["code", "crisis", "p_crisis", "p_base", "delta_pp"]]

    tidy = pd.concat([tidy, pooled], ignore_index=True)
    tidy["code"] = tidy["code"].map(normalize_code)
    return tidy

# ============================================================
# Figure A: Small-multiples delta bars (pp)
# ============================================================
def plot_small_multiples_delta_bars(
    tidy: pd.DataFrame,
    codes: list[str],
    crises=("Schleswigian Wars", "Occupation", "COVID-19", "Pooled"),
    outpath=out("fig_A_delta_small_multiples", "png"),
):
    assert_codes_exist(tidy, codes)
    df = tidy[tidy["code"].isin(codes) & tidy["crisis"].isin(crises)].copy()
    df["code"] = pd.Categorical(df["code"], categories=codes[::-1], ordered=True)

    n_panels = len(crises)
    fig_h = 1.35 * n_panels
    fig, axes = plt.subplots(n_panels, 1, figsize=(SINGLE_COL_IN, fig_h), sharex=True)
    if n_panels == 1:
        axes = [axes]

    for ax, crisis in zip(axes, crises):
        sub = df[df["crisis"] == crisis].sort_values("code")
        ax.axvline(0, linewidth=0.8)

        ylabels = [lab(c) for c in sub["code"]]
        ax.barh(ylabels, sub["delta_pp"], color="0.75", edgecolor="black", linewidth=0.6)

        for ylab, val in zip(ylabels, sub["delta_pp"]):
            if pd.isna(val):
                continue
            ha = "left" if val >= 0 else "right"
            x = val + (1.0 if val >= 0 else -1.0)
            ax.text(x, ylab, f"{val:.1f} pp", va="center", ha=ha)

        ax.set_title(crisis, loc="left", fontsize=10, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(False)

    axes[-1].set_xlabel("Δ percentage points\n(crisis-explicit − baseline)")
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.10)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)

# ============================================================
# Figure B: Paired delta bars (affect vs exhortation)
# ============================================================
def plot_delta_bars_hinge(
    tidy: pd.DataFrame,
    affect_codes=("Frygt", "Sårbarhed"),
    exhort_codes=("Modstandskraft (resiliens)", "Sammenhængskraft"),
    crises=("Schleswigian Wars", "Occupation", "COVID-19", "Pooled"),
    outpath=out("fig_B_delta_hinge", "png"),
):
    codes = list(affect_codes) + list(exhort_codes)
    assert_codes_exist(tidy, codes)

    df = tidy[tidy["code"].isin(codes) & tidy["crisis"].isin(crises)].copy()

    ordered = list(affect_codes) + list(exhort_codes)
    df["code"] = pd.Categorical(df["code"], categories=ordered[::-1], ordered=True)

    xmax = float(np.nanmax(df["delta_pp"].values))
    xmin = float(np.nanmin(df["delta_pp"].values))
    pad = max(2.0, 0.08 * (xmax - xmin))
    xlim = (min(0.0, xmin - pad), xmax + pad)

    n_panels = len(crises)
    fig_h = 1.15 * n_panels
    fig, axes = plt.subplots(n_panels, 1, figsize=(SINGLE_COL_IN, fig_h), sharex=True)
    if n_panels == 1:
        axes = [axes]

    for ax, crisis in zip(axes, crises):
        sub = df[df["crisis"] == crisis].sort_values("code")

        ax.axvline(0, linewidth=0.8)

        sub_aff = sub[sub["code"].isin(list(affect_codes))]
        sub_exh = sub[sub["code"].isin(list(exhort_codes))]

        ax.barh(
            [lab(c) for c in sub_aff["code"]],
            sub_aff["delta_pp"],
            color="0.75",
            edgecolor="black",
            linewidth=0.6,
        )

        bars = ax.barh(
            [lab(c) for c in sub_exh["code"]],
            sub_exh["delta_pp"],
            color="white",
            edgecolor="black",
            linewidth=0.6,
        )
        for b in bars:
            b.set_hatch("//")

        for code, val in zip(sub["code"], sub["delta_pp"]):
            if pd.isna(val):
                continue
            ylab = lab(code)
            ha = "left" if val >= 0 else "right"
            x = val + (0.8 if val >= 0 else -0.8)
            ax.text(x, ylab, f"{val:.1f} pp", va="center", ha=ha)

        ax.axhline(1.5, color="black", linewidth=0.4)

        ax.set_title(crisis, loc="left", fontsize=9, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(False)
        ax.set_xlim(*xlim)

    axes[-1].set_xlabel("Δ percentage points (crisis-explicit − baseline)")
    plt.tight_layout()
    fig.subplots_adjust(bottom=0.10)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)


# ============================================================
# Figure C: Identity repertoire deltas
# ============================================================
def plot_fig_C_identity_frame_deltas(
    tidy: pd.DataFrame,
    codes: list[str],
    crises=("Schleswigian Wars", "Occupation", "COVID-19", "Pooled"),
    outpath=out("fig_C_identity_frame_deltas", "png"),
):
    assert_codes_exist(tidy, codes)

    df = tidy[tidy["code"].isin(codes) & tidy["crisis"].isin(crises)].copy()
    df["code"] = pd.Categorical(df["code"], categories=codes[::-1], ordered=True)

    xmax = float(np.nanmax(df["delta_pp"].values))
    xmin = float(np.nanmin(df["delta_pp"].values))
    pad = max(2.0, 0.08 * (xmax - xmin))
    xlim = (min(0.0, xmin - pad), xmax + pad)

    n_panels = len(crises)
    fig_h = 1.15 * n_panels
    fig, axes = plt.subplots(n_panels, 1, figsize=(SINGLE_COL_IN, fig_h), sharex=True)
    if n_panels == 1:
        axes = [axes]

    for ax, crisis in zip(axes, crises):
        sub = df[df["crisis"] == crisis].sort_values("code")
        ax.axvline(0, linewidth=0.9, color="black")

        ylabels = [lab(c) for c in sub["code"]]
        ax.barh(ylabels, sub["delta_pp"], color="0.75", edgecolor="black", linewidth=0.6)

        ax.set_xlim(*xlim)
        xmin_ax, xmax_ax = ax.get_xlim()
        xr = xmax_ax - xmin_ax

        # Numeric labels: show positives; skip near-zero and negatives (keeps it clean)
        for ylab, val in zip(ylabels, sub["delta_pp"]):
            if pd.isna(val) or abs(val) < 0.05:
                continue
            if val < 0:
                continue
            x = val + 0.02 * xr
            ax.text(x, ylab, f"{val:.1f} pp", va="center", ha="left")

        ax.set_title(crisis, loc="left", fontsize=9, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_linewidth(0.8)
        ax.spines["bottom"].set_linewidth(0.8)
        ax.tick_params(axis="both", width=0.8)
        ax.grid(False)

    axes[-1].set_xlabel("Δ percentage points\n(crisis-explicit − baseline)")
    plt.tight_layout()
    fig.subplots_adjust(left=0.40, bottom=0.12)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)

# ============================================================
# Figure D: Enemy vs civic-minded solidarity
# ============================================================
def plot_fig_D_enemy_vs_civic_deltas(
    tidy: pd.DataFrame,
    codes: list[str],
    crises=("Schleswigian Wars", "Occupation", "COVID-19"),
    outpath=out("fig_D_enemy_vs_civic_deltas", "png"),
):
    assert_codes_exist(tidy, codes)

    df = tidy[tidy["code"].isin(codes) & tidy["crisis"].isin(crises)].copy()
    df["code"] = pd.Categorical(df["code"], categories=codes[::-1], ordered=True)

    xmax = float(np.nanmax(df["delta_pp"].values))
    xmin = float(np.nanmin(df["delta_pp"].values))
    pad = max(2.0, 0.08 * (xmax - xmin))
    xlim = (min(0.0, xmin - pad), xmax + pad)

    n_panels = len(crises)
    fig_h = 1.15 * n_panels
    fig, axes = plt.subplots(n_panels, 1, figsize=(SINGLE_COL_IN, fig_h), sharex=True)
    if n_panels == 1:
        axes = [axes]

    for ax, crisis in zip(axes, crises):
        sub = df[df["crisis"] == crisis].sort_values("code")
        ax.axvline(0, linewidth=0.9, color="black")

        ylabels = [lab(c) for c in sub["code"]]
        ax.barh(ylabels, sub["delta_pp"], color="0.75", edgecolor="black", linewidth=0.6)

        ax.set_xlim(*xlim)
        xmin_ax, xmax_ax = ax.get_xlim()
        xr = xmax_ax - xmin_ax

        for ylab, val in zip(ylabels, sub["delta_pp"]):
            if pd.isna(val) or abs(val) < 0.05:
                continue
            if val < 0:
                continue
            x = val + 0.02 * xr
            ax.text(x, ylab, f"{val:.1f} pp", va="center", ha="left")

        ax.set_title(crisis, loc="left", fontsize=9, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_linewidth(0.8)
        ax.spines["bottom"].set_linewidth(0.8)
        ax.tick_params(axis="both", width=0.8)
        ax.grid(False)

    axes[-1].set_xlabel("Δ percentage points\n(crisis-explicit − baseline)")
    plt.tight_layout()
    fig.subplots_adjust(left=0.40, bottom=0.12)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)

# ============================================================
# Figure E: Pooled theology reweighting (selected motifs)
# Delta bars (pp), includes BOTH positive + negative value labels
# ============================================================

def plot_fig_E_pooled_theology_reweighting_profile(
    tidy: pd.DataFrame,
    codes: list[str],
    crisis: str = "Pooled",
    outpath: str = out("fig_E_pooled_theology_reweighting_profile", "png"),
):
    """
    Figure E: Pooled theology reweighting (selected motifs), Δpp bars.

    Implements:
      1) Fixed x-axis to [-20, +20]
      2) Separator between Text central and Text peripheral (robust to ordering)
      3) Plot reads "top-down" with Theodicy-group visually at the top
         (done by inverting the y-axis; no need to reorder codes)
    """

    assert_codes_exist(tidy, codes)

    df = tidy[(tidy["crisis"] == crisis) & (tidy["code"].isin(codes))].copy()
    if df.empty:
        raise ValueError(f"No rows found for crisis='{crisis}' and selected codes.")

    # Preserve the user-provided order for grouping logic,
    # but we'll invert the y-axis to make it read top-down.
    df["code"] = pd.Categorical(df["code"], categories=codes, ordered=True)
    df = df.sort_values("code")

    ylabels = [lab(c) for c in df["code"]]
    vals = df["delta_pp"].astype(float).values
    codes_in_plot = list(df["code"].values)

    fig, ax = plt.subplots(figsize=(SINGLE_COL_IN, 4.2))

    # Zero line
    ax.axvline(0, color="black", linewidth=0.9, zorder=1)

    # Bars
    ax.barh(
        ylabels,
        vals,
        color="0.75",
        edgecolor="black",
        linewidth=0.6,
        zorder=2,
    )

    # (1) Fixed x-axis
    ax.set_xlim(-20, 20)

    # (2) Separator between Text central and Text peripheral (wherever they are)
    code_central = "Tekst i centrum"
    code_periph = "Tekst i periferi"
    if (code_central in codes_in_plot) and (code_periph in codes_in_plot):
        i_c = codes_in_plot.index(code_central)
        i_p = codes_in_plot.index(code_periph)
        y_sep = (i_c + i_p) / 2.0  # halfway between the two rows
        ax.axhline(y_sep, color="0.55", linewidth=0.4, zorder=1)

    # Value labels (include negatives)
    xmin_ax, xmax_ax = ax.get_xlim()
    xr = xmax_ax - xmin_ax
    off = 0.02 * xr

    for i, val in enumerate(vals):
        if np.isnan(val):
            continue
        txt = f"{val:.1f} pp"
        if val >= 0:
            x, ha = val + off, "left"
        else:
            x, ha = val - off, "right"
        ax.text(x, i, txt, va="center", ha=ha, zorder=3)

    # Titles/labels
    ax.set_title("Pooled crisis effect on motifs and text-use (Δpp)", loc="left")
    ax.set_xlabel("Δ percentage points (crisis-explicit − baseline)")

    # Style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.8)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.tick_params(axis="both", width=0.8)
    ax.grid(False)

    # (3) Make it read top-down: first item appears at the top
    ax.invert_yaxis()

    plt.tight_layout()
    fig.subplots_adjust(left=0.30)
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)


# ============================================================
# RUN
# ============================================================

# ---- LOAD DATA (the load-data line)
tidy = load_tidy_from_udregninger2(DATA_PATH)

# Uncomment to inspect available labels if you hit a missing-code error:
# print(sorted(tidy["code"].unique()))

# ---- FIGURE A
codes_A = ["Tilstand", "Frygt", "Sårbarhed"]
codes_A = [c for c in codes_A if c in set(tidy["code"].unique())]
if codes_A:
    plot_small_multiples_delta_bars(tidy, codes=codes_A, outpath=out("fig_A_delta_small_multiples", "png"))

# ---- FIGURE B
plot_delta_bars_hinge(
    tidy,
    affect_codes=("Frygt", "Sårbarhed"),
    exhort_codes=("Modstandskraft (resiliens)", "Sammenhængskraft"),
    outpath=out("fig_B_delta_hinge", "png"),
)

# ---- FIGURE C (identity frames activated)
codes_C = ["Nationen", "Militær", "Kongehus", "Kirke",]
codes_C = [c for c in codes_C if c in set(tidy["code"].unique())]
if codes_C:
    plot_fig_C_identity_frame_deltas(
        tidy,
        codes=codes_C,
        crises=("Schleswigian Wars", "Occupation", "COVID-19", "Pooled"),
        outpath=out("fig_C_identity_frame_deltas", "png"),
    )

# ---- FIGURE D (enemy vs civic-minded solidarity)
codes_D = ["Ekstern modstander", "Samfundsmæssig transformation", "Trøst", "Savn"]
codes_D = [c for c in codes_D if c in set(tidy["code"].unique())]
if codes_D:
    plot_fig_D_enemy_vs_civic_deltas(
        tidy,
        codes=codes_D,
        crises=("Schleswigian Wars", "Occupation", "COVID-19"),
        outpath=out("fig_D_enemy_vs_civic_deltas", "png"),
    )

# ---- RUN Figure E (example)
# Keep the order as you want it to appear top -> bottom.
codes_E = [
    "Teodicé-problematik",
    "Kærlighed",
    "Næstekærlighed",
    "Tekst i periferi",
    "Tekst i centrum",
    "Synd",
    "Korsfæstelse/offer/opstandelse",
    "Frelse",
    "Tro",
    "Vantro/manglende tro",
]
codes_E = [c for c in codes_E if c in set(tidy["code"].unique())]

if codes_E:
    plot_fig_E_pooled_theology_reweighting_profile(
        tidy,
        codes=codes_E,
        crisis="Pooled",
        outpath=out("fig_E_pooled_theology_reweighting_profile", "png"),
    )


# ---- FIGURE J
plot_text_centrality_100pct(
    tidy,
    outpath=out("fig_J_text_centrality_100pct", "png"),
)

print(f"Saved figures to: {RESULTS_DIR}")

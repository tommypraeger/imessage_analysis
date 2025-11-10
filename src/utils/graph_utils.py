import os
import glob
import math
from datetime import datetime
from typing import Iterable, List, Tuple, Optional, Dict

import numpy as np
import matplotlib

# Use non-interactive backend suitable for servers/CLI
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patheffects as path_effects  # noqa: E402


IMAGES_DIR = os.path.join("images")


def _ensure_images_dir() -> None:
    os.makedirs(IMAGES_DIR, exist_ok=True)


def _cleanup_previous_images() -> None:
    pattern = os.path.join(IMAGES_DIR, "*.png")
    for path in glob.glob(pattern):
        try:
            print("removing old image:", path)
            os.remove(path)
        except OSError:
            # Best effort cleanup
            pass


def _fit_regression(xs: np.ndarray, ys: np.ndarray) -> Optional[Tuple[float, float, float]]:
    """
    Returns (slope, intercept, r_squared) if fit is possible, else None.
    """
    if xs.size < 2:
        return None
    try:
        slope, intercept = np.polyfit(xs, ys, 1)
        # Compute R^2
        y_pred = slope * xs + intercept
        ss_res = float(np.sum((ys - y_pred) ** 2))
        ss_tot = float(np.sum((ys - np.mean(ys)) ** 2))
        r2 = 0.0 if ss_tot == 0.0 else 1 - ss_res / ss_tot
        return slope, intercept, r2
    except Exception:
        return None


def _format_r2(r2: float) -> str:
    try:
        return f"R²={r2:.3f}"
    except Exception:
        return "R²=NA"


def generate_scatter_image(
    points: Iterable[Tuple[str, float, float]],
    *,
    x_label: str,
    y_label: str,
    title: str,
    subtitle: Optional[str] = None,
    slug: str,
    add_regression: bool = False,
    add_residuals: bool = False,
    x_percent: bool = False,
    y_percent: bool = False,
    add_quadrant_axes: bool = False,
    x_left_label: Optional[str] = None,
    x_right_label: Optional[str] = None,
    y_bottom_label: Optional[str] = None,
    y_top_label: Optional[str] = None,
    footer_text: Optional[str] = None,
    add_identity_line: bool = False,
    residuals_to_identity: bool = False,
) -> Dict[str, str]:
    """
    Generate a scatter image under ui/public/analysis and return {imagePath, title, subtitle}.

    - points: iterable of (label, x, y) for each member/entity
    - slug: filename/stem for cleanup and saving (e.g., "lfwt")
    - add_regression: overlay best-fit line and append R² to subtitle
    - add_residuals: include residuals subplot below the main chart
    """
    _ensure_images_dir()
    _cleanup_previous_images()

    labels: List[str] = []
    xs_list: List[float] = []
    ys_list: List[float] = []
    for name, x, y in points:
        if x is None or y is None:
            continue
        if isinstance(x, float) and (math.isinf(x) or math.isnan(x)):
            continue
        if isinstance(y, float) and (math.isinf(y) or math.isnan(y)):
            continue
        labels.append(str(name))
        xs_list.append(float(x))
        ys_list.append(float(y))

    xs = np.array(xs_list, dtype=float)
    ys = np.array(ys_list, dtype=float)

    # Single-axes layout; residuals (if any) are drawn on the main plot
    fig, ax_main = plt.subplots(1, 1, figsize=(8, 6))

    # Main scatter plot
    ax_main.scatter(xs, ys, c="#1f78b4", alpha=0.85, edgecolors="white", linewidths=0.5)
    # Create text labels with a small offset; keep simple and predictable
    for i, name in enumerate(labels):
        t = ax_main.annotate(
            name,
            (xs[i], ys[i]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=9,
            color="#111111",
        )
        t.set_path_effects([
            path_effects.withStroke(linewidth=2, foreground="white", alpha=0.85)
        ])
    ax_main.set_xlabel(x_label)
    ax_main.set_ylabel(y_label)
    fig.suptitle(title, y=0.88, fontsize=14, fontweight="bold")
    ax_main.grid(True, linestyle=":", alpha=0.4)

    # Optional percentage tick formatting
    if x_percent:
        from matplotlib.ticker import FuncFormatter

        ax_main.xaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:.0f}%"))
    if y_percent:
        from matplotlib.ticker import FuncFormatter

        ax_main.yaxis.set_major_formatter(FuncFormatter(lambda v, pos: f"{v:.0f}%"))

    # Regression line and residuals
    subtitle_text = subtitle
    if add_regression and xs.size >= 2:
        fit = _fit_regression(xs, ys)
        if fit is not None:
            slope, intercept, r2 = fit
            # Line across data range
            x_min, x_max = float(xs.min()), float(xs.max())
            xr = np.array([x_min, x_max], dtype=float)
            yr = slope * xr + intercept
            ax_main.plot(xr, yr, color="#e31a1c", linewidth=1.5, label="Best fit")
            ax_main.legend()

            # Append R^2 to subtitle if present
            r2_text = _format_r2(r2)
            if subtitle_text:
                subtitle_text = f"{subtitle_text} ({r2_text})"
            else:
                subtitle_text = r2_text
            # Optional residuals as vertical dotted lines on main plot
            if add_residuals:
                y_pred = slope * xs + intercept
                for xi, yi, yhat in zip(xs, ys, y_pred):
                    # Vertical dotted line from predicted (on regression) to actual point
                    ax_main.plot([xi, xi], [yhat, yi], linestyle=":", color="#6b7280", linewidth=1.0, alpha=0.9)
                    # Show signed residual next to the line
                    resid_val = float(yi - yhat)
                    mid_y = (float(yi) + float(yhat)) / 2.0
                    _col = "#059669" if resid_val >= 0 else "#b91c1c"
                    ax_main.annotate(
                        f"{resid_val:+.2f}",
                        (xi, mid_y),
                        textcoords="offset points",
                        xytext=(2, 0),
                        va="center",
                        fontsize=8,
                        color=_col,
                    )

    # Optional y = x identity line (useful when both axes share units)
    if add_identity_line and xs.size >= 1:
        # Draw y = x only within the current view box without expanding limits
        x_min, x_max = ax_main.get_xlim()
        y_min, y_max = ax_main.get_ylim()
        lo = max(x_min, y_min)
        hi = min(x_max, y_max)
        if lo < hi:
            diag_x = np.array([lo, hi], dtype=float)
            ax_main.plot(diag_x, diag_x, color="#6b7280", linestyle="-.", linewidth=1.0, alpha=0.8, label="y = x")
            # Restore original limits to avoid autoscale widening
            ax_main.set_xlim(x_min, x_max)
            ax_main.set_ylim(y_min, y_max)
            # Only show legend if something else also provided a legend entry
            handles, labels = ax_main.get_legend_handles_labels()
            if handles and labels:
                ax_main.legend()

    # Residuals to identity (y = x): draw even if regression is not requested
    if residuals_to_identity and xs.size >= 1:
        for xi, yi in zip(xs, ys):
            yhat = xi  # identity baseline
            ax_main.plot([xi, xi], [yhat, yi], linestyle=":", color="#6b7280", linewidth=1.0, alpha=0.9)
            resid_val = float(yi - yhat)
            mid_y = (float(yi) + float(yhat)) / 2.0
            _col = "#059669" if resid_val >= 0 else "#b91c1c"
            ax_main.annotate(
                f"{resid_val:+.2f}",
                (xi, mid_y),
                textcoords="offset points",
                xytext=(2, 0),
                va="center",
                fontsize=8,
                color=_col,
            )

    # Render subtitle as axes title so it appears beneath the main figure title
    if subtitle_text:
        ax_main.set_title(subtitle_text, fontsize=10, color="#374151")

    # Optional quadrant axes drawn at midpoints with directional labels
    if add_quadrant_axes:
        # After initial draw, use current limits to place midlines
        x_min, x_max = ax_main.get_xlim()
        y_min, y_max = ax_main.get_ylim()
        x_mid = (x_min + x_max) / 2.0
        y_mid = (y_min + y_max) / 2.0
        ax_main.axvline(x_mid, color="#9ca3af", linestyle="--", linewidth=1.0, alpha=0.8)
        ax_main.axhline(y_mid, color="#9ca3af", linestyle="--", linewidth=1.0, alpha=0.8)
        # Use axes-fraction coords for labels so they hug the edges
        if x_left_label:
            ax_main.annotate(x_left_label, xy=(0.02, 0.52), xycoords="axes fraction", ha="left", va="center", fontsize=10, color="#374151")
        if x_right_label:
            ax_main.annotate(x_right_label, xy=(0.98, 0.52), xycoords="axes fraction", ha="right", va="center", fontsize=10, color="#374151")
        if y_top_label:
            ax_main.annotate(y_top_label, xy=(0.5, 0.98), xycoords="axes fraction", ha="center", va="top", fontsize=10, color="#374151")
        if y_bottom_label:
            ax_main.annotate(y_bottom_label, xy=(0.5, 0.02), xycoords="axes fraction", ha="center", va="bottom", fontsize=10, color="#374151")

    fig.tight_layout(rect=[0, 0, 1, 0.92])

    # Optional footer text (e.g., date range)
    if footer_text:
        # Bottom-right corner, slightly lower
        fig.text(0.995, 0.005, footer_text, ha="right", va="bottom", fontsize=9, color="#4b5563")

    # Save image
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{slug}-{ts}.png"
    filepath = os.path.join(IMAGES_DIR, filename)
    fig.savefig(filepath, dpi=160)
    plt.close(fig)

    return {
        "imagePath": f"/images/{filename}",
        "title": title,
        "subtitle": subtitle_text or "",
    }

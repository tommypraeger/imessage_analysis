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
    for i, name in enumerate(labels):
        ax_main.annotate(name, (xs[i], ys[i]), textcoords="offset points", xytext=(5, 5), fontsize=9, alpha=0.9)
    ax_main.set_xlabel(x_label)
    ax_main.set_ylabel(y_label)
    fig.suptitle(title, y=0.88, fontsize=14, fontweight="bold")
    ax_main.grid(True, linestyle=":", alpha=0.4)

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
                    # Show residual magnitude next to the line (absolute difference)
                    resid_mag = abs(float(yi - yhat))
                    mid_y = (float(yi) + float(yhat)) / 2.0
                    ax_main.annotate(
                        f"{resid_mag:.2f}",
                        (xi, mid_y),
                        textcoords="offset points",
                        xytext=(6, 0),
                        va="center",
                        fontsize=8,
                        color="#6b7280",
                    )

    # Render subtitle as axes title so it appears beneath the main figure title
    if subtitle_text:
        ax_main.set_title(subtitle_text, fontsize=10, color="#374151")

    fig.tight_layout(rect=[0, 0, 1, 0.92])

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

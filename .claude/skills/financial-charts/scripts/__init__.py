"""Financial charts module - chart generation utilities."""

from .themes import get_theme, get_palette, list_themes, list_palettes
from .sankey_chart import create_sankey_chart, create_income_statement_sankey
from .waterfall_chart import create_waterfall_chart, create_profit_walkdown, create_revenue_bridge
from .bar_chart import (
    create_bar_chart,
    create_grouped_bar_chart,
    create_margin_comparison_chart,
    create_revenue_segment_chart,
)
from .line_chart import (
    create_line_chart,
    create_multi_line_chart,
    create_trend_chart,
    create_margin_trend_chart,
)

__all__ = [
    "get_theme",
    "get_palette",
    "list_themes",
    "list_palettes",
    "create_sankey_chart",
    "create_income_statement_sankey",
    "create_waterfall_chart",
    "create_profit_walkdown",
    "create_revenue_bridge",
    "create_bar_chart",
    "create_grouped_bar_chart",
    "create_margin_comparison_chart",
    "create_revenue_segment_chart",
    "create_line_chart",
    "create_multi_line_chart",
    "create_trend_chart",
    "create_margin_trend_chart",
]

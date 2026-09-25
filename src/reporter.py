from tabulate import tabulate
from src.profiler import GLOBAL_REGISTRY
from typing import List, Dict, Any

class ReportGenerator:
    """تولید گزارش‌های تحلیلی عملکرد به فرمت جدول ترمینال و Markdown"""
    @staticmethod
    def get_aggregated_stats() -> List[Dict[str, Any]]:
        return [stats.summary() for stats in GLOBAL_REGISTRY.values()]

    @classmethod
    def generate_markdown_table(cls) -> str:
        stats = cls.get_aggregated_stats()
        if not stats:
            return "No profiling data captured."

        headers = ["Function", "Calls", "Mean (ms)", "P50 (ms)", "P95 (ms)", "P99 (ms)", "Peak RAM (KB)"]
        rows = [[s["function"], s["call_count"], s["mean_ms"], s["p50_ms"], s["p95_ms"], s["p99_ms"], s["avg_peak_memory_kb"]] for s in stats]
        return tabulate(rows, headers=headers, tablefmt="github")

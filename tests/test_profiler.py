import pytest
import asyncio
from src.profiler import async_trace, GLOBAL_REGISTRY
from src.reporter import ReportGenerator

@pytest.mark.asyncio
async def test_async_trace_decorator():
    """تست ثبت موفقیت‌آمیز تاخیر و حافظه توسط دکوراتور"""
    GLOBAL_REGISTRY.clear()

    @async_trace
    async def sample_task():
        await asyncio.sleep(0.01)
        return "completed"

    result = await sample_task()
    assert result == "completed"
    
    assert len(GLOBAL_REGISTRY) == 1
    stats = list(GLOBAL_REGISTRY.values())[0]
    summary = stats.summary()
    
    assert summary["call_count"] == 1
    assert summary["mean_ms"] >= 9.0  # باید حداقل ۱۰ میلی‌ثانیه باشد
    assert "avg_peak_memory_kb" in summary

@pytest.mark.asyncio
async def test_markdown_report_generation():
    """تست قالب خروجی گزارش مارک‌داون"""
    @async_trace
    async def quick_operation():
        return sum(range(100))

    await quick_operation()
    report = ReportGenerator.generate_markdown_table()
    assert "Function" in report
    assert "quick_operation" in report

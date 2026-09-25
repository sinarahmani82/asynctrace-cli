import time
import asyncio
import tracemalloc
import functools
import numpy as np
from typing import Callable, Any, Dict, List

class ProfilerStats:
    """کلاس نگهداری و محاسبه آمار تجمیعی تاخیر و حافظه"""
    def __init__(self, function_name: str):
        self.function_name = function_name
        self.latencies: List[float] = [] # به میلی‌ثانیه
        self.peak_memory_kb: List[float] = []

    def record(self, latency_ms: float, memory_kb: float):
        self.latencies.append(latency_ms)
        self.peak_memory_kb.append(memory_kb)

    def summary(self) -> Dict[str, Any]:
        arr = np.array(self.latencies)
        mem = np.array(self.peak_memory_kb)
        return {
            "function": self.function_name,
            "call_count": len(arr),
            "mean_ms": round(float(np.mean(arr)), 3),
            "p50_ms": round(float(np.percentile(arr, 50)), 3),
            "p95_ms": round(float(np.percentile(arr, 95)), 3),
            "p99_ms": round(float(np.percentile(arr, 99)), 3),
            "avg_peak_memory_kb": round(float(np.mean(mem)), 2)
        }

# مخزن نگهداری آمار تمام توابع پروفایل‌شده
GLOBAL_REGISTRY: Dict[str, ProfilerStats] = {}

def async_trace(func: Callable) -> Callable:
    """دکوراتور ناهمگام برای اندازه‌گیری تاخیر و مصرف رم توابع"""
    func_name = func.__qualname__
    if func_name not in GLOBAL_REGISTRY:
        GLOBAL_REGISTRY[func_name] = ProfilerStats(func_name)

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        tracemalloc.start()
        start_time = time.perf_counter()
        
        try:
            return await func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            GLOBAL_REGISTRY[func_name].record(elapsed_ms, peak / 1024.0)

    return wrapper

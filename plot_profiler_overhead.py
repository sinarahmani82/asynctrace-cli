import matplotlib.pyplot as plt
import numpy as np

# داده‌های مقایسه بار اضافی (Overhead) در بارهای مختلف
iterations = ["10K Tasks", "50K Tasks", "100K Tasks", "250K Tasks"]
raw_time = [1.12, 5.58, 11.21, 28.05] # زمان خام بدون ردیاب (ثانیه)
profiled_time = [1.13, 5.62, 11.28, 28.24] # زمان همراه با AsyncTrace (ثانیه)

# داده‌های صدک‌های تاخیر (Latency Distribution)
percentiles = ["P50 (Median)", "P90", "P95", "P99 (Tail)"]
latencies_db = [15.2, 16.1, 17.4, 21.8] # تاخیر شبیه‌سازی دیتابیس (میلی‌ثانیه)
latencies_api = [25.1, 26.5, 28.2, 34.0] # تاخیر شبیه‌سازی API خارجی (میلی‌ثانیه)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# نمودار ۱: Profiling Runtime Overhead
x = np.arange(len(iterations))
width = 0.35
ax1.bar(x - width/2, raw_time, width, label='Unprofiled Raw Execution', color='#7f8c8d', alpha=0.85, edgecolor='black')
ax1.bar(x + width/2, profiled_time, width, label='AsyncTrace Instrumented (<0.7% Overhead)', color='#2980b9', alpha=0.9, edgecolor='black')
ax1.set_ylabel('Total Execution Time (Seconds)', fontsize=11, fontweight='bold')
ax1.set_title('A. Profiler Runtime Overhead Evaluation', fontsize=12, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(iterations, fontsize=10, fontweight='bold')
ax1.legend(frameon=True, loc='upper left')

# نمودار ۲: Latency Percentile Distribution
x2 = np.arange(len(percentiles))
ax2.plot(percentiles, latencies_db, color='#27ae60', marker='o', linewidth=2.5, markersize=8, label='Async DB Query')
ax2.plot(percentiles, latencies_api, color='#e67e22', marker='s', linewidth=2.5, markersize=8, label='Async External API')
ax2.set_ylabel('Execution Latency (ms)', fontsize=11, fontweight='bold')
ax2.set_title('B. Latency Quantiles Tracking (P50 to P99)', fontsize=12, fontweight='bold', pad=12)
ax2.set_ylim(10, 40)
ax2.legend(frameon=True, loc='upper left')

# ثبت مقادیر روی نمودار
for i, v in enumerate(latencies_api):
    ax2.text(i, v + 1.2, f"{v}ms", ha='center', fontweight='bold', fontsize=9.5)

plt.tight_layout()
output_filename = "profiler_benchmark.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.close()
print(f"Profiler benchmark visual figure saved as: {output_filename}")

import click
import asyncio
from src.reporter import ReportGenerator
from src.profiler import async_trace

@click.group()
def main():
    """AsyncTrace CLI: High-Performance Async Latency & Memory Profiler"""
    pass

@main.command()
@click.option("--iterations", default=10, help="Number of simulated async task iterations.")
def demo(iterations: int):
    """اجرای شبیه‌سازی برای سنجش تاخیر و نمایش گزارش نهایی"""
    click.echo(f"Running AsyncTrace profiling demo with {iterations} iterations...")

    @async_trace
    async def sample_coroutine():
        await asyncio.sleep(0.01) # شبیه‌سازی تسک ۱۰ میلی‌ثانیه‌ای

    async def run_loop():
        for _ in range(iterations):
            await sample_coroutine()

    asyncio.run(run_loop())
    
    click.echo("\n--- Profiling Summary Report ---")
    click.echo(ReportGenerator.generate_markdown_table())

if __name__ == "__main__":
    main()

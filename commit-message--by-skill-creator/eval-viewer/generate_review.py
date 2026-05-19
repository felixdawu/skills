#!/usr/bin/env python3
"""
Commit Message Skill Eval Viewer Generator

Generates a standalone HTML file for reviewing commit message test results.

Usage:
    python generate_review.py <workspace_path> --skill-name <name> [--benchmark <benchmark.json>] [--static <output.html>]
"""

import json
import os
import sys
import argparse
import http.server
import webbrowser
import threading
from pathlib import Path
from datetime import datetime


def load_eval_data(workspace_path):
    """Load eval data from workspace directory."""
    results = []
    iteration_dir = Path(workspace_path)

    for eval_dir in sorted(iteration_dir.glob("eval-*")):
        eval_id = eval_dir.name
        metadata_path = eval_dir / "eval_metadata.json"

        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)
        else:
            metadata = {"eval_name": eval_id, "prompt": ""}

        # Load with_skill result
        with_skill_path = eval_dir / "with_skill" / "outputs" / "commit_message.txt"
        with_skill_msg = ""
        if with_skill_path.exists():
            with_skill_msg = with_skill_path.read_text()

        # Load without_skill result
        without_skill_path = eval_dir / "without_skill" / "outputs" / "commit_message.txt"
        without_skill_msg = ""
        if without_skill_path.exists():
            without_skill_msg = without_skill_path.read_text()

        # Load timing
        timing = {}
        for side in ["with_skill", "without_skill"]:
            timing_path = eval_dir / side / "timing.json"
            if timing_path.exists():
                with open(timing_path) as f:
                    timing[side] = json.load(f)

        results.append({
            "eval_id": eval_id,
            "eval_name": metadata.get("eval_name", eval_id),
            "prompt": metadata.get("prompt", ""),
            "with_skill": with_skill_msg,
            "without_skill": without_skill_msg,
            "timing": timing,
        })

    return results


def load_benchmark(benchmark_path):
    """Load benchmark data if available."""
    if benchmark_path and os.path.exists(benchmark_path):
        with open(benchmark_path) as f:
            return json.load(f)
    return None


def generate_html(results, benchmark, skill_name):
    """Generate standalone HTML for review."""
    timing_rows = ""
    for r in results:
        t = r.get("timing", {})
        ws_time = t.get("with_skill", {}).get("total_duration_seconds", "N/A")
        ws_tokens = t.get("with_skill", {}).get("total_tokens", "N/A")
        nos_time = t.get("without_skill", {}).get("total_duration_seconds", "N/A")
        nos_tokens = t.get("without_skill", {}).get("total_tokens", "N/A")
        timing_rows += f"""
        <tr>
            <td>{r['eval_name']}</td>
            <td>{ws_time}s / {ws_tokens} tokens</td>
            <td>{nos_time}s / {nos_tokens} tokens</td>
        </tr>"""

    eval_cards = ""
    for i, r in enumerate(results):
        def escape_html(text):
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")

        eval_cards += f"""
        <div class="eval-card" id="eval-{i}">
            <h3>Test {i+1}: {r['eval_name']}</h3>
            <div class="prompt"><strong>提示:</strong> {escape_html(r['prompt'])}</div>
            <div class="comparison">
                <div class="side">
                    <h4>带 Skill</h4>
                    <pre class="message">{escape_html(r['with_skill'])}</pre>
                </div>
                <div class="side">
                    <h4>不带 Skill</h4>
                    <pre class="message">{escape_html(r['without_skill'])}</pre>
                </div>
            </div>
        </div>"""

    benchmark_section = ""
    if benchmark:
        benchmark_section = f"""
        <div class="benchmark-section">
            <h2>性能对比</h2>
            <table>
                <tr><th>测试</th><th>带 Skill</th><th>不带 Skill</th></tr>
                {timing_rows}
            </table>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Commit Message Skill Review — {skill_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a1a2e; margin-bottom: 8px; }}
        h2 {{ color: #16213e; margin: 30px 0 15px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }}
        h3 {{ color: #0f3460; margin-bottom: 10px; }}
        .subtitle {{ color: #666; margin-bottom: 30px; }}
        .eval-card {{ background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .prompt {{ background: #f8f9fa; padding: 12px; border-radius: 4px; margin-bottom: 15px; border-left: 3px solid #4a90d9; }}
        .comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .side {{ border: 1px solid #e0e0e0; border-radius: 6px; padding: 15px; }}
        .side h4 {{ color: #4a90d9; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; }}
        pre.message {{ background: #1a1a2e; color: #e0e0e0; padding: 12px; border-radius: 4px; overflow-x: auto; font-size: 13px; white-space: pre-wrap; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e0e0e0; }}
        th {{ background: #1a1a2e; color: white; }}
        tr:hover {{ background: #f8f9fa; }}
        .nav {{ display: flex; gap: 10px; margin-bottom: 20px; }}
        .nav button {{ padding: 8px 16px; background: #4a90d9; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        .nav button:hover {{ background: #357abd; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Commit Message Skill Review</h1>
        <p class="subtitle">Skill: {skill_name} | 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="nav">
            <button onclick="document.querySelectorAll('.eval-card')[0]?.scrollIntoView({{behavior:'smooth'}})">← 上一个</button>
            <button onclick="document.querySelectorAll('.eval-card')[document.querySelectorAll('.eval-card').length-1]?.scrollIntoView({{behavior:'smooth'}})">下一个 →</button>
        </div>

        {benchmark_section}

        <h2>测试结果</h2>
        {eval_cards}
    </div>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate commit message skill review HTML")
    parser.add_argument("workspace", help="Path to workspace directory")
    parser.add_argument("--skill-name", required=True, help="Name of the skill")
    parser.add_argument("--benchmark", help="Path to benchmark.json")
    parser.add_argument("--static", help="Path to output HTML file (standalone mode)")
    args = parser.parse_args()

    results = load_eval_data(args.workspace)
    benchmark = load_benchmark(args.benchmark)
    html = generate_html(results, benchmark, args.skill_name)

    if args.static:
        with open(args.static, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML written to: {args.static}")
    else:
        # Start local server
        import tempfile
        tmpdir = tempfile.mkdtemp()
        html_path = os.path.join(tmpdir, "review.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        port = 8765
        handler = http.server.SimpleHTTPRequestHandler
        httpd = http.server.HTTPServer(("", port), handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        url = f"http://localhost:{port}/review.html"
        print(f"Review viewer running at: {url}")
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

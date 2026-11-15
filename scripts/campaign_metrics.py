#!/usr/bin/env python3
"""宣教活动数据统计：从活动明细 CSV 汇总过程指标、生成台账汇总与同比对比。

对应 R4 效果评估者「数据收集 / 数据分析」两步，字段口径见
templates/data-ledger.md 的「工作表 1：活动明细」。

用法：
    python3 campaign_metrics.py 活动明细.csv --period 2026Q3 --outdir ./out
    python3 campaign_metrics.py 本期.csv --compare 上期.csv --period 2026Q3 --outdir ./out

输出：
    <outdir>/<period>_指标汇总.json   汇总指标、分维度结构、同比、数据质量警告
    <outdir>/<period>_台账汇总.csv    按活动类型/渠道/目标人群/五进入类别的分组汇总

依赖：仅 Python 3.9+ 标准库。CSV 编码自动尝试 utf-8-sig / utf-8 / gb18030。
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

# 数值列（必需列缺失时报错，可选列缺失时按 0 处理并给出警告）
NUMERIC_FIELDS = [
    "场次",
    "参与员工数",
    "覆盖人次_线下",
    "覆盖人次_线上",
    "发放资料数",
    "原创作品数",
    "媒体报道数",
    "费用支出（元）",
]
GROUP_FIELDS = ["活动类型", "渠道", "目标人群", "五进入类别"]
OPTIONAL_FIELDS = ["活动名称", "活动日期", "形式", "负责人", "数据来源"] + GROUP_FIELDS

# 常见列名变体 → 标准列名
ALIASES = {
    "活动场次": "场次",
    "覆盖人次（线下）": "覆盖人次_线下",
    "覆盖人次（线上）": "覆盖人次_线上",
    "覆盖人次线下": "覆盖人次_线下",
    "覆盖人次线上": "覆盖人次_线上",
    "线下覆盖人次": "覆盖人次_线下",
    "线上覆盖人次": "覆盖人次_线上",
    "费用支出": "费用支出（元）",
    "费用支出(元)": "费用支出（元）",
    "费用": "费用支出（元）",
    "媒体报道": "媒体报道数",
    "原创作品": "原创作品数",
    "参与员工": "参与员工数",
    "sessions": "场次",
    "staff": "参与员工数",
    "offline_reach": "覆盖人次_线下",
    "online_reach": "覆盖人次_线上",
    "works": "原创作品数",
    "cost": "费用支出（元）",
}


def read_rows(path: Path):
    """读取 CSV，返回 (标准化后的行列表, 警告列表)。"""
    last_err = None
    for enc in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            with path.open("r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f)
                raw = list(reader)
            break
        except UnicodeDecodeError as e:
            last_err = e
    else:
        raise SystemExit(f"无法解码 CSV：{path}（{last_err}）")

    warnings = []
    rows = []
    for i, row in enumerate(raw, start=2):
        item = {}
        for k, v in row.items():
            if k is None:
                continue
            key = k.strip()
            key = ALIASES.get(key, key)
            item[key] = (v or "").strip()
        rows.append(item)
    if not rows:
        warnings.append("CSV 无数据行")

    headers = set().union(*(r.keys() for r in rows)) if rows else set()
    missing_required = [c for c in NUMERIC_FIELDS if c not in headers]
    if missing_required:
        raise SystemExit(
            "CSV 缺少必需数值列："
            + ", ".join(missing_required)
            + "\n参见 templates/data-ledger.md「工作表 1：活动明细」"
        )
    for c in OPTIONAL_FIELDS:
        if c not in headers:
            warnings.append(f"缺少可选列「{c}」，相关维度分析将归并到「未填」")
    return rows, warnings, sorted(headers)


def to_num(value: str, row_no: int, field: str, warnings: list):
    """把单元格转成非负数值；非法值记警告并按 0 计，绝不猜数。"""
    if value == "":
        return 0.0
    if value in ("待补", "-", "N/A", "NA"):
        warnings.append(f"第 {row_no} 行「{field}」标记为「{value}」，按 0 计且需补齐")
        return 0.0
    cleaned = value.replace(",", "").replace("，", "").replace("元", "").strip()
    try:
        n = float(cleaned)
    except ValueError:
        warnings.append(f"第 {row_no} 行「{field}」值无法解析：{value!r}，按 0 计")
        return 0.0
    if n < 0:
        warnings.append(f"第 {row_no} 行「{field}」为负数：{value!r}，按 0 计")
        return 0.0
    return n


def summarize(rows, warnings):
    """汇总过程指标。"""
    totals = {c: 0.0 for c in NUMERIC_FIELDS}
    for i, row in enumerate(rows, start=2):
        for c in NUMERIC_FIELDS:
            totals[c] += to_num(row.get(c, ""), i, c, warnings)

    offline = totals["覆盖人次_线下"]
    online = totals["覆盖人次_线上"]
    reach = offline + online
    cost = totals["费用支出（元）"]

    metrics = {
        "活动场次": totals["场次"],
        "参与员工数": totals["参与员工数"],
        "覆盖人次_线下": offline,
        "覆盖人次_线上": online,
        "覆盖人次_合计_未去重": reach,
        "发放资料数": totals["发放资料数"],
        "原创作品数": totals["原创作品数"],
        "媒体报道数": totals["媒体报道数"],
        "费用支出（元）": cost,
        "单位覆盖成本（元/人次）": round(cost / reach, 2) if reach else None,
        "口径提示": "线上线下覆盖人次直接相加，未做跨渠道去重；对外报送前须按活动方案约定的去重口径复核",
    }

    groups = {}
    for key in GROUP_FIELDS:
        bucket = defaultdict(lambda: {"场次": 0.0, "覆盖人次": 0.0, "原创作品数": 0.0,
                                      "费用支出（元）": 0.0, "记录数": 0})
        for i, row in enumerate(rows, start=2):
            label = row.get(key, "") or "未填"
            b = bucket[label]
            b["场次"] += to_num(row.get("场次", ""), i, "场次", [])
            b["覆盖人次"] += (
                to_num(row.get("覆盖人次_线下", ""), i, "覆盖人次_线下", [])
                + to_num(row.get("覆盖人次_线上", ""), i, "覆盖人次_线上", [])
            )
            b["原创作品数"] += to_num(row.get("原创作品数", ""), i, "原创作品数", [])
            b["费用支出（元）"] += to_num(row.get("费用支出（元）", ""), i, "费用支出（元）", [])
            b["记录数"] += 1
        groups[key] = {k: dict(v) for k, v in sorted(bucket.items())}

    return metrics, groups


def growth(cur, prev):
    if prev in (None, 0):
        return None
    return round((cur - prev) / prev * 100, 2)


def main():
    ap = argparse.ArgumentParser(description="宣教活动数据统计与台账汇总")
    ap.add_argument("input", type=Path, help="本期活动明细 CSV")
    ap.add_argument("--compare", type=Path, help="上期活动明细 CSV，用于同比对比")
    ap.add_argument("--period", default="本期", help="统计周期标识，用于输出文件名")
    ap.add_argument("--outdir", type=Path, default=Path("."), help="输出目录")
    args = ap.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"找不到输入文件：{args.input}")
    args.outdir.mkdir(parents=True, exist_ok=True)

    rows, warnings, headers = read_rows(args.input)
    metrics, groups = summarize(rows, warnings)

    result = {
        "统计周期": args.period,
        "数据来源": str(args.input),
        "明细行数": len(rows),
        "CSV列": headers,
        "过程指标": metrics,
        "结构分析": groups,
        "同比对比": None,
        "数据质量警告": warnings,
    }

    if args.compare:
        if not args.compare.is_file():
            raise SystemExit(f"找不到对比文件：{args.compare}")
        prev_rows, prev_warnings, _ = read_rows(args.compare)
        prev_metrics, _ = summarize(prev_rows, prev_warnings)
        compare = {}
        for k, v in metrics.items():
            if not isinstance(v, (int, float)) or v is None:
                continue
            p = prev_metrics.get(k)
            compare[k] = {"本期": v, "上期": p, "同比变化(%)": growth(v, p)}
        result["同比对比"] = {
            "对比文件": str(args.compare),
            "指标": compare,
            "说明": "上期为 0 或缺失时同比为 null；缺失数据不得估算填充",
        }
        warnings.extend(f"[上期] {w}" for w in prev_warnings)

    json_path = args.outdir / f"{args.period}_指标汇总.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_path = args.outdir / f"{args.period}_台账汇总.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["分组维度", "分组值", "场次", "覆盖人次", "原创作品数", "费用支出（元）", "记录数"])
        for dim, buckets in groups.items():
            for label, b in buckets.items():
                w.writerow([dim, label, b["场次"], b["覆盖人次"], b["原创作品数"],
                            b["费用支出（元）"], b["记录数"]])

    print(f"明细行数：{len(rows)}")
    print(f"活动场次：{metrics['活动场次']:.0f}  覆盖人次（未去重）：{metrics['覆盖人次_合计_未去重']:.0f}")
    print(f"原创作品数：{metrics['原创作品数']:.0f}  费用支出：{metrics['费用支出（元）']:.2f} 元")
    if warnings:
        print(f"数据质量警告 {len(warnings)} 条（详见 JSON）", file=sys.stderr)
    print(f"已输出：{json_path}")
    print(f"已输出：{csv_path}")


if __name__ == "__main__":
    main()

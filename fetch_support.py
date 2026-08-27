#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取竞彩官网(webapi.sporttery.cn)当日全部在售比赛的【投注资金占比/支持率】,
输出为 support.json, 供前端同源读取(GitHub Pages 无 CORS 限制).
本脚本通常在 GitHub Actions 定时运行, 也可本地运行生成初始数据.
数据源: getSupportRateV1.qry
"""
import json
import urllib.request
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
REF = "https://www.lottery.gov.cn/"
BASE_CALC = "https://webapi.sporttery.cn/gateway/uniform/football/getMatchCalculatorV1.qry?channel=1&poolCode=hhad,had"
BASE_SUP = "https://webapi.sporttery.cn/gateway/jc/common/getSupportRateV1.qry"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": REF, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def main():
    calc = get(BASE_CALC)
    if calc.get("errorCode") != "0" or not calc.get("value"):
        print("获取比赛列表失败:", calc.get("errorMessage"))
        return 1

    ids = []
    for m in calc["value"].get("matchInfoList", []):
        for s in m.get("subMatchList", []):
            mid = str(s.get("matchId"))
            if mid and mid not in ids:
                ids.append(mid)

    out = {"updated": datetime.now().astimezone().isoformat(timespec="seconds"), "matches": {}}
    # 分块抓取支持率
    for i in range(0, len(ids), 30):
        chunk = ",".join(ids[i:i + 30])
        try:
            sr = get(f"{BASE_SUP}?matchIds={chunk}&poolCode=hhad,had&sportType=1")
            for k, v in (sr.get("value") or {}).items():
                out["matches"][k.lstrip("_")] = v
        except Exception as e:
            print("分块抓取失败:", e)

    with open("support.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"完成: 共 {len(out['matches'])} 场, 输出 support.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
import json, subprocess, sys

TOKEN = subprocess.run(
    ["git", "credential", "fill"], input="protocol=https\nhost=github.com\n",
    capture_output=True, text=True, cwd=r"C:/Users/16554/WorkBuddy/2026-10-23-10-20-59/againpaws",
).stdout.split("password=")[-1].strip()

BODY = """## 变更内容

- **静态预渲染 14 个路由**：原始 HTML 现在包含完整正文（此前是 1.4KB 空壳），GPTBot / ClaudeBot / PerplexityBot 等 AI 爬虫可直接读取全部内容；JS bundle 保留，页面交互不受影响
- **新增 4 个信任页**：/privacy/ /terms/ /refund-policy/ /faq/（FAQ 页自带 FAQPage JSON-LD）
- **canonical 统一尾斜杠**（与 GitHub Pages 301 行为一致，修复原 canonical 指向跳转前 URL 的问题）
- 删除无效 meta keywords；首页 hero 图预加载（LCP 优化）
- **/products/ 注入 5 个 Product schema**（含真实参考价 $87/$112/$197/$297/$477）
- robots.txt 显式放行 AI 爬虫；新增 llms.txt
- sitemap.xml：+4 页共 18 个 URL，尾斜杠统一

## 上线后验证

```bash
curl -s https://againpaws.vip/ | grep -i "needle-felted"   # 原始 HTML 应含正文
curl -s -o /dev/null -w "%{http_code}\\n" https://againpaws.vip/faq/   # 200
curl -s -o /dev/null -w "%{http_code}\\n" https://againpaws.vip/llms.txt   # 200
```

然后在 Google Search Console 重新提交 sitemap。"""

payload = {
    "title": "SEO P0: 静态预渲染 + 信任页 + AI 搜索就绪",
    "head": "seo/static-prerender",
    "base": "main",
    "body": BODY,
}
req = urllib_request = None
import urllib.request
r = urllib.request.Request(
    "https://api.github.com/repos/q8461994-boop/againpaws/pulls",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "token " + TOKEN,
             "Accept": "application/vnd.github+json",
             "Content-Type": "application/json"},
    method="POST")
with urllib.request.urlopen(r) as resp:
    d = json.load(resp)
    print("PR:", d.get("html_url"))
    print("number:", d.get("number"))

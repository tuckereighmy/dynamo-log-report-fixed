Analyze the Apache-style access log at `/app/access.log` and write a summary report
to `/app/report.json`.

`/app/report.json` must contain a single JSON object with exactly these three keys:

- `total_requests` (integer) — the total number of requests in the log. Each
  non-blank line is one request; blank lines are not requests.
- `unique_ips` (integer) — the number of distinct client IP addresses. The client
  IP is the first whitespace-separated field on a line.
- `top_path` (string) — the path requested most often, taken from the request line
  (for example, the `/index.html` in `"GET /index.html HTTP/1.1"`).

Write no other keys.

For example, a log with four requests from two clients where `/contact.html` was
requested most often would produce:

```json
{"total_requests": 4, "unique_ips": 2, "top_path": "/contact.html"}
```

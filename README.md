# TALI Book Reader

A Go web app for reading the TALI book — matching the TMS-99 dark terminal aesthetic.

## Structure
```
tali-book/
├── cmd/
│   └── main.go          # Go HTTP server
├── frontend/
│   └── index.html       # Single-file frontend (HTML + CSS + JS)
├── data/
│   └── chapters.json    # Book data (auto-generated from markdown)
├── go.mod
└── README.md
```

## Run

```bash
go build -o tali-book-server ./cmd/
./tali-book-server
# Open http://localhost:8080
```

Or without building:
```bash
go run ./cmd/
```

## Features
- Table of contents with all 59 chapters grouped by part
- Full chapter reading view with serif body text
- Prev/Next navigation (keyboard: ← → or h/l)
- Full-text search across all chapters
- Reading progress bar
- Mobile responsive with slide-out sidebar
- ~50,000 words across 10 parts

## API
- `GET /api/meta` — book stats and parts
- `GET /api/chapters` — all chapters (summary)
- `GET /api/chapters/{num}` — single chapter with paragraphs
- `GET /api/search?q=...` — full-text search

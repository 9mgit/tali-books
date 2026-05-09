package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
)

// ── Data types ──────────────────────────────────────────────────────────────

type Chapter struct {
	Num        int      `json:"num"`
	Title      string   `json:"title"`
	Part       string   `json:"part"`
	PartNum    int      `json:"part_num"`
	Paragraphs []string `json:"paragraphs"`
	WordCount  int      `json:"word_count"`
}

type BookMeta struct {
	TotalChapters int    `json:"total_chapters"`
	TotalWords    int    `json:"total_words"`
	Parts         []Part `json:"parts"`
}

type Part struct {
	Num      int    `json:"num"`
	Name     string `json:"name"`
	Chapters []int  `json:"chapters"`
}

// ── Global state ─────────────────────────────────────────────────────────────

var chapters []Chapter
var bookMeta BookMeta

func loadChapters() error {
	data, err := os.ReadFile("data/chapters.json")
	if err != nil {
		return fmt.Errorf("reading chapters.json: %w", err)
	}
	if err := json.Unmarshal(data, &chapters); err != nil {
		return fmt.Errorf("parsing chapters.json: %w", err)
	}

	// Build meta
	partsMap := map[int]*Part{}
	totalWords := 0
	for _, ch := range chapters {
		totalWords += ch.WordCount
		if _, ok := partsMap[ch.PartNum]; !ok {
			partsMap[ch.PartNum] = &Part{
				Num:  ch.PartNum,
				Name: ch.Part,
			}
		}
		partsMap[ch.PartNum].Chapters = append(partsMap[ch.PartNum].Chapters, ch.Num)
	}

	parts := make([]Part, 0, len(partsMap))
	for i := 1; i <= len(partsMap); i++ {
		if p, ok := partsMap[i]; ok {
			parts = append(parts, *p)
		}
	}

	bookMeta = BookMeta{
		TotalChapters: len(chapters),
		TotalWords:    totalWords,
		Parts:         parts,
	}

	log.Printf("Loaded %d chapters, %d words, %d parts", len(chapters), totalWords, len(parts))
	return nil
}

// ── Middleware ────────────────────────────────────────────────────────────────

func withCORS(h http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Request: %s %s", r.Method, r.URL.Path)
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		h(w, r)
	}
}

func jsonResp(w http.ResponseWriter, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	json.NewEncoder(w).Encode(v)
}

func errResp(w http.ResponseWriter, code int, msg string) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(map[string]string{"error": msg})
}

// ── API Handlers ──────────────────────────────────────────────────────────────

// GET /api/meta
func handleMeta(w http.ResponseWriter, r *http.Request) {
	jsonResp(w, bookMeta)
}

// GET /api/chapters — list all (num, title, part, word_count only)
func handleChapterList(w http.ResponseWriter, r *http.Request) {
	type Summary struct {
		Num       int    `json:"num"`
		Title     string `json:"title"`
		Part      string `json:"part"`
		PartNum   int    `json:"part_num"`
		WordCount int    `json:"word_count"`
		Preview   string `json:"preview"`
	}
	list := make([]Summary, 0, len(chapters))
	for _, ch := range chapters {
		preview := ""
		if len(ch.Paragraphs) > 0 {
			p := ch.Paragraphs[0]
			if len(p) > 200 {
				p = p[:200] + "…"
			}
			preview = p
		}
		list = append(list, Summary{
			Num:       ch.Num,
			Title:     ch.Title,
			Part:      ch.Part,
			PartNum:   ch.PartNum,
			WordCount: ch.WordCount,
			Preview:   preview,
		})
	}
	jsonResp(w, list)
}

// GET /api/chapters/{num}
func handleChapter(w http.ResponseWriter, r *http.Request) {
	// Extract chapter number from path
	path := strings.TrimPrefix(r.URL.Path, "/api/chapters/")
	path = strings.TrimSuffix(path, "/")
	
	log.Printf("Handling chapter request for path: %s", path)

	if path == "all" {
		log.Printf("Serving all chapters")
		jsonResp(w, chapters)
		return
	}

	num, err := strconv.Atoi(path)
	if err != nil || num < 1 {
		log.Printf("Invalid chapter number: %s (err: %v)", path, err)
		errResp(w, http.StatusBadRequest, "invalid chapter number")
		return
	}

	for _, ch := range chapters {
		if ch.Num == num {
			// Add prev/next
			type FullChapter struct {
				Chapter
				Prev *int `json:"prev"`
				Next *int `json:"next"`
			}
			var prev, next *int
			if num > 1 {
				p := num - 1
				prev = &p
			}
			if num < len(chapters) {
				n := num + 1
				next = &n
			}
			jsonResp(w, FullChapter{Chapter: ch, Prev: prev, Next: next})
			return
		}
	}
	errResp(w, http.StatusNotFound, fmt.Sprintf("chapter %d not found", num))
}

// GET /api/search?q=...
func handleSearch(w http.ResponseWriter, r *http.Request) {
	q := strings.ToLower(strings.TrimSpace(r.URL.Query().Get("q")))
	if q == "" {
		errResp(w, http.StatusBadRequest, "missing query parameter 'q'")
		return
	}

	type Result struct {
		Num     int    `json:"num"`
		Title   string `json:"title"`
		Part    string `json:"part"`
		PartNum int    `json:"part_num"`
		Match   string `json:"match"`
		Count   int    `json:"count"`
	}

	var results []Result
	for _, ch := range chapters {
		count := 0
		var matchSnippet string
		for _, para := range ch.Paragraphs {
			lower := strings.ToLower(para)
			idx := strings.Index(lower, q)
			if idx >= 0 {
				count++
				if matchSnippet == "" {
					start := idx - 60
					if start < 0 {
						start = 0
					}
					end := idx + len(q) + 120
					if end > len(para) {
						end = len(para)
					}
					matchSnippet = "…" + para[start:end] + "…"
				}
			}
		}
		// Also check title
		if strings.Contains(strings.ToLower(ch.Title), q) {
			count++
			if matchSnippet == "" {
				matchSnippet = ch.Title
			}
		}
		if count > 0 {
			results = append(results, Result{
				Num:     ch.Num,
				Title:   ch.Title,
				Part:    ch.Part,
				PartNum: ch.PartNum,
				Match:   matchSnippet,
				Count:   count,
			})
		}
	}

	jsonResp(w, map[string]any{
		"query":   q,
		"count":   len(results),
		"results": results,
	})
}

// ── Static files ──────────────────────────────────────────────────────────────

func handleStatic(w http.ResponseWriter, r *http.Request) {
	path := r.URL.Path
	
	// Skip API routes
	if strings.HasPrefix(path, "/api/") {
		http.NotFound(w, r)
		return
	}
	
	if path == "/" || path == "/index.html" {
		http.ServeFile(w, r, "frontend/index.html")
		return
	}
	// Serve frontend files
	file := "frontend" + path
	if _, err := os.Stat(file); os.IsNotExist(err) {
		// SPA fallback
		http.ServeFile(w, r, "frontend/index.html")
		return
	}
	http.ServeFile(w, r, file)
}

// ── Translations ───────────────────────────────────────────────────────────────

func handleTranslation(w http.ResponseWriter, r *http.Request) {
	log.Printf("Translation request: %s", r.URL.Path)
	filename := strings.TrimPrefix(r.URL.Path, "/api/translations/")
	
	var filePath string
	if strings.HasPrefix(filename, "cover_") {
		filePath = "data/translations/" + filename
	} else {
		filePath = "data/translations/chapters_" + filename
	}
	
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		errResp(w, http.StatusNotFound, "translation not found")
		return
	}
	data, err := os.ReadFile(filePath)
	if err != nil {
		errResp(w, http.StatusInternalServerError, "failed to read translation")
		return
	}
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Write(data)
}

// ── Router ────────────────────────────────────────────────────────────────────

func main() {
	if err := loadChapters(); err != nil {
		log.Fatalf("Failed to load chapters: %v", err)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8880"
	}

	mux := http.NewServeMux()

	// API routes (must be registered BEFORE static handler)
	mux.HandleFunc("/api/meta", withCORS(handleMeta))
	mux.HandleFunc("/api/chapters", withCORS(handleChapterList))
	mux.HandleFunc("/api/chapters/", withCORS(handleChapter))
	mux.HandleFunc("/api/search", withCORS(handleSearch))
	mux.HandleFunc("/api/translations/", withCORS(handleTranslation))

	// Static / SPA (fallback for everything else)
	mux.HandleFunc("/", handleStatic)

	addr := ":" + port
	log.Printf("TALI Book Reader running on http://localhost%s", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}

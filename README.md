# 職人 Go (shokunin-go) 🛠️
>
> **"A Shokunin does not just write code; they refine the craft until it reaches its essence."**

`shokunin-go` adalah jurnal teknis dan dokumentasi perjalanan saya dalam bertransisi dari **Middle-level Software Engineer** menuju **Senior-level Engineering**. Repositori ini berfokus pada pendalaman ekosistem **Go (Golang)**, pemahaman *runtime internals*, desain sistem yang skalabel, hingga *engineering excellence*.

---

## 🎯 Fokus Utama & Objektif Teknis

Proyek ini dirancang untuk melampaui abstraksi sintaksis, berfokus pada penguasaan **Engineering Trade-offs** di ekosistem Go:

* **Runtime Mastery:** Melampaui abstraksi Go dengan memahami *stack/heap allocation*, *escape analysis*, dan mekanisme *GMP Scheduler* untuk optimasi *low-level*.
* **High-Throughput Concurrency:** Mengelola *resource lifecycle* secara ketat menggunakan *advanced synchronization*, *worker pools*, dan pencegahan *memory leaks* (bukan sekadar `go func`).
* **Zero-Guesswork Performance:** Mengganti asumsi dengan data. Menggunakan `pprof`, `trace`, dan *benchmarking* untuk mengidentifikasi serta mengeliminasi *bottleneck* sistem secara presisi.
* **Maintainable Architecture:** Implementasi *Decoupled Systems* menggunakan *Hexagonal Architecture* dan *Domain-Driven Design (DDD)* untuk memastikan kode tetap *testable* dan modular seiring skala sistem berkembang.
* **Reliability Engineering:** Standarisasi kualitas melalui *Fuzz Testing*, *Integration Testing* dengan *Testcontainers*, dan *Observability* (Tracing/Metrics) sebagai standar utama produksi.

---

## 🗓️ Roadmap & Kurikulum (5 Fase)

| Fase | Topik Utama | Fokus Kompetensi | Status |
| :--- | :--- | :--- | :---: |
| **01** | **Go Runtime Internals** | Memory Management, GC Tuning, GMP Scheduler | ⏳ *In Progress* |
| **02** | **Advanced Concurrency** | Sync Pool, Atomic, Advanced Patterns, Context | 📅 *Pending* |
| **03** | **Perf & Observability** | Pprof, Tracing, Slog, Prometheus/OpenTelemetry | 📅 *Pending* |
| **04** | **Arch & System Design** | Hexagonal, DDD, gRPC, Dependency Injection | 📅 *Pending* |
| **05** | **Engineering Excellence** | Fuzzing, Testcontainers, CI/CD, Go Mod Adv | 📅 *Pending* |

---

## 📂 Struktur Repositori

Setiap modul berisi catatan teknis (`.md`), *Proof of Concept* (`.go`), dan hasil analisis performa.

```bash
.
├── 01-runtime-internals/      # Deep Dive: Stack/Heap, GC, Scheduler
├── 02-advanced-concurrency/   # Patterns: Worker Pools, Context, Atomic
├── 03-perf-observability/     # Measure: Pprof, Trace, Structured Logging
├── 04-arch-design/            # Design: DDD, Hexagonal, gRPC, Wire
├── 05-eng-excellence/         # Quality: Fuzzing, Testcontainers, Docker
└── logs/                      # Daily Kaizen: Refleksi dan temuan harian
```

---

## 🛠️ Tech Stack & Tools

* **Language:** Go (Latest Stable)
* **Profiling:** `net/http/pprof`, `runtime/trace`
* **Testing:** `testing`, `testcontainers-go`, `go-fuzz`
* **Observability:** OpenTelemetry (OTEL), Jaeger, Prometheus
* **Architecture:** Hexagonal Architecture, Modular Monolith

---

## 📖 Filosofi Belajar (Kaizen Log)

Setiap sesi /hari dialokasikan untuk:

1. **Deep Reading:** Membedah *Source Code* Standard Library Go (e.g., `sync`, `runtime`, `net`).
2. **Implementation:** Mengonversi teori ke dalam kode yang fungsional dan terukur.
3. **Analysis:** Mengukur dampak setiap perubahan menggunakan benchmark dan profilier.

---

### "Shokunin means not only having technical skills, but also having an attitude... the obligation to do their best."

---
*Developed by Sabiq*

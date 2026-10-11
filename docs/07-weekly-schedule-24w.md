# Tabel Tugas Mingguan 24 Pekan (dengan pembagian 8 jam dan kriteria penerimaan)

> Cara pakai: buka halaman ini sebelum mulai kerja setiap pekan, salin "Kriteria Penerimaan" pekan ini ke catatan mingguan Anda; centang di akhir pekan.
> **Lanjut ke pekan berikutnya tanpa centang = pekan ini sia-sia.** Lebih baik molor satu pekan daripada maju membawa pekerjaan setengah jadi.

---

## Cara Menggunakan Tabel Ini

| Kolom | Arti |
| --- | --- |
| Teori 2j | Tepatnya apa yang dibaca (bukan "baca buku", tapi bab/link spesifik) |
| Implementasi 4j | Kode tepat apa yang ditulis |
| Pengukuran 1j | Perintah apa yang dijalankan dan angka apa yang dilihat |
| Retrospeksi 1j | Dokumen apa yang ditulis |
| Penerimaan | Kondisi selesai yang **dapat diputuskan** (tidak boleh memakai kata kabur seperti "paham" atau "menguasai") |

---

## Fase 1 · Mekanisme Internal Go dan Memori

### Minggu 1 · Compiler, build, biner, assembly

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca 1/3 pertama `go.dev/doc/gc-guide`; cari "Go compiler SSA phases"; baca bantuan `go tool compile -h` |
| Implementasi 4j | Tulis 10 fungsi kecil, masing-masing mendemonstrasikan satu skenario escape (return pointer, boxing, closure, channel, `make` dinamis, argumen `fmt`, dll.) |
| Pengukuran 1j | Jalankan `go build -gcflags="-m=2"` untuk semuanya, catat satu per satu rantai `flow:` yang diberikan compiler |
| Retrospeksi 1j | `01-go-internals/week01/README.md`: diagram alur kompilasi + tabel 10 kasus escape |

**Penerimaan**:
- [ ] Semua 10 kasus punya bukti output `-m=2`, dan Anda bisa menjelaskan secara lisan alasan masing-masing
- [ ] Ada satu diagram pipeline kompilasi yang Anda gambar/salin sendiri
- [ ] Tahu apa efek samping dari `-s -w`

---

### Minggu 2 · Stack, heap, pointer, alokasi, siklus hidup objek

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca blog Go "Go 1.18 slice growth"; cari "Go memory allocator mcache mcentral mheap" |
| Implementasi 4j | Tiga set benchmark: pointer vs value (dua ukuran: 16B dan 4KB), slice pre-allocated vs tidak, padding layout struct |
| Pengukuran 1j | `go test -bench=. -benchmem -count=10` + `benchstat`; verifikasi dengan `unsafe.Sizeof` |
| Retrospeksi 1j | `docs/benchmarks/week02.md`; ubah 3 jebakan memori menjadi test |

**Penerimaan**:
- [ ] Ketiga set benchmark punya `ns/op`, `B/op`, `allocs/op`
- [ ] Bisa menyebutkan **ambang hasil pengukuran nyata** untuk "struct kecil pakai value, struct besar pakai pointer"
- [ ] Ketiga jebakan (slice menahan array besar, pool tanpa batas kapasitas, `append` berbagi underlying array) punya test reproduksi

---

### Minggu 3 · Interface, method set, generics

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca bab method set di `go.dev/ref/spec`; baca dokumen desain generics `go.dev/design/43651-type-parameters` |
| Implementasi 4j | Ring buffer generics + container terurut; benchmark penjumlahan tiga arah: interface vs konkret vs generics |
| Pengukuran 1j | Perbandingan tiga arah dengan `benchstat`; `-gcflags="-m=2"` untuk melihat apakah stencil generics di-inline |
| Retrospeksi 1j | `docs/benchmarks/week03.md` + ADR-0000 (mengapa proyek ini memakai/tidak memakai generics) |

**Penerimaan**:
- [ ] Container generics punya unit test lengkap (kosong/penuh/overwrite/nilai nol)
- [ ] Data benchmark tiga arah lengkap dan disertai penjelasan (bukan sekadar angka)
- [ ] Bisa menjelaskan dengan jelas "kapan generics sebaiknya tidak dipakai"

---

### Minggu 4 · GC, laju alokasi, tekanan GC

| Slot | Isi |
| --- | --- |
| Teori 2j | Selesaikan `go.dev/doc/gc-guide`; baca "Go GC: Prioritizing low latency and simplicity" |
| Implementasi 4j | Request handler versi alokasi tinggi (`Sprintf`, `[]any`, slice sementara); tulis ulang menjadi versi alokasi rendah |
| Pengukuran 1j | Perbandingan dua versi dengan `GODEBUG=gctrace=1`; `benchstat`; coba `GOGC=50/100/400` dan catat perubahan throughput serta memori |
| Retrospeksi 1j | `docs/benchmarks/week04-gc.md`: perbandingan jumlah GC, GC%, dan `B/op` sebelum/sesudah |

**Penerimaan**:
- [ ] Ada output mentah `gctrace`, dan Anda bisa menjelaskan tiap field-nya
- [ ] Ada data hasil pengukuran nyata untuk tiga tingkat `GOGC` (throughput + memori puncak)
- [ ] Tahu apa yang masing-masing dikendalikan oleh `GOMEMLIMIT` dan `GOGC`, serta bagaimana keduanya berinteraksi

---

### Minggu 5 · Profiling CPU / heap / alokasi

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca `go.dev/doc/diagnostics`; baca satu artikel praktik pprof |
| Implementasi 4j | Lakukan diagnosis lengkap pada satu program yang "sengaja ditulis lambat": CPU → alloc → optimasi → ukur ulang |
| Pengukuran 1j | `go tool pprof -http`; ekspor flame graph; pasang `net/http/pprof` |
| Retrospeksi 1j | `docs/benchmarks/week05-profile.md`: satu catatan lengkap "temukan → optimasi → verifikasi" |

**Penerimaan**:
- [ ] Ada perbandingan dua sudut pandang, inuse_space dan alloc_space (menunjukkan Anda paham perbedaan keduanya)
- [ ] Ada output `benchstat` sebelum dan sesudah optimasi
- [ ] Pernah menghasilkan `go tool trace` dan bisa menjelaskan tampilan "scheduling latency"

---

### Minggu 6 · Inlining, bound check elimination, optimasi compiler

| Slot | Isi |
| --- | --- |
| Teori 2j | Cari "Go inlining cost budget"; baca diskusi terkait SSA prove pass |
| Implementasi 4j | Benchmark perbandingan inlining on/off; benchmark sebelum/sesudah BCE; verifikasi dengan `objdump` |
| Pengukuran 1j | Perbandingan dengan `go build -gcflags="-l"`; cari `panicBounds` dengan `go tool objdump` |
| Retrospeksi 1j | `docs/benchmarks/week06.md`, **wajib memuat minimal satu optimasi yang gagal** |

**Penerimaan**:
- [ ] Bisa menyebutkan 4 situasi "tidak bisa di-inline"
- [ ] BCE punya bukti objdump atau benchmark
- [ ] Mencatat minimal satu optimasi yang "dikira efektif tapi terbukti tidak berdampak"

**🚦 Gate G1**: 6 pekan di atas harus semuanya hijau sebelum masuk Fase 2.

---

## Fase 2 · Konkurensi dan Sistem Operasi

### Minggu 7 · Scheduler goroutine G-M-P

| Slot | Isi |
| --- | --- |
| Teori 2j | Tonton talk "Go scheduler"; baca komentar di `runtime/proc.go` (pilih bagian yang Anda pahami) |
| Implementasi 4j | Benchmark paralel CPU-bound; eksperimen sapuan `GOMAXPROCS`; benchmark biaya pembuatan goroutine |
| Pengukuran 1j | `go test -bench -cpu=1,2,4,8`; lihat scheduling latency dengan `go tool trace` |
| Retrospeksi 1j | `docs/benchmarks/week07-scheduler.md`: kurva skalabilitas |

**Penerimaan**:
- [ ] Bisa menggambar diagram G-M-P dan menjelaskan work stealing, sysmon, serta preemption asinkron
- [ ] Ada tabel data skalabilitas untuk `-cpu=1,2,4,8`
- [ ] Bisa menjelaskan "goroutine yang terblokir pada I/O jaringan tidak memakan M"

---

### Minggu 8 · Channel, Mutex, RWMutex, Atomics

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca `go.dev/ref/mem` (model memori, dibaca per butir); baca dokumen paket `sync/atomic` |
| Implementasi 4j | Empat jenis counter konkuren; test batas semantik channel (nil/closed/buffered/select) |
| Pengukuran 1j | `go test -race`; perbandingan benchmark dengan beberapa `-cpu` |
| Retrospeksi 1j | `docs/benchmarks/week08-sync.md` + decision tree primitif sinkronisasi |

**Penerimaan**:
- [ ] Data benchmark beserta penjelasan untuk keempat counter
- [ ] Test batas channel mencakup nil / sudah ditutup / buffer penuh / buffer kosong
- [ ] Bisa menyebutkan lebih dari 5 jaminan happens-before dari ingatan

---

### Minggu 9 · Race, deadlock, starvation, backpressure → `go-worker-pool`

| Slot | Isi |
| --- | --- |
| Teori 2j | Cari "backpressure in distributed systems"; baca source `errgroup` |
| Implementasi 4j | worker pool: antrean berbatas, pembatalan context, pemulihan panic, graceful shutdown, metrik |
| Pengukuran 1j | `go test -race -count=100`; deteksi kebocoran goroutine; benchmark throughput |
| Retrospeksi 1j | README (**wajib menjelaskan strategi saat antrean penuh**) + `docs/benchmarks/week09-pool.md` |

**Penerimaan**:
- [ ] `-race -count=100` lolos secara stabil
- [ ] Test kebocoran lolos (jumlah goroutine kembali ke basis setelah shutdown)
- [ ] 8 test semuanya ada (lihat tabel 9.4 di dokumen `02-*`)
- [ ] Kurva tingkat konkurensi vs throughput

---

### Minggu 10 · Proses Linux, thread, syscall, fd, sinyal

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca `man 2 write` / `man 2 fsync`; pahami struktur filesystem `/proc` |
| Implementasi 4j | Program keluar secara graceful (SIGTERM); test deteksi kebocoran fd; reproduksi kehabisan fd |
| Pengukuran 1j | `strace -f -c` terhadap worker pool dan HTTP server; catat syscall teratas |
| Retrospeksi 1j | `docs/week10-strace.md`: tabel statistik syscall + penjelasan |

**Penerimaan**:
- [ ] Bisa menjelaskan perbedaan `CLOSE_WAIT` dan `TIME_WAIT` serta bug apa yang masing-masing wakili
- [ ] Laporan `strace -c`, dan bisa menunjukkan letak masalahnya
- [ ] Test kebocoran fd lolos

**🚦 Gate G2**

---

## Fase 3 · Jaringan dan Protokol

### Minggu 11 · TCP, UDP, Socket, DNS

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca Beej's Guide bab 2-5; ulangi state machine TCP |
| Implementasi 4j | TCP echo server + client; program demonstrasi paket menggabung/paket setengah |
| Pengukuran 1j | `ss -lntp`, `tcpdump -X`, `strace -e trace=network` |
| Retrospeksi 1j | `docs/week11-tcpdump.md`: penjelasan per field untuk satu hasil tangkapan paket |

**Penerimaan**:
- [ ] echo server punya deadline, dan terverifikasi bahwa klien lambat akan diputus
- [ ] Ada satu output `tcpdump -X` + penjelasan per field
- [ ] Bisa menjelaskan bahwa TCP adalah aliran byte, bukan aliran pesan (buktikan dengan eksperimen)

---

### Minggu 12 · HTTP/1.1, Keep-Alive, timeout, connection pool

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca artikel Cloudflare "Complete guide to Go net/http timeouts"; baca dokumen `net/http.Transport` |
| Implementasi 4j | Server yang diperkuat (4 timeout) + client yang dikonfigurasi (connection pool) |
| Pengukuran 1j | Test matriks timeout (7 skenario); verifikasi reuse koneksi (amati reuse port) |
| Retrospeksi 1j | `docs/week12-timeouts.md` + README |

**Penerimaan**:
- [ ] Server lengkap dengan `ReadHeaderTimeout`/`ReadTimeout`/`WriteTimeout`/`IdleTimeout`
- [ ] `MaxIdleConnsPerHost` di client sudah dinaikkan (bukan nilai default 2)
- [ ] 7 test skenario timeout semuanya hijau

---

### Minggu 13 · Framing, serialisasi, pembacaan parsial, TLS → `go-kv-protocol`

| Slot | Isi |
| --- | --- |
| Teori 2j | Rancang protokol; baca framing Redis RESP / gRPC HTTP2 untuk perbandingan |
| Implementasi 4j | Framing length-prefixed + layanan KV + klien |
| Pengukuran 1j | 9 test protokol (setengah paket/paket menggabung/paket kotor/ukuran berlebih/putus koneksi/klien lambat/konkurensi) |
| Retrospeksi 1j | `docs/protocol.md` (spesifikasi level byte) + ADR-0001 + verifikasi tangkapan paket |

**Penerimaan**:
- [ ] Dokumen protokol sedetail mungkin sampai orang lain bisa mengimplementasikan klien dalam bahasa lain
- [ ] 9 test semuanya hijau, terutama "kirim per 1 byte" dan "length berlebih"
- [ ] Kesalahan protokol memutus koneksi, kesalahan bisnis tidak memutus koneksi

**🚦 Gate G3**

---

## Fase 4 · Storage Engine

### Minggu 14 · Filesystem, buffered I/O, page cache, fsync

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca PostgreSQL "Reliability and the Write-Ahead Log"; `man 2 fsync` |
| Implementasi 4j | append-only log: CRC + panjang + tipe; replay + truncate |
| Pengukuran 1j | Benchmark tiga strategi sync; uji pemulihan dengan menyuntikkan kerusakan secara sengaja |
| Retrospeksi 1j | `docs/benchmarks/week14-fsync.md` |

**Penerimaan**:
- [ ] `Flush()` dipanggil sebelum `Sync()`
- [ ] Tiga test pemulihan lolos: kerusakan di ekor / di tengah / setengah record
- [ ] Data throughput untuk tiga strategi sync (perbedaannya harus terlihat sampai level 100×)

---

### Minggu 15 · WAL, MemTable, SSTable, Compaction → `gostore`

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca LevelDB `doc/impl.md`; pahami prinsip Bloom filter |
| Implementasi 4j | MemTable + flush + SSTable (termasuk footer/sparse index) + compaction sederhana |
| Pengukuran 1j | Benchmark tulis berurutan / baca acak; test pemulihan setelah restart |
| Retrospeksi 1j | README + ADR-0002 (LSM vs B-tree) |

**Penerimaan**:
- [ ] Data tetap utuh setelah restart
- [ ] Penghapusan tombstone berfungsi, dan compaction benar-benar membersihkannya
- [ ] Ada test baca lewat jalur SSTable (bukan hanya yang langsung hit MemTable)

---

### Minggu 16 · B-tree, LSM, indeks, transaksi, isolasi

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca DDIA bab 3; baca bagian B+tree di source bbolt |
| Implementasi 4j | B-tree minimal (atau eksperimen perbandingan); tambahkan transaksi mini ke gostore (satu record `TXN_COMMIT` menjamin atomisitas) |
| Pengukuran 1j | Benchmark biaya tulis untuk indeks sekunder; test konkurensi transaksi |
| Retrospeksi 1j | `docs/benchmarks/week16-index.md` + ADR-0003 |

**Penerimaan**:
- [ ] Bisa membandingkan write amplification / read amplification / space amplification antara B-tree dan LSM
- [ ] Biaya indeks punya angka
- [ ] Test atomisitas transaksi lolos (termasuk konkuren)

**🚦 Gate G4**

---

## Fase 5 · Sistem Terdistribusi

### Minggu 17 · Timeout, retry, idempotency

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca "Timeouts, retries and backoff with jitter" (blog AWS) |
| Implementasi 4j | Library retry yang dapat dikonfigurasi (backoff + jitter + budget); layanan idempotent (tabel dedup) |
| Pengukuran 1j | Eksperimen badai retry: 1000 klien × 4 strategi, catat tingkat keberhasilan |
| Retrospeksi 1j | `docs/benchmarks/week17-retry-storm.md` |

**Penerimaan**:
- [ ] Grafik perbandingan tingkat keberhasilan 4 strategi retry
- [ ] Test idempotency: key yang sama secara konkuren hanya dieksekusi sekali
- [ ] Bisa menjelaskan "mengapa jitter lebih baik daripada backoff tetap"

---

### Minggu 18 · Replikasi, pemilihan leader, model konsistensi

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca DDIA bab 5 (replikasi); lihat visualisasi Raft |
| Implementasi 4j | KV primary-replica: tiga mode sinkron/asinkron/quorum; metrik replication lag |
| Pengukuran 1j | 6 test replikasi (termasuk stale read, kegagalan quorum, fencing) |
| Retrospeksi 1j | ADR-0004 + dokumen penjelasan konsistensi |

**Penerimaan**:
- [ ] Matematika `W + R > N` bisa Anda turunkan dan verifikasi
- [ ] Stale read adalah **perilaku yang diharapkan** dan bisa Anda jelaskan
- [ ] Test fencing lolos

---

### Minggu 19 · Konsensus: Raft

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca paper Raft (bagian 1-8); baca bagian jebakan di "Students' Guide to Raft" |
| Implementasi 4j | State machine + pemilihan + replikasi log + penerapan commit |
| Pengukuran 1j | 8 test (termasuk Figure 8, partisi, persistensi); `go test -race -count=20` |
| Retrospeksi 1j | `docs/failure-analysis/raft-partition.md` |

**Penerimaan**:
- [ ] 3 node secara stabil memilih tepat satu leader
- [ ] Test partisi: minoritas tidak commit, konvergen setelah pulih
- [ ] Test Figure 8 lolos (ini yang paling mudah salah)
- [ ] README dengan jujur mencantumkan "apa yang belum diimplementasikan"

---

### Minggu 20 · Sharding, rebalancing, pemulihan kegagalan

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca DDIA bab 6 (partisi); pahami consistent hashing |
| Implementasi 4j | Routing shard + redirect error + skrip migrasi |
| Pengukuran 1j | Jalankan semua matriks injeksi kegagalan (8 jenis kegagalan) |
| Retrospeksi 1j | `docs/failure-analysis/week20-matrix.md` + ADR-0005 |

**Penerimaan**:
- [ ] Injeksi kegagalan **berbasis skrip**, bisa direproduksi dengan satu perintah
- [ ] Tabel matriks terisi penuh dengan hasil pengukuran nyata
- [ ] Bisa menjelaskan tiga risiko selama migrasi

**🚦 Gate G5**

---

## Fase 6 · Rekayasa Produksi

### Minggu 21 · Antrean, semantik pengiriman, Outbox

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca pola "Transactional Outbox"; pahami `FOR UPDATE SKIP LOCKED` |
| Implementasi 4j | Antrean (visibility timeout + DLQ) + konsumsi idempotent + relay Outbox |
| Pengukuran 1j | Test pengiriman ganda; test DLQ; test pengiriman ulang karena visibility timeout |
| Retrospeksi 1j | ADR-0006 |

**Penerimaan**:
- [ ] Bisa menjelaskan tiga semantik pengiriman kata per kata dengan tepat
- [ ] Atomisitas Outbox dibuktikan dengan test
- [ ] DLQ punya alerting dan alat replay

---

### Minggu 22 · Observability

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca dokumen konsep OTel; baca praktik terbaik penamaan Prometheus |
| Implementasi 4j | Metrik Prometheus + log terstruktur `slog` + tracing OTel; jalankan Grafana dengan docker-compose |
| Pengukuran 1j | Lakukan satu latihan triase end-to-end (lihat dokumen `06-*` bagian 22.5) |
| Retrospeksi 1j | `docs/failure-analysis/week22-triage.md` laporan triase |

**Penerimaan**:
- [ ] Metrik RED + USE lengkap, tanpa label berkardinalitas tinggi
- [ ] Trace bisa menyebar lintas layanan/lintas komponen
- [ ] Laporan triase mencantumkan alat dan waktu yang dihabiskan di setiap langkah

---

### Minggu 23 · Perencanaan kapasitas, load test, kontrol overload

| Slot | Isi |
| --- | --- |
| Teori 2j | Pelajari Little's Law dan teori antrean; baca bab "Handling Overload" di buku SRE |
| Implementasi 4j | Rate limiting (token bucket) + circuit breaker + degradasi; skrip load test (beberapa tingkat konkurensi) |
| Pengukuran 1j | Hasilkan tabel load test lengkap (throughput/P50/P90/P99/error rate/CPU/memori) |
| Retrospeksi 1j | `docs/benchmarks/week23-loadtest.md` + ADR-0007 |

**Penerimaan**:
- [ ] Menemukan titik belok throughput (bukan sekadar melaporkan satu angka QPS)
- [ ] Metrik sisi server ikut dikumpulkan saat load test
- [ ] Rate limiting / circuit breaker punya test

---

### Minggu 24 · Trade-off arsitektur, analisis kegagalan, kesiapan produksi

| Slot | Isi |
| --- | --- |
| Teori 2j | Baca template MADR; baca "Postmortem Culture" di buku SRE |
| Implementasi 4j | Integrasikan `go-infrastructure-lab`; lengkapi komponen yang hilang |
| Pengukuran 1j | Load test seluruh rantai + satu latihan kegagalan |
| Retrospeksi 1j | Ringkasan ADR + runbook + checklist kesiapan produksi + retrospeksi akhir |

**Penerimaan**:
- [ ] ≥3 ADR, masing-masing memuat "opsi yang ditolak beserta alasannya"
- [ ] Runbook mencakup ≥5 skenario, setiap skenario lengkap empat elemennya
- [ ] Checklist kesiapan produksi diperiksa per butir, item yang belum tercapai dicantumkan secara eksplisit

**🚦 Gate G6**

---

## Jika Tertinggal: Strategi Pemadatan

Kesalahan paling umum orang yang tertinggal adalah "melompati phase di belakang". Cara pemadatan yang benar:

| Tingkat ketertinggalan | Strategi |
| --- | --- |
| Tertinggal 1-2 pekan | Potong "item bonus" tiap pekan (misalnya Bloom filter di Minggu 15, snapshot di Minggu 19), pertahankan **item penerimaan** |
| Tertinggal 3-4 pekan | Gabungkan Minggu 11+12 (jaringan), Minggu 14+15 (storage); di Fase 5 kerjakan hanya Minggu 17+18,Minggu 19-20 diganti menjadi **membaca paper Raft + menyelesaikan sebagian MIT lab** |
| Tertinggal > 5 pekan | **Jangan terus memaksakan diri maju.** Kembali ke Gate terdekat yang belum lolos, dan selesaikan itu. 24 pekan setengah jadi kalah oleh 16 pekan yang solid |

**Yang tidak boleh dipotong**: Minggu 5 (profiling), Minggu 9 (worker pool), Minggu 13 (framing), Minggu 15 (WAL), Minggu 17 (retry & idempotency). Kelima ini adalah garis batas kemampuan.

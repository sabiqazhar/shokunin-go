# Kumpulan template dokumen

> Salin lalu pakai. Fungsi template bukanlah "mengisi formulir", melainkan **memaksa Anda memikirkan hal-hal yang seharusnya dipikirkan**.
> Field yang ditebalkan di setiap template **tidak boleh dibiarkan kosong**.

---

## 1. Template catatan mingguan(1 jam per minggu)

Nama file: `docs/weekly/week-XX.md`

```markdown
# Minggu XX · <topik>

Tanggal: YYYY-MM-DD ~ YYYY-MM-DD
Fase: Fase N · Gate GN
Waktu: teori __h / implementasi __h / pengukuran __h / retrospeksi __h (total __h / target 8h)

## Target minggu ini
- [ ] Target 1
- [ ] Target 2

## Apa yang dikerjakan
- Mengimplementasikan ______(`pkg/path/file.go`)
- Membaca ______(bab / makalah / tautan)

## Apa yang terukur(harus ada angkanya)

| Skenario | Metrik | Sebelum | Sesudah | Perubahan |
| --- | --- | --- | --- | --- |
| | ns/op | | | |
| | B/op | | | |
| | allocs/op | | | |

Perintah: `______`(harus bisa direproduksi)

## **Di mana saya salah(kolom yang paling penting)**
1. Saya tadinya mengira ______, kenyataannya ______. Sebabnya: ______
2. Hal yang menyita waktu: ______(bagaimana menghindarinya lain kali)

## Belum selesai / TODO
- ______(alasan: waktu kurang / mentok / perubahan prioritas)

## Minggu depan
- Melanjutkan ______
- Fokus menyelesaikan ______

## Cek mandiri penerimaan(bandingkan dengan docs/07)
- [ ] Semua item penerimaan dicentang
- [ ] Ada data pengukuran yang bisa direproduksi
```

**Aturan**: kalau di catatan mingguan kolom "di mana saya salah" tidak berisi apa-apa, berarti minggu itu Anda entah tidak benar-benar mengerjakan, entah tidak benar-benar berpikir.

---

## 2. Template ADR

Nama file: `docs/adr/000N-<topik-keputusan>.md`

```markdown
# ADR-000N: <keputusan dalam satu kalimat>

## Status
Proposed | **Accepted** | Deprecated | Superseded by ADR-000X
Tanggal: YYYY-MM-DD
Pengambil keputusan: <orang atau peran>

## Konteks
**Apa masalahnya? Dengan data apa Anda membuktikan bahwa ini sebuah masalah?**

- Gejala: ______
- Data: ______(angka uji beban, error rate, kurva latensi, tautkan ke docs/benchmarks/)
- Batasan: ______(waktu, orang, tumpukan teknologi yang ada, SLO)

## Keputusan
**Secara konkret memilih apa. Jangan menulis "mempertimbangkan untuk mengadopsi", tulis yang pasti.**

- Solusi: ______
- Parameter kunci: ______(misalnya timeout 5s, antrean 1000, GOGC 200)
- Ruang lingkup: ______(layanan / modul mana)

## Alternatif(**wajib diisi**)

| Opsi | Kelebihan | Kekurangan | Mengapa ditolak |
| --- | --- | --- | --- |
| A | | | |
| B | | | |
| C | | | |

## Konsekuensi

**Positif**: ______
**Negatif**: ______(harus ditulis dengan jujur)
**Risiko baru**: ______
**Yang perlu dipantau**: ______(dalam kondisi apa keputusan ini harus dievaluasi ulang)

## Cara memvalidasi
- Bagaimana membuktikan keputusan ini efektif: ______
- Perintah / metrik konkretnya: ______
- Rencana rollback: ______
```

**Kriteria penerimaan ADR**: ADR tanpa "alternatif + alasan penolakan" tidak lulus —— itu hanya catatan yang dibuat setelah kejadian, bukan sebuah keputusan.

---

## 3. Template laporan benchmark

Nama file: `docs/benchmarks/weekNN-<topik>.md`

```markdown
# Benchmark: <topik>

## Lingkungan(**wajib diisi, kalau tidak datanya tidak bermakna**)
- Mesin: CPU __ core(model __)· memori __ GB · disk __(SSD/HDD, model __)
- OS: __ / kernel __
- Versi Go: __ · GOMAXPROCS=__ · GOGC=__ · GOMEMLIMIT=__
- Beban: mesin penekan dan mesin yang diuji**terpisah atau tidak**: ya / tidak
- Gangguan: apakah program lain dimatikan: ya / tidak

## Perintah reproduksi
```bash
go test -bench=BenchmarkX -benchmem -count=10 ./pkg | tee new.txt
benchstat base.txt new.txt
```

## Hasil

| Benchmark | ns/op | B/op | allocs/op |
| --- | --- | --- | --- |
| | | | |

Perbandingan `benchstat`: 

```
<tempel keluaran aslinya, jangan hanya menulis kesimpulan>
```

## Analisis

- Bottleneck-nya di: ______(sertakan nama file profile / tangkapan layar)
- Sebab utamanya: ______
- Cara optimasinya: ______

## Kesimpulan

- Efektif: ______(naik __%)
- **Tidak efektif**: ______(**harus ditulis**: mengapa tidak efektif)
- Apakah akan digabung: ya / tidak

## Lampiran
- `cpu_before.svg` / `cpu_after.svg`
- `mem.out`
- Data mentah `base.txt` / `new.txt`
```

---

## 4. Template runbook insiden

Nama file: `docs/failure-analysis/runbook.md`

```markdown
# Runbook insiden

## Gambaran layanan
- Nama layanan: ______ · Penanggung jawab: ______
- SLO: ketersediaan __% · P99 < __ms · throughput __ QPS
- Dependensi: ______(layanan hilir / DB / antrean)
- Dashboard utama: <tautan Grafana>
- Daftar alert: <tautan>

---

## Skenario N: <gejala dalam satu kalimat>

### Deteksi
- Aturan alert: `______`(PromQL)
- Ambang pemicu: ______ · Durasi: ______
- Dashboard: <tautan>

### Dampak
- Terlihat oleh pengguna: ______
- Cakupan dampak: ______(seluruh situs / satu endpoint / satu shard)

### Lokalisasi(**jalankan secara berurutan, setiap langkah cantumkan perkiraan durasi**)

| Langkah | Perintah / operasi | Apa yang diamati | Apa artinya |
| --- | --- | --- | --- |
| 1 | `______` | ______ | jika ___ maka ___ |
| 2 | `______` | ______ | |
| 3 | `______` | ______ | |

### Pemulihan(**diurutkan dari risiko terendah ke tertinggi**)

1. ______(operasi + perintah)
2. ______
3. Upaya terakhir: ______(misalnya rollback versi, mengalihkan traffic)

### Pencegahan
- Akar masalah kali ini: ______(wajib diisi setelah kejadian)
- Jangka pendek: ______
- Jangka panjang: ______
- Monitoring baru: ______
```

**Minimal mencakup 5 skenario**(disarankan 8): 

1. Latensi P99 naik
2. Error rate melonjak mendadak(5xx)
3. Memori terus bertumbuh(dugaan kebocoran)
4. Jumlah goroutine meledak
5. Antrean menumpuk dan tidak dikonsumsi
6. Disk penuh
7. Replika tertinggal / replikasi terputus
8. Layanan dependensi tidak tersedia

---

## 5. Template catatan eksperimen injeksi kegagalan

Nama file: `docs/failure-analysis/<nama-eksperimen>.md`

```markdown
# Injeksi kegagalan: <jenis kegagalan>

## Hipotesis(ditulis sebelum eksperimen)
- Kami memperkirakan sistem akan: ______
- Alasannya: ______

## Cara menginjeksi
- Perintah / skrip: `scripts/chaos/____.sh`
- Titik injeksi: ______(node mana / jalur yang mana)
- Durasi: ______

## Metrik yang diamati
- ______
- ______

## Hasil aktual(**diisi setelah eksperimen**)

| Metrik | Ekspektasi | Aktual | Sesuai atau tidak |
| --- | --- | --- | --- |
| | | | |

## Hal yang tidak sesuai dengan hipotesis(**bagian yang paling bernilai**)
- Gejala: ______
- Akar masalah: ______
- Perbaikan: ______

## Kesimpulan
- Sistem di bawah kegagalan ini: tersedia / terdegradasi / tidak tersedia
- Apakah ada data yang hilang: ______
- Yang perlu diperbaiki: ______
```

---

## 6. Template spesifikasi protokol

Nama file: `docs/protocol.md`

```markdown
# Spesifikasi <nama protokol> v1

## Ringkasan
- Lapisan transport: TCP / UDP
- Port: ______
- Model koneksi: request-response / streaming / koneksi panjang
- Encoding: biner / teks
- **Cara framing**: panjang awalan / delimiter / TLV

## Tata letak byte

```
Offset  Panjang  Field    Keterangan
0       1        magic    tetap 0x__
1       1        version  saat ini 0x01
2       1        type     lihat tabel di bawah
3       1        flags    bit __ = __
4       4        length   jumlah byte payload, big-endian, **batas atas __**
8       N        payload
8+N     4        crc32    IEEE, mencakup [0, 8+N)
```

## Jenis pesan

| type | Nama | Arah | Format payload |
| --- | --- | --- | --- |
| 0x01 | PUT | C→S | `[keyLen u16][key][valLen u32][val]` |
| 0x81 | OK | S→C | kosong |

## State machine
(diagram state mermaid)

## Penanganan error

| Kondisi | Perilaku |
| --- | --- |
| magic salah | **tutup koneksi** |
| length melewati batas | kembalikan ERROR + tutup koneksi |
| CRC tidak cocok | tutup koneksi |
| key tidak ada | kembalikan NOT_FOUND, **pertahankan koneksi** |

## Batasan
- Pesan maksimal: __ byte
- Key maksimal: __ byte
- Timeout idle: __ detik(ditutup oleh server)
- Permintaan konkuren: tidak didukung / didukung(pipelining)

## Evolusi versi
- Strategi kompatibilitas v1 → v2: ______
- flags yang tidak dikenali sebaiknya: diabaikan / dilaporkan sebagai error
```

---

## 7. Template PR

Nama file: `.github/pull_request_template.md`

````markdown
## Apa yang diubah
<!-- Satu kalimat. Jangan menulis "memperbaiki bug", tulis "memperbaiki Z yang disebabkan oleh Y pada skenario X" -->

## Mengapa
<!-- Tautkan ke issue / ADR / benchmark -->

## Jenis
- [ ] Fitur baru
- [ ] Perbaikan
- [ ] Optimasi performa(**wajib menyertakan benchstat**)
- [ ] Refactor(tanpa perubahan perilaku)
- [ ] Dokumentasi

## Checklist tinjauan mandiri
- [ ] `gofmt` / `goimports` sudah dijalankan
- [ ] `go vet ./...` tanpa keluaran
- [ ] `golangci-lint run` tanpa peringatan baru
- [ ] Ada tes, dan mencakup jalur gagal
- [ ] Kode konkuren dijalankan dengan `go test -race -count=10`
- [ ] Perubahan performa menyertakan perbandingan `benchstat` sebelum/sesudah
- [ ] Setiap goroutine baru punya jalan keluar
- [ ] Sumber daya(fd / conn / body / ticker)semuanya di-defer penutupannya
- [ ] Pemanggilan eksternal semuanya punya timeout/pembatalan
- [ ] Tidak ada error yang ditelan
- [ ] Dokumentasi sudah disinkronkan

## Dampak performa
<!-- Kalau ada, tempel keluaran benchstat; kalau tidak ada, tulis "tidak ada" -->

```
<tempel di sini>
```

## Keterbatasan yang diketahui
<!-- Hal yang belum dikerjakan / tidak bisa dikerjakan kali ini -->
````

---

## 8. Template README subproyek

```markdown
# <nama proyek>

<!-- Satu kalimat: masalah apa yang ia selesaikan -->

## Tujuan
- 
- 

## Apa yang bukan ini(**wajib diisi, untuk mencegah salah paham**)
- Ia bukan komponen kelas produksi, belum menangani ______
- Tidak menjamin ______

## Arsitektur
<!-- diagram mermaid -->

## Mulai cepat
```bash
make build
make test
./bin/app --config config.yaml
```

## Keputusan desain
| Keputusan | Pilihan | Alasan | Lihat |
| --- | --- | --- | --- |
| | | | ADR-000X |

## Data performa
- Tulis sekuensial: __ ops/s(`make bench`)
- Baca acak: __ ops/s
- Lihat `../../docs/benchmarks/____.md`

## Pengujian
```bash
go test ./...
go test -race ./...        # konkurensi
go test -fuzz=FuzzX ./...  # parsing protokol
```

## **Keterbatasan yang diketahui**
1. ______
2. ______

## Langkah berikutnya(jika ingin dilanjutkan)
- [ ] ______
```

---

## 9. Template retrospeksi kuartal

```markdown
# Retrospeksi kuartal: <periode>

## Status penyelesaian Gate

| Gate | Minggu | Status | Tanggal selesai |
| --- | --- | --- | --- |
| G1 Go internals | 1-6 | ✅/❌ | |
| G2 Concurrency | 7-10 | | |
| G3 Networking | 11-13 | | |
| G4 Storage | 14-16 | | |
| G5 Distributed | 17-20 | | |
| G6 Production | 21-24 | | |

## Penilaian mandiri kemampuan(1-5)

| Dimensi | Awal kuartal | Akhir kuartal | Bukti |
| --- | --- | --- | --- |
| Memori & GC | | | |
| Konkurensi | | | |
| Jaringan | | | |
| Storage | | | |
| Terdistribusi | | | |
| Kualitas rekayasa | | | |

## Tiga hal paling bernilai yang dipelajari
1. 
2. 
3. 

## Tiga hal yang paling banyak menyita waktu
1. (bagaimana menghindarinya lain kali)
2. 
3. 

## Penyesuaian untuk periode berikutnya
- Ritme: ______
- Urutan: ______
- Yang dipotong: ______
```

---

## 10. Template Makefile

```makefile
GO ?= go
BIN := bin
PKGS := ./...

.PHONY: all build test race bench cover lint fmt vet tidy clean profile trace

all: fmt vet lint test

build:
	@mkdir -p $(BIN)
	$(GO) build -o $(BIN)/ ./...

test:
	$(GO) test -count=1 $(PKGS)

race:
	$(GO) test -race -count=1 $(PKGS)

# Simpan baseline: make bench-save
bench-save:
	$(GO) test -bench=. -benchmem -count=10 $(PKGS) > bench-base.txt
	@echo "saved bench-base.txt"

bench:
	$(GO) test -bench=. -benchmem -count=10 $(PKGS) > bench-new.txt
	@benchstat bench-base.txt bench-new.txt 2>/dev/null || cat bench-new.txt

cover:
	$(GO) test -covermode=atomic -coverprofile=cover.out $(PKGS)
	$(GO) tool cover -func=cover.out | tail -1

lint:
	golangci-lint run --timeout=5m

fmt:
	gofmt -w .
	goimports -w .

vet:
	$(GO) vet $(PKGS)

tidy:
	$(GO) mod tidy

profile:
	$(GO) test -bench=BenchmarkHot -cpuprofile=cpu.out -memprofile=mem.out -o bench.test .
	@echo "run: go tool pprof -http=:8080 cpu.out"

trace:
	$(GO) test -run TestX -trace=trace.out .
	@echo "run: go tool trace trace.out"

clean:
	rm -rf $(BIN) *.out bench-*.txt bench.test
```

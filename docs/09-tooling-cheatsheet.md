# Cheatsheet Perkakas

> Prinsipnya: **kuasai sesuai kebutuhan**. Jangan belajar `perf` hanya demi menghafal parameternya — tunggu sampai Anda benar-benar menemui hari di mana "CPU profile tidak menunjukkan masalah".
> Tabel ini disusun berdasarkan "menemui masalah apa → pakai apa", bukan berdasarkan nama perkakasnya.

---

## 1. Diagnosis Dulu, Baru Pilih Perkakas

| Gejala | Langkah 1 | Langkah 2 | Langkah 3 |
| --- | --- | --- | --- |
| CPU tinggi, throughput rendah | `pprof cpu` | `pprof -http` lihat flame graph | `objdump` lihat instruksi panas |
| CPU tidak tinggi, tapi latensi tinggi | `pprof goroutine` | `go tool trace` | block / mutex profile |
| Memori terus naik | `pprof heap -sample_index=inuse_space` | bandingkan dua kali sampling | periksa goroutine / cache |
| GC terlalu sering | `GODEBUG=gctrace=1` | `pprof heap alloc_space` | turunkan laju alokasi |
| Nge-lag sesekali | `go tool trace` | lihat GC dan latensi scheduling | lihat network blocking profile |
| Jumlah koneksi tidak wajar | `ss -s` / `ss -tnp` | lihat `CLOSE_WAIT` | periksa pemanggilan Close di kode |
| fd habis | `lsof -p` / `/proc/pid/fd` | temukan titik kebocorannya | tambahkan tes penghitung fd |
| Penulisan disk lambat | `strace -c -e trace=fsync,write` | `iostat -x` | periksa strategi sync |
| Jaringan lambat | `tcpdump` | `ss -i` (lihat RTT/retransmit) | `netstat -s` |
| Inkonsistensi terdistribusi | lihat log dan term/epoch | injeksi partisi untuk mereproduksi | periksa fencing |

---

## 2. Compiler dan Runtime

```bash
# Escape analysis (yang paling penting)
go build -gcflags="-m=2" ./...                    # alasan lengkap
go build -gcflags="-m" ./...                      # ringkas
go build -gcflags="all=-m" ./...                  # termasuk package dependensi

# Inlining
go build -gcflags="-m=2" ./... 2>&1 | grep inline
go build -gcflags="-l" ./...                      # nonaktifkan inlining
go build -gcflags="-l -l" ./...                   # nonaktifkan lebih kuat

# Assembly
go build -gcflags="-S" ./...                      # cetak assembly ke stdout
go tool objdump -s "main\.myFunc" ./binary        # disassembly fungsi tertentu
go tool objdump ./binary | grep panicBounds       # cari bounds check

# Visualisasi SSA
GOSSAFUNC=myFunc go build ./pkg                   # menghasilkan ssa.html
GOSSAFUNC=myFunc GOSSADIR=./ssa go build ./pkg

# Linking dan binary
go build -ldflags="-s -w" -o app .                # mengecilkan ukuran (mengorbankan info debug)
go tool nm ./app | head                           # tabel simbol
go tool buildid ./app
go version -m ./app                               # lihat info build dan versi dependensi

# Variabel debug runtime
GODEBUG=gctrace=1 ./app                           # log GC
GODEBUG=schedtrace=1000 ./app                     # scheduler mencetak tiap detik
GODEBUG=schedtrace=1000,scheddetail=1 ./app       # lebih terperinci
GODEBUG=inittrace=1 ./app                         # durasi init tiap package
GODEBUG=allocfreetrace=1 ./app                    # setiap alokasi/free (sangat lambat, hanya untuk debug)
GODEBUG=madvdontneed=1 ./app                      # kebijakan pengembalian memori
GODEBUG=netdns=go ./app                           # paksa resolver DNS murni Go
GODEBUG=http2client=0 ./app                       # matikan HTTP/2

# Parameter runtime
GOMAXPROCS=4 ./app
GOGC=200 ./app                                    # GC baru jalan kalau heap tumbuh 200%
GOGC=off ./app                                    # matikan GC otomatis (berbahaya)
GOMEMLIMIT=4GiB ./app                             # batas memori lunak (disarankan diset di container)
GOTRACEBACK=all ./app                             # cetak semua goroutine saat panic
```

---

## 3. Tes dan Benchmark

```bash
# Dasar
go test ./...
go test -v -run TestFoo ./pkg
go test -shuffle=on ./...                         # acak urutannya, temukan ketergantungan antar tes
go test -count=1 ./...                            # nonaktifkan cache (penting!)
go test -timeout=60s ./...

# Race (kode konkuren wajib dijalankan dengan ini)
go test -race ./...
go test -race -count=100 -run TestConcurrent ./...
go test -race -covermode=atomic -coverprofile=cover.out ./...

# Benchmark
go test -bench=. -benchmem ./...
go test -bench=BenchmarkFoo -benchtime=10s ./...
go test -bench=. -benchtime=100x ./...            # jumlah tetap
go test -bench=. -cpu=1,2,4,8 ./...               # beberapa tingkat konkurensi
go test -bench=. -count=10 ./... | tee new.txt    # banyak sampel

# Perbandingan (standar tim)
go install golang.org/x/perf/cmd/benchstat@latest
benchstat base.txt new.txt
benchstat -alpha=0.01 base.txt new.txt            # lebih ketat
benchstat -split-x base.txt new.txt               # dipisah per nama

# Coverage
go test -coverprofile=c.out ./...
go tool cover -html=c.out                         # lihat di browser
go tool cover -func=c.out | tail -1               # total coverage

# Fuzz (Go 1.18+, sangat disarankan untuk parsing protokol)
go test -fuzz=FuzzFrame -fuzztime=2m ./...
# contoh yang gagal akan disimpan ke testdata/fuzz/
```

### Cara Membaca Output `benchstat`

```
name            old time/op    new time/op    delta
Hot-8            1.20µs ± 2%    0.85µs ± 1%   -29.17%  (p=0.000 n=10+10)
```

| Field | Arti |
| --- | --- |
| `± 2%` | Variansi. **Kalau lebih dari 10% berarti lingkungannya tidak bersih dan kesimpulannya tidak bisa dipercaya** |
| `p=0.000` | Signifikansi statistik. Baru bisa dipercaya kalau di bawah 0.05 |
| `n=10+10` | Jumlah sampel. **Minimal 5, disarankan 10** |

---

## 4. Profiling

```bash
# Dihasilkan dari tes
go test -bench=BenchmarkHot -cpuprofile=cpu.out -memprofile=mem.out -o b.test ./pkg
go tool pprof -http=:8080 cpu.out

# Dihasilkan dari layanan yang berjalan (butuh import _ "net/http/pprof")
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/profile?seconds=30
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/heap
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/goroutine?debug=2
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/block
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/mutex
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/allocs

# Lihat langsung dengan curl
curl -s http://localhost:6060/debug/pprof/goroutine?debug=1 | head -50
curl -s http://localhost:6060/debug/pprof/heap?debug=1 | head -30

# Mengganti sudut pandang memori (krusial)
go tool pprof -sample_index=inuse_space  mem.out   # yang sedang ditahan → cari kebocoran
go tool pprof -sample_index=alloc_space  mem.out   # alokasi kumulatif → cari beban GC
go tool pprof -sample_index=alloc_objects mem.out  # jumlah kumulatif

# Perintah interaktif
(pprof) top                    # Top berdasarkan waktu sendiri
(pprof) top --cum              # waktu kumulatif (termasuk rantai panggilan)
(pprof) list funcName          # biaya per baris
(pprof) peek regex             # lihat hulu dan hilir suatu simbol
(pprof) traces                 # semua stack yang tersampling
(pprof) web                    # butuh graphviz
(pprof) png > out.png

# Execution trace
go test -run TestX -trace=trace.out ./pkg
go tool trace trace.out
go tool trace -http=:8080 trace.out
# Ekstraksi lewat command line (Go 1.21+)
go tool trace -pprof=net trace.out > net.pprof
```

### Cara Mengaktifkan Masing-Masing Profile

| Profile | Aktif secara default? | Cara mengaktifkan |
| --- | --- | --- |
| CPU | Frekuensi sampling ~100Hz, mulai bersama pprof | otomatis |
| Heap | Sampling default (satu sampel tiap alokasi 512KB) | otomatis; `runtime.MemProfileRate` bisa disetel |
| Goroutine | Snapshot | otomatis |
| Block | **Nonaktif secara default** | `runtime.SetBlockProfileRate(1)` |
| Mutex | **Nonaktif secara default** | `runtime.SetMutexProfileFraction(1)` |

> Kalau ingin menyelidiki "CPU tidak tinggi tapi sangat lambat", **Anda harus mengaktifkan block/mutex profile terlebih dahulu**, kalau tidak yang Anda dapat hanya file kosong.

---

## 5. Perkakas Sistem Linux

```bash
# Proses dan thread
ps -eLf                                  # -L menampilkan thread
top -H -p <pid>                          # CPU per thread
pidstat -t -p <pid> 1                    # statistik per thread
cat /proc/<pid>/status                   # Threads / VmRSS / VmSize
cat /proc/<pid>/limits                   # batas sumber daya (termasuk Max open files)
cat /proc/<pid>/io                       # jumlah byte baca/tulis (jagoan untuk troubleshooting I/O)
cat /proc/<pid>/smaps_rollup             # ringkasan memori
cat /proc/<pid>/stack                    # stack kernel (butuh hak akses)

# File descriptor
lsof -p <pid>
ls /proc/<pid>/fd | wc -l
lsof -i :8080                            # siapa yang memakai port ini
cat /proc/sys/fs/file-nr                 # pemakaian fd di level sistem

# System call
strace -f -c -p <pid>                    # statistik (akan memperlambat, hati-hati di produksi)
strace -f -e trace=network ./app
strace -f -e trace=file ./app
strace -f -e trace=write,fsync ./app
strace -f -tt -T -o trace.txt ./app      # dengan timestamp dan durasi
strace -f -c -e trace=epoll_pwait,futex,write ./app

# Memori
free -m
vmstat 1                                 # si/so (swap), cs (context switch)
sar -r 1
pmap -x <pid>

# CPU
mpstat -P ALL 1
pidstat -u -p <pid> 1
perf top -p <pid>                        # butuh linux-tools
perf record -F 99 -g -p <pid> -- sleep 30 && perf report

# I/O disk
iostat -x 1                              # %util, await, svctm
iotop -o
blktrace -d /dev/sda -o - | blkparse -i -
```

### Context Switch dan Interrupt

```bash
vmstat 1
# Perhatikan:
#   cs  context switch per detik (kalau lebih dari 100 ribu harus diselidiki)
#   in  interrupt per detik
#   r   panjang run queue (kalau terus-menerus lebih dari jumlah core CPU berarti overload)
#   b   uninterruptible sleep (status D, biasanya mentok di I/O)
```

---

## 6. Perkakas Jaringan

```bash
# Status koneksi (ss menggantikan netstat)
ss -lntp                                 # port listening + prosesnya
ss -tnp                                  # semua koneksi TCP
ss -tnp state established '( sport = :8080 )'
ss -s                                    # ringkasan
ss -i                                    # menampilkan RTT, cwnd, retransmit (sangat berguna)
ss -tnp state close-wait                 # cari penumpukan CLOSE_WAIT ← tanda bug di kode
ss -tnp state time-wait | wc -l

# Statistik protokol
netstat -s                               # retransmit, hitungan error
nstat -az                                # lebih mudah dibaca

# Menangkap paket
tcpdump -i lo -nn -X port 8080
tcpdump -i any -nn -w out.pcap port 8080
tcpdump -r out.pcap -X | less
tcpdump -i lo -nn 'tcp[tcpflags] & tcp-syn != 0'
tcpdump -i lo -nn 'tcp[tcpflags] & tcp-rst != 0'
tcpdump -i lo -nn -A 'tcp port 8080'     # ASCII (untuk debug protokol plaintext)

# Proba manual
nc -vz host port                         # konektivitas
nc -v host port                          # interaktif
printf 'GET / HTTP/1.0\r\n\r\n' | nc host 80
printf '\x9b\x01\x01\x00\x00\x00\x00\x05hello' | nc localhost 8080 | xxd

# TLS
openssl s_client -connect host:443 -servername host
openssl x509 -in cert.pem -noout -text

# DNS
dig +short example.com
dig +trace example.com
nslookup example.com
```

### Injeksi Kegagalan Jaringan (butuh root / NET_ADMIN)

```bash
# Latensi
tc qdisc add dev eth0 root netem delay 100ms 20ms distribution normal
# Packet loss
tc qdisc add dev eth0 root netem loss 5%
# Reorder + duplikasi
tc qdisc add dev eth0 root netem reorder 5% delay 20ms
# Pembatasan bandwidth
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
# Membersihkan
tc qdisc del dev eth0 root

# Lingkungan Docker
docker run --cap-add=NET_ADMIN ...
docker exec node-b sh -c "tc qdisc add dev eth0 root netem delay 200ms"
```

### Simulasi Partisi

```bash
# Docker Compose
docker network disconnect mynet node-c
docker network connect mynet node-c

# iptables
iptables -A INPUT -s <other-node-ip> -j DROP
iptables -D INPUT -s <other-node-ip> -j DROP
```

---

## 7. Perkakas Load Testing

```bash
# vegeta (pilihan utama di ekosistem Go, outputnya ramah)
echo "GET http://localhost:8080/api" | vegeta attack -rate=100/s -duration=60s | vegeta report
vegeta attack -targets=targets.txt -rate=0 -max-workers=100 -duration=60s > r.bin
vegeta report -type=text r.bin
vegeta report -type=json r.bin > r.json
vegeta plot r.bin > plot.html
vegeta encode --to csv r.bin > r.csv

# Dengan body
echo "POST http://localhost:8080/api" | \
  vegeta attack -body=payload.json -header="Content-Type: application/json" \
  -rate=50/s -duration=30s | vegeta report

# Tekanan bertahap (step)
for r in 10 50 100 200 500 1000; do
  echo "GET http://localhost:8080/api" | \
    vegeta attack -rate=$r/s -duration=30s > r_$r.bin
  echo "=== $r ==="; vegeta report r_$r.bin | head -12
done

# wrk
wrk -t4 -c100 -d30s --latency http://localhost:8080/api
wrk -t4 -c100 -d30s -s post.lua http://localhost:8080/api

# hey (sederhana)
hey -n 10000 -c 100 http://localhost:8080/api

# Database
pgbench -c 20 -T 60 -j 4 mydb
sysbench oltp_read_write --threads=16 --time=60 run
```

### Hal yang Wajib Dikumpulkan Bersamaan Saat Load Testing

```bash
# Metrik sisi server (dijalankan bersamaan dengan load test)
curl -s http://localhost:6060/debug/pprof/heap > heap_$r.out
curl -s localhost:9090/metrics | grep -E 'queue_depth|goroutines|gc_'
GODEBUG=gctrace=1 ./app 2> gc.log

# Metrik sistem
sar -u -r -n DEV 1 60 > sys.log
iostat -x 1 60 > io.log
```

---

## 8. Container dan Orkestrasi

```bash
# Batasan sumber daya dan pengamatannya
docker run --memory=512m --cpus=2 ...
docker stats
docker inspect <id> | jq '.[0].HostConfig.Memory'

# Melihat batasan cgroup dari dalam container (program Go perlu menyadarinya)
cat /sys/fs/cgroup/memory.max            # cgroup v2
cat /sys/fs/cgroup/cpu.max
cat /sys/fs/cgroup/memory/memory.limit_in_bytes   # cgroup v1

# Kunci: buat Go menyadari cgroup
#   CPU:    go.uber.org/automaxprocs
#   Memori: set GOMEMLIMIT ke 80~90% dari limit
docker run -e GOMEMLIMIT=460MiB --memory=512m myapp

# Keluar secara graceful
docker stop <id>          # kirim SIGTERM, setelah grace period kirim SIGKILL
docker kill -s TERM <id>
# Catatan: PID 1 di dalam container yang tidak menangani sinyal akan dibunuh paksa setelah timeout 10 detik
#   Solusinya: pakai tini atau docker run --init
```

---

## 9. Alias Lokal yang Disarankan (tambahkan ke `~/.zshrc` / `~/.bashrc`)

```bash
alias gt='go test ./...'
alias gtr='go test -race ./...'
alias gtb='go test -bench=. -benchmem -count=10'
alias gtc='go test -coverprofile=/tmp/c.out ./... && go tool cover -html=/tmp/c.out'
alias gv='go vet ./...'
alias gm='go build -gcflags="-m=2"'
alias prof='go tool pprof -http=:8080'
alias ssa='GOSSAFUNC'
alias benchcmp='benchstat'
```

---

## 10. Prioritas Penguasaan Perkakas (jangan serakah)

| Prioritas | Perkakas | Kapan wajib dikuasai |
| --- | --- | --- |
| **P0 (bulan 1)** | `go test -race`, `-benchmem`, `-m=2`, `pprof -http`, `benchstat`, `gofmt`, `go vet` | sekarang juga |
| **P1 (bulan 2-3)** | `go tool trace`, `strace`, `ss`, `tcpdump`, `lsof`, `objdump` | saat menemui masalah yang bersangkutan |
| **P2 (bulan 5-6)** | `vegeta`, `docker network`, `tc netem`, `OTel`, `Prometheus` | Fase 6 |
| **P3 (sesuai kebutuhan)** | `perf`, `blktrace`, `bpftrace`, `Wireshark` | pelajari saat benar-benar perlu |

**Jangan** mempelajari sebuah perkakas hanya demi mencentang tabel ini. Perkakas itu digerakkan oleh gejala: begitu Anda menemui masalah "CPU tidak tinggi tapi latensi tinggi", barulah `strace` dan block profile benar-benar masuk ke memori otot Anda.

## Apa yang diubah

<!-- Satu kalimat. Jangan menulis "memperbaiki bug", tulis "memperbaiki Z yang disebabkan oleh Y pada skenario X". -->

## Mengapa

<!-- Tautkan ke issue / ADR / laporan benchmark -->

## Jenis perubahan

- [ ] Fitur baru
- [ ] Perbaikan
- [ ] Optimasi performa (**wajib menyertakan perbandingan benchstat**)
- [ ] Refactor (tanpa perubahan perilaku)
- [ ] Dokumentasi

## Checklist swa-review

> Centang satu per satu. Yang tidak dicentang wajib dijelaskan alasannya di bawah.

- [ ] `gofmt` / `goimports` sudah dijalankan
- [ ] `go vet ./...` tanpa output
- [ ] `golangci-lint run` tanpa peringatan baru
- [ ] Ada test, dan mencakup jalur gagal (bukan cuma happy path)
- [ ] Kode konkuren dijalankan dengan `go test -race -count=10`
- [ ] Perubahan performa menyertakan perbandingan `benchstat` sebelum/sesudah
- [ ] Setiap goroutine baru punya jalur keluar yang pasti
- [ ] Resource (fd / conn / body / ticker / rows) semuanya di-`defer close`
- [ ] Semua pemanggilan eksternal punya timeout / cancellation
- [ ] Tidak ada error yang ditelan (tidak ada `_ = err`, `_ = f()`)
- [ ] Antrean / worker / connection pool semuanya berbatas (bounded)
- [ ] Dokumentasi dan README sudah disinkronkan

## Khusus konkurensi / resource (isi hanya jika relevan)

- [ ] Pihak yang menutup channel tunggal dan jelas
- [ ] State bersama punya sinkronisasi (lock / atomic / channel)
- [ ] Tidak ada I/O sambil memegang lock
- [ ] `WaitGroup.Add` dipanggil di luar goroutine
- [ ] Ada test deteksi kebocoran goroutine / fd

## Dampak performa

<!-- Jika ada, tempel output benchstat. Jika tidak, tulis "tidak ada" -->

```
<tempel output benchstat di sini>
```

## Keterbatasan yang diketahui / yang belum dikerjakan

<!-- Hal yang sengaja tidak dikerjakan atau tidak bisa dikerjakan. Tulis jelas, jangan biarkan reviewer menebak -->

-

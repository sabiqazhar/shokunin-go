GO ?= go
BIN := bin
PKGS := ./...

.PHONY: all build test race bench bench-save cover lint fmt vet tidy clean \
        profile trace leak fuzz docker-up docker-down help

all: fmt vet lint test ## Bawaan: format + vet + lint + test

help: ## Tampilkan bantuan
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

build: ## Kompilasi
	@mkdir -p $(BIN)
	$(GO) build -o $(BIN)/ ./...

test: ## Unit test
	$(GO) test -count=1 $(PKGS)

race: ## Deteksi race (wajib untuk kode konkuren)
	$(GO) test -race -count=10 $(PKGS)

leak: ## Deteksi kebocoran goroutine (butuh go.uber.org/goleak)
	$(GO) test -run TestLeak -count=1 $(PKGS)

fuzz: ## Fuzz test (ganti variabel FUZZ untuk menentukan target, default 2 menit)
	$(GO) test -fuzz=$(FUZZ) -fuzztime=2m $(PKGS)

bench-save: ## Simpan baseline performa
	$(GO) test -bench=. -benchmem -count=10 $(PKGS) > bench-base.txt
	@echo "bench-base.txt tersimpan"

bench: ## Jalankan benchmark lalu bandingkan dengan baseline
	$(GO) test -bench=. -benchmem -count=10 $(PKGS) > bench-new.txt
	@benchstat bench-base.txt bench-new.txt 2>/dev/null || cat bench-new.txt

cover: ## Coverage
	$(GO) test -covermode=atomic -coverprofile=cover.out $(PKGS)
	$(GO) tool cover -func=cover.out | tail -1

lint: ## golangci-lint
	golangci-lint run --timeout=5m

fmt: ## Format
	gofmt -w .
	@command -v goimports >/dev/null 2>&1 && goimports -w . || true

vet: ## go vet
	$(GO) vet $(PKGS)

tidy: ## Rapikan dependensi
	$(GO) mod tidy

profile: ## Profil CPU + memori
	$(GO) test -bench=. -benchtime=5s \
	  -cpuprofile=cpu.out -memprofile=mem.out -o bench.test .
	@echo "Langkah berikutnya:  go tool pprof -http=:8080 cpu.out"
	@echo "        go tool pprof -sample_index=alloc_space -http=:8080 mem.out"

trace: ## Execution trace (ganti variabel RUN untuk menentukan test)
	$(GO) test -run $(RUN) -trace=trace.out .
	@echo "Langkah berikutnya:  go tool trace trace.out"

docker-up: ## Nyalakan stack observability
	docker compose -f docker-compose.observability.yml up -d

docker-down: ## Matikan stack observability
	docker compose -f docker-compose.observability.yml down

clean: ## Bersihkan artefak
	rm -rf $(BIN) *.out bench-*.txt bench.test


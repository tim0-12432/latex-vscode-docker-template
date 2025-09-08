# Benchmark

## Usage

1. Save local TexLive iamge to benchmark folder
```bash
docker image save texlive/texlive:latest -o ./texlive.tar
```

2. Build image
```bash
docker build -t latex-template-benchmark:latest -f .\benchmark\Dockerfile .
```

3. Execute with mode as you wish
```bash
docker run --privileged --rm -it -e MODE=<mode> latex-template-benchmark:latest
```

Mode can be one of 
- `ORIGINAL`: Generation process without any adjustments
- `MAKEGLOSSARIES`: Pre-generate glossaries as additional step 
- `DRAFTING`: Change pdflatex to not ourput to pdf
- `NOCONSOLE`: Change pdflatex to not log to console
- `PREAMBLE`: Pre-compile all libraries in the preamble
- `COMBINED`: All optimizing steps combined

## Results

|                           | Original | makeglossaries | Draft | No console | Preamble | Combined |
| ---:                      | ---     | ---     | ---     | ---   | ---   | ---   |
| Compilation Time          | 24.141s | 18.162s | 14.240s | 19.376s | 13.685s | 10.594s |
| Compilation Time per Page | 1.341s  | 1.009s  | 0.791s  | 1.076s  | 0.760s  | 0.589s  |
| Increase to Original      | 0       | 24.767% | 41.013% | 19.738% | 43.312% | 56.116% |

> **Used Hardware**: AMD Ryzen 7 PRO 4750U with Radeon iGPU, 32GB RAM, Samsung 980 1TB NVMe

> **Used Software**: Win11 24H2, TeX Live 2024 Docker image with pdfTex 3.141592653-2.6-1.40.26

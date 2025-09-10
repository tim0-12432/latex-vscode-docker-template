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

Using the template document with 18 pages.

|                           | Original | makeglossaries | Draft | No console | Preamble | Combined |
| ---:                      | ---     | ---     | ---     | ---   | ---   | ---   |
| Compilation Time          | 30.778s | 16.710s | 16.171s | 13.225s | 13.160s | 9.212s |
| Compilation Time per Page | 1.710s  | 0.928s  | 0.898s  | 0.735s  | 0.731s  | 0.512s  |
| Increase to Original      | 0       | 45.708% | 47.459% | 57.031% | 57.242% | 70.070% |
| Compile Time for each step| 10.86, 1.49, 9.40, 9.03 | 6.12, 0.73, 0.98, 4.23, 4.65 | 6.52, 0.78, 4.35, 4.53 | 4.82, 0.95, 3.73, 3.73 | 6.54, 1.88, 0.73, 1.96, 2.06 | 4.10, 1.25, 0.73, 0.66, 1.20, 1.23 |

> **Used Hardware**: AMD Ryzen 7 PRO 4750U with Radeon iGPU, 32GB RAM, Samsung 980 1TB NVMe

> **Used Software**: Win11 24H2, TeX Live 2024 Docker image with pdfTex 3.141592653-2.6-1.40.26

# Pico SDKマップファイル解析スクリプト

Pico SDKのマップファイルを解析するPythonスクリプト

## 概要ℹ️

Pico SDKでビルド時に生成されるRP2040、RP2350のマップファイル（*.map）を
スクリプトで解析してROM,RAMの使用量を表示する

## 使い方 💻

```bash
python picosdk_mapfile_parse.py
```

```bash
python picosdk_mapfile_parse.py [mapファイルのパス]
```

### 出力例 📊

※自動的にlogフォルダが生成されログファイル保存📚️

```shell
使用するファイル: C:\dev_work\git\my\rp2350_dev\picosdk_mapfile_paser_py\rp2350_dev.elf.map

【RP2040/RP2350 マップ解析スクリプト】

Copyright (c) 2025 Chimipupu(https://github.com/Chimipupu)

マップファイル: C:\dev_work\git\my\rp2350_dev\picosdk_mapfile_paser_py\rp2350_dev.elf.map

=== フラッシュ使用量 ===
.text                 76,084 bytes ( 74.30 KB)
.rodata               47,768 bytes ( 46.65 KB)
.init                     20 bytes (  0.02 KB)
.fini                    112 bytes (  0.11 KB)
.ARM.exidx                32 bytes (  0.03 KB)
合計使用量:          124,016 bytes (121.11 KB)
Flash容量:         4,194,304 bytes (  4.00 MB)
使用率:              2.96%

=== RAM使用量 ===
.data                  7,344 bytes (  7.17 KB)
.bss                   4,656 bytes (  4.55 KB)
.stack                 8,192 bytes (  8.00 KB)
.heap                  4,096 bytes (  4.00 KB)
合計使用量:           24,288 bytes ( 23.72 KB)
SRAM容量:            524,288 bytes (512.00 KB)
使用率:               4.63%

Script execution completed.
```

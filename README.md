# Pico SDKマップファイル解析スクリプト

Pico SDKのマップファイルを解析するPythonスクリプト

## 概要ℹ️

Pico SDKでRP2040、RP2350をビルドして生成されるマップファイル（*.map）
スクリプトは下記を解析して各種使用量を表示する

## 解析対象

### フラッシュメモリの使用状況 💾
- コードセクション 📝
  - `.text` - 実行コード
  - `.init` - 初期化コード
  - `.fini` - 終了コード
- データセクション 📊
  - `.rodata` - 読み取り専用データ
  - `.data.rel.ro` - 読み取り専用の相対データ
- ARM関連セクション 🔧
  - `.ARM.extab` - ARM例外処理テーブル
  - `.ARM.exidx` - ARM例外インデックス
  - `.ARM.attributes` - ARM属性
- デバッグ情報 🐛
  - `.debug_info` - デバッグ情報
  - `.debug_abbrev` - デバッグ省略情報
  - `.debug_loc` - デバッグ位置情報
  - `.debug_aranges` - デバッグアドレス範囲
  - `.debug_ranges` - デバッグ範囲情報
  - `.debug_line` - デバッグ行情報
  - `.debug_str` - デバッグ文字列
- その他 📋
  - `.comment` - コンパイラやリンカが生成するメタデータ（コンパイラバージョン、ビルド環境情報など）。フラッシュROMに保存される読み取り専用データ
- メモリ使用量 📈
  - 合計使用量（バイト、KB）
  - Flash容量（バイト、MB）
  - 使用率（%）

### SRAMの使用状況 🧠
- データセクション 📊
  - `.data` - 初期化済みデータ
  - `.bss` - 未初期化データ
  - `.noinit` - 初期化不要データ
- システムセクション ⚙️
  - `.ram_vector_table` - RAMベクターテーブル
  - `.stack` - スタック領域
  - `.heap` - ヒープ領域
- メモリ使用量 📈
  - 合計使用量（バイト、KB）
  - SRAM容量（バイト、KB）
  - 使用率（%）

## 自動検索機能 🔍

mapファイルのパスを指定しない場合は下記の場所を自動的に検索する

1. スクリプトと同じディレクトリの `src/build/` 内の任意の `.map` ファイル
2. スクリプトと同じディレクトリ内の任意の `.map` ファイル
3. 親ディレクトリの `build/` 内の任意の `.map` ファイル

各ディレクトリ内で最初に見つかった `.map` ファイルが使用される

## 使い方 💻

```bash
python picosdk_mapfile_parse.py
```

```bash
python picosdk_mapfile_parse.py [mapファイルのパス]
```

### 出力例 📊

```shell
C:\dev_work\git\my\rp2350_dev\src>python picosdk_mapfile_parse.py
Pico SDK Map File Parser
Copyright (c) 2025 Chimipupu(https://github.com/Chimipupu)

探している場所: C:\dev_work\git\my\rp2350_dev\src\src\build\*.map
探している場所: C:\dev_work\git\my\rp2350_dev\src\*.map

【RP2040/RP2350 マップ解析スクリプト】

Copyright (c) 2025 Chimipupu(https://github.com/Chimipupu)

マップファイル: C:\dev_work\git\my\rp2350_dev\src\rp2350_dev.elf.map

=== フラッシュ使用量 ===
.text                 77,774 bytes ( 75.95 KB)
.rodata               51,240 bytes ( 50.04 KB)
.init                     20 bytes (  0.02 KB)
.fini                    112 bytes (  0.11 KB)
.ARM.exidx                32 bytes (  0.03 KB)
.comment               5,878 bytes (  5.74 KB)
.debug_info          589,892 bytes (576.07 KB)
.debug_abbrev        103,246 bytes (100.83 KB)
.debug_aranges         7,088 bytes (  6.92 KB)
.debug_line          324,835 bytes (317.22 KB)
.debug_str           253,317 bytes (247.38 KB)
合計使用量:        1,413,434 bytes (1380.31 KB)
Flash容量:         4,194,304 bytes (  4.00 MB)
使用率:             33.70%

=== RAM使用量 ===
.data                  5,476 bytes (  5.35 KB)
.bss                   4,605 bytes (  4.50 KB)
.stack                 8,192 bytes (  8.00 KB)
.heap                  4,096 bytes (  4.00 KB)
合計使用量:           22,369 bytes ( 21.84 KB)
SRAM容量:            524,288 bytes (512.00 KB)
使用率:               4.27%
```

## 注意事項 ⚠️

- ※スクリプトはマップファイルをUTF-8でエンコードして読み込む
- ※相対パスで指定した場合、スクリプトからの相対パスとして解釈される
- ※マップファイルが見つからない場合は、エラーメッセージと使用方法が表示されます
- ※出力されるサイズは、Byte単位とKB/MB単位の両方で表示される
- ※使用率は小数点以下2桁まで表示される

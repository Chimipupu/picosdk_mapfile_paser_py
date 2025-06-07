# Pico SDKマップファイル解析スクリプト

Pico SDKのマップファイルを解析するPythonスクリプト

## 概要

このスクリプトは、Raspberry Pi Picoのビルド時に生成されるマップファイル（.map）を解析し、以下の情報を表示します：

## 解析対象

### フラッシュメモリの使用状況

- コードセクション
  - `.text` - 実行コード
  - `.init` - 初期化コード
  - `.fini` - 終了コード
- データセクション
  - `.rodata` - 読み取り専用データ
  - `.data.rel.ro` - 読み取り専用の相対データ
- ARM関連セクション
  - `.ARM.extab` - ARM例外処理テーブル
  - `.ARM.exidx` - ARM例外インデックス
  - `.ARM.attributes` - ARM属性
- デバッグ情報
  - `.debug_info` - デバッグ情報
  - `.debug_abbrev` - デバッグ省略情報
  - `.debug_loc` - デバッグ位置情報
  - `.debug_aranges` - デバッグアドレス範囲
  - `.debug_ranges` - デバッグ範囲情報
  - `.debug_line` - デバッグ行情報
  - `.debug_str` - デバッグ文字列
- その他
  - `.comment` - コンパイラやリンカが生成するメタデータ（コンパイラバージョン、ビルド環境情報など）。フラッシュROMに保存される読み取り専用データ
- メモリ使用量
  - 合計使用量（バイト、KB）
  - Flash容量（バイト、MB）
  - 使用率（%）

### SRAMの使用状況
- データセクション
  - `.data` - 初期化済みデータ
  - `.bss` - 未初期化データ
  - `.noinit` - 初期化不要データ
- システムセクション
  - `.ram_vector_table` - RAMベクターテーブル
  - `.stack` - スタック領域
  - `.heap` - ヒープ領域
- メモリ使用量
  - 合計使用量（バイト、KB）
  - SRAM容量（バイト、KB）
  - 使用率（%）

## 自動検索機能

mapファイルのパスを指定しない場合、スクリプトは以下の場所を自動的に検索します：

1. スクリプトと同じディレクトリの `src/build/` 内の任意の `.map` ファイル
2. スクリプトと同じディレクトリ内の任意の `.map` ファイル
3. 親ディレクトリの `build/` 内の任意の `.map` ファイル

各ディレクトリ内で最初に見つかった `.map` ファイルが使用されます。

## 使い方

```bash
python picosdk_mapfile_parse.py
```

```bash
python picosdk_mapfile_parse.py [mapファイルのパス]
```

### 出力例

```shell
C:\dev_work\git\my\picosdk_mapfile_paser_py>python picosdk_mapfile_parse.py

Pico SDK Map File Parser
Copyright (c) 2025 Chimipupu(https://github.com/Chimipupu)

探している場所: C:\dev_work\git\my\picosdk_mapfile_paser_py\src\build\*.map
探している場所: C:\dev_work\git\my\picosdk_mapfile_paser_py\*.map

解析ファイル: C:\dev_work\git\my\picosdk_mapfile_paser_py\rp2350_dev.elf.map

=== フラッシュ使用量 ===
.text                 46,064 bytes ( 44.98 KB)
.rodata               16,852 bytes ( 16.46 KB)
.init                     20 bytes (  0.02 KB)
.fini                     96 bytes (  0.09 KB)
合計使用量:           63,032 bytes ( 61.55 KB)
Flash容量:         4,194,304 bytes (  4.00 MB)
使用率:           1.50%

=== RAM使用量 ===
.data                  4,896 bytes (  4.78 KB)
.bss                   3,925 bytes (  3.83 KB)
合計使用量:            8,821 bytes (  8.61 KB)
SRAM容量:            524,288 bytes (512.00 KB)
使用率:           1.68%
```

## 注意事項

- ※スクリプトはマップファイルをUTF-8でエンコードして読み込む
- ※相対パスで指定した場合、スクリプトからの相対パスとして解釈される
- ※マップファイルが見つからない場合は、エラーメッセージと使用方法が表示されます
- ※出力されるサイズは、Byte単位とKB/MB単位の両方で表示される
- ※使用率は小数点以下2桁まで表示される

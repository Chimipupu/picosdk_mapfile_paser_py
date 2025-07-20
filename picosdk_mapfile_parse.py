import sys
import re
import os
import datetime
from pathlib import Path

class Tee:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()

def print_header():
    print("Pico SDK Map File Parser")
    print("Copyright (c) 2025 Chimipupu(https://github.com/Chimipupu)")
    print()

def find_map_file(map_path=None):
    # スクリプトの場所を基準にする
    script_dir = Path(__file__).parent
    parent_dir = script_dir.parent
    print(f'スクリプトの場所: {script_dir}')
    print(f'親ディレクトリ: {parent_dir}')

    if map_path is None:
        # 検索するディレクトリとパターンのリスト
        search_locations = [
            (script_dir, '*.map'),              # スクリプトディレクトリ直下
            (script_dir, 'build/*.map'),        # スクリプトディレクトリ/build/
            (script_dir, 'src/build/*.map'),    # スクリプトディレクトリ/src/build/
            (parent_dir, '*.map'),              # 親ディレクトリ直下
            (parent_dir, 'build/*.map'),        # 親ディレクトリ/build/
            (parent_dir, 'src/build/*.map'),    # 親ディレクトリ/src/build/
            (parent_dir, 'src/../build/*.map'), # 親ディレクトリの各サブディレクトリ/build/
        ]

        all_map_files = []
        for base_dir, pattern in search_locations:
            found_files = list(base_dir.glob(pattern))
            all_map_files.extend(found_files)
            print(f'検索: {base_dir / pattern}')
            print(f'  見つかったファイル数: {len(found_files)}')
            for file in found_files:
                print(f'    -> {file}')

        if all_map_files:
            print(f'\n使用するファイル: {all_map_files[0]}')
            return str(all_map_files[0])
        print('エラー: mapファイルが見つかりません。')

        # 実際にファイルが存在するか手動確認
        print('\n手動確認:')
        script_maps = list(script_dir.glob('*.map'))
        parent_maps = list(parent_dir.glob('*.map'))
        print(f'スクリプトディレクトリの.mapファイル: {script_maps}')
        print(f'親ディレクトリの.mapファイル: {parent_maps}')
        sys.exit(1)

    # 相対パスの場合は、スクリプトの場所からの相対パスとして解釈
    if not os.path.isabs(map_path):
        resolved_path = script_dir / map_path
        map_path = str(resolved_path)

    # パスの存在確認
    if not os.path.exists(map_path):
        print(f'エラー: ファイル {map_path} が見つかりません。')
        print('現在の作業ディレクトリ:', os.getcwd())
        sys.exit(1)
    return map_path

def parse_map_file(map_path):
    # セクションの分類
    flash_sections = {
        '.text': 0,              # 実行コード
        '.rodata': 0,            # 読み取り専用データ
        '.data.rel.ro': 0,       # 読み取り専用の相対データ
        '.init': 0,              # 初期化コード
        '.fini': 0,              # 終了コード
        '.ARM.extab': 0,         # ARM例外処理テーブル
        '.ARM.exidx': 0,         # ARM例外インデックス
        '.ARM.attributes': 0,    # ARM属性
        # '.comment': 0,           # コメント情報
        # '.debug_info': 0,        # デバッグ情報
        # '.debug_abbrev': 0,      # デバッグ省略情報
        # '.debug_loc': 0,         # デバッグ位置情報
        # '.debug_aranges': 0,     # デバッグアドレス範囲
        # '.debug_ranges': 0,      # デバッグ範囲情報
        # '.debug_line': 0,        # デバッグ行情報
        # '.debug_str': 0,         # デバッグ文字列
    }
    ram_sections = {
        '.data': 0,              # 初期化済みデータ
        '.bss': 0,               # 未初期化データ
        '.ram_vector_table': 0,  # RAMベクターテーブル
        '.stack': 0,             # スタック領域
        '.heap': 0,              # ヒープ領域
        '.noinit': 0,            # 初期化不要データ
    }

    # メモリ設定の初期値
    flash_capacity = 0
    ram_capacity = 0

    try:
        with open(map_path, encoding='utf-8', errors='ignore') as f:
            for line in f:
                # メモリ設定の行を探す
                # 例: FLASH           0x10000000    0x200000
                # 例: RAM             0x20000000    0x42000
                m = re.match(r'\s*(FLASH|RAM)\s+0x[0-9a-fA-F]+\s+0x([0-9a-fA-F]+)', line)
                if m:
                    memory_type = m.group(1)
                    size = int(m.group(2), 16)
                    if memory_type == 'FLASH':
                        flash_capacity = size
                    elif memory_type == 'RAM':
                        ram_capacity = size
                    continue

                # セクション行のパターン: .text           0x10000100    0x1234
                m = re.match(r'\s*(\.\S+)\s+0x[0-9a-fA-F]+\s+0x([0-9a-fA-F]+)', line)
                if m:
                    section = m.group(1)
                    size = int(m.group(2), 16)
\
                    # メインセクションの判定
                    main_section = section.split('.')[1] if '.' in section else section

                    # フラッシュセクションの処理
                    for flash_section in flash_sections:
                        if section.startswith(flash_section):
                            flash_sections[flash_section] += size
                            break

                    # RAMセクションの処理
                    for ram_section in ram_sections:
                        if section.startswith(ram_section):
                            ram_sections[ram_section] += size
                            break

        # 結果の表示
        print('\n【RP2040/RP2350 マップ解析スクリプト】\n')
        print('Copyright (c) 2025 Chimipupu(https://github.com/Chimipupu)')
        print(f'\nマップファイル: {map_path}')
        # フラッシュ使用量の表示
        print('\n=== フラッシュ使用量 ===')
        flash_total = sum(flash_sections.values())
        for section, size in flash_sections.items():
            if size > 0:
                print(f'{section:15} {size:12,d} bytes ({size/1024:6.2f} KB)')
        print(f'合計使用量:     {flash_total:12,d} bytes ({flash_total/1024:6.2f} KB)')
        print(f'Flash容量:      {flash_capacity:12,d} bytes ({flash_capacity/1024/1024:6.2f} MB)')
        print(f'{"使用率:":15} {(flash_total/flash_capacity*100):6.2f}%')

        # RAM使用量の表示
        print('\n=== RAM使用量 ===')
        ram_total = sum(ram_sections.values())
        for section, size in ram_sections.items():
            if size > 0:
                print(f'{section:15} {size:12,d} bytes ({size/1024:6.2f} KB)')
        print(f'合計使用量:     {ram_total:12,d} bytes ({ram_total/1024:6.2f} KB)')
        print(f'SRAM容量:       {ram_capacity:12,d} bytes ({ram_capacity/1024:6.2f} KB)')
        print(f'{"使用率:":15}  {(ram_total/ram_capacity*100):6.2f}%')

    except Exception as e:
        print(f'エラー: ファイルの処理中にエラーが発生しました: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    # ログファイルの準備
    today_str = datetime.datetime.now().strftime('%Y%m%d')
    script_dir = Path(__file__).parent
    log_dir = script_dir / 'log'
    log_dir.mkdir(exist_ok=True)  # フォルダ作成
    log_file = log_dir / f'log_picosdk_map_parse_{today_str}.log'
    sys.stdout = Tee(log_file)  # 標準出力を複製

    # マップファイルの解析結果
    print_header()
    map_path = sys.argv[1] if len(sys.argv) > 1 else None
    map_path = find_map_file(map_path)
    parse_map_file(map_path)
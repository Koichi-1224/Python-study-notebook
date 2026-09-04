# drills — 自動採点ドリル

Python 基礎文法（変数〜関数・ライブラリ）を、テンポよく解ける形にまとめた自作ドリル。
買い物・旅行の割り勘・ゲームのスコア・読書記録・モンスター図鑑・駐車場・送料など、身近な題材で「自分で書いて即採点」。

| ノート | 内容 | 問題数 |
|---|---|---|
| [01_variables.ipynb](01_variables.ipynb) | 変数・演算子・データ型・型変換・f-string | 30 |
| [02_lists_dicts.ipynb](02_lists_dicts.ipynb) | リスト・二次元リスト・辞書 | 18 |
| [03_if_for.ipynb](03_if_for.ipynb) | if / and・or・not / for / 総合 | 27 |
| [04_functions_modules.ipynb](04_functions_modules.ipynb) | 関数・デフォルト引数・math・import各種 | 24 |

## 遊び方

1. ノートを開いてカーネルに `.venv` を選ぶ
2. 先頭のセルを実行（`from drill import ...`）
3. 各問題の `...` を自分のコードに置き換えて `Shift + Enter`
4. その場で ✅ / ❌ と進捗バーが出る。連続正解で 🔥 が付く

```python
check('1-3', result)   # 答え合わせ
hint('1-3')            # ヒント
answer('1-3')          # 解答例（3回外したら見てもOK）
score()                # 全章の進捗
score('2')             # 第2章だけ（未クリア一覧つき）
```

進捗はカーネルを再起動するとリセットされる（毎回まっさらから周回できる）。

## 仕組み

- `drill.py` … 採点・ヒント・スコア表示。解答は base64 で入れてあるので、うっかり目に入らない
- `build_notebooks.py` … 4つのノートブックを生成するスクリプト。問題を足す・直すときはこれを編集して `python build_notebooks.py`

## 問題を足したいとき

1. `drill.py` の `_BANK` に `"章-番号": _q("期待値を作る式", "ヒント", "解答例")` を追加
2. `build_notebooks.py` の該当章に Markdown セルとコードセルを追加
3. `python build_notebooks.py` で再生成

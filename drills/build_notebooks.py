"""drills/ の4つのノートブックを生成するスクリプト（開発用）"""
import json
from pathlib import Path

HERE = Path(__file__).parent

INTRO = """\
# {title}

**遊び方**

1. 上から順にセルを見て、`...` の部分を自分のコードに置き換える
2. `Shift + Enter` で実行 → その場で ✅ / ❌ が出る
3. 詰まったら `hint('番号')`、どうしても無理なら `answer('番号')`
4. 最後に `score()` で進捗を見る

書き写し問題はなし。「自分で書く」問題だけ。
"""

SETUP = """\
from drill import check, hint, answer, score
print('準備OK！ さっそく Q{ch}-1 から')
"""


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": text}


def build(filename, title, source, ch, cells):
    nb = {
        "cells": [md(INTRO.format(title=title, source=source)), code(SETUP.format(ch=ch))],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    for c in cells:
        nb["cells"].append(c)
    nb["cells"].append(md("---\n## おわり\n\n進捗を確認しよう。"))
    nb["cells"].append(code(f"score('{ch}')"))
    (HERE / filename).write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", filename, len(nb["cells"]), "cells")


# ======================================================================
# 第1章 変数・演算子・データ型
# ======================================================================
ch1 = [
    md("## 変数"),
    md("### Q1-1  変数 `player` に文字列 `'koichi'` を代入"),
    code("player = ...\n\ncheck('1-1', player)"),
    md("### Q1-2  `level` は今 1。レベルアップして 2 を再代入（上書き）"),
    code("level = 1\n\n...\n\ncheck('1-2', level)"),

    md("## 算術演算子"),
    md("### Q1-3  `7 × 6` を `result` に"),
    code("result = ...\n\ncheck('1-3', result)"),
    md("### Q1-4  1年は365日。何週間あるか（**整数部分**）を `weeks` に"),
    code("weeks = ...\n\ncheck('1-4', weeks)"),
    md("### Q1-5  365日を7で割った**余り**を `rest` に"),
    code("rest = ...\n\ncheck('1-5', rest)"),
    md("### Q1-6  `5 の 2 乗` を `result` に"),
    code("result = ...\n\ncheck('1-6', result)"),
    md("## 予想クイズ：演算子の優先度\n\n実行せずに結果を予想して、数字を書く。"),
    md("### Q1-7\n```python\n10 - 2 * 3\n```"),
    code("prediction = ...\n\ncheck('1-7', prediction)"),
    md("### Q1-8\n```python\n(10 - 2) * 3\n```"),
    code("prediction = ...\n\ncheck('1-8', prediction)"),
    md("### Q1-9\n```python\n3 * 2 ** 2\n```"),
    code("prediction = ...\n\ncheck('1-9', prediction)"),
    md("### Q1-10\n```python\n100 // 3 * 3\n```"),
    code("prediction = ...\n\ncheck('1-10', prediction)"),

    md("## 文章題：スーパーで買い物\n\n卵1パック 250円、牛乳 180円、食パン 160円。"),
    md("### Q1-11  卵を2パック買ったときの金額を `eggs_price` に"),
    code("egg = 250\nmilk = 180\nbread = 160\n\neggs_price = ...\n\ncheck('1-11', eggs_price)"),
    md("### Q1-12  牛乳3本 + 食パン2斤の金額を `drink_bread` に"),
    code("drink_bread = ...\n\ncheck('1-12', drink_bread)"),
    md("### Q1-13  3つを1個ずつ買って、消費税8%（= 1.08倍）を掛けた金額を `total_with_tax` に"),
    code("total_with_tax = ...\n\ncheck('1-13', total_with_tax)"),

    md("## 文章題：旅行の割り勘\n\n4人で旅行。ホテル 24,000円、レンタカー 9,600円。"),
    md("### Q1-14  ホテルとレンタカーの合計を `total` に"),
    code("hotel = 24000\nrental_car = 9600\npeople = 4\n\ntotal = ...\n\ncheck('1-14', total)"),
    md("### Q1-15  1人あたりの負担額を `per_person` に"),
    code("per_person = ...\n\ncheck('1-15', per_person)"),
    md("### Q1-16  ガソリンは 1L 170円で 30L 入れた。ガソリン代の1人分を `gas_per_person` に"),
    code("gas_price = 170\nliters = 30\n\ngas_per_person = ...\n\ncheck('1-16', gas_per_person)"),

    md("## データ型"),
    md("### Q1-17  文字列 `'42'` を整数に変換して `x` に入れ直し、`type_name` に型の名前を入れる（ヒント: `type(x).__name__`）"),
    code("x = '42'\nx = ...\ntype_name = ...\n\ncheck('1-17', type_name)"),
    md("### Q1-18  【予想】`int(9.99)` はいくつ？"),
    code("prediction = ...\n\ncheck('1-18', prediction)"),
    md("### Q1-19  【予想】\n```python\nint('3') * float('1.5')\n```"),
    code("prediction = ...\n\ncheck('1-19', prediction)"),
    md("### Q1-20  【予想】`str(7) + str(7)` は？（数値か文字列かに注意）"),
    code("prediction = ...\n\ncheck('1-20', prediction)"),
    md("### Q1-21  【バグ修正】`age + 1` はエラーになる。来年の年齢を **数値で** `next_age` に"),
    code("age = '25'\n\nnext_age = ...\n\ncheck('1-21', next_age)"),
    md("### Q1-22  【予想】`bool('')`（空の文字列）は True か False か"),
    code("prediction = ...\n\ncheck('1-22', prediction)"),
    md("### Q1-23  姓と名の間に半角スペースを入れて `'山田 太郎'` を `full_name` に"),
    code("first = '山田'\nlast = '太郎'\n\nfull_name = ...\n\ncheck('1-23', full_name)"),
    md("### Q1-24  f-string で `'りんごを3個買って360円'` を作り `text` に"),
    code("item = 'りんご'\nqty = 3\nprice = 360\n\ntext = ...\n\ncheck('1-24', text)"),
    md("### Q1-25  残高 1200円、値段 1500円。**買えるなら True、買えないなら False** になる式を `can_buy` に"),
    code("balance = 1200\nprice = 1500\n\ncan_buy = ...\n\ncheck('1-25', can_buy)"),

    md("## 総合：ゲームのスコア\n\nステージ1: 1200点、ステージ2: 950点、ステージ3: 1830点。"),
    md("### Q1-26  3ステージの合計を `total` に"),
    code("stage1 = 1200\nstage2 = 950\nstage3 = 1830\n\ntotal = ...\n\ncheck('1-26', total)"),
    md("### Q1-27  平均を `average` に"),
    code("average = ...\n\ncheck('1-27', average)"),
    md("### Q1-28  `'平均スコアは1326.7点'` のように**小数1桁**で表示する文字列を `text` に（ヒント: `{average:.1f}`）"),
    code("text = ...\n\ncheck('1-28', text)"),

    md("## 総合：ランニング記録\n\n| 月 | 火 | 水 | 木 | 金 |\n|---|---|---|---|---|\n| 3.5 km | 0 km | 5 km | 2.5 km | 4 km |\n\n週の目標は 15 km。"),
    md("### Q1-29  各曜日を変数にして、合計を `total_km` に"),
    code("mon = ...\ntue = ...\nwed = ...\nthu = ...\nfri = ...\n\ntotal_km = ...\n\ncheck('1-29', total_km)"),
    md("### Q1-30  目標を達成したか を `achieved` に（bool）"),
    code("goal = 15\n\nachieved = ...\n\ncheck('1-30', achieved)"),
]

# ======================================================================
# 第2章 リスト・辞書
# ======================================================================
ch2 = [
    md("## リスト：読書記録\n\n1週間で読んだページ数。\n\n| 1日目 | 2日目 | 3日目 | 4日目 | 5日目 | 6日目 | 7日目 |\n|---|---|---|---|---|---|---|\n| 120 | 0 | 85 | 200 | 60 | 0 | 150 |"),
    md("### Q2-1  表のページ数をリスト `pages` に"),
    code("pages = ...\n\ncheck('2-1', pages)"),
    md("### Q2-2  記録した日数を `days` に"),
    code("days = ...\n\ncheck('2-2', days)"),
    md("### Q2-3  合計ページ数を `total_pages` に"),
    code("total_pages = ...\n\ncheck('2-3', total_pages)"),
    md("### Q2-4  一番読んだ日のページ数を `max_pages` に"),
    code("max_pages = ...\n\ncheck('2-4', max_pages)"),
    md("### Q2-5  一番少ない日のページ数を `min_pages` に"),
    code("min_pages = ...\n\ncheck('2-5', min_pages)"),
    md("### Q2-6  5日目は本当は 65 ページだった。修正して、リスト全体を採点"),
    code("pages = [120, 0, 85, 200, 60, 0, 150]\n\n...\n\ncheck('2-6', pages)"),

    md("## リスト：自分の点数"),
    md("### Q2-7  `[国語, 数学, 英語]` の順。数学の点数を `math_score` に"),
    code("my_scores = [72, 95, 88]\n\nmath_score = ...\n\ncheck('2-7', math_score)"),
    md("### Q2-8  平均点を `my_average` に（`sum` と `len` を使う）"),
    code("my_average = ...\n\ncheck('2-8', my_average)"),

    md("## 二次元リスト：気温と時刻表"),
    md("### Q2-9  `[最低気温, 最高気温]` が曜日ごとに並んでいる。火曜の最高気温を `tue_max` に"),
    code("temps = [\n    [22, 28],  # 月\n    [21, 30],  # 火\n    [19, 25],  # 水\n]\n\ntue_max = ...\n\ncheck('2-9', tue_max)"),
    md("### Q2-10  電車の時刻表 `[時, 分]`。3本目の「分」を `third_minute` に"),
    code("timetable = [\n    [7, 15],\n    [7, 32],\n    [8, 5],\n    [8, 20],\n]\n\nthird_minute = ...\n\ncheck('2-10', third_minute)"),
    md("### Q2-11  水曜の `[最低, 最高]` をまるごと `wed_temps` に"),
    code("wed_temps = ...\n\ncheck('2-11', wed_temps)"),

    md("## 辞書：カフェのメニュー"),
    md("### Q2-12  紅茶の値段を `tea_price` に"),
    code("menu = {'コーヒー': 400, '紅茶': 350, 'ケーキ': 500}\n\ntea_price = ...\n\ncheck('2-12', tea_price)"),
    md("### Q2-13  ジュース 300円 を追加して、辞書全体を採点"),
    code("...\n\ncheck('2-13', menu)"),
    md("### Q2-14  店舗ごとのメニュー（ネスト）から、公園店の紅茶の値段を `park_tea` に"),
    code("shops = {\n    '駅前店': {'コーヒー': 400, '紅茶': 350},\n    '公園店': {'コーヒー': 420, '紅茶': 360},\n}\n\npark_tea = ...\n\ncheck('2-14', park_tea)"),

    md("## 辞書：モンスター図鑑"),
    code("# まずこのセルを実行（図鑑の定義）\nmonsters = {\n    'm01': {'name': 'スライム',  'hp': 30,  'type': '水'},\n    'm02': {'name': 'ゴブリン',  'hp': 55,  'type': '土'},\n    'm03': {'name': 'ドラゴン',  'hp': 300, 'type': '火'},\n}\nprint('図鑑準備OK')"),
    md("### Q2-15  `m02` の名前を `name` に"),
    code("name = ...\n\ncheck('2-15', name)"),
    md("### Q2-16  `m01` の hp を 35 に変更して、その hp を採点"),
    code("...\n\ncheck('2-16', monsters['m01']['hp'])"),
    md("### Q2-17  `m03` の情報（内側の辞書）をまるごと `dragon` に"),
    code("dragon = ...\n\ncheck('2-17', dragon)"),
    md("### Q2-18  メニューの商品名だけのリスト `items` を作る（`.keys()` と `list()`）"),
    code("menu = {'コーヒー': 400, '紅茶': 350, 'ケーキ': 500}\n\nitems = ...\n\ncheck('2-18', items)"),
]

# ======================================================================
# 第3章 条件分岐・繰り返し
# ======================================================================
ch3 = [
    md("## if 文"),
    md("### Q3-1  気温で `feeling` を決める。30以上 → `'あつい'`、15以上 → `'ちょうどいい'`、それ以外 → `'さむい'`"),
    code("temp = 31\n\n...\n\ncheck('3-1', feeling)"),
    md("### Q3-2  18歳以上なら `'成人'`、それ以外は `'未成年'` を `status` に"),
    code("age = 17\n\n...\n\ncheck('3-2', status)"),
    md("### Q3-3  信号で `action` を決める if/elif/else\n\n- `'青'` → `'進め'`\n- `'黄'` → `'注意'`\n- `'赤'` → `'止まれ'`\n- それ以外 → `'不明'`"),
    code("signal = '黄'\n\n...\n\ncheck('3-3', action)"),
    md("### Q3-4  `a` と `b` を比べて文を `message` に。`'3 は 5 より小さい'` / `'3 と 3 は同じ'` / `'5 は 3 より大きい'` の3パターン"),
    code("a = 3\nb = 3\n\n...\n\ncheck('3-4', message)"),
    md("## if 文：ネットショップの送料\n\n- 5000円以上 → `'送料無料'`\n- 2000円以上 → `'送料300円'`\n- それ以外 → `'送料500円'`"),
    md("### Q3-5  上のルールで `shipping` を決める if 文を書く（amount = 6000）"),
    code("amount = 6000\n\n...\n\ncheck('3-5', shipping)"),
    md("### Q3-6  同じ if 文をコピーして amount = 3500 で"),
    code("amount = 3500\n\n...\n\ncheck('3-6', shipping)"),
    md("### Q3-7  amount = 1200 で"),
    code("amount = 1200\n\n...\n\ncheck('3-7', shipping)"),

    md("## 論理演算子 and / or / not"),
    md("### Q3-8  身長120cm以上 **かつ** 6歳以上なら乗れる。`can_ride` に bool で"),
    code("height = 130\nage = 7\n\ncan_ride = ...\n\ncheck('3-8', can_ride)"),
    md("### Q3-9  会員 **または** 誕生日なら無料。`free` に"),
    code("is_member = False\nis_birthday = True\n\nfree = ...\n\ncheck('3-9', free)"),
    md("### Q3-10  雨が降って**いない**なら出かける。`go_out` に"),
    code("is_raining = True\n\ngo_out = ...\n\ncheck('3-10', go_out)"),
    md("### Q3-11  22時以降 **または** 6時より前なら深夜。`late_night` に"),
    code("hour = 23\n\nlate_night = ...\n\ncheck('3-11', late_night)"),
    md("### Q3-12  平日 **かつ** 9時以上 **かつ** 18時未満なら営業中。`open_now` に（and は3つつなげられる）"),
    code("is_weekday = True\nhour = 10\n\nopen_now = ...\n\ncheck('3-12', open_now)"),

    md("## 文章題：駐車場\n\n150分停めた。非会員、休日。"),
    md("### Q3-13  60分以内なら `'無料'`、そうでなければ `'有料'` を `fee` に"),
    code("minutes = 150\nis_member = False\nis_holiday = True\n\n...\n\ncheck('3-13', fee)"),
    md("### Q3-14  休日 **かつ** 120分以上なら割増。`holiday_surcharge` に bool で"),
    code("holiday_surcharge = ...\n\ncheck('3-14', holiday_surcharge)"),
    md("### Q3-15  会員 **または** 60分以内なら無料。`free` に bool で"),
    code("free = ...\n\ncheck('3-15', free)"),

    md("## for 文"),
    md("### Q3-16  `'level1'` 〜 `'level5'` の5つを for と `range` で作り、リスト `levels` に"),
    code("levels = []\n...\n\ncheck('3-16', levels)"),
    md("### Q3-17  カウントダウン `['3', '2', '1', 'GO!']` を作って `countdown` に（`range(3, 0, -1)` と `str()`）"),
    code("countdown = []\n...\n\ncheck('3-17', countdown)"),
    md("### Q3-18  1週間の歩数の合計を for で `total` に（`sum()` 禁止）"),
    code("steps = [8000, 12000, 6500, 9000, 11000, 4000, 7500]\n\ntotal = 0\n...\n\ncheck('3-18', total)"),
    md("### Q3-19  **奇数インデックス**（1, 3, 5）だけの合計を `odd_total` に（`range(1, len(...), 2)`）"),
    code("odd_total = 0\n...\n\ncheck('3-19', odd_total)"),
    md("### Q3-20  果物の値段の辞書から合計を `total` に（`.items()` を使う）"),
    code("prices = {'りんご': 120, 'バナナ': 80, 'みかん': 60}\n\ntotal = 0\n...\n\ncheck('3-20', total)"),
    md("### Q3-21  歩数が8000以上だった日数を `count` に"),
    code("count = 0\n...\n\ncheck('3-21', count)"),

    md("## for + if：真夏日判定\n\n最高気温 `[28, 32, 35, 30, 25]`。30度以上が真夏日。"),
    md("### Q3-22  各日の `'真夏日'` / `'通常'` を順に並べたリスト `labels` に"),
    code("temps = [28, 32, 35, 30, 25]\n\nlabels = []\n...\n\ncheck('3-22', labels)"),
    md("### Q3-23  真夏日の日数を `hot_count` に"),
    code("hot_count = 0\n...\n\ncheck('3-23', hot_count)"),

    md("## 総合：勉強時間\n\n| 月 | 火 | 水 | 木 | 金 | 土 | 日 |\n|---|---|---|---|---|---|---|\n| 2 | 0 | 3 | 1 | 2 | 4 | 0 |\n\n2時間以上を「ちゃんとやった日」とする。"),
    md("### Q3-24  表を辞書 `study` に（キーは `'月'` のような1文字）"),
    code("study = ...\n\ncheck('3-24', study)"),
    md("### Q3-25  ちゃんとやった日数を `good_count` に"),
    code("good_count = 0\n...\n\ncheck('3-25', good_count)"),
    md("### Q3-26  ちゃんとやった曜日のリストを `good_days` に"),
    code("good_days = []\n...\n\ncheck('3-26', good_days)"),
    md("### Q3-27  【ちょい難】一番勉強した曜日を `best_day` に（`max()` は使わず for と if で）"),
    code("best_day = ''\nbest_hours = 0\n...\n\ncheck('3-27', best_day)"),
]

# ======================================================================
# 第4章 関数・ライブラリ
# ======================================================================
ch4 = [
    md("## 関数の定義"),
    md("### Q4-1  正なら `'plus'`、負なら `'minus'`、0なら `'zero'` を返す `sign(x)` を定義"),
    code("...\n\ncheck('4-1', sign(-5))"),
    md("### Q4-2  長方形の面積を返す `area(width, height)` を定義"),
    code("...\n\ncheck('4-2', area(4, 5))"),
    md("### Q4-3  【デフォルト引数】`area` を、`width` も `height` も省略したら 1 になるように定義し直す"),
    code("...\n\ncheck('4-3', area(height=7))"),
    md("### Q4-4  おつりを返す `change(price, paid)` を定義"),
    code("...\n\ncheck('4-4', change(380, 500))"),
    md("### Q4-5  【バグ修正】このコードはエラーになる。直して実行"),
    code("def double(n):\nreturn n * 2\n\ncheck('4-5', double(21))"),
    md("### Q4-6  BMI = 体重(kg) ÷ 身長(m)² を返す `bmi(weight, height_m)` を定義"),
    code("...\n\ncheck('4-6', bmi(60, 1.7))"),
    md("### Q4-7  Q4-6 の `bmi` を中で呼んで、18.5未満 → `'やせ'`、25未満 → `'普通'`、それ以外 → `'肥満'` を返す `bmi_label(weight, height_m)` を定義"),
    code("...\n\ncheck('4-7', bmi_label(60, 1.7))"),

    md("## 関数：摂氏→華氏\n\n華氏 = 摂氏 × 9 ÷ 5 + 32"),
    md("### Q4-8  `c_to_f(c)` を定義"),
    code("...\n\ncheck('4-8', c_to_f(25))"),
    md("### Q4-9  【キーワード引数】100度を **名前付き** で渡して呼び出し、結果を `f` に"),
    code("f = ...\n\ncheck('4-9', f)"),
    md("### Q4-10  【デフォルト引数】割り勘の `split_bill(total, people)` を、人数を省略したら 2 になるように定義"),
    code("...\n\ncheck('4-10', split_bill(3000))"),
    md("### Q4-11  `tag(word, prefix='#')` を定義。`'#python'` のように返す"),
    code("...\n\ncheck('4-11', tag('python'))"),
    md("### Q4-12  【複数の戻り値】リストの合計と要素数を `(合計, 要素数)` のタプルで返す `stats(lst)` を定義"),
    code("...\n\ncheck('4-12', stats([1, 2, 3]))"),

    md("## 総合：レベルアップ判定\n\n経験値 + ボーナス が 必要値 以上ならレベルアップ。"),
    md("### Q4-13  `can_level_up(exp, need, bonus)` を定義。条件を満たせば True を返す"),
    code("...\n\ncheck('4-13', can_level_up(80, 100, 10))"),
    md("### Q4-14  同じ関数でボーナス25なら？"),
    code("check('4-14', can_level_up(80, 100, 25))"),

    md("## ライブラリ：math"),
    md("### Q4-15  `7.01` を切り上げて `ceil_value` に"),
    code("import math\n\nceil_value = ...\n\ncheck('4-15', ceil_value)"),
    md("### Q4-16  `144` の平方根を `sqrt_value` に"),
    code("sqrt_value = ...\n\ncheck('4-16', sqrt_value)"),
    md("### Q4-17  `math` から `pi` **だけ** を取り出して `pi_value` に（`math.pi` と書かずに）"),
    code("...\n\npi_value = ...\n\ncheck('4-17', pi_value)"),
    md("## ライブラリ：いろいろ import"),
    md("### Q4-18  `calendar` モジュールで 2030年1月 のカレンダー文字列を `text` に"),
    code("...\n\ntext = ...\n\ncheck('4-18', text)"),
    md("### Q4-19  【バグ修正】numpy を `np` として使いたい。直して円周率を `pi_value` に"),
    code("from numpy import np\npi_value = np.pi\n\ncheck('4-19', pi_value)"),
    md("### Q4-20  【バグ修正】9.99 を切り捨てて `floor_value` に"),
    code("from math import floor\nfloor_value = math.floor(9.99)\n\ncheck('4-20', floor_value)"),
    md("### Q4-21  pandas を `pd` という名前で読み込み、`pd.__name__` を `lib_name` に"),
    code("...\n\nlib_name = ...\n\ncheck('4-21', lib_name)"),
    md("### Q4-22  `random` から `choice` **だけ** を読み込む。`random.seed(3)` を呼んでから `hands` から1つ選んで `my_hand` に"),
    code("import random\nhands = ['グー', 'チョキ', 'パー']\n\n...\nrandom.seed(3)\nmy_hand = ...\n\ncheck('4-22', my_hand)"),
    md("### Q4-23  `random.seed(42)` を呼んだ直後に `random.randint(1, 100)` を `n` に"),
    code("...\n\ncheck('4-23', n)"),
    md("### Q4-24  半径 `r`、高さ `h` の円柱の体積を返す `cylinder_volume(r, h)` を定義（π は `np.pi`）"),
    code("import numpy as np\n\n...\n\ncheck('4-24', cylinder_volume(3, 10))"),
]

build("01_variables.ipynb", "ドリル1：変数・演算子・データ型", "", "1", ch1)
build("02_lists_dicts.ipynb", "ドリル2：リスト・辞書", "", "2", ch2)
build("03_if_for.ipynb", "ドリル3：条件分岐・繰り返し", "", "3", ch3)
build("04_functions_modules.ipynb", "ドリル4：関数・ライブラリ", "", "4", ch4)

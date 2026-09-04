"""
自動採点ドリル用のモジュール。

使い方（各ノートブックの先頭セルで実行）:
    from drill import check, hint, answer, score, weak_list

    check('1-3', result)   # 答え合わせ（正解すると模範解答も表示）
    hint('1-3')            # ヒントを見る
    answer('1-3')          # どうしても分からないとき（解答を表示）
    score()                # この章の進捗＋苦手リストを表示
    weak_list()             # 苦手リストだけを表示（復習用）

解答はこのファイルの中に base64 で入れてある（うっかり目に入らないようにしてあるだけ）。
"""

import base64
import math

# ---------------------------------------------------------------
# 採点の状態（カーネルを再起動するとリセットされる）
# ---------------------------------------------------------------
_state = {
    "solved": set(),     # 正解済みの問題ID
    "tries": {},         # 問題ID -> 挑戦回数
    "streak": 0,         # 連続正解数
    "best_streak": 0,
}


def _enc(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def _dec(text: str) -> str:
    return base64.b64decode(text.encode("ascii")).decode("utf-8")


def _expected(qid: str):
    """期待値を計算して返す。式は base64 で隠してある。"""
    expr = _dec(_BANK[qid]["expr"])
    env = {"math": math}
    try:
        import calendar
        env["calendar"] = calendar
    except ImportError:
        pass
    try:
        import random
        env["random"] = random
    except ImportError:
        pass
    return eval(expr, env)


def _same(got, exp) -> bool:
    """型をゆるく見つつ値を比較する。小数は誤差を許す。"""
    if isinstance(exp, bool) or isinstance(got, bool):
        return got is exp
    if isinstance(exp, (int, float)) and isinstance(got, (int, float)):
        return math.isclose(got, exp, rel_tol=1e-6, abs_tol=1e-6)
    if isinstance(exp, (list, tuple)) and isinstance(got, (list, tuple)):
        return len(got) == len(exp) and all(_same(g, e) for g, e in zip(got, exp))
    if isinstance(exp, dict) and isinstance(got, dict):
        return got.keys() == exp.keys() and all(_same(got[k], exp[k]) for k in exp)
    return got == exp


def _chapter_ids(chapter: str):
    return [q for q in _BANK if q.split("-")[0] == chapter]


def _bar(done: int, total: int, width: int = 20) -> str:
    filled = int(width * done / total) if total else 0
    return "█" * filled + "░" * (width - filled)


# ---------------------------------------------------------------
# 公開関数
# ---------------------------------------------------------------
def check(qid: str, got):
    """答え合わせ。正解なら ✅、不正解なら ❌ と次の一手を表示する。"""
    if qid not in _BANK:
        print(f"⚠️  問題ID '{qid}' は存在しません")
        return

    if got is Ellipsis:
        print(f"✏️  {qid}: まだ書いてないよ。`...` の部分を自分のコードに置き換えてから実行してね")
        return

    _state["tries"][qid] = _state["tries"].get(qid, 0) + 1
    tries = _state["tries"][qid]
    exp = _expected(qid)
    chapter = qid.split("-")[0]
    ids = _chapter_ids(chapter)

    if _same(got, exp):
        first = qid not in _state["solved"]
        _state["solved"].add(qid)
        if first:
            _state["streak"] += 1
            _state["best_streak"] = max(_state["best_streak"], _state["streak"])
        done = len([q for q in ids if q in _state["solved"]])
        fire = f"  🔥{_state['streak']}連続" if _state["streak"] >= 2 else ""
        tag = "正解！" if first else "正解（クリア済み）"
        print(f"✅ {qid} {tag}{fire}   第{chapter}章 {done}/{len(ids)}  {_bar(done, len(ids))}")
        print(f"   値: {got!r}  型: {type(got).__name__}")
        model = _dec(_BANK[qid]["ans"])
        lines = model.split("\n")
        print(f"   📖 模範解答: {lines[0]}")
        for line in lines[1:]:
            print(f"             {line}")
        if done == len(ids) and first:
            print(f"🎉 第{chapter}章 コンプリート！ 最長連続正解: {_state['best_streak']}")
    else:
        _state["streak"] = 0
        print(f"❌ {qid} 不正解（{tries}回目）")
        print(f"   あなたの値: {got!r}  型: {type(got).__name__}")
        if isinstance(exp, (int, float, str, bool)) and not isinstance(got, type(exp)):
            print(f"   期待している型: {type(exp).__name__}")
        if tries == 1:
            print(f"   👉 hint('{qid}') でヒントが見られるよ")
        elif tries >= 3:
            print(f"   👉 かなり粘ったね。answer('{qid}') で解答を見てもOK")
        else:
            print(f"   👉 hint('{qid}') / answer('{qid}')")


def hint(qid: str):
    if qid not in _BANK:
        print(f"⚠️  問題ID '{qid}' は存在しません")
        return
    print(f"💡 {qid} ヒント: {_BANK[qid]['hint']}")


def answer(qid: str):
    if qid not in _BANK:
        print(f"⚠️  問題ID '{qid}' は存在しません")
        return
    print(f"📖 {qid} 解答例:\n{_dec(_BANK[qid]['ans'])}")


_WEAK_THRESHOLD = 2  # この回数以上つまずいたら「苦手」扱い


def _weak_ids():
    """つまずいた回数（tries）が多い順の問題IDリストを返す。"""
    weak = [(qid, n) for qid, n in _state["tries"].items() if n >= _WEAK_THRESHOLD]
    weak.sort(key=lambda x: (-x[1], x[0]))
    return weak


def score(chapter: str | None = None):
    """進捗表示。chapter を省略すると全章を表示。"""
    chapters = [chapter] if chapter else sorted({q.split('-')[0] for q in _BANK}, key=int)
    print("=" * 44)
    for ch in chapters:
        ids = _chapter_ids(ch)
        done = len([q for q in ids if q in _state["solved"]])
        print(f"第{ch}章  {done:2d}/{len(ids):2d}  {_bar(done, len(ids))}")
        rest = [q for q in ids if q not in _state["solved"]]
        if rest and chapter:
            print(f"   未クリア: {', '.join(rest)}")
    print(f"最長連続正解: {_state['best_streak']}")

    weak = _weak_ids()
    if chapter:
        weak = [(qid, n) for qid, n in weak if qid.split("-")[0] == chapter]
    if weak:
        print("-" * 44)
        print(f"🧠 苦手リスト（{_WEAK_THRESHOLD}回以上つまずいた問題。復習はここから）")
        for qid, n in weak:
            mark = "✅" if qid in _state["solved"] else "❌"
            print(f"   {mark} {qid}  {n}回")
    print("=" * 44)


def weak_list(chapter: str | None = None):
    """苦手リストだけを表示する（score() の中でも一緒に出る）。"""
    weak = _weak_ids()
    if chapter:
        weak = [(qid, n) for qid, n in weak if qid.split("-")[0] == chapter]
    if not weak:
        print(f"🧠 苦手リストは空だよ（{_WEAK_THRESHOLD}回以上つまずいた問題がまだ無い）")
        return
    print(f"🧠 苦手リスト（{_WEAK_THRESHOLD}回以上つまずいた問題。復習はここから）")
    for qid, n in weak:
        mark = "✅ クリア済み" if qid in _state["solved"] else "❌ 未クリア"
        print(f"   {qid}  {n}回  {mark}")


# ---------------------------------------------------------------
# 問題バンク
#   expr: 期待値を作る Python 式（base64）
#   hint: ヒント（平文）
#   ans : 解答例（base64）
# ---------------------------------------------------------------
def _q(expr: str, hint_text: str, ans_text: str) -> dict:
    return {"expr": _enc(expr), "hint": hint_text, "ans": _enc(ans_text)}


_BANK = {
    # ===== 第1章 変数・演算子・データ型 =====
    "1-1": _q("'koichi'", "文字列はクォートで囲む", "player = 'koichi'"),
    "1-2": _q("2", "同じ変数名にもう一度 = で入れると上書きされる", "level = 2"),
    "1-3": _q("7 * 6", "掛け算は *", "result = 7 * 6"),
    "1-4": _q("365 // 7", "商の整数部分は // （スラッシュ2つ）", "weeks = 365 // 7"),
    "1-5": _q("365 % 7", "余りは %", "rest = 365 % 7"),
    "1-6": _q("5 ** 2", "べき乗は ** （アスタリスク2つ）", "result = 5 ** 2"),
    "1-7": _q("10 - 2 * 3", "掛け算が先", "prediction = 4"),
    "1-8": _q("(10 - 2) * 3", "括弧が最優先", "prediction = 24"),
    "1-9": _q("3 * 2 ** 2", "** が * より先。2 ** 2 = 4 を先に", "prediction = 12"),
    "1-10": _q("100 // 3 * 3", "// と * は同じ優先度なので左から。100 // 3 = 33 を先に", "prediction = 99"),
    "1-11": _q("250 * 2", "単価 × 個数", "eggs_price = egg * 2"),
    "1-12": _q("180 * 3 + 160 * 2", "それぞれ掛けてから足す", "drink_bread = milk * 3 + bread * 2"),
    "1-13": _q("(250 + 180 + 160) * 1.08", "1つずつの合計を括弧でまとめてから 1.08 倍", "total_with_tax = (egg + milk + bread) * 1.08"),
    "1-14": _q("24000 + 9600", "2つを足す", "total = hotel + rental_car"),
    "1-15": _q("(24000 + 9600) / 4", "合計 / 人数", "per_person = total / people"),
    "1-16": _q("170 * 30 / 4", "1L の値段 × リットル数 を人数で割る", "gas_per_person = gas_price * liters / people"),
    "1-17": _q("'int'", "文字列→整数は int()。type(x).__name__ で型の名前", "x = int(x)\ntype_name = type(x).__name__"),
    "1-18": _q("int(9.99)", "int() は四捨五入ではなく切り捨て", "prediction = 9"),
    "1-19": _q("int('3') * float('1.5')", "int と float の掛け算は float になる", "prediction = 4.5"),
    "1-20": _q("str(7) + str(7)", "str 同士の + は結合", "prediction = '77'"),
    "1-21": _q("26", "age は文字列なので int(age) で数値にしてから +1", "next_age = int(age) + 1"),
    "1-22": _q("bool('')", "空文字列は False 扱い（中身がある文字列は True）", "prediction = False"),
    "1-23": _q("'山田 太郎'", "間に ' '（半角スペース）を挟んで + でつなぐ", "full_name = first + ' ' + last"),
    "1-24": _q("'りんごを3個買って360円'", "f'{item}を{qty}個買って{price}円'", "text = f'{item}を{qty}個買って{price}円'"),
    "1-25": _q("1200 >= 1500", "「買える」= 残高 が 値段 以上。比較演算子の結果は bool", "can_buy = balance >= price"),
    "1-26": _q("1200 + 950 + 1830", "3つを足す", "total = stage1 + stage2 + stage3"),
    "1-27": _q("(1200 + 950 + 1830) / 3", "合計 / 3", "average = total / 3"),
    "1-28": _q("'平均スコアは1326.7点'", "f-string の中で {average:.1f} と書くと小数1桁になる", "text = f'平均スコアは{average:.1f}点'"),
    "1-29": _q("3.5 + 0 + 5 + 2.5 + 4", "各曜日を変数に入れて足す", "total_km = mon + tue + wed + thu + fri"),
    "1-30": _q("(3.5 + 0 + 5 + 2.5 + 4) >= 15", "合計 が 目標 以上か？ を bool で", "achieved = total_km >= goal"),

    # ===== 第2章 リスト・辞書 =====
    "2-1": _q("[120, 0, 85, 200, 60, 0, 150]", "角かっこの中にカンマ区切り", "pages = [120, 0, 85, 200, 60, 0, 150]"),
    "2-2": _q("7", "要素数は len()", "days = len(pages)"),
    "2-3": _q("615", "合計は sum()", "total_pages = sum(pages)"),
    "2-4": _q("200", "最大は max()", "max_pages = max(pages)"),
    "2-5": _q("0", "最小は min()", "min_pages = min(pages)"),
    "2-6": _q("[120, 0, 85, 200, 65, 0, 150]", "5日目はインデックス 4。リスト名[4] = 新しい値", "pages[4] = 65"),
    "2-7": _q("95", "[国語, 数学, 英語] なので数学はインデックス 1", "math_score = my_scores[1]"),
    "2-8": _q("85.0", "平均 = sum() / len()", "my_average = sum(my_scores) / len(my_scores)"),
    "2-9": _q("30", "外側[行][列]。火曜は1行目、最高気温は1列目", "tue_max = temps[1][1]"),
    "2-10": _q("5", "3本目は行インデックス2、「分」は列インデックス1", "third_minute = timetable[2][1]"),
    "2-11": _q("[19, 25]", "行だけ指定すると、その行のリストがまるごと取れる", "wed_temps = temps[2]"),
    "2-12": _q("350", "辞書はキーで引く。辞書名['キー']", "tea_price = menu['紅茶']"),
    "2-13": _q("{'コーヒー': 400, '紅茶': 350, 'ケーキ': 500, 'ジュース': 300}", "存在しないキーに代入すると追加される", "menu['ジュース'] = 300"),
    "2-14": _q("360", "ネストは [キー][キー] と2段で引く", "park_tea = shops['公園店']['紅茶']"),
    "2-15": _q("'ゴブリン'", "monsters['m02'] が内側の辞書。そこからさらに ['name']", "name = monsters['m02']['name']"),
    "2-16": _q("35", "2段で指定した場所に = で代入", "monsters['m01']['hp'] = 35"),
    "2-17": _q("{'name': 'ドラゴン', 'hp': 300, 'type': '火'}", "1段だけ指定すると内側の辞書がまるごと取れる", "dragon = monsters['m03']"),
    "2-18": _q("['コーヒー', '紅茶', 'ケーキ']", "辞書のキー一覧は .keys()。list() でリストにする", "items = list(menu.keys())"),

    # ===== 第3章 条件分岐・繰り返し =====
    "3-1": _q("'あつい'", "if temp >= 30: / elif temp >= 15: / else:", "if temp >= 30:\n    feeling = 'あつい'\nelif temp >= 15:\n    feeling = 'ちょうどいい'\nelse:\n    feeling = 'さむい'"),
    "3-2": _q("'未成年'", "if age >= 18: / else:", "if age >= 18:\n    status = '成人'\nelse:\n    status = '未成年'"),
    "3-3": _q("'注意'", "文字列の比較は ==。elif を並べる", "if signal == '青':\n    action = '進め'\nelif signal == '黄':\n    action = '注意'\nelif signal == '赤':\n    action = '止まれ'\nelse:\n    action = '不明'"),
    "3-4": _q("'3 と 3 は同じ'", "if a < b / elif a == b / else の3段。f-string で文を作る", "if a < b:\n    message = f'{a} は {b} より小さい'\nelif a == b:\n    message = f'{a} と {b} は同じ'\nelse:\n    message = f'{a} は {b} より大きい'"),
    "3-5": _q("'送料無料'", "if 条件: / elif 条件: / else: の3段。上から順に判定される", "if amount >= 5000:\n    shipping = '送料無料'\nelif amount >= 2000:\n    shipping = '送料300円'\nelse:\n    shipping = '送料500円'"),
    "3-6": _q("'送料300円'", "同じ if 文で amount = 3500 のとき", "（3-5 と同じコードで amount = 3500）"),
    "3-7": _q("'送料500円'", "同じ if 文で amount = 1200 のとき", "（3-5 と同じコードで amount = 1200）"),
    "3-8": _q("True", "「かつ」は and", "can_ride = height >= 120 and age >= 6"),
    "3-9": _q("True", "「または」は or", "free = is_member or is_birthday"),
    "3-10": _q("False", "反転は not", "go_out = not is_raining"),
    "3-11": _q("True", "22時以降 or 6時より前", "late_night = hour >= 22 or hour < 6"),
    "3-12": _q("True", "平日 and 9時以上 and 18時未満（and は3つ以上つなげられる）", "open_now = is_weekday and hour >= 9 and hour < 18"),
    "3-13": _q("'有料'", "if minutes <= 60: / else:", "if minutes <= 60:\n    fee = '無料'\nelse:\n    fee = '有料'"),
    "3-14": _q("True", "休日 and 120分以上", "holiday_surcharge = is_holiday and minutes >= 120"),
    "3-15": _q("False", "会員 or 60分以内", "free = is_member or minutes <= 60"),
    "3-16": _q("[f'level{i}' for i in range(1, 6)]", "range(1, 6) で 1〜5。f'level{i}' を append", "levels = []\nfor i in range(1, 6):\n    levels.append(f'level{i}')"),
    "3-17": _q("['3', '2', '1', 'GO!']", "range(3, 0, -1) で 3,2,1 と減る。str(i) で文字列に。最後に 'GO!' を append", "countdown = []\nfor i in range(3, 0, -1):\n    countdown.append(str(i))\ncountdown.append('GO!')"),
    "3-18": _q("8000 + 12000 + 6500 + 9000 + 11000 + 4000 + 7500", "total = 0 から始めて、for の中で total = total + s", "total = 0\nfor s in steps:\n    total = total + s"),
    "3-19": _q("12000 + 9000 + 4000", "range(1, len(steps), 2) で 1,3,5 のインデックスを回す", "odd_total = 0\nfor i in range(1, len(steps), 2):\n    odd_total = odd_total + steps[i]"),
    "3-20": _q("120 + 80 + 60", "辞書は for name, price in 辞書.items(): で回す", "total = 0\nfor name, price in prices.items():\n    total = total + price"),
    "3-21": _q("4", "for の中で if s >= 8000: なら +1", "count = 0\nfor s in steps:\n    if s >= 8000:\n        count = count + 1"),
    "3-22": _q("['通常', '真夏日', '真夏日', '真夏日', '通常']", "for t in temps: の中で if/else で文字列を決めて append", "labels = []\nfor t in temps:\n    if t >= 30:\n        labels.append('真夏日')\n    else:\n        labels.append('通常')"),
    "3-23": _q("3", "カウンタ 0 から、30 以上で +1", "hot_count = 0\nfor t in temps:\n    if t >= 30:\n        hot_count = hot_count + 1"),
    "3-24": _q("{'月': 2, '火': 0, '水': 3, '木': 1, '金': 2, '土': 4, '日': 0}", "波かっこで キー: 値 をカンマ区切り", "study = {'月': 2, '火': 0, '水': 3, '木': 1, '金': 2, '土': 4, '日': 0}"),
    "3-25": _q("4", "カウンタを 0 で作り、for の中の if で 2 以上なら +1", "good_count = 0\nfor day, hours in study.items():\n    if hours >= 2:\n        good_count = good_count + 1"),
    "3-26": _q("['月', '水', '金', '土']", "空リストに、条件を満たした day を append", "good_days = []\nfor day, hours in study.items():\n    if hours >= 2:\n        good_days.append(day)"),
    "3-27": _q("'土'", "最大値を覚える変数と、そのときの曜日を覚える変数の2つを for で更新", "best_day = ''\nbest_hours = 0\nfor day, hours in study.items():\n    if hours > best_hours:\n        best_hours = hours\n        best_day = day"),

    # ===== 第4章 関数・ライブラリ =====
    "4-1": _q("'minus'", "def sign(x): の中に if/elif/else、それぞれで return", "def sign(x):\n    if x > 0:\n        return 'plus'\n    elif x < 0:\n        return 'minus'\n    else:\n        return 'zero'"),
    "4-2": _q("20", "return width * height", "def area(width, height):\n    return width * height"),
    "4-3": _q("7", "def area(width=1, height=1): のようにデフォルト値を付ける", "def area(width=1, height=1):\n    return width * height"),
    "4-4": _q("120", "return paid - price", "def change(price, paid):\n    return paid - price"),
    "4-5": _q("42", "return の前にインデント（スペース4つ）が必要", "def double(n):\n    return n * 2"),
    "4-6": _q("60 / 1.7 ** 2", "BMI = 体重 / 身長 ** 2", "def bmi(weight, height_m):\n    return weight / height_m ** 2"),
    "4-7": _q("'普通'", "関数の中で bmi() を呼んで、その値で if/elif/else", "def bmi_label(weight, height_m):\n    b = bmi(weight, height_m)\n    if b < 18.5:\n        return 'やせ'\n    elif b < 25:\n        return '普通'\n    else:\n        return '肥満'"),
    "4-8": _q("25 * 9 / 5 + 32", "華氏 = 摂氏 × 9 / 5 + 32", "def c_to_f(c):\n    return c * 9 / 5 + 32"),
    "4-9": _q("100 * 9 / 5 + 32", "キーワード引数は 名前=値 の形で渡す", "f = c_to_f(c=100)"),
    "4-10": _q("3000 / 2", "def split_bill(total, people=2): とすると people を省略できる", "def split_bill(total, people=2):\n    return total / people"),
    "4-11": _q("'#python'", "def tag(word, prefix='#'): → return prefix + word", "def tag(word, prefix='#'):\n    return prefix + word"),
    "4-12": _q("(6, 3)", "return sum(lst), len(lst) のようにカンマで並べるとタプルで返る", "def stats(lst):\n    return sum(lst), len(lst)"),
    "4-13": _q("False", "経験値 + ボーナス が 必要値 以上か？ を return", "def can_level_up(exp, need, bonus):\n    return exp + bonus >= need"),
    "4-14": _q("True", "同じ関数で bonus=25 のとき", "（4-13 と同じ関数で can_level_up(80, 100, 25)）"),
    "4-15": _q("math.ceil(7.01)", "切り上げは math.ceil()", "import math\nceil_value = math.ceil(7.01)"),
    "4-16": _q("math.sqrt(144)", "平方根は math.sqrt()", "sqrt_value = math.sqrt(144)"),
    "4-17": _q("math.pi", "from math import pi と書くと pi だけ取り出せる", "from math import pi\npi_value = pi"),
    "4-18": _q("calendar.month(2030, 1)", "import calendar してから calendar.month(年, 月)", "import calendar\ntext = calendar.month(2030, 1)"),
    "4-19": _q("math.pi", "from X import Y は「XからYを取り出す」。np という名前は numpy の中にはない。import numpy as np", "import numpy as np\npi_value = np.pi"),
    "4-20": _q("9", "math.floor と書きたいなら import math が必要。from math import floor なら floor(9.99)", "import math\nfloor_value = math.floor(9.99)"),
    "4-21": _q("'pandas'", "import pandas as pd。pd.__name__ で本名が取れる", "import pandas as pd\nlib_name = pd.__name__"),
    "4-22": _q("(random.seed(3), random.choice(['グー', 'チョキ', 'パー']))[1]", "from random import choice → random.seed(3) → choice(hands)", "from random import choice\nrandom.seed(3)\nmy_hand = choice(hands)"),
    "4-23": _q("(random.seed(42), random.randint(1, 100))[1]", "random.seed(42) を呼んだ直後に random.randint(1, 100)", "random.seed(42)\nn = random.randint(1, 100)"),
    "4-24": _q("3 ** 2 * math.pi * 10", "体積 = 半径 ** 2 * π * 高さ", "import numpy as np\ndef cylinder_volume(r, h):\n    return r ** 2 * np.pi * h"),
}

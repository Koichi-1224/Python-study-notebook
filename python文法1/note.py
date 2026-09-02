# ====生徒の名前を入力する===
seito = input('生徒の名前を入力してください:')

# ===3教科の点数を入力する===
kokugo = int(input('国語の点数を入力してください: '))
sugaku = int(input('数学の点数を入力してください: '))
eigo = int(input('英語の点数を入力してください: '))

# ===合計点を計算する===
total = kokugo + sugaku + eigo

# ===平均点を計算する===
average = total / 3

# ===結果を表示する=== 
print('---') #区切り線
print(seito+'の点数')
print('3教科合計点は'+str(total)+'点です')
print(f'平均点は{average}点です')

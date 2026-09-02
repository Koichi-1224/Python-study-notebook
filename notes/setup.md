# setup
## 仮想環境(.venv)
- Pythonのpip installは仮想環境なしだとPC全体で共有される１つの場所にライブラリを入れる
- 複数ライブラリがある場合、どちらかか壊れる可能性がある
- .venvは「このフォルダ専用のPython一式」を作る仕組み。
- .\.venv\Scripts\Activate.ps1は切り替えるときに使用
### 手順
1. PowerShellを起動
2. cd ~ #ディレクトリ移動
3. python -m venv .venv
4. .\.venv\Scripts\Activate.ps1
5. pip install -r requirements.txt
※次回起動時は3のみでOK
## requirements.txt
- pip installするものリスト
- .venvは.gitignoreで除外するためGithubには上がらないため。
- 同じ環境をもし別の人が作る場合はpip install -r requirements.txtでリストを読んで入れる
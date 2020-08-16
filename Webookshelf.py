# -*- coding: utf-8 -*-

import os
import subprocess
import urllib.parse

from flask import Flask, render_template, request

import jsonIO

app = Flask(__name__)

# 定数
JSON = jsonIO.jsonIO(r"./setting.json")

SERVER_IP = JSON.get_IpAddress()
PORT = JSON.get_Port()
ROOT_URL = "http://" + SERVER_IP + ":" + PORT +"/"

IMAGE_PATH = JSON.get_ImagePath()
ROOT_DIR   = "." + IMAGE_PATH

NO_TITLE_IMAGE = "/static/system/images/noTitle.png"
POST = "POST"
GET = "GET"

# TOP画面
@app.route("/", methods=[GET, POST])
def handler_TopPage():
    if request.method == POST:
        return postRequest(request=request.get_data().decode('utf-8'))
    else:
        return getRequest(name="本棚TOP")

# 参照画面
@app.route("/<path:path>", methods=[GET, POST])
def handler_SubPage(path=None):
    # 名前を取得
    bookname = path.split("/")

    if request.method == POST:
        return postRequest(request.get_data().decode('utf-8'), path)
    else:
        return getRequest(bookname[-1], path)

# GETリクエスト処理
def getRequest(name, path=""):
    # フォルダ一覧取得
    files = get_folders(joinPath(path, rootPath=ROOT_DIR))
    if files == []:
        # 読み込み先にフォルダが無ければ本
        return get_Book(path, name)
    else:
        # 読み込み先にフォルダが有れば本棚
        return get_Bookshelf(path, name)

# POSTリクエスト処理
def postRequest(request, path=""):
    # シャットダウン要求
    if "shutdown" in request:
        return shutdown()

    # フォルダオープン要求
    if "openDir" in request:
        return openDir(path)

# 本棚生成処理
def get_Bookshelf(path, bookname):

    # URLデコード
    path = urllib.parse.unquote(path)

    # フォルダ一覧取得
    files = get_folders(joinPath(path, rootPath=ROOT_DIR))

    # 本棚画面生成
    item = []
    for name in files:
        dic = {}

        # タイトルの設定
        dic["title"] = name

        # 本へのURLを生成
        dic["url"] = joinPath(path, name, rootPath=ROOT_URL)

        # 本の表紙を取得
        title = get_BookTitle(path, name)
        if title != None:
            dic["image"] = joinPath(IMAGE_PATH, path, name, title, rootPath=ROOT_URL)
        else:
            # ダミータイトルを表示
            dic["image"] = joinPath(NO_TITLE_IMAGE, rootPath=ROOT_URL)

        item.append(dic)

    # 画面生成
    return render_template("bookshelf.html", rootURL=ROOT_URL, title=bookname, books=item)

# 本生成処理
def get_Book(path, bookname):
    files = get_files(joinPath(path, rootPath=ROOT_DIR))

    # book.jsonを除外した画像一覧を取得
    imgs = [s for s in files if "book.json" not in s]

    # ファイル名でソート
    try:
        sorted = sort_img(imgs)
    except ValueError:
        return render_template("error.html", title=bookname)

    # 本生成
    item = []
    for name in sorted:
        dic = {}
        dic["url"] = joinPath(IMAGE_PATH, path, name, rootPath=ROOT_URL)
        item.append(dic)

    # 画面生成
    return render_template("book.html", title=bookname, images=item)

# 表紙画像取得
def get_BookTitle(path, name):
    # 検索対象のPATH
    target_path = joinPath(path, name, rootPath=ROOT_DIR)

    # book.jsonをチェック
    if (os.path.exists(target_path + "/" + "book.json")):
        return jsonIO.jsonIO(target_path + "/" + "book.json").get_TitleImagePath()

    # タイトル画像の存在をチェック
    for name in get_files(target_path):
        # タイトル画像
        if "title" in name:
            return name

        # タイトル扱いの画像
        if "0" in name:
            return name

    return None

# ディレクトリ内のフォルダ一覧取得
def get_folders(path):
    items = os.listdir(path)
    folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
    return folders

# ディレクトリ内のファイル一覧取得
def get_files(path):
    items = os.listdir(path)
    files = [f for f in items if os.path.isfile(os.path.join(path, f))]
    return files

# 画像を名前順でソート
def sort_img(imgs):
    # 番号と拡張子に分割
    imgs = list(map(spilit, imgs))

    # ファイル名(番号)でソート
    imgs.sort(key=lambda x: x[0])

    # ファイル名と拡張子を結合
    return list(map(lambda x: str(x[0]) + "." + x[1], imgs))

# ファイル名分割
def spilit(item):
    # 名前と拡張子に分割
    value, extension = item.split(".")
    return [int(value), extension]

# パス結合処理
def joinPath(*args, rootPath):
    path = ""

    # パスを結合
    for name in args:
        path += name + "/"

    # 重複箇所を削除
    beforePath = ""
    while path != beforePath:
        beforePath = path
        path = path.replace("//", "/")

    # 先頭と末尾の / を削除
    path = path.strip("/")

    # 全てを結合
    return rootPath + path

# シャットダウン処理
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')

    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    else:
        func()

    # 終了画面の描画処理
    return render_template("shutdown.html")

# フォルオープン処理
def openDir(path):
    subprocess.run('explorer ' + os.path.abspath(joinPath(path, rootPath=ROOT_DIR)))
    return ""

# Main処理
if __name__ == "__main__":
    import webbrowser
    import threading
    import time

    # 遅延起動関数
    def web_open():
        # 起動遅延時間
        time.sleep(1)

        # サーバアクセス (設定ファイルからPath取得)
        browser = webbrowser.get('"' + jsonIO.jsonIO(r"./setting.json").get_BrowserPath() + '" %s')
        browser.open(ROOT_URL)

    # ブラウザ遅延起動呼び出し
    threading.Thread(target=web_open).start()

    # サーバ起動 (ここでループ)
    app.run(debug=False, host=SERVER_IP, port=PORT)

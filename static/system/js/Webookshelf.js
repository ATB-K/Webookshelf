// ページ読み込み完了時
window.onload = function() {
    changeTitle();
    loadingDone();
}

// コンテンツエリア読み込み完了時
$(document).ajaxStop(function() {
    changeTitle();
    loadingDone();
});

// タイトル文字設定
function changeTitle() {
    title = document.getElementById('title').value;
    $('title').html(title);
}

// 読み込み完了処理
function loadingDone() {
    const spinner = document.getElementById('loading');
    spinner.classList.add('loaded');
}

// ページ変更のリクエスト
function changePage(url) {
    // URLエンコード
    encodeURL = encodeURI(url)

    // コンテンツ切り替え処理
    changeContents(encodeURL);

    // パンくずリストに追加
    window.history.pushState(null, null, encodeURL);
}

// 戻る・進むボタンを押したとき
onpopstate = function(event) {
    changeContents(location.pathname);
}

// コンテンツの切り替え
function changeContents(url) {
    $('article').load(url + ' section');
}

// シャットダウンリクエスト送信
function shutdown() {
    xhr = new XMLHttpRequest();
    xhr.open('POST', location.href, true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send("shutdown");

    // 応答データ処理
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4 && xhr.status === 200) {
            // 取得htmlを反映
            document.getElementById('main_space').innerHTML = xhr.responseText;
        }
    }
}

// ディレクトリで開く
function openDir() {
    xhr = new XMLHttpRequest();
    xhr.open('POST', location.href, true);
    xhr.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhr.send("openDir");

    // 応答データ処理
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4 && xhr.status === 200) {
            // 何もしない
        }
    }
}

// 先頭へ戻る
function goTop() {
    document.getElementById('main_space').scrollTo(0, 0);
}
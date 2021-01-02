import datetime
import locale
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

# Chromeを起動する関数
from selenium.webdriver.common.by import By


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')  # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)


def write_csv_log(out_value):
    path = 'log.txt'
    with open(path, mode='a') as f:
        now_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.writelines(f"{now_datetime}:{out_value}\n")


# main処理
def main():
    # 課題2(4) 任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう
    print('検索キーワードを入力下さい。')
    search_keyword = input('>> ')

    print(locale.getpreferredencoding())

    # driverを起動
    write_csv_log("driver起動処理開始")
    if os.name == 'nt':  # Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix':  # Mac
        driver = set_driver("chromedriver", False)
    write_csv_log("driver起動処理完了")

    write_csv_log("Webサイトを開く処理開始")
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    write_csv_log("Webサイトを開く処理完了")

    try:
        write_csv_log("ポップアップを閉じる処理開始")
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        write_csv_log("ポップアップを閉じる処理完了")
    except Exception as e:
        print(e.args)

    write_csv_log("検索窓に入力処理開始")
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    write_csv_log("検索窓に入力処理完了")

    time.sleep(5)

    # 課題2(6) エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう(try文)
    # ※ 2ページ目が無い場合でも処理を行う
    try:
        write_csv_log("2ページ目遷移処理開始")
        # 課題2 (3)２ページ目以降の情報も含めて取得できるようにしてみましょう
        a = driver.findelement_by_css_selector(
            "ul.pager__list > li:nth-child(2) > a"
        )
        # クリックしたい要素までスクロール
        driver.execute_script("arguments[0].scrollIntoView(true);", a)
        a.click()
        write_csv_log("2ページ目遷移処理完了")
    except Exception as e:
        print(e.args)

    time.sleep(5)
    # 検索結果の一番上の会社名を取得
    # name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    # exp_name_list = []
    # 1ページ分繰り返し
    # print(len(name_list))
    ##for name in name_list:
    #    print(name.text)
    #    exp_name_list.append(name.text)

    # 課題2 (1)会社名以外の項目を取得して画面にprint文で表示してみましょう。
    # copy_list = driver.find_elements_by_class_name("cassetteRecruit__copy")
    # print(len(copy_list))
    # for name in copy_list:
    #    print(name.text)

    # 課題2(2) for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
    write_csv_log("複数項目の取得処理開始")
    exp_tr_list = []
    for num in range(1, 5):
        tr = driver.find_elements_by_css_selector(
            f"div.cassetteRecruit__main > table > tbody > tr:nth-child({num})"
        )
        tmp_list = [""] * len(tr)
        for i, value in enumerate(tr):
            tmp_list[i] = value.text
        print(tmp_list)
        exp_tr_list.append(tmp_list)
        write_csv_log("項目目の取得完了")

    write_csv_log("複数項目の取得処理完了")

    # 課題2 (5)取得した結果をpandasモジュールを使ってCSVファイに出力してみましょう
    # CSV出力
    write_csv_log("CSV出力処理開始")
    exp_csv_list = []
    for num in range(0, len(exp_tr_list[0])):
        exp_csv_list.append([exp_tr_list[0][num], exp_tr_list[1][num], exp_tr_list[2][num], exp_tr_list[3][num]])
        write_csv_log("行目のデータ作成完了")
    df = pd.DataFrame(exp_csv_list)
    df.columns = ['仕事内容', '対象となる方', '勤務地', '給与']
    # CSV ファイル (employee.csv) として出力
    df.to_csv("employee.csv", index=False)
    write_csv_log("CSV出力処理完了")


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()

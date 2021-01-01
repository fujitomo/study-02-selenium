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

# main処理
def main():
    # 課題2(4) 任意のキーワードをコンソール（黒い画面）から指定して検索できるようにしてみましょう
    print('検索キーワードを入力下さい。')
    search_keyword = input('>> ')
    path = 'log.txt'

    with open(path, mode='w') as f:
        print(locale.getpreferredencoding())

        # driverを起動
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "driver起動処理開始\n")
        if os.name == 'nt':  # Windows
            driver = set_driver("chromedriver.exe", False)
        elif os.name == 'posix':  # Mac
            driver = set_driver("chromedriver", False)
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "driver起動処理完了\n")

        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "Webサイトを開く処理開始\n")
        # Webサイトを開く
        driver.get("https://tenshoku.mynavi.jp/")
        time.sleep(5)
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "Webサイトを開く処理完了\n")

        try:
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "ポップアップを閉じる処理開始\n")
            # ポップアップを閉じる
            driver.execute_script('document.querySelector(".karte-close").click()')
            time.sleep(5)
            # ポップアップを閉じる
            driver.execute_script('document.querySelector(".karte-close").click()')
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "ポップアップを閉じる処理完了\n")
        except Exception as e:
            print(e.args)

        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "検索窓に入力処理開始\n")
        # 検索窓に入力
        driver.find_element_by_class_name(
            "topSearch__text").send_keys(search_keyword)
        # 検索ボタンクリック
        driver.find_element_by_class_name("topSearch__button").click()
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "検索窓に入力処理完了\n")

        time.sleep(5)

        # 課題2(6) エラーが発生した場合に、処理を停止させるのではなく、スキップして処理を継続できるようにしてみましょう(try文)
        # ※ 2ページ目が無い場合でも処理を行う
        try:
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "2ページ目遷移処理開始\n")
            # 課題2 (3)２ページ目以降の情報も含めて取得できるようにしてみましょう
            a = driver.findelement_by_css_selector(
                "ul.pager__list > li:nth-child(2) > a"
            )
            # クリックしたい要素までスクロール
            driver.execute_script("arguments[0].scrollIntoView(true);", a)
            a.click()
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "2ページ目遷移処理完了\n")
        except Exception as e:
            print(e.args)

        time.sleep(5)
        # 検索結果の一番上の会社名を取得
        #name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        #exp_name_list = []
        # 1ページ分繰り返し
        #print(len(name_list))
        ##for name in name_list:
        #    print(name.text)
        #    exp_name_list.append(name.text)

        # 課題2 (1)会社名以外の項目を取得して画面にprint文で表示してみましょう。
        #copy_list = driver.find_elements_by_class_name("cassetteRecruit__copy")
        #print(len(copy_list))
        #for name in copy_list:
        #    print(name.text)

        # 課題2(2) for文を使って、１ページ内の３つ程度の項目（会社名、年収など）を取得できるように改造してみましょう
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "複数項目の取得処理開始\n")
        exp_tr_list = []
        for num in range(1, 5):
            tr = driver.find_elements_by_css_selector(
                  f"div.cassetteRecruit__main > table > tbody > tr:nth-child({num})"
            )
            tmp_list = [""] * len(tr)
            for i,value in enumerate(tr):
                tmp_list[i] = value.text
            print(tmp_list)
            exp_tr_list.append(tmp_list)
            f.write("  　　　　" + str(num) + "項目目の取得完了\n")

        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "複数項目の取得処理完了\n")

        # 課題2 (5)取得した結果をpandasモジュールを使ってCSVファイに出力してみましょう
        # CSV出力
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "CSV出力処理開始\n")
        exp_csv_list = []
        for num in range(0,len(exp_tr_list[0])):
            exp_csv_list.append([exp_tr_list[0][num],exp_tr_list[1][num],exp_tr_list[2][num],exp_tr_list[3][num]])
            f.write("  　　　　" + str(num + 1) + "行目のデータ作成完了\n")
        df = pd.DataFrame(exp_csv_list)
        df.columns = ['仕事内容','対象となる方','勤務地','給与']
        # CSV ファイル (employee.csv) として出力
        df.to_csv("employee.csv",index=False)
        f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  " + "CSV出力処理完了\n")

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()

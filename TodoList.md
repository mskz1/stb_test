stbの読み込み、修正、書き出しを行うライブラリ構築計画
pyStb


cstデータ
座標値を取得し、節点データを生成する



# 1.主な機能
計画
* STB読み込み
  * 一貫計算ソフトから生成したSTB読み込み
  * Excel（xlsx）簡易入力データからの生成
  * 新規生成？
* 各データ要素へのアクセス、内容表示
  * StbNode
    * .
  * StbX_Axis
  * StbY_Axis
  * StbStory
  * StbMembers
    * StbColumns
    * StbGirders
    * StbBeams
    * StbBraces
  * StbSections
    * StbSecColumn_S
      * StbSecSteelColumn
    * StbSecBeam_RC
      * StbSecFigure
        * StbSecStraight
      * StbSecBar_Arrangement
        * StbSecBeam_Same_Section
    * StbSecBeam_S
      * StbSecSteelBeam
    * StbSecBrace_S
      * StbSecSteelBrace
    * StbSecSteel
      * StbSecRoll-BOX
      * StbSecRoll-H
      * StbSecRoll-C
      * StbSecRoll-FB
      
* データの修正
  * StbNode

xml.etree help[https://docs.python.jp/3/library/xml.etree.elementtree.html]
-----
* ✔ タグ、アトリビュートを指定して該当するエレメントを返す関数。複数のときはリスト？
* ✔ STBファイルの保存(tostringでは改行がLF？)
* ☐ matplotlibで形状表示？
  * ✔ plotルーチンの改良-分割
  * ☐ plotルーチンの改良-部材名表示
  * ✔ 通り心 線表示
  * ✔ 通り心 名表示
  * ✔ 伏せ図表示（レベル指定）
  * ✔ 伏せ図 柱表示
  * ✔ 伏せ図 梁表示
  * ☐ 伏せ図 梁 符号タテ向き設定
  * ✔ 伏せ図　梁　端部を縮める
  * ☐ 軸組図表示（軸指定）
  
* ✔ 節点座標の最小・最大値を得る
* ☐ Axisの追加
* ✔ Nodeの追加
* ✔ 指定したエレメントのアトリビュートの変更
* ☐ 断面(Section)の抽出
* ☐ 断面(Section)の修正
* ☐ 部材の追加
  * ☐ add_beam
  * ☐ add_post
* ☐ ある条件（レベル、通り）に合致する要素の抽出










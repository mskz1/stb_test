stbの読み込み、修正、書き出しを行うライブラリ構築計画
pyStb

# 1.主な機能
計画
* STB読み込み
  * 一貫計算ソフトから生成したSTB読み込み
  * Excelからの簡易入力データからの生成
  * 新規生成？
* 各データ要素へのアクセス、内容表示
  * StbNode
    * 
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
* ☑ タグ、アトリビュートを指定して該当するエレメントを返す関数。複数のときはリスト？
* □ STBファイルの保存(tostringでは改行がLF？)
* □ matplotlibで形状表示？
* □ Axisの追加
* □ Nodeの追加
* □ 
* □ 
* □ 
* □ 








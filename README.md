# XI Measure Blender アドオン

このBlenderアドオンは、Edit Modeで選択された2つの頂点間の距離を測定します。

## 機能

- Edit Modeで正確に2つの頂点が選択されたときに自動的に距離を測定。
- Nパネル（Toolタブ）にユークリッド距離とX、Y、Zグローバル座標の差を表示。
- 各コンポーネント（X、Y、Z）とすべての値のコピーボタンをクリップボードに提供。
- X、Y、Z軸の距離を個別に均一化するための前段ツールとして有用。

## インストール

1. [Releases](https://github.com/XIpher-Desco/blender-addon-xi-measure/releases) から最新の `xi-measure-addon.zip` をダウンロード。
2. BlenderでEdit > Preferences > Add-onsを開く。
3. "Install..."をクリックし、ダウンロードしたzipファイルを選択。
4. アドオン"XI Measure"を有効化。

## 使用方法

1. メッシュオブジェクトでEdit Modeに入る。
2. 正確に2つの頂点を選択。
3. 距離がNパネル > Toolタブ > XI Measureに自動的に表示される。
4. 各値の横の"Copy"をクリックして個別にコピー、または"Copy All"ですべてをコピー。

## スクリーンショット

![使用例](img/image.png)

## 注意事項

- 正確に2つの頂点が選択された場合のみ動作。
- 距離はグローバル座標で計算。
- パネルは選択変更時に自動的に更新。

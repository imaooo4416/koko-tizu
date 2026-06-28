# 関西6府県 高等学校 所在地マップ

大阪府・兵庫県・京都府・奈良県・滋賀県・和歌山県の公立・私立高等学校の所在地を地図上にプロットしたインタラクティブマップ。

## 収録状況

| 府県 | 収録数 |
|---|---:|
| 大阪府 | 247校 |
| 兵庫県 | 198校 |
| 京都府 | 99校 |
| 奈良県 | 49校 |
| 滋賀県 | 56校 |
| 和歌山県 | 39校 |
| **合計** | **688校** |

## 機能

- 関西6府県の全日制高校の所在地を OpenStreetMap 上にプロット（実座標）
- 府県・種別（公立／私立）・別学（共学／男子校／女子校）でフィルタ
- 学校名のあいまい検索（ひらがな・カタカナ・記号差を無視）
- 学校クリックで最寄駅・路線・徒歩時間・公式サイトのアクセス情報を表示
- 府県別・エリア別 PDF 出力（A4 横向き、地図と一覧を1ページに、公立/私立を区別）
- スマホ対応（地図と学校一覧を上下分割表示）

## 技術スタック

- 純粋な HTML / CSS / JavaScript（ビルド不要・単一ファイル）
- [Leaflet 1.9.4](https://leafletjs.com/) — 地図ライブラリ
- [Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP) — 日本語フォント

## 地図タイル・データの出典

このアプリは以下の第三者提供のタイル・データを利用しています。各規約に従って配信しており、地図UI下部に attribution を常時表示しています。

| 種別 | 提供元 | 規約 |
|---|---|---|
| 淡色地図タイル | [地理院タイル](https://maps.gsi.go.jp/development/ichiran.html) | [国土地理院コンテンツ利用規約](https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html) |
| シンプル地図タイル | [CartoDB Positron](https://carto.com/attributions) | CC BY 3.0 + ODbL |
| 鉄道路線オーバーレイ | [OpenRailwayMap](https://www.openrailwaymap.org/) | [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) |
| 地図データ（OSM 由来） | [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) | ODbL |
| 鉄道路線・駅データ（加工） | [国土数値情報 鉄道時系列データ N02](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html)（国土交通省） | [公共データ利用規約 第1.0版（PDL1.0）](https://www.digital.go.jp/resources/open_data/public_data_license_v1.0) |

出典：「国土数値情報（鉄道時系列データ）」（国土交通省）（https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N02-v3_1.html）をもとに koko-tizu project が加工して作成。PDL1.0は商用利用・再配布・改変いずれも許諾（CC BY 4.0互換）。加工内容（関西エリア絞り込み・JR西日本東海道線の3区間分割など）は [LICENSE](LICENSE) を参照してください。

## ライセンス

- **アプリ本体のソースコード（`index.html`）**: [MIT License](LICENSE)
- **同梱データ（`rail_lines.json` / `rail_stations.json`）**: PDL1.0（国土数値情報 N02 を加工した派生データ／CC BY 4.0互換）
- **地図タイル・フォント等の第三者依存**: それぞれの規約に従う

詳細は [LICENSE](LICENSE) を参照してください。

## 注意事項

- 学校所在地・アクセス情報は公開情報を元にしたものです。最新・正確な情報は各学校の公式ホームページをご確認ください。
- 本マップは個人が運営する非公式の参考情報サービスで、教育委員会・自治体・各学校との関連はありません。

## ローカル開発

ビルド不要。任意の静的ファイルサーバーで起動できます。

```bash
npx serve . -l 8765
# ブラウザで http://localhost:8765 を開く
```


1. mocker.patch

mocker.patch は、モジュールやクラス、関数をモックオブジェクトで置き換えるための便利な機能です。

利点

外部システムとの連携を不要化
実際の API やデータベースなどとの通信を必要とせず、テストコード単体で実行できます。
テスト実行時間の短縮
外部システムとの通信待ち時間を削減し、テストの高速化を実現します。
テストの安定化
外部システムの状態に左右されることなく、一貫したテスト結果を得られます。
テスト対象コードの明確化
外部システムの影響を受けずに、テスト対象コードの動作に焦点を当てられます。
例:

```Python
from unittest import mock

@mock.patch('my_module.my_function')
def test_my_function(mock_my_function):
    # テスト対象コードを実行
    my_function()

    # モックオブジェクトの検証
    mock_my_function.assert_called_with(arg1, arg2)
```

2. mocker.spy

mocker.spy は、実際のオブジェクトをラップして、メソッド呼び出しや属性アクセスを追跡するための機能です。

利点

オブジェクトの動作検証
テスト対象コードがオブジェクトをどのように利用しているかを詳細に確認できます。
副作用の検知
オブジェクトの呼び出し順序や属性の変更など、意図しない副作用を検出できます。
テスト対象コードとオブジェクトの連携検証
テスト対象コードとオブジェクトがどのように連携しているかを検証できます。
例:

```Python
from unittest import mock

my_object = mock.spy()

# テスト対象コードを実行
my_function(my_object)

# モックオブジェクトの検証
my_object.method.assert_called_with(arg1, arg2)
my_object.attribute.assert_has_calls([mock.call(1), mock.call(2)])
Use code with caution.

```
3. mocker.stub

mocker.stub は、特定のメソッド呼び出しに対して事前定義された挙動を返すモックオブジェクトを作成するための機能です。

利点

特定の条件をシミュレート
特定のエラー発生や特定の値の返却など、テストに必要な条件をシミュレートできます。
テスト対象コードの特定部分のテスト
特定のメソッド呼び出しに依存する部分のみをテストできます。
依存関係の簡略化
複雑な依存関係をモックオブジェクトで置き換えることで、テストコードを簡潔にできます。
例:

```
Python
from unittest import mock

my_stub = mock.Mock()
my_stub.method.return_value = 'mocked value'

# テスト対象コードを実行
my_function(my_stub)

# モックオブジェクトの検証
my_stub.method.assert_called_with(arg1, arg2)
Use code with caution.
```
4. その他の Test Doubles 手法

上記の 3 つの方法以外にも、以下のような Test Doubles 手法があります。

ダミーオブジェクト: 何もしない空のオブジェクト
フェイクオブジェクト: 実際のオブジェクトの一部機能のみを実装したオブジェクト
テストデータジェネレータ: テストデータ生成のためのツール
テストフレームワークのモック機能: 多くのテストフレームワークは独自のモック機能を提供
これらの手法は、それぞれ異なる利点と欠点を持つため、テストの目的に合わせて適切なものを選択する必要があります。

Test Doubles を活用する際の注意点

テスト対象コードとの密接な連携が必要
テストコードの複雑化を招く可能性
モックオブジェクトの使い過ぎはテストの信頼性を低下させる
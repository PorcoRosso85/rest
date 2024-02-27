from app.models import TestOrganizationModel as TOM
from app.test_models import TestMembershipModel, TestOrganizationModel
from app.test_serializer import TestOrganizationSerializer
from core.tests.test_urls import TestOrganizationView, TestUserView

test_design_for_organization = {
    "組織の作成": [
        TestOrganizationModel.test200_最低1人のオーナーが存在する,
        TestOrganizationView.test200_作成したユーザーとオーナーが一致する,
        "組織を作成したユーザーがメンバーとして関連する",
        {"組織が作成されない": []},
        {
            "作成したユーザーが、その組織のオーナーになっていない": [
                TestOrganizationModel.test500_関連するユーザーが存在しない,
                TestOrganizationModel.test400_オーナーユーザーが存在しない,
            ]
        },
    ],
    "組織一覧の取得": [
        TestOrganizationModel.test200_クエリが成功する場合,
        TestOrganizationModel.test200_組織一覧が取得できる,
        TestOrganizationView.test200_組織一覧を取得できる,
        {"組織一覧が取得できない": []},
    ],
    "ユーザーに関連した組織が表示されている": [
        {
            "ユーザーに関連する組織の取得ができる": [
                # ログインができる
                TestMembershipModel.test_正常_関連するorganizationとuserを取得する
            ]
        },
        {
            "取得された組織をレスポンスできる": [
                TestOrganizationSerializer.test200_バリデーションエラーがない,
                TestOrganizationView.test200_組織を作成しレスポンスできる,
            ]
        },
    ],
    "ユーザーに関連した組織が表示されていない": [
        {
            "ユーザーに関連する組織の取得できない": [
                TestOrganizationModel.test200_関連する組織が存在しない,
                TestOrganizationModel.test500_関連するユーザーが存在しない,
                TestOrganizationView.test400_ユーザーが存在するが取得できない,
            ]
        },
        {
            "リクエストができない": [],
            "レスポンスができない": [
                # "ユーザーが存在しないレスポンスエラー",
                TestOrganizationView.test異常_ユーザーIDが提供されていないレスポンスエラー,
                # "ユーザーがどの組織にも関連していないレスポンスエラー",
                # "ユーザーに関連する組織が存在しないレスポンスエラー",
            ],
        },
    ],
    "組織情報の取得": [
        TestOrganizationView.test200_組織情報を取得できる,
        TestOrganizationView.test400_組織情報が取得できていない,
        TestOrganizationView.test200_組織メンバーの一覧を取得できる,
    ],
    "組織に関連するスペースの取得": [
        TestOrganizationView.test200_組織に属するスペースの一覧が取得できる,
        "組織に属するスペースの一覧が取得できていない",
    ],
    "組織情報の更新": [
        TestOrganizationView.test200_組織名を更新できる,
        TestOrganizationView.test200_組織オーナーを更新できる,
        TestOrganizationView.test200_組織メンバーの追加ができる,
        TestOrganizationView.test200_組織メンバーの削除ができる,
        {
            "組織メンバーが存在しない": [
                TestOrganizationView.test400_組織メンバーの削除ができない
            ]
        },
        TestOrganizationView.test200_組織メンバーを更新できる,
        TOM.test200_組織アイコンをサーバーに保存および取得ができる,
        TestOrganizationView.test200_組織アイコンをアップロードできる,
        "組織アイコンを取得できる",
        "組織アイコンを削除できる",
    ],
    "組織の削除": [
        "認証されたオーナーにより組織が削除される",
        "組織削除後、関連するスペースやデータが削除される",
        "未認証ユーザーが組織削除を試みた場合のエラーハンドリング",
        "オーナー以外のユーザーが組織削除を試みた場合のエラーハンドリング",
    ],
    "権限管理": [
        "オーナー、管理者、メンバーの各ロールに応じたアクセス権限が適用されている",
        "オーナーは組織の設定を変更できる",
        "管理者は組織のメンバーを管理できるが組織の削除はできない",
        "メンバーは自分の情報のみ編集できる",
        "不適切な権限で組織設定を変更しようとした場合のエラーレスポンス",
        "不適切な権限で他のメンバー情報を編集しようとした場合のエラーレスポンス",
    ],
    "組織メンバーの取得": [
        TestUserView.test200_ユーザー一覧を取得できる,
        # []check
        TestUserView.test200_ユーザーが存在しない,
    ],
    "組織メンバーの招待": [
        "認証されたユーザーが新しいメンバーを組織に招待できる",
        "招待されたメンバーがメール通知を受け取る",
        "未認証ユーザーがメンバーを招待しようとした場合のエラーレスポンス",
        "無効なメールアドレスで招待しようとした場合のバリデーションエラー",
    ],
    "組織メンバーの役割変更": [
        "管理者がメンバーの役割を変更できる",
        "変更された役割に応じてユーザーの権限が更新される",
        "オーナー以外のユーザーが役割変更を試みた場合のエラーレスポンス",
        "無効な役割で更新しようとした場合のバリデーションエラー",
    ],
    "セキュリティテスト": [
        "組織情報のエンドポイントが適切にセキュリティ対策されている",
        "クロスサイトリクエストフォージェリ(CSRF)攻撃に対する防御",
        "SQLインジェクション攻撃に対する防御",
        "セッションハイジャック攻撃に対する防御",
    ],
    "パフォーマンステスト": [
        "高負荷時でも組織情報の読み込みと更新が適切に機能する",
        "大量の組織メンバーが同時にアクセスしてもシステムが安定している",
        "リソースの限界を超えた場合のシステムの応答を検証",
    ],
}

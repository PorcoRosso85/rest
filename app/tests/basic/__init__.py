test_design_for_basic = {
    "セキュリティテスト": {
        "項目": ["SQLインジェクション", "XSS", "HTTPS使用確認"],
    },
    "データベーステスト": {
        "項目": ["トランザクション動作確認", "バックアップ・復元テスト"],
    },
    "ユーザーエクスペリエンステスト": {
        "項目": ["ユーザビリティテスト", "アクセシビリティテスト"],
    },
    "バックアップ・復旧テスト": {
        "項目": ["データのバックアップ・復元プロセス検証"],
    },
    "パフォーマンステスト": ["大量リクエスト処理能力確認", "応答時間計測"],
}
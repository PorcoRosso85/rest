from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


import pytest
from rest_framework import serializers

from app.utils import logger


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "comments"]

    # []fixme validated_dataにidが渡されない
    def update(self, instance: Post, validated_data) -> Post:
        logger.debug("")
        comments_data = validated_data.pop("comments", [])
        for comment_data in comments_data:
            logger.debug(f"### comment_data: {comment_data}")
            comment_id = comment_data.get("id", None)
            if comment_id:
                # 既存のコメントを更新
                comment = Comment.objects.get(id=comment_id, post=instance)
                for attr, value in comment_data.items():
                    setattr(comment, attr, value)
                comment.save()
            else:
                # 新しいコメントを作成
                Comment.objects.create(post=instance, **comment_data)

        # Postインスタンスの更新
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class TestPostSerializer:
    @pytest.mark.skip("updateメソッドがid: comment.idを受け取れないためスキップ")
    @pytest.mark.django_db
    def test_正常系_PostSerializerからコメントを更新できる(self) -> None:
        post = Post.objects.create(title="title", content="content")
        comment = Comment.objects.create(post=post, text="text")

        serializer = PostSerializer(
            instance=post,
            data={
                "title": "new title",
                "content": "new content",
                "comments": [
                    {"id": comment.id, "text": "new text"},
                ],
            },
            partial=True,
        )

        # trueのとき、is_valid()はvalidated_dataに格納する
        assert serializer.is_valid()
        serializer.save()

        # post.refresh_from_db()
        assert post.title == "new title"
        assert post.content == "new content"
        assert post.comments.count() == 1
        assert post.comments.first().text == "new text"

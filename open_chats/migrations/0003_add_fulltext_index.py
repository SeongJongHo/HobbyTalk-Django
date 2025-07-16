# Generated manually for MySQL FULLTEXT index

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('open_chats', '0002_rename_deleted_time_openchat_deleted_at_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE open_chat_rooms ADD FULLTEXT(title) WITH PARSER ngram;",
            reverse_sql="ALTER TABLE open_chat_rooms DROP INDEX title;"
        ),
    ]

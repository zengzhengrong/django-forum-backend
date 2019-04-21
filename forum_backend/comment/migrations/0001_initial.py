# Generated by Django 2.1.7 on 2019-04-19 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('content', models.TextField(blank=True, verbose_name='内容')),
                ('object_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='关联类型ID')),
                ('nested', models.BooleanField(default=False, verbose_name='评论内联性质')),
                ('voted', models.BooleanField(default=False, verbose_name='投票性质')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='contenttypes.ContentType', verbose_name='关联类型')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='评论人')),
            ],
            options={
                'verbose_name': '评论/回复/投票',
                'verbose_name_plural': '评论/回复/投票',
                'ordering': ['-created'],
            },
        ),
    ]
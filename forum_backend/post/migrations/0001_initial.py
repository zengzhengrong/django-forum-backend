# Generated by Django 2.1.7 on 2019-04-19 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import utils.models_field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=128, verbose_name='标题')),
                ('body', models.TextField(blank=True, verbose_name='正文')),
                ('views', models.PositiveIntegerField(default=0, editable=False, verbose_name='浏览量')),
                ('pinned', models.BooleanField(default=False, verbose_name='置顶性质')),
                ('highlighted', models.BooleanField(default=False, verbose_name='加精性质')),
                ('hidden', models.BooleanField(default=False, verbose_name='隐藏性质')),
                ('voted', models.BooleanField(default=False, verbose_name='投票性质')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='category.Category', verbose_name='分类')),
            ],
            options={
                'verbose_name': '帖子',
                'verbose_name_plural': '帖子',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('question', models.CharField(blank=True, max_length=100, null=True, verbose_name='投票问题')),
                ('options', utils.models_field.ListField(blank=True, null=True, verbose_name='选项')),
                ('post', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vote', to='post.Post', verbose_name='关联帖子')),
                ('promoter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes', to=settings.AUTH_USER_MODEL, verbose_name='发起人')),
            ],
            options={
                'verbose_name': '投票',
                'verbose_name_plural': '投票',
                'ordering': ['-created'],
            },
        ),
    ]
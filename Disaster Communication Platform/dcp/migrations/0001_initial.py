# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-10 19:14
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('maxOutsideRadius', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('location_y', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('radius', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
            ],
        ),
        migrations.CreateModel(
            name='Bump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Bump_Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Catastrophe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('locationString', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('location_x', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('location_y', models.FloatField(validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('radius', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('maxOutsideRadius', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
            ],
            options={
                'permissions': (('EditCatastrophe', 'Kann eine Katastrophe editieren/löschen'), ('CreateCatastrophe', 'Kann eine Katastrophe erstellen')),
            },
        ),
        migrations.CreateModel(
            name='CategorysGoods',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('glyphiconString', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, null=True)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Comment_Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receiver', to=settings.AUTH_USER_MODEL)),
                ('Starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Starter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=5000)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('begin_date', models.DateTimeField(null=True)),
                ('numberOfUsers', models.PositiveSmallIntegerField(default=2, validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(100)])),
                ('numberOfCars', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('numberOfSpecials', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('cars', models.ManyToManyField(blank=True, to='dcp.Car')),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createdEvents', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Government',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_short', models.CharField(max_length=3)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GovernmentArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isFullAdmin', models.BooleanField(default=False)),
                ('canDeleteElements', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('canCreateSubArea', models.BooleanField(default=False)),
                ('canManageNgo', models.BooleanField(default=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Area')),
                ('government', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government')),
            ],
        ),
        migrations.CreateModel(
            name='GovernmentMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isOrganizationAdmin', models.BooleanField(default=False)),
                ('isAreaAdmin', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('government', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government')),
            ],
        ),
        migrations.CreateModel(
            name='Immaterial_Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(null=True)),
                ('location_y', models.FloatField(null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/goods/')),
                ('visibility', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField(max_length=5000)),
                ('SendTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('Conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Conversation', to='dcp.Conversation')),
                ('From', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='From', to=settings.AUTH_USER_MODEL)),
                ('To', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='To', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MissedPeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=5000)),
                ('gender', models.CharField(max_length=1)),
                ('age', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('name', models.CharField(max_length=100)),
                ('size', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(250)])),
                ('eyeColor', models.CharField(max_length=50)),
                ('hairColor', models.CharField(max_length=50)),
                ('characteristics', models.CharField(max_length=500)),
                ('picture', models.ImageField(null=True, upload_to='upload/people/')),
                ('bumps', models.ManyToManyField(related_name='PeopleBumps', to=settings.AUTH_USER_MODEL)),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('reports', models.ManyToManyField(related_name='PeopleReports', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ngo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_short', models.CharField(max_length=3)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NgoArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isFullAdmin', models.BooleanField(default=False)),
                ('canDeleteElements', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Area')),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo')),
            ],
        ),
        migrations.CreateModel(
            name='NgoMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isOrganizationAdmin', models.BooleanField(default=False)),
                ('isAreaAdmin', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('pubdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=256, null=True)),
                ('noticedBy', models.ManyToManyField(related_name='noticedNotifications', to=settings.AUTH_USER_MODEL)),
                ('toUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customNotifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer_Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(null=True)),
                ('location_y', models.FloatField(null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/goods/')),
                ('visibility', models.BooleanField(default=True)),
                ('timeline_badge_color', models.CharField(default='red', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-transfer', max_length=100)),
                ('bumps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Bump_Relation')),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcp.CategorysGoods')),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Comment_Relation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post_Dangers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(null=True)),
                ('location_y', models.FloatField(null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/goods/')),
                ('visibility', models.BooleanField(default=True)),
                ('timeline_badge_color', models.CharField(default='yellow', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-info-sign', max_length=100)),
                ('bumps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Bump_Relation')),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Comment_Relation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post_News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(null=True)),
                ('location_y', models.FloatField(null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/goods/')),
                ('visibility', models.BooleanField(default=True)),
                ('timeline_badge_color', models.CharField(default='yellow', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-info-sign', max_length=100)),
                ('bumps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Bump_Relation')),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Comment_Relation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post_Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(null=True)),
                ('location_y', models.FloatField(null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/goods/')),
                ('visibility', models.BooleanField(default=True)),
                ('timeline_badge_color', models.CharField(default='yellow', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-info-sign', max_length=100)),
                ('bumps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Bump_Relation')),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Comment_Relation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_map', models.BooleanField(default=True)),
                ('show_picture', models.BooleanField(default=True)),
                ('currentCatastrophe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dcp.Catastrophe')),
                ('government', models.ManyToManyField(through='dcp.GovernmentMember', to='dcp.Government')),
                ('ngo', models.ManyToManyField(through='dcp.NgoMember', to='dcp.Ngo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(blank=True, max_length=500, null=True)),
                ('choice_text', models.CharField(default='Ja; Nein', max_length=500)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2016, 7, 10, 19, 14, 37, 331570, tzinfo=utc), verbose_name='date published')),
                ('catastrophe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voted_users', models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Report_Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Search_Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('locationString', models.CharField(default='', max_length=200, null=True)),
                ('location_x', models.FloatField(null=True)),
                ('location_y', models.FloatField(null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, null=True, upload_to='upload/goods/')),
                ('visibility', models.BooleanField(default=True)),
                ('radius', models.PositiveSmallIntegerField(choices=[(0, '0 km'), (1, '1 km'), (2, '2 km'), (5, '5 km'), (10, '10 km'), (50, '50 km'), (100, '100 km'), (1000, '1000 km')], default=0)),
                ('timeline_badge_color', models.CharField(default='blue', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-search', max_length=100)),
                ('bumps', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Bump_Relation')),
                ('catastrophe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcp.CategorysGoods')),
                ('comments', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Comment_Relation')),
                ('reports', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Report_Relation')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GovernmentInvite',
            fields=[
                ('invite_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Invite')),
            ],
            bases=('dcp.invite',),
        ),
        migrations.CreateModel(
            name='NgoInvite',
            fields=[
                ('invite_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Invite')),
            ],
            bases=('dcp.invite',),
        ),
        migrations.CreateModel(
            name='Offer_Immaterial',
            fields=[
                ('immaterial_goods_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Immaterial_Goods')),
                ('timeline_badge_color', models.CharField(default='red', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-transfer', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('dcp.immaterial_goods',),
        ),
        migrations.CreateModel(
            name='Search_Immaterial',
            fields=[
                ('immaterial_goods_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Immaterial_Goods')),
                ('radius', models.PositiveSmallIntegerField(choices=[(0, '0 km'), (1, '1 km'), (2, '2 km'), (5, '5 km'), (10, '10 km'), (50, '50 km'), (100, '100 km'), (1000, '1000 km')], default=0)),
                ('timeline_badge_color', models.CharField(default='blue', max_length=100)),
                ('timeline_glyphicon', models.CharField(default='glyphicon-search', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('dcp.immaterial_goods',),
        ),
        migrations.AddField(
            model_name='report',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Report_Relation'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post_questions',
            name='reports',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Report_Relation'),
        ),
        migrations.AddField(
            model_name='post_questions',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post_news',
            name='reports',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Report_Relation'),
        ),
        migrations.AddField(
            model_name='post_news',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post_dangers',
            name='reports',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Report_Relation'),
        ),
        migrations.AddField(
            model_name='post_dangers',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offer_material',
            name='reports',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Report_Relation'),
        ),
        migrations.AddField(
            model_name='offer_material',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ngomember',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile'),
        ),
        migrations.AddField(
            model_name='ngo',
            name='areas',
            field=models.ManyToManyField(through='dcp.NgoArea', to='dcp.Area'),
        ),
        migrations.AddField(
            model_name='immaterial_goods',
            name='bumps',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Bump_Relation'),
        ),
        migrations.AddField(
            model_name='immaterial_goods',
            name='catastrophe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe'),
        ),
        migrations.AddField(
            model_name='immaterial_goods',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Comment_Relation'),
        ),
        migrations.AddField(
            model_name='immaterial_goods',
            name='reports',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Report_Relation'),
        ),
        migrations.AddField(
            model_name='immaterial_goods',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='governmentmember',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile'),
        ),
        migrations.AddField(
            model_name='government',
            name='areas',
            field=models.ManyToManyField(through='dcp.GovernmentArea', to='dcp.Area'),
        ),
        migrations.AddField(
            model_name='event',
            name='specials',
            field=models.ManyToManyField(blank=True, to='dcp.Special'),
        ),
        migrations.AddField(
            model_name='comment',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Comment_Relation'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='dcp.Question'),
        ),
        migrations.AddField(
            model_name='catastrophe',
            name='governments',
            field=models.ManyToManyField(related_name='catastrophes', to='dcp.Government'),
        ),
        migrations.AddField(
            model_name='catastrophe',
            name='ngos',
            field=models.ManyToManyField(related_name='catastrophes', to='dcp.Ngo'),
        ),
        migrations.AddField(
            model_name='bump',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Bump_Relation'),
        ),
        migrations.AddField(
            model_name='bump',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='area',
            name='catastrophe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe'),
        ),
        migrations.AddField(
            model_name='area',
            name='parrent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dcp.Area'),
        ),
        migrations.AlterUniqueTogether(
            name='ngomember',
            unique_together=set([('profile', 'ngo')]),
        ),
        migrations.AddField(
            model_name='ngoinvite',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo'),
        ),
        migrations.AddField(
            model_name='ngoinvite',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile'),
        ),
        migrations.AlterUniqueTogether(
            name='ngoarea',
            unique_together=set([('ngo', 'area')]),
        ),
        migrations.AlterUniqueTogether(
            name='governmentmember',
            unique_together=set([('profile', 'government')]),
        ),
        migrations.AddField(
            model_name='governmentinvite',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government'),
        ),
        migrations.AddField(
            model_name='governmentinvite',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile'),
        ),
        migrations.AlterUniqueTogether(
            name='governmentarea',
            unique_together=set([('government', 'area')]),
        ),
        migrations.AlterUniqueTogether(
            name='conversation',
            unique_together=set([('Starter', 'Receiver')]),
        ),
        migrations.AlterUniqueTogether(
            name='catastrophe',
            unique_together=set([('title', 'locationString')]),
        ),
        migrations.AlterUniqueTogether(
            name='ngoinvite',
            unique_together=set([('profile', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='governmentinvite',
            unique_together=set([('profile', 'organization')]),
        ),
    ]

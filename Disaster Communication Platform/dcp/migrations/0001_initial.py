# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-24 21:41
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
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
                ('Title', models.CharField(max_length=200)),
                ('Location', models.CharField(max_length=100)),
                ('PubDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
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
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('canAddNgo', models.BooleanField(default=False)),
                ('canDeleteNgo', models.BooleanField(default=False)),
                ('canDeleteElements', models.BooleanField(default=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Area')),
                ('government', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government')),
            ],
        ),
        migrations.CreateModel(
            name='Immaterial_Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
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
            name='Invite_Government',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invite_Ngo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
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
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('canDeleteElements', models.BooleanField(default=False)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Area')),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo')),
            ],
        ),
        migrations.CreateModel(
            name='Offer_Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
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
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_organization_admin', models.BooleanField(default=False)),
                ('date_joined_organization', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('show_map', models.BooleanField(default=True)),
                ('show_picture', models.BooleanField(default=True)),
                ('currentCatastrophe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='currentCatastrophe', to='dcp.Catastrophe')),
                ('government', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Government')),
                ('ngo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dcp.Ngo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
            model_name='ngo',
            name='areas',
            field=models.ManyToManyField(through='dcp.NgoArea', to='dcp.Area'),
        ),
        migrations.AddField(
            model_name='invite_ngo',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo'),
        ),
        migrations.AddField(
            model_name='invite_ngo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
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
        migrations.AlterUniqueTogether(
            name='catastrophe',
            unique_together=set([('Title', 'Location')]),
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
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dcp.Catastrophe'),
        ),
        migrations.AlterUniqueTogether(
            name='conversation',
            unique_together=set([('Starter', 'Receiver')]),
        ),
    ]

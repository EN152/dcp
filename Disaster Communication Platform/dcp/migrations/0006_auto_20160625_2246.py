# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-25 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dcp', '0005_auto_20160625_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isOrganizationAdmin', models.BooleanField(default=False)),
                ('isAreaAdmin', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='invite_government',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='invite_government',
            name='user',
        ),
        migrations.RemoveField(
            model_name='invite_ngo',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='invite_ngo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='date_joined_organization',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_organization_admin',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='government',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='ngo',
        ),
        migrations.CreateModel(
            name='GovernmentInvite',
            fields=[
                ('invite_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Invite')),
                ('government', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile')),
            ],
            bases=('dcp.invite',),
        ),
        migrations.CreateModel(
            name='GovernmentMember',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Member')),
                ('government', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Government')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile')),
            ],
            bases=('dcp.member',),
        ),
        migrations.CreateModel(
            name='NgoInvite',
            fields=[
                ('invite_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Invite')),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile')),
            ],
            bases=('dcp.invite',),
        ),
        migrations.CreateModel(
            name='NgoMember',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcp.Member')),
                ('ngo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Ngo')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dcp.Profile')),
            ],
            bases=('dcp.member',),
        ),
        migrations.DeleteModel(
            name='Invite_Government',
        ),
        migrations.DeleteModel(
            name='Invite_Ngo',
        ),
        migrations.AddField(
            model_name='profile',
            name='government',
            field=models.ManyToManyField(through='dcp.GovernmentMember', to='dcp.Government'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ngo',
            field=models.ManyToManyField(through='dcp.NgoMember', to='dcp.Ngo'),
        ),
        migrations.AlterUniqueTogether(
            name='ngomember',
            unique_together=set([('profile', 'ngo')]),
        ),
        migrations.AlterUniqueTogether(
            name='ngoinvite',
            unique_together=set([('profile', 'ngo')]),
        ),
        migrations.AlterUniqueTogether(
            name='governmentmember',
            unique_together=set([('profile', 'government')]),
        ),
        migrations.AlterUniqueTogether(
            name='governmentinvite',
            unique_together=set([('profile', 'government')]),
        ),
    ]
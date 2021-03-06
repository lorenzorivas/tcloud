# Generated by Django 3.2.9 on 2021-12-06 14:41

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_title', models.CharField(max_length=255, verbose_name='Area')),
                ('responsable', models.CharField(max_length=255, verbose_name='Lider Area')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='País')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='virtualization.area')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Colaborador',
                'verbose_name_plural': 'Colaboradores',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=200, verbose_name='Titulo')),
                ('year', models.IntegerField(null=True, verbose_name='Año Proyectado')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Pais')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='project_title')),
                ('resume', tinymce.models.HTMLField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('planned_date', models.DateField(null=True, verbose_name='Fecha Planificada')),
                ('done_date', models.DateField(blank=True, null=True, verbose_name='Fecha de termino Real')),
                ('state', models.BooleanField(blank=True, default=False, null=True, verbose_name='Terminando?')),
                ('collaborator', models.ManyToManyField(related_name='Colaborador', to='virtualization.Collaborator', verbose_name='Colaboradores')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=255, verbose_name='Proveedor')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, verbose_name='Sitio')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant_hostname', models.CharField(max_length=255, verbose_name='Hostname')),
                ('ip_inband', models.GenericIPAddressField(blank=True, null=True)),
                ('ip_outband', models.GenericIPAddressField(blank=True, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.site')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_name', models.CharField(max_length=200, verbose_name='Nombre VM')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='vm_name')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('state', models.BooleanField(blank=True, default=False, null=True, verbose_name='Activa')),
                ('vcpu_total', models.IntegerField(null=True, verbose_name='vCPU')),
                ('ram_total', models.IntegerField(null=True, verbose_name='RAM')),
                ('internal_disk_total', models.IntegerField(null=True, verbose_name='Disco IN')),
                ('external_disk_total', models.IntegerField(blank=True, null=True, verbose_name='Disco EX')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.project')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.site')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='virtualization.tenant')),
            ],
            options={
                'verbose_name': 'Virtual Machine',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todo_title', models.CharField(max_length=200, verbose_name='Titulo')),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, editable=False, null=True, populate_from='todo_title')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('deadline_date', models.DateField(null=True, verbose_name='Fecha planificación')),
                ('done_date', models.DateField(blank=True, null=True, verbose_name='Fecha termino')),
                ('state', models.BooleanField(blank=True, default=False, null=True, verbose_name='Terminado')),
                ('progress', models.IntegerField(blank=True, default=0, null=True)),
                ('ordering_position', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('collaborator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='virtualization.collaborator', verbose_name='Encargado')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='virtualization.project')),
            ],
            options={
                'verbose_name': 'Tareas de Proyecto',
                'ordering': ['ordering_position'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.provider', verbose_name='Proveedor'),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('ip_address_mask', models.CharField(max_length=200, verbose_name='IP/MASK')),
                ('vlan_id', models.CharField(max_length=200, verbose_name='VLAN')),
                ('vrrp_vip', models.GenericIPAddressField(blank=True, null=True)),
                ('vrrp_r1', models.GenericIPAddressField(blank=True, null=True)),
                ('vrrp_r2', models.GenericIPAddressField(blank=True, null=True)),
                ('vrf_name', models.CharField(max_length=200, verbose_name='VRF')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.project')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.site')),
            ],
        ),
        migrations.CreateModel(
            name='Descriptor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptor_name', models.CharField(max_length=200, verbose_name='Titulo')),
                ('descriptor', tinymce.models.HTMLField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='virtualization.project')),
            ],
        ),
    ]

# Generated by Django 2.1.5 on 2019-02-16 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=15)),
                ('cipher_format', models.CharField(max_length=255)),
                ('compromised_data', models.TextField()),
                ('description', models.TextField()),
                ('path', models.FilePathField(allow_folders=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.TextField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.TextField()),
                ('now', models.DateTimeField(auto_now=True)),
                ('all_datasets', models.BooleanField(default=False)),
                ('datasets', models.ManyToManyField(to='search.Dataset')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Search'),
        ),
        migrations.AddField(
            model_name='item',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Result'),
        ),
    ]
# Generated by Django 4.0.5 on 2022-11-10 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0001_initial'),
        ('order_app', '0002_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('failed', 'Rejected'), ('success', 'Accepted'), ('pending', 'Pending'), ('cancelled', 'Cancelled'), ('delivered', 'Delivered')], default='pending', max_length=20),
        ),
    ]

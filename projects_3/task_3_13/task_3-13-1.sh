#!/bin/bash
# Замена старого пути на новый с помощью sed (альтернативный разделитель |)
sed -i 's|/var/lib/mysql/data|/mnt/ssd/mysql|g' settings.php

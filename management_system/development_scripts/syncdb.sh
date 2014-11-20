#!/bin/bash
echo 'default'
python ../manage.py syncdb
echo 'sub1'
python ../manage.py syncdb --database='sub1'
echo 'sub2'
python ../manage.py syncdb --database='sub2'

#!/usr/bin/perl -w
use strict;
use warnings;

system(docker-compose exec spark spark-submit /w205/w205-final-project/write_purchase_stream.py &);

#!/usr/bin/env python
# vi:ai:et:ts=4 sw=4
#
# -*- coding: utf8 -*-
#
# PyMmr My Music Renamer
# Copyright (C) 2007-2010  mathgl67@gmail.com
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import os
from optparse import OptionParser

try:
    import MySQLdb
except ImportError:
    print "MySQLdb is needed by this script"
    sys.exit(-1)


def verbose_print(options, text):
    if options.verbose:
        print(text)

def parse_args():
    usage = "usage: %prog [options] create|destroy|add|do"
    
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="make the script more verbose...")
    parser.add_option("", "--host", dest="host", type="string", default="localhost", help="define the mysql host server")
    parser.add_option("", "--user", dest="user", type="string", default="root", help="define the mysql user name")
    parser.add_option("", "--pass", dest="password", type="string", default="", help="define the mysql password")
    parser.add_option("", "--db", dest="db", type="string", default="freedb", help="define the mysql password")
    parser.add_option("-m", "--max", dest="max", type="int", default=20, help="set the maximum job numer the do action can done...")

    return (parser, parser.parse_args(sys.argv))

def mysql_connect(options):
    db = MySQLdb.connect(host=options.host, user=options.user, passwd=options.password, db=options.db)
    if not db:
        print "Cannot connect to mysql database"
        sys.exit(-2)
    return db

def parse_line(line, result):
    if line[0] == "#":
        return (None, None)

    (key, value) = line.split("=", 1)
    if key == "DISCID":
        result['discid'] = value
    elif key == "DTITLE":
        splited = value.split("/", 1)
        if len(splited) is 2:
            result['artist'] = splited[0].strip()
            result['title'] = splited[1].strip()
        else:
            result['artist'] = ""
            result['title'] = value 
    elif key == "DGENRE":
        result['genre'] = value
    elif key == "DYEAR":
        if value == "":
            result['year'] = "NULL"
        else:
            result['year'] = int(value)
    elif key.startswith("TTITLE"):
        keysplit = key.split("TTITLE", 1)
        num = int(keysplit[1]) + 1
        result['tracks'].append({"number": num, "title": value })

def parse_file(fullpath):
    result = { "tracks": [] }
    with open(fullpath, "r") as file:
        for line in file:
            parse_line(line[:-1], result)
    return result

def job_add(options, db, fullpath):
    db.query("""INSERT INTO job ( file ) VALUES ( "%s" );""" % db.escape_string(fullpath))
    db.commit()
    verbose_print(options, "job '%s' added" % fullpath)

def job_directory_add(options, db, fullpath):
    for (filepath, dirnames, filenames) in os.walk(fullpath):
        # recursive for sub directory
        for dirname in dirnames:
            job_directory_add(options, db, os.path.join(filepath, dirname))

        # add file to job list
        for filename in filenames:
            job_add(options, db, os.path.join(filepath, filename))

    verbose_print(options, "directory '%s' added." % (fullpath))

def action_add(options, args):
    verbose_print(options, "action add")

    db = mysql_connect(options) 
    verbose_print(options, "connected to mysql")

    job_directory_add(options, db, args[2])

def action_do(options, args):
    verbose_print(options, "action do")
 
    db = mysql_connect(options) 
    verbose_print(options, "connected to mysql")

    # SOULD BE LOCKED OPERATION TO BE THREAD SAFE
    db.query("""SELECT id, file FROM job LIMIT 0,%d""" % (options.max))
    r = db.store_result()
    res = r.fetch_row(0)

    for (id, file) in res:
        verbose_print(options, "delete job...")
        db.query("""DELETE FROM job WHERE id = %d""" % (id))
    
    db.commit()
    # SOULD BE LOCKED OPERATION TO BE THREAD SAFE

    verbose_print(options, "Parse file and add..")
    for (id, file) in res:
        print "file: %s (id:%d)" % (file, id)
        data = parse_file(file)
        db.query("""
        INSERT INTO album (
            discid, artist, title, genre, year
        ) VALUES (
            "%s", "%s", "%s", "%s", %s
        )
        """ % (
            db.escape_string(data['discid']),
            db.escape_string(data['artist']),
            db.escape_string(data['title']),
            db.escape_string(data['genre']),
            data['year'])
        )

        id = db.insert_id()
        for track in data['tracks']:
            db.query("""
            INSERT INTO track (
                album_id, number, title
            ) VALUES (
                %d, %d, "%s"
            )
            """ % ( id, track['number'], db.escape_string(track['title'] )))
        db.commit()

def action_destroy(options, args, db=None):
    verbose_print(options, "action destroy")

    if not db:
        db = mysql_connect(options) 
        verbose_print(options, "connected to mysql")

    verbose_print(options, "destroy job table")
    db.query("""DROP TABLE IF EXISTS job""")

    verbose_print(options, "destroy track table")
    db.query("""DROP TABLE IF EXISTS track""")

    verbose_print(options, "destroy album table")
    db.query("""DROP TABLE IF EXISTS album""")

    print("all tables destroyed!")
   

def action_create(options, args, db=None):
    verbose_print(options, "action create")

    if not db:
        db = mysql_connect(options) 
        verbose_print(options, "connected to mysql")

    action_destroy(options, args, db=db) 

    verbose_print(options, "create job table")
    db.query("""DROP TABLE IF EXISTS job""")
    db.query("""
    CREATE TABLE `job` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `file` TEXT NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """)

    verbose_print(options, "create album table")
    db.query("""DROP TABLE IF EXISTS album""")
    db.query("""
    CREATE TABLE `album` (
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `discid` varchar(25) NOT NULL,
        `artist` varchar(255),
        `title` varchar(255) NOT NULL,
        `genre` varchar(255) DEFAULT NULL,
        `year` int(11) DEFAULT NULL,
        PRIMARY KEY (`id`),
        KEY `_idx_artist` (`artist`),
        KEY `_idx_title` (`title`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """)

    verbose_print(options, "create track table")
    db.query("""DROP TABLE IF EXISTS track""")
    db.query("""
    CREATE TABLE `track` (
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `album_id` bigint(20) NOT NULL,
        `number` int(11) NOT NULL,
        `title` varchar(512) NOT NULL,
        PRIMARY KEY (`id`),
        KEY `_fk_album_id` (`album_id`),
        KEY `_idx_title` (`title`(255)),
        CONSTRAINT `_fk_album_id` FOREIGN KEY (`album_id`) REFERENCES `album` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    """)

    print("all tables created!")


def main():
    (parser, (options, args)) = parse_args()

    if len(args) is 1:
        parser.error("action must be set")

    if args[1] == "create":
        action_create(options, args)
    elif args[1] == "destroy":
        action_destroy(options, args)
    elif args[1] == "add":
        if len(args) is 2:
            parser.error("action add need a path")
        action_add(options, args)
    elif args[1] == "do":
        action_do(options, args)
    else:
        parser.error("action not understand")

main()

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Studio.extra'
        db.add_column('machineapp_studio', 'extra',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Studio.extra'
        db.delete_column('machineapp_studio', 'extra')


    models = {
        'machineapp.boxoffice': {
            'Meta': {'object_name': 'BoxOffice'},
            'box_office_date': ('django.db.models.fields.DateField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gross': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Movie']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'machineapp.casting': {
            'Meta': {'object_name': 'Casting'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Movie']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Person']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'machineapp.emailsignup': {
            'Meta': {'object_name': 'EmailSignup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'machineapp.movie': {
            'Meta': {'object_name': 'Movie'},
            'boxofficemojo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'budget': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cast': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['machineapp.Person']", 'through': "orm['machineapp.Casting']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fandango_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'mpaa_rating': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'runtime': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'studio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Studio']", 'null': 'True'}),
            'thenumbers_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'machineapp.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {}),
            'birth_city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'birth_country': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'birth_state': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'bname_first': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'bname_last': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'bname_middle': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'boxofficemojo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fandango_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'known_for': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'thenumbers_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'machineapp.picture': {
            'Meta': {'object_name': 'Picture'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Movie']", 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Person']", 'null': 'True'})
        },
        'machineapp.prediction': {
            'Meta': {'object_name': 'Prediction'},
            'accuracy': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '4'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gross': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machineapp.Movie']"}),
            'prediction_date': ('django.db.models.fields.DateField', [], {}),
            'rank': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'machineapp.studio': {
            'Meta': {'object_name': 'Studio'},
            'boxofficemojo_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'fandango_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'thenumbers_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['machineapp']
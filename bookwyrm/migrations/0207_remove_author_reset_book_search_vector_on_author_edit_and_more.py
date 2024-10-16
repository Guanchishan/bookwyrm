# Generated by Django 4.2.11 on 2024-10-11 06:54

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookwyrm', '0206_merge_20240415_1537'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='author',
            name='reset_book_search_vector_on_author_edit',
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name='book',
            name='update_search_vector_on_book_edit',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='author',
            trigger=pgtrigger.compiler.Trigger(name='reset_book_search_vector_on_author_edit', sql=pgtrigger.compiler.UpsertTriggerSql(func="WITH updated_books AS (SELECT book_id FROM bookwyrm_book_authors WHERE author_id = new.id) UPDATE bookwyrm_book SET search_vector = '' FROM updated_books WHERE id = updated_books.book_id;RETURN NEW;", hash='4eeb17d1c9c53f543615bcae1234bd0260adefcc', operation='UPDATE OF "name", "aliases"', pgid='pgtrigger_reset_book_search_vector_on_author_edit_a50c7', table='bookwyrm_author', when='AFTER')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='book',
            trigger=pgtrigger.compiler.Trigger(name='update_search_vector_on_book_edit', sql=pgtrigger.compiler.UpsertTriggerSql(func="WITH author_names AS (SELECT array_to_string(bookwyrm_author.name || bookwyrm_author.aliases, ' ') AS name_and_aliases FROM bookwyrm_author LEFT JOIN bookwyrm_book_authors ON bookwyrm_author.id = bookwyrm_book_authors.author_id WHERE bookwyrm_book_authors.book_id = new.id) SELECT setweight(coalesce(nullif(to_tsvector('english', new.title), ''), to_tsvector('simple', new.title)), 'A') || setweight(to_tsvector('english', coalesce(new.subtitle, '')), 'B') || (SELECT setweight(to_tsvector('simple', coalesce(array_to_string(array_agg(name_and_aliases), ' '), '')), 'C') FROM author_names) || setweight(to_tsvector('english', coalesce(new.series, '')), 'D') INTO new.search_vector;RETURN NEW;", hash='676d929ce95beff671544b6add09cf9360b6f299', operation='INSERT OR UPDATE OF "title", "subtitle", "series", "search_vector"', pgid='pgtrigger_update_search_vector_on_book_edit_bec58', table='bookwyrm_book', when='BEFORE')),
        ),
    ]

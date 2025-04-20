import click
from flask.cli import with_appcontext
from scripts.populate_wines import populate_wines_from_data

@click.command('populate-wines')
@with_appcontext
def populate_wines_command():
    """Populate the database with wines from the data files."""
    click.echo('Populating wines from data files...')
    wines_created = populate_wines_from_data()
    click.echo(f'Successfully created {wines_created} wines in the database.')

def init_app(app):
    app.cli.add_command(populate_wines_command) 
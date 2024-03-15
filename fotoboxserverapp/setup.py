import click
import os
import fotoboxserverapp.db
from flask import current_app, g
from werkzeug.security import check_password_hash, generate_password_hash

@click.command('makeconfig')
@click.option('--apikey', help='The API key used to authorize foto uploads.')
@click.option('--adminpassword', help='The admin password for the web backend login.')
@click.option('--initdb', is_flag=True, help='Initialize database (mandatory for first setup)')
def setup_command(apikey, adminpassword, initdb):

    if apikey:
        pwhash = generate_password_hash(apikey)
        current_app.config['API_KEY'] = pwhash

    if adminpassword:
        pwhash = generate_password_hash(adminpassword)
        current_app.config['ADMIN_PASSWORD'] = pwhash

    # also auto-generate secure secret key if none is set yet
    if current_app.config['SECRET_KEY'] == 'nope':
        current_app.config['SECRET_KEY'] = str(os.urandom(32).hex())

    if initdb:
        fotoboxserverapp.db.init_db()


    if not 'API_KEY' in current_app.config:
        click.echo('No API Key! Please run makeconfig with --apikey')
        return

    if not 'ADMIN_PASSWORD' in current_app.config:
        click.echo('No Admin Password! Please run makeconfig with --adminpassword')
        return


    # why is there no built-in way to write config?
    click.echo()
    click.echo('# generated configuration file')
    click.echo('# save this to instance/config.py')
    click.echo("API_KEY='" + current_app.config['API_KEY'] + "'")
    click.echo("ADMIN_PASSWORD='" + current_app.config['ADMIN_PASSWORD'] + "'")
    click.echo("SECRET_KEY='" + current_app.config['SECRET_KEY'] + "'")
    click.echo()

def init_app(app):
    app.cli.add_command(setup_command)
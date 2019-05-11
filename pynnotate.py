import click
import os

from annotate import write_to_file

@click.command()
@click.option('--model-path', required=True)
@click.option('--db-name')
@click.option('--db')
@click.option('--db-host')
@click.option('--db-user')
@click.option('--db-password')
@click.option('--config-path')
def main(model_path, db, db_name, db_host, db_user, db_password, config_path):
    write_to_file(model_path, config_path,
        db_name=db_name, db_host=db_host,
        db_user=db_user, db_password=db_password, db=db
    )

if __name__ == '__main__':
    main()
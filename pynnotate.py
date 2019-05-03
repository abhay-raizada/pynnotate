import click
from annotate import write_to_file

@click.command()
@click.option('--model-path', required=True)
@click.option('--db-name', required=True)
@click.option('--db', required=True)
@click.option('--db-host', required=True)
@click.option('--db-user', required=True)
@click.option('--db-password', required=True)
def main(model_path, db_name, db, db_host, db_user, db_password):
    print(model_path, db_name, db)
    write_to_file(model_path, db_name, db, db_host, db_user, db_password)

if __name__ == '__main__':
    main()
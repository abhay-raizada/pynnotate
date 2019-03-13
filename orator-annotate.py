import click
from annotate import write_to_file

@click.command()
@click.option('--model-path', required=True)
@click.option('--config-path', required=True)
def main(model_path, config_path):
    print(model_path, config_path)
    write_to_file(model_path, config_path)

if __name__ == '__main__':
    main()
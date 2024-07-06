import click
from utils.env_manager import update_hot_keywords, get_hot_keywords
from core.tasks import trigger_cache_preheat

# use 'python cli.py update-keywords AI Machine-Learning NLP' to update the .env file and trigger the preheating
@click.group()
def cli():
    pass

@cli.command()
@click.argument('keywords', nargs=-1)
def update_keywords(keywords):
    """Update HOT_KEYWORDS in .env file"""
    if not keywords:
        click.echo("Please provide at least one keyword.")
        return
    update_hot_keywords(keywords)
    click.echo(f"Updated HOT_KEYWORDS to: {', '.join(keywords)}")
    click.echo("Triggering cache preheat...")
    trigger_cache_preheat.delay()

@cli.command()
def show_keywords():
    """Show current HOT_KEYWORDS"""
    keywords = get_hot_keywords()
    click.echo(f"Current HOT_KEYWORDS: {', '.join(keywords)}")

if __name__ == '__main__':
    cli()
#!/usr/bin/env python
# coding: utf-8

import logging
import click

from mkdocs import __version__
from mkdocs import build
from mkdocs import gh_deploy
from mkdocs import new
from mkdocs import serve
from mkdocs import utils
from mkdocs.config import load_config

log = logging.getLogger(__name__)


def configure_logging(log_name='mkdocs', level=logging.INFO):
    '''When a --verbose flag is passed, increase the verbosity of mkdocs'''

    logger = logging.getLogger(log_name)
    logger.propagate = False
    stream = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)-7s -  %(message)s ")
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    logger.setLevel(level)


clean_help = "Remove old files from the site_dir before building"
config_file_help = "Provide a specific MkDocs config"
dev_addr_help = ("IP address and port to serve documentation locally (default: "
                 "localhost:8000)")
strict_help = ("Enable strict mode. This will cause MkDocs to abort the build "
               "on any warnings.")
theme_help = "The theme to use when building your documentation."
theme_choices = utils.get_theme_names()
site_dir_help = "The directory to output the result of the documentation build."
reload_help = "Enable and disable the live reloading in the development server."


@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output")
@click.version_option(__version__)
def cli(verbose):
    """
    MkDocs - Project documentation with Markdown.
    """

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    configure_logging(level=level)


@cli.command(name="serve")
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
@click.option('--dev-addr', help=dev_addr_help, metavar='<IP:PORT>')
@click.option('--strict', is_flag=True, help=strict_help)
@click.option('--theme', type=click.Choice(theme_choices), help=theme_help)
@click.option('--livereload/--no-livereload', default=True, help=reload_help)
def serve_command(dev_addr, config_file, strict, theme, livereload):
    """Run the builtin development server"""

    logging.getLogger('tornado').setLevel(logging.WARNING)

    serve.serve(
        config_file=config_file,
        dev_addr=dev_addr,
        strict=strict,
        theme=theme,
        livereload=livereload,
    )


@cli.command(name="build")
@click.option('--clean', is_flag=True, help=clean_help)
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
@click.option('--strict', is_flag=True, help=strict_help)
@click.option('--theme', type=click.Choice(theme_choices), help=theme_help)
@click.option('--site-dir', type=click.Path(), help=site_dir_help)
def build_command(clean, config_file, strict, theme, site_dir):
    """Build the MkDocs documentation"""
    build.build(load_config(
        config_file=config_file,
        strict=strict,
        theme=theme,
        site_dir=site_dir
    ), clean_site_dir=clean)


@cli.command(name="json")
@click.option('--clean', is_flag=True, help=clean_help)
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
@click.option('--strict', is_flag=True, help=strict_help)
@click.option('--site-dir', type=click.Path(), help=site_dir_help)
def json_command(clean, config_file, strict, site_dir):
    """Build the MkDocs documentation to JSON files

    Rather than building your documentation to HTML pages, this
    outputs each page in a simple JSON format. This command is
    useful if you want to index your documentation in an external
    search engine.
    """

    log.warning("The json command is deprcated and will be removed in a future "
                "MkDocs release. For details on updating: "
                "http://www.mkdocs.org/about/release-notes/")

    build.build(load_config(
        config_file=config_file,
        strict=strict,
        site_dir=site_dir
    ), dump_json=True, clean_site_dir=clean)


@cli.command(name="gh-deploy")
@click.option('--clean', is_flag=True, help=clean_help)
@click.option('--config-file', type=click.File('rb'), help=config_file_help)
def gh_deploy_command(config_file, clean):
    """Deply your documentation to GitHub Pages"""
    config = load_config(
        config_file=config_file
    )
    build.build(config, clean_site_dir=clean)
    gh_deploy.gh_deploy(config)


@cli.command(name="new")
@click.argument("project_directory")
def new_command(project_directory):
    """Create a new MkDocs project"""
    new.new(project_directory)

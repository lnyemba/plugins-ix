#!/usr/bin/env python
__doc__ = """


"""
import pandas as pd
import numpy as np
import json 
import sys
import time
from multiprocessing import Process

import os
import typer
from typing_extensions import Annotated
from typing import Optional
import time
from termcolor import colored
from enum import Enum
from rich import print
# from rich.console import Console
from rich.table import Table
import plugins
app = typer.Typer()
# app_e = typer.Typer()   #-- handles etl (run, generate)
# app_x = typer.Typer()   #-- handles plugins (list,add, test)
# app_i = typer.Typer()   #-- handles information (version, license)
appr = typer.Typer()   #-- handles registry    
# REGISTRY_PATH=os.sep.join([os.environ['HOME'],'.data-transport'])
# REGISTRY_FILE= 'transport-registry.json'
CHECK_MARK = '[ [green]\u2713[/green] ]' #' '.join(['[',colored(u'\u2713', 'green'),']'])
TIMES_MARK= '[ [red]\u2717[/red] ]' #' '.join(['[',colored(u'\u2717','red'),']'])
# @app.command()





@app.command(name="plugin")
def inspect (file: Annotated[str,typer.Argument(help="python file that contains functions look into")],
             decorator:str=typer.Option(default=None,help="decorator attribute name (if any) ") ) :
    """
    This function allows plugin management / testing 
    """
    loader = plugins.Loader()
    if loader.load(file=file,decorator= decorator) :
        n = len(loader._modules.keys())
        print (f"""{CHECK_MARK} Found {n} functions in [bold]{file}[/bold]""")
    else:
        _msg = f"""{TIMES_MARK} Invalid python file {file}"""
        print (_msg)
@appr.command(name="add")
def add_registry(
    
    python_file: Annotated[str,typer.Argument(help="python file that contains functions to be used as plugins")],
    registry_folder:str=typer.Option(default=os.environ.get('REGISTRY_FOLDER',None),help="path of the plugin registry folder")
    ):
    """
    This function will add/override a file to the registry
    """
    # reg = plugins.Registry(rg_file)
    loader = plugins.Loader(file=python_file)
    if loader.get() :
        _names = list(loader.get().keys())
        reg = plugins.Registry(registry_folder)
        reg.set(python_file,_names)
        print (f"""{CHECK_MARK} Import was [bold]successful[/bold] into {reg._folder}""")
    else:
        print (f"""{TIMES_MARK} Import [bold]Failed[/bold] into {registry_folder}, please consider setting environment REGISTRY_FOLDER """)        

def to_Table(df: pd.DataFrame):
    """Displays a Pandas DataFrame as a rich table."""
    table = Table(show_header=True, header_style="bold magenta")
    
    for col in df.columns:
        table.add_column(col)
    
    for _, row in df.iterrows():
        table.add_row(*row.astype(str).tolist())
    
    # console.print(table)
    return table
@appr.command(name="list")
def list_registry(
        folder:str=typer.Option(default=os.environ.get('REGISTRY_FOLDER',None),help="path of the plugin registry folder")):
              #folder: Annotated[str,typer.Argument(help="registry folder where")]=plugins.REGISTRY_PATH) :
    """
    This function will summarize the registry in a table
    """
    try:
        reg = plugins.Registry(folder)

        print (to_Table(reg.stats()))
    except Exception as e :
        print (e)
        print (f"""{TIMES_MARK} Please provide registry folder or set environment REGISTRY_FOLDER """)

def exe(file,name,_args):
    pass

app.add_typer(appr,name='registry',help='This enables registry management')
if __name__ == '__main__' :

    app()

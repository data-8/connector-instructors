"""Functions to assist with grading."""
import nbformat
import os
from copy import deepcopy
from nbformat.notebooknode import NotebookNode


def create_student_notebook(nbpath, match_string='### STUDENT ANSWER',
                            output_suffix='student', remove_cell=False,
                            clear_outputs=True, path_save=None,
                            add_md_cell=False, md_cell_text=None):
    """Clean inputs / outputs of notebooks to send to students.

    This will search for a string within notebook cells, and then allow you
    to do various things with the cell in which the string is found. Currently
    you can clear all remaining text in the cell, remove the cell entirely, or
    add an extra markdown cell afterward. These are all useful for various
    usecases of preparing notebooks for students to use on their own.

    Parameters
    ----------
    nbpath : str
        The path to a jupyter notebook file.
    match_string : str
        A string to search for in input cells. If the string is
        found, then anything in the cell AFTER the string is removed.
    output_suffix : str
        An output to be appended to a saved jupyter notebook.
    remove_cell : bool
        Whether to remove the cell w/ `match_string` in it.
    clear_outputs : bool
        Whether to clear outputs for the cells before saving.
    path_save : string
        An optional path to a folder where the output notebook will
        be saved. If None, no new file will be created.
    add_md_cell : bool
        Whether to add a markdown cell after each matched cell, this is
        useful if you want students to add an answer to the MD cell so that
        text isn't cut off after saving.
    md_cell_text : str | None
        Text to add to the added MD cell.

    Returns
    -------
    nb : instance of NotebookNode
        The NotebookNode corresponding to the cleaned notebook.
    """
    nb = nbformat.read(nbpath, 4)
    new_cells = []
    for ii, cell in enumerate(nb['cells']):
        # Only check code cells
        if cell['cell_type'] != 'code':
            new_cells.append(cell)
            continue

        # Clean outputs
        if clear_outputs is True:
            cell['outputs'] = []

        # Clear prompt numbers
        cell['execution_count'] = None
        cell.pop('prompt_number', None)

        # See if the cell matches the string
        ix = cell['source'].find(match_string)
        if ix != -1:
            # If so, remove text after the string
            newstr = cell['source'][:ix + len(match_string)] + '\n'
            cell['source'] = newstr
            if remove_cell is False:
                # Only append to new cells is we don't want to remove the cell
                new_cells.append(cell)

            # Add the markdown if requested
            if add_md_cell is True:
                if md_cell_text is None:
                    md_cell_text = ('---\n## Student Answer\n\n*Double-click'
                                    ' and add your answer here*\n\n---')
                md_cell = NotebookNode(cell_type='markdown',
                                       metadata={},
                                       source=md_cell_text)
                new_cells.append(md_cell)
        else:
            # If the string doesn't match, just append and move on
            new_cells.append(cell)
            continue

    nb['cells'] = new_cells

    if path_save is not None:
        filename = os.path.basename(nbpath)
        # In case they specified a specific file
        path_save = os.path.dirname(path_save)
        name, ext = filename.split('.')
        outname = '{}_{}.{}'.format(name, output_suffix, ext)
        save_file = '{}{}{}'.format(path_save, os.sep, outname)
        print('Saving to {}'.format(save_file))
        if not os.path.isdir(path_save):
            os.makedirs(path_save)
        nbformat.write(nb, save_file)
    return nb

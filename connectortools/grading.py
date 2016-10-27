"""Functions to assist with grading."""
import nbformat
import os


def strip_answers(nbpath, strip_string='### STUDENT ANSWER',
                  output_suffix='student', keep_strip_string=True,
                  remove_cell=False, clean_outputs=True, save=True,
                  path_save=None):
    """Clean inputs / outputs of notebooks to send to students.

    Parameters
    ----------
    nbpath : str
        The path to a jupyter notebook file.
    strip_string : str
        A string to search for in input cells. If the string is
        found, then anything in the cell AFTER the string is removed.
    output_suffix : str
        An output to be appended to a saved jupyter notebook.
    save : bool
        Whether to save the output notebook.
    clean_outputs : bool
        Whether to clear outputs for the cells before saving.
    path_save : string
        An optional path to a folder where the output notebook will
        be saved. If None, save in the same directory as nbpath.

    Returns
    -------
    nb : instance of NotebookNode
        The NotebookNode corresponding to the cleaned notebook.
    """
    nb = nbformat.read(nbpath, 4)
    for ii, cell in enumerate(nb['cells']):
        # Only check code cells
        if cell['cell_type'] != 'code':
            continue

        # Replace some input cells
        ix = cell['source'].find(strip_string)
        if ix != -1:
            if remove_cell is True:
                # Remove the whole cell and move on
                _ = nb['cells'].pop(ii)
                continue
            newstr = cell['source'][:ix + len(strip_string)] + '\n'
            cell['source'] = newstr

        # Clean outputs
        if clean_outputs is True:
            cell['outputs'] = []

        # Clear prompt numbers
        cell['execution_count'] = None
        cell.pop('prompt_number', None)

    if save is True:
        filename = os.path.basename(nbpath)
        path_save = os.path.dirname(nbpath) if path_save is None else path_save
        name, ext = filename.split('.')
        outname = '{}_{}.{}'.format(name, output_suffix, ext)
        save_file = '{}{}{}'.format(path_save, os.sep, outname)
        print('Saving to {}'.format(save_file))
        if not os.path.isdir(path_save):
            os.makedirs(path_save)
        nbformat.write(nb, save_file)
    return nb
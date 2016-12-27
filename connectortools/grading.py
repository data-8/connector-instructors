"""Functions to assist with grading."""
import nbformat as nbf
import os
from copy import deepcopy
from nbformat.notebooknode import NotebookNode
from nbconvert.preprocessors import ClearOutputPreprocessor


def _check_nb_file(ntbk):
    if isinstance(ntbk, str):
        ntbk = nbf.read(ntbk, nbf.NO_CONVERT)
    elif not isinstance(ntbk, NotebookNode):
        raise TypeError('`ntbk` must be type string or `NotebookNode`')
    return ntbk

class NotebookCleaner(object):
    """Prepare Jupyter notebooks for distribution to students.
    
    Parameters
    ----------
    ntbk : string | instance of NotebookNode
        The input notebook.
    """
    def __init__(self, ntbk):
        self.ntbk = _check_nb_file(ntbk)

    def clear_outputs(self):
        """Clear the outputs of a notebook.
        """
        self.ntbk = ClearOutputPreprocessor().preprocess(self.ntbk, {})[0]
        return self

    def remove_cells(self, match_string='### TEACHER INFO'):
        """Remove cells that contain a specific string.

        Parameters
        ----------
        match_string : str
            A string to search for in input cells. Any cells with the
            `match_string` inside will be removed.
        """
        # See if the cell matches the string
        new_cells = []
        for ii, cell in enumerate(self.ntbk['cells']):
            # If it doesn't match the string, then keep the cell
            if cell['source'].find(match_string) == -1:
                new_cells.append(cell)
        self.ntbk['cells'] = new_cells
        return self

    def create_answer_cells(self, match_string='### STUDENT ANSWER',
                            text_cell=False, md_cell_text=None):
        """Create answer cells for students to fill out.

        This will remove all text after `match_string`. Students should then give
        their answers in this section. Alternatively, a markdown cell will replace
        the student answer cell

        Parameters
        ----------
        match_string : str
            A string to search for in input cells. If the string is
            found, then anything in the cell AFTER the string is removed.
        text_cell : bool
            Whether to treat this cell as a text cell rather than a code cell.
            If True, a new markdown cell will be created. This is
            useful if you want students to add an answer to the MD cell so that
            text isn't cut off after saving.
        md_cell_text : str | None
            Text to add to the added MD cell. If `None`, a template will be used.
        """
        new_cells = []
        for ii, cell in enumerate(self.ntbk['cells']):
            # Only check code cells
            if cell['cell_type'] != 'code':
                new_cells.append(cell)
                continue

            # See if the cell matches the string
            ix = cell['source'].find(match_string)
            if ix != -1:
                if text_cell is True:
                    if md_cell_text is None:
                        md_cell_text = ('---\n## Student Answer\n\n*Double-click'
                                        ' and add your answer here*\n\n---')
                    cell = NotebookNode(cell_type='markdown',
                                        metadata={},
                                        source=md_cell_text)
                else:
                    # If so, remove text after the string
                    newstr = cell['source'][:ix + len(match_string)] + '\n'
                    cell['source'] = newstr
            new_cells.append(cell)

        self.ntbk['cells'] = new_cells
        return self

    def save(self, path_save):
        """Save the notebook to disk.

        Parameters
        ----------
        path_save : string
            The path for saving the file.
        """
        dir_save = os.path.dirname(path_save)
        print('Saving to {}'.format(path_save))
        if not os.path.isdir(dir_save):
            os.makedirs(dir_save)
        nbf.write(self.ntbk, path_save)

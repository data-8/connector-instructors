"""Functions to assist with grading."""
import nbformat as nbf
import os
from copy import deepcopy
from nbformat.notebooknode import NotebookNode
from nbgrader.preprocessors import (ClearOutput,
                                    ClearSolutions,
                                    NbGraderPreprocessor)
from traitlets import Unicode


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
        self.preprocessors = []

    def __repr__(self):
        s = "Number of preprocessors: {}\n---".format(
            len(self.preprocessors))
        for pre in self.preprocessors:
            s += '\n' + str(pre)
        return s

    def clear_outputs(self):
        """Clear the outputs of a notebook.
        """
        pre = ClearOutput()
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
        return self

    def remove_cells(self, match_text='### TEACHER INFO'):
        """Remove cells that contain a specific string.

        Parameters
        ----------
        match_text : str
            A string to search for in input cells. Any cells with the
            `match_text` inside will be removed.
        """
        # See if the cell matches the string
        pre = RemoveCells(match_text=match_text)
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
        return self

    def create_answer_cells(self, text_solution_begin='### SOLUTION BEGIN',
                            text_solution_end='### SOLUTION END',
                            text_code=None, text_md=None):
        """Create answer cells for students to fill out.

        This will remove all text after `match_string`. Students should then give
        their answers in this section. Alternatively, a markdown cell will replace
        the student answer cell

        Parameters
        ----------
        text_solution_begin : str
            A string to search for in input cells. If the string is
            found, then anything between it and `text_solution_end` is removed.
        text_solution_end : str
            The ending delimiter for solution cells.
        text_code : str | None
            Text to add to code solution cells. If None, `nbgrader`
            default is used.
        text_md : str | None
            Text to add to markdown solution cells. If None, a default template
            will be used.
        """
        kwargs = dict(begin_solution_delimeter=dict(python=text_solution_begin),
                      end_solution_delimeter=dict(python=text_solution_end),
                      enforce_metadata=False)
        if text_code is not None:
            kwargs['code_stub'] = dict(python=text_code)
        if text_md is None:
            text_md = ('---\n## <span style="color:red">Student Answer</span>'
                       '\n\n*Double-click and add your answer between the '
                       'lines*\n\n---')
        kwargs['text_stub'] = text_md
        pre = ClearSolutions(**kwargs)
        self.ntbk = pre.preprocess(self.ntbk, {})[0]
        self.preprocessors.append(pre)
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


class RemoveCells(NbGraderPreprocessor):

    match_text = Unicode(
        "### TEACHER INFO",
        config=True,
        help=("A string to search for in cells. Any cells with"
              "`match_text` inside will be removed.")
        )

    def preprocess(self, nb, resources):
        ntbk = deepcopy(nb)
        new_cells = []
        for ii, cell in enumerate(ntbk['cells']):
            # If it doesn't match the string, then keep the cell
            if cell['source'].find(self.match_text) == -1:
                new_cells.append(cell)
        ntbk['cells'] = new_cells
        return ntbk, resources



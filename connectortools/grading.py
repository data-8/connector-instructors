"""Functions to assist with grading."""
import nbformat as nbf
import os
import os.path as op
from copy import deepcopy
from nbformat.notebooknode import NotebookNode
from nbgrader.preprocessors import (ClearOutput, ClearSolutions,
                                    NbGraderPreprocessor, LimitOutput,
                                    Execute)
from glob import glob
from traitlets import Unicode


def _check_nb_file(ntbk):
    if isinstance(ntbk, str):
        ntbk = nbf.read(ntbk, nbf.NO_CONVERT)
    elif not isinstance(ntbk, NotebookNode):
        raise TypeError('`ntbk` must be type string or `NotebookNode`')
    ntbk = deepcopy(ntbk)
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

    def create_answer_cells(self, text_solution_begin=u'### SOLUTION BEGIN',
                            text_solution_end=u'### SOLUTION END',
                            text_code=None, text_md=None):
        """Create answer cells for students to fill out.

        This will remove all text after `match_string`. Students should then
        give their answers in this section. Alternatively, a markdown cell will
        replace the student answer cell

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
        kwargs = dict(begin_solution_delimeter=text_solution_begin,
                      end_solution_delimeter=text_solution_end,
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
    """A helper class to remove cells from a notebook.

    This should not be used directly, instead, use the
    NotebookCleaner class.
    """

    match_text = Unicode(
        "### TEACHER INFO",
        config=True,
        help=("A string to search for in cells. Any cells with"
              "`match_text` inside will be removed.")
        )

    def preprocess(self, nb, resources):
        new_cells = []
        for ii, cell in enumerate(nb['cells']):
            # If it doesn't match the string, then keep the cell
            if cell['source'].find(self.match_text) == -1:
                new_cells.append(cell)
        nb['cells'] = new_cells
        return nb, resources


def run_notebook_directory(path, path_save=None, max_output_lines=1000,
                           overwrite=False):
    """Run all the notebooks in a directory and save them somewhere else.

    Parameters
    ----------
    path : str
        A path to a directory that contains jupyter notebooks. All of these
        notebooks will be run, and the outputs will be placed in `path_save`.
    path_save : str | None
        A path to a directory to save the notebooks. If this doesn't exist,
        it will be created. If `None`, notebooks will not be saved.
    max_output_lines : int | None
        The maximum number of lines allowed in notebook outputs.
    overwrite : bool
        Whether to overwrite the output directory if it exists.

    Returns
    -------
    notebooks : list
        A list of the `NotebookNode` instances, one for each notebook.
    """
    if not op.exists(path):
        raise ValueError("You've specified an input path that doesn't exist")
    path = _enforce_endswith_sep(path)
    notebooks = glob(path + '*.ipynb')
    print('Executing {} notebooks'.format(len(notebooks)))
    outputs = [run_notebook(notebook, max_output_lines=max_output_lines)
               for notebook in notebooks]
    if path_save is not None:
        print('Saving {} notebooks to: {}'.format(len(notebooks), path_save))
        path_save = _enforce_endswith_sep(path_save)
        if not op.exists(path_save):
            os.makedirs(path_save)
        elif overwrite is True:
            print('Overwriting output directory')
            for ifile in glob(path_save + '*-exe.ipynb'):
                os.remove(ifile)
        else:
            raise ValueError('path_save exists and overwrite is not True')

        for filename, notebook in zip(notebooks, outputs):
            this_name = op.basename(filename)
            left, right = this_name.split('.')
            left += '-exe'
            this_name = '.'.join([left, right])
            nbf.write(notebook, path_save + this_name)


def run_notebook(ntbk, max_output_lines=1000):
    """Run the cells in a notebook and limit the output length.

    Parameters
    ----------
    ntbk : string | instance of NotebookNode
        The input notebook.
    max_output_lines : int | None
        The maximum number of lines allowed in notebook outputs.
    """
    ntbk = _check_nb_file(ntbk)

    preprocessors = [Execute()]
    if max_output_lines is not None:
        preprocessors.append(LimitOutput(max_lines=max_output_lines,
                                         max_traceback=max_output_lines))
    for prep in preprocessors:
        ntbk, _ = prep.preprocess(ntbk, {})
    return ntbk


def _enforce_endswith_sep(path):
    """Force a path to end with an os separator."""
    if not path.endswith(os.sep):
        path += os.sep

    return path

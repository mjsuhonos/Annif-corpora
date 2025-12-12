# cannif
> Every magician needs a beautiful assistant!

Cannif is a web GUI for the [Annif toolkit](https://annif.org). It provides:

- a sortable, searchable, export-able list of projects and details
- an editor for projects and backend parameters
- simple charts of evaluation metrics

It is a pretty small script built using [Streamlit](https://streamlit.io).

## why

For Annif installations of a few projects, editing projects by hand and managing them isn't too much work.  However, for cases where there are tens of projects or more, it quickly becomes onerous.  Additionally, gathering the output of dozens of evaluations and keeping them organized can be a pain.  These things aren't the job of Annif, so cannif was created.

Why `cannif`?  In Canada we often prepend 'can' to names, so can-Annif, cannif.  In French, `canif` means `pocket knife` (with an [interesting history](https://fr.wikipedia.org/wiki/Canif)), which is a very useful tool indeed.

## installation

The recommended way is to install cannif into a virtual environment.

    python3 -m venv cannif-venv
    source cannif-venv/bin/activate
    pip install annif
    pip install streamlit

Open a new terminal.  Start up the application:

    streamlit run cannif_streamlit.py

You should see:

    You can now view your Streamlit app in your browser.

    Local URL: http://localhost:8501
    Network URL: http://192.168.1.107:8501

cannif will automatically try to start an Annif REST server running at `http://localhost:5000/v1/`. cannif looks for project information in the default location, `projects.d`.  If cannif is run from the `Annif` folder, it will use the projects defined there.

## usage

When connected, it presents an interactive table of projects and their details.  The table can be downloaded as a CSV file.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/cannif.png?raw=true)

When you select a project in the table, details about that project and its backend appear below the table.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/project.png?raw=true)

When metrics are available, they are displayed in both the project details and in a series of comparative charts.  Cannif looks for evaluation information in the `data/eval` directory.  JSON files in the Annif `--metrics-file` format will be used if they match the name of a project_id.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/metrics.png?raw=true)

### creating projects

Projects can be created through the "New Project" pop-up.  A project requires:
- a name
- a loaded vocabulary
- a language
- an analyzer
- a backend

Vocabularies can be loaded for a project by entering a vocab ID and a language, and uploading a vocabulary file.  Once loaded, the vocabulary can then be used in any new project.

## that's all folks

If you have any other ideas for how to improve cannif, get in touch or submit an issue!

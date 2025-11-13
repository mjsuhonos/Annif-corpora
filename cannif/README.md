# cannif
> Every magician needs a beautiful assistant!

Cannif is a web GUI for the [Annif toolkit](https://annif.org). It provides:

- a sortable, searchable, export-able list of projects and details
- an editor for project backend parameters
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

Make sure Annif is running:

    annif run

    INFO:     Started server process [58021]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)

Open a new terminal.  Start up the application:

    streamlit run cannif_streamlit.py

You should see:

    You can now view your Streamlit app in your browser.

    Local URL: http://localhost:8501
    Network URL: http://192.168.1.107:8501

    For better performance, install the Watchdog module:

    $ pip install watchdog

By default cannif connects to the REST API of an Annif server running at `http://localhost:5000/v1/`.  You can edit `ANNIF_API` to point at any Annif server, eg. `https://api.annif.org/v1`:

When connected, it presents an interactive table of projects and their details.  The table can be downloaded as a CSV file.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/cannif.png?raw=true)

Depending on how and where Annif is installed on your system, the local version may not match the version at the REST API.  This is usually OK, but ideally they should be as similar as possible.

Cannif looks for project information in the default location, `projects.d`.  If cannif is run from the `Annif` folder, it will use the projects defined there.  I like to run it from its own folder, with a symlink to `Annif/projects.d`.

When you select a project in the table, details about that project and its backend appear below the table.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/project.png?raw=true)

Cannif looks for evaluation information in the `data/eval` directory.  JSON files in the Annif `--metrics-file` format will be used if they match the name of a project_id.  When metrics are available, they are displayed in both the project details and in a series of comparative charts.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/metrics.png?raw=true)

## that's all folks

Cannif doesn't do some things yet, but they are being developed:

- load vocabularies
- create new projects
- drag-and-drop file upload for training and evaluation
- split-ensemble creation for reduced memory during training

If you have any other ideas for how to improve cannif, get in touch or submit a pull request!

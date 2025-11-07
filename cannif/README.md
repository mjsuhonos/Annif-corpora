# cannif
> Every magician needs a beautiful assistant!

Cannif is a web GUI for the [Annif toolkit](https://annif.org). It provides:

- a sortable, searchable DataFrame-based list of projects
- an editor for project backend parameters

It is a pretty small script built using [Streamlit](https://streamlit.io).

Because Streamlit apps are just regular Python scripts, cannif can also interact with a local copy of Annif directly, potentially providing full functionality.  However, cannif is a development tool and as such, should be used with caution when executing actions that modify data.

## why

For Annif installations of a few projects, editing projects by hand and managing them isn't too much work.  However, for cases where there are tens of projects or more, it quickly becomes onerous.  Additionally, gathering the output of dozens of evaluations and keeping them organized can be a pain.  These things aren't the job of Annif, so cannif was created.

Why `cannif`?  In Canada we often prepend 'can' to names, so can-Annif, cannif.  From Toronto to Helsinki. 🇨🇦🤝🇫🇮

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

When connected, it presents an interactive table of projects and their details.  One of the features is that the table can be downloaded as a CSV file.

By default cannif connects to the REST API of an Annif server running at `http://localhost:5000/v1/`.  You can edit `ANNIF_API` to point at any Annif server, eg. `https://api.annif.org/v1`:

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/cannif.png?raw=true)

Depending on how and where Annif is installed on your system, the local version may not match the version at the REST API.  This is usually OK, but ideally they should be as similar as possible.

Cannif looks for project information in the default location, `projects.d`.  If cannif is run from the Annif root folder, it will use the projects defined there.  I like to run it from its own folder, with a symlink to `Annif/projects.d`.

Now when you select projects in the table, details about that project appear below.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/project.png?raw=true)

## that's all folks

Cannif doesn't do anything else yet, but there are some things being developed:

- create and load vocabularies
- drag-and-drop training and evaluation
- split-ensemble training for memory reduction

If you have any other ideas for how to improve cannif, get in touch or submit a pull request!

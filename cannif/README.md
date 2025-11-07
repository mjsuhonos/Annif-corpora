# cannif
> Every magician needs a beautiful assistant!

Cannif is a web GUI for the [Annif toolkit](https://annif.org). It provides:

- a sortable, searchable DataFrame-based list of projects
- an editor for project backend parameters

It is a pretty small script built using [Streamlit](https://streamlit.io).

## installation

Cannif connects to the Annif REST API. By default this is an Annif server running at `http://localhost:5000/v1/`.  When connected, it presents an interactive table of projects and their details.  One of the features is that the table can be downloaded as a CSV file.

You can edit the `ANNIF_API` constant to point at any Annif server, eg. `https://api.annif.org/v1`:

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/cannif.png?raw=true)

Because Streamlit apps are just regular Python scripts, cannif can also interact with a local copy of Annif directly, potentially providing full functionality.  However, cannif is a development tool and as such, should be used with caution when executing actions that modify data.  Thankfully, none of those work yet.

The recommended way is to install cannif into a virtual environment.

    python3 -m venv cannif-venv
    source cannif-venv/bin/activate
    pip install annif
    pip install streamlit

Depending on how and where Annif is installed on your system, the local version may not match the version at the REST API.  This is usually OK, but ideally they should be as similar as possible.

Cannif looks for project information in the default location, `projects.d`.  If cannif is run from the Annif root folder, it will use the projects defined there.  I like to run it from its own folder, with a symlink to `Annif/projects.d` to improve isolation.

Start up the application:

    streamlit run cannif_streamlit.py

You should see:

    You can now view your Streamlit app in your browser.

    Local URL: http://localhost:8501
    Network URL: http://192.168.1.107:8501

    For better performance, install the Watchdog module:

    $ pip install watchdog

Now when you select projects in the table, details about that project appear below.

![a screenshot](https://github.com/mjsuhonos/Annif-corpora/blob/master/cannif/project.png?raw=true)

## that's all folks

Cannif doesn't do anything else yet, but there are some things being developed:

- drag-and-drop training and evaluation
- split-ensemble training for memory reduction

If you have any other ideas for how to improve cannif, get in touch or submit a pull request!

🇨🇦🤝🇫🇮

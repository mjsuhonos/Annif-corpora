import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
from annif.config import AnnifConfigDirectory, find_config
from annif.registry import AnnifRegistry
from annif.project import Access

# external dependencies
import iso639

ANNIF_API = "http://localhost:5000/v1"
#ANNIF_API = "http://api.annif.org/v1"

########################################
def get_annif_version():
    # Connect to running instance via API
    try:
        r = requests.get(f"{ANNIF_API}/")
        r.raise_for_status()
        return r.json()["version"]

    except Exception as e:
        st.error(f"Error connecting to Annif: {e}")
        return []

########################################
def get_vocabs():
    
    # TODO: check version for field (v1.4.0+)
    try:
        r = requests.get(f"{ANNIF_API}/vocabs")
        r.raise_for_status()        
        vocabs = r.json()["vocabs"]

    except Exception as e:
        # st.error(f"Error connecting to Annif: {e}")
        # TODO: implement real vocabs
        vocabs = [
              {
                "languages": ["en"],
                "loaded": True,
                "size": 826287,
                "vocab_id": "uP279_P910_P361"
              },
              {
                "languages": ["en"],
                "loaded": True,
                "size": 958101,
                "vocab_id": "u0_broader"
              },
              {
                "languages": ["en"],
                "loaded": True,
                "size": 817567,
                "vocab_id": "u1_broader"
              },
              {
                "languages": ["en"],
                "loaded": True,
                "size": 1887927,
                "vocab_id": "u2_broader"
              },
              {
                "languages": ["en"],
                "loaded": True,
                "size": 825067,
                "vocab_id": "u3_broader"
              },
              {
                "languages": ["en"],
                "loaded": True,
                "size": 825067,
                "vocab_id": "u3_norel"
              }
            ]
    return vocabs

########################################
def get_api_projects():
    try:
        r = requests.get(f"{ANNIF_API}/projects")
        r.raise_for_status()
        
        projects = r.json().get("projects")
        
        # Flatten backend and vocab levels
        for project in projects:
            backend_info = project.get("backend", {})
            if isinstance(backend_info, dict) and "backend_id" in backend_info:
                project["backend"] = backend_info["backend_id"]

            vocab = project.get("vocab", {})

            if isinstance(vocab, dict) and "vocab_id" in vocab:
                project["vocab"] = vocab["vocab_id"]

        return projects

    except Exception as e:
        st.error(f"Error fetching API projects: {e}")
        return []

########################################
def get_local_projects():
    # TODO Add robustness

    # Locate the configuration directory
    # Default is "projects.d"
    try:
        config_path = find_config()
    except Exception as e:
        st.error(f"Error fetching local projects: {e}")

    # Initialize the Annif registry
    registry = AnnifRegistry(
        projects_config_path=config_path,
        datadir="cannif",
        init_projects=False
    )

    # Get all available projects
    return registry.get_projects(min_access=Access.private)

########################################
# Displays an interactive table of project details
def list_projects(projects):
    if not projects:
        return

    with st.container():
        # Show a sortable table of all projects
        df = pd.DataFrame(projects)
        
        df["available"] = df["is_trained"].apply(lambda x: "✓" if x else "")

        column_order = ["name", "vocab", "backend", "language", "modification_time", "available"]
        column_config = {
            "name": "Project",
            "backend": "Backend",
            "vocab": "Vocab",
            "language": "Language",
            "modification_time": st.column_config.DatetimeColumn("Modified"),
            "available": "Available",
        }

        st.dataframe(df, hide_index=True, column_config=column_config, column_order=column_order, key="table", selection_mode="single-row", on_select="rerun")

########################################
def project_details(projects):
    # Get the selected row index (Streamlit stores it in session state)
    try:
        selected_rows = st.session_state.table["selection"]["rows"] if "selection" in st.session_state.table else []
    except:
        return

    if selected_rows:
        row_index = selected_rows[0]

        # FIXME: should we do a key lookup instead of relying on array index?
        api_project = get_api_projects()[row_index]
        
        try:
            project = projects[api_project['project_id']]
            # add vocab data to api_project
            # TODO: this can come from the Annif /projects API in 1.4+
            api_project['vocab_spec'] = project.vocab_spec
            api_project['transform_spec'] = project.transform_spec

        except Exception as e:
            st.error(f"Error fetching local project: {e}")
            return []

        with st.expander(f"**{project.name}**", expanded=True):
            col1, col2 = st.columns([1,2])
            with col1:
                project_form(api_project)
            with col2:
                backend_form(project)

########################################
# Uses an api_project dict
def project_form(project):
    lang = iso639.Language.from_part1(project['language'])

    vocabs = get_vocabs()
    vocab_id = re.match(r"([^(]+)", project['vocab_spec']).group(1)

    if None == project['is_trained']:
        pass

    elif "ensemble" == project['backend'] or "yake" == project['backend']:
        st.subheader("Training Not Required", divider="green")

    elif project['is_trained']:
        st.subheader("Trained", divider="green")

    else:
        st.subheader("Not Trained", divider="red")

    st.write(f"**Language:** {lang.name}")

    vocab_ids = [item["vocab_id"] for item in vocabs if "vocab_id" in item]
    index = vocab_ids.index(vocab_id)

    st.selectbox("**Vocab**", vocab_ids, index)

    analyzers = ["simple", "snowball", "simplemma", "voikko", "spacy", "estnltk"]
    try:
        # Find index in list (handle case if not found)
        analyzer = project.analyzer_spec.split('(')[0]
        index = analyzers.index(analyzer)
    except:
        index = None
    
    st.selectbox("**Analyzer**", analyzers, index)
    
    st.text_input("**Transform:**",
        value=project['transform_spec'],
        key=f"{project['project_id']}_transform"
    )

    if None == project['is_trained']:
        pass

    elif "ensemble" == project['backend'] or "yake" == project['backend']:
        if st.button("Evaluate", key=f"eval_{project['project_id']}"):
            st.info(f"⚙️ Evaluate action triggered for {project['name']}")

    elif project['is_trained']:
        dt = datetime.fromisoformat(project['modification_time'])
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")

        uploaded_file = st.file_uploader("Upload File", key=project['project_id'], type=["tsv", "csv", "json", "jsonl"])
        
        st.write(f"**Modified:** {formatted_time}")
        if st.button("Evaluate", key=f"eval_{project['project_id']}"):
            st.info(f"⚙️ Evaluate action triggered for {project['name']}")

    else:
        uploaded_file = st.file_uploader("Upload File", key=project['project_id'], type=["tsv", "csv", "json", "jsonl"])

        st.badge("Training can be very resource-intensive!", color="orange", icon="⚠️")
        if st.button("Train", key=f"train_{project['project_id']}", type="primary"):
            st.info(f"⚙️ Train action triggered for {project['name']}")


########################################
# Uses a local project object
def backend_form(project):
    backend = project.backend
    
    if backend:
        st.subheader(f"{backend.backend_id} parameters", divider="gray")

        with st.container(border=True):

            # Start response body
            response = {
                "project_id": project.project_id,
                "name": project.name,
                "language": project.language,
                "backend": {"backend_id": backend.backend_id}
            }

            for key, value in backend.DEFAULT_PARAMETERS.items():
                col1, col2 = st.columns([2,1])

                with col1:
                    if isinstance(value, bool):
                        response[key] = st.checkbox(
                            f"{key}",
                            value=backend.params[key],
                            key=f"{project.project_id}_{backend.backend_id}_{key}"
                        )
                    elif isinstance(value, (int, float)):
                        response[key] = st.number_input(
                            f"{key}",
                            value=float(backend.params[key]),
                            key=f"{project.project_id}_{backend.backend_id}_{key}"
                        )
                    else:
                        response[key] = st.text_input(
                            f"{key}",
                            value=str(backend.params[key]),
                            key=f"{project.project_id}_{backend.backend_id}_{key}"
                        )

                with col2:
                    st.caption(f"Default: {value}")

            if "ensemble" in backend.backend_id:
                # Show list of sources for the ensemble
                sources = backend.params['sources']

                # split sources by comma and display a textbox for each (for now)
                source_list = sources.split(",")

                projects = get_api_projects()
                project_ids = [item["project_id"] for item in projects]
                new_sources = st.multiselect("Sources", project_ids, source_list)
            
            if st.button("Save Configuration", key=f"save_{project.project_id}_{backend.backend_id}", type="primary"):
                st.success(f"Configuration for **{project.project_id}** saved successfully!")

                try:
                    response['sources'] = ",".join(new_sources)
                except NameError:
                    pass

                st.json(response)
    else:
        st.error(f"Error fetching backend.")

########################################
# Function to load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

########################################
def main():
    # Load the CSS file
    local_css("style.css")
    
    st.set_page_config(page_title="cannif", layout="wide")
    st.markdown("# <span style='color:red;'>can</span><span style='color:#002D72;'>nif</span>", unsafe_allow_html=True)

    version = get_annif_version()
    if version:
        st.caption(f"Annif {version} at {ANNIF_API}")

    list_projects(get_api_projects())

    project_details(get_local_projects())

    st.write("🇨🇦🤝🇫🇮")

if __name__ == "__main__":
    main()
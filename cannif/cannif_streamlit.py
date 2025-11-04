import streamlit as st
import pandas as pd
import requests
import re
from datetime import datetime
from annif.config import AnnifConfigDirectory, find_config
from annif.registry import AnnifRegistry
from annif.project import Access

ANNIF_API = "http://localhost:5000/v1"

########################################
def get_annif_version():
    # Connect to running instance via API
    try:
        r = requests.get(ANNIF_API)
        r.raise_for_status()
        return r.json()["version"]

    except Exception as e:
        st.error(f"Error connecting to Annif: {e}")
        return []

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
def get_local_projects():
    # TODO Add robustness

    # Locate the configuration directory
    config_path = find_config()
    config_dir = AnnifConfigDirectory(config_path)

    # Initialize the Annif registry
    registry = AnnifRegistry(
        projects_config_path=config_path,
        datadir=".",
        init_projects=False
    )

    # Get all available projects
    return registry.get_projects(min_access=Access.private)

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
        st.error(f"Error fetching projects: {e}")
        return []    

# Displays an interactive table of project details
def list_projects(projects):

    with st.container():
        # Show a sortable table of all projects
        df = pd.DataFrame(projects)

        column_order = ["name", "vocab", "backend", "is_trained", "language", "modification_time"]
        column_config = {
            "name": "Project",
            "backend": "Backend",
            "vocab": "Vocab",
            "is_trained": st.column_config.CheckboxColumn("Trained"),
            "language": "Language",
            "modification_time": st.column_config.DatetimeColumn("Modified")
        }

        st.dataframe(df, hide_index=True, column_config=column_config, column_order=column_order, key="table", selection_mode="single-row", on_select="rerun")

########################################
def project_details(projects):
    # Get the selected row index (Streamlit stores it in session state)
    selected_rows = st.session_state.table["selection"]["rows"] if "selection" in st.session_state.table else []

    if selected_rows:
        row_index = selected_rows[0]

        # FIXME: should we do a key lookup instead of relying on array index?
        api_project = get_api_projects()[row_index]
        
        try:
            project = projects[api_project['project_id']]

        except Exception as e:
            st.error(f"Error fetching project: {e}")
            return []    

        with st.expander(f"**{project.name}**", expanded=True):

            col1, col2, col3 = st.columns([1,1,1])

            col1.write(f"**Analyzer:** {project.analyzer_spec}")
            col2.write(f"**Transform:** {project.transform_spec}")
            col3.write(f"**Vocab:** {project.vocab_spec}")

            vocabs = get_vocabs()
                
            vocab_name = re.match(r"([^(]+)", project.vocab_spec).group(1)
            vocab_size = next((v["size"] for v in vocabs if v["vocab_id"] == vocab_name), None)

            col3.badge(f"**Size:** {vocab_size}")

            col1, col2 = st.columns([2,1])
            with col1:
                backend_form(project)
            with col2:
                project_form(api_project)

########################################
def project_form(project):
    if project['is_trained']:
        st.subheader("Trained", divider="green")
        
        dt = datetime.fromisoformat(project['modification_time'])
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        st.write(f"**Modified:** {formatted_time}")
        if st.button("Evaluate", key=f"eval_{project['project_id']}"):
            st.info(f"⚡ Evaluate action triggered for {project['name']}")

    else:
        st.subheader("Not Trained", divider="red")
        st.badge("Training can be very resource-intensive!", color="orange", icon="⚠️")
        if st.button("Train", key=f"train_{project['project_id']}", type="primary"):
            st.info(f"⚡ Train action triggered for {project['name']}")

    uploaded_file = st.file_uploader("Upload a file to train or evaluate", key=project['project_id'], type=["tsv", "csv", "rdf", "xml", "ttl", "nt", "jsonl", "txt", "gz"])

########################################
def backend_form(project):
    backend = project.backend

    if backend:
        st.subheader(f"{backend.backend_id} parameters", divider="gray")

        updated_params = {}

        with st.container(border=True):
            for key, value in backend.DEFAULT_PARAMETERS.items():
                col1, col2 = st.columns([2,1])

                with col1:
                    if isinstance(value, bool):
                        updated_params[key] = st.checkbox(
                            f"{key}",
                            value=backend.params[key],
                            key=f"{project.project_id}_{backend.backend_id}_{key}"
                        )
                    elif isinstance(value, (int, float)):
                        updated_params[key] = st.number_input(
                            f"{key}",
                            value=float(backend.params[key]),
                            key=f"{project.project_id}_{backend.backend_id}_{key}"
                        )
                    else:
                        updated_params[key] = st.text_input(
                            f"{key}",
                            value=str(backend.params[key]),
                            key=f"{project.project_id}_{backend.backend_id}_{key}"
                        )

                with col2:
                    st.caption(f"Default: {value}")

        if st.button("Save Configuration", key=f"save_{project.project_id}_{backend.backend_id}", type="primary"):
            st.success(f"Configuration for **{project.project_id}** saved successfully!")
            st.json({
                "backend_id": backend.backend_id,
                "language": project.language,
                "params": updated_params,
            })

########################################
def main():
    st.set_page_config(page_title="cannif", layout="wide")
    st.markdown(
        "# <span style='color:red;'>can</span><span style='color:#002D72;'>nif</span>",
        unsafe_allow_html=True
    )

    version = get_annif_version()
    if version:
        st.caption(f"Annif {version} at {ANNIF_API}")

    list_projects(get_api_projects())
    project_details(get_local_projects())


if __name__ == "__main__":
    main()
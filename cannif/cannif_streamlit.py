import streamlit as st
import pandas as pd
import requests
from datetime import datetime

import streamlit as st
from annif.config import AnnifConfigDirectory, find_config
from annif.registry import AnnifRegistry
from annif.project import Access

ANNIF_API = "http://localhost:5000/v1"

def get_annif_version():
    # Connect to running instance via API
    try:
        r = requests.get(ANNIF_API)
        r.raise_for_status()
        return r.json()["version"]

    except Exception as e:
        st.error(f"Error connecting to Annif: {e}")
        return []

def get_projects():
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


# Displays an interactive table of project details
def list_projects(projects):

    ####################################################
    try:
        r = requests.get(f"{ANNIF_API}/projects")
        r.raise_for_status()
        raw_projects = r.json()

        # Flatten backend level
        for project in raw_projects.get("projects", []):
            backend_info = project.get("backend", {})
            if isinstance(backend_info, dict) and "backend_id" in backend_info:
                project["backend"] = backend_info["backend_id"]

    except Exception as e:
        st.error(f"Error fetching projects: {e}")
        return []

    ####################################################
    # Show a sortable table of all projects

    column_order = ["name", "backend", "is_trained", "language", "modification_time"]
    column_config = {
        "name": "Project",
        "backend": "Backend",
        "is_trained": st.column_config.CheckboxColumn("Trained"),
        "language": "Language",
        "modification_time": st.column_config.DatetimeColumn("Modified")
    }
    
    with st.container(border=True):
        
        df = pd.DataFrame(raw_projects["projects"])
        st.dataframe(df, column_config=column_config, column_order=column_order, key="table", selection_mode="single-row", on_select="rerun")

    with st.container(border=True):
        details = st.empty()

        # Get the selected row index (Streamlit stores it in session state)
        selected_rows = st.session_state.table["selection"]["rows"] if "selection" in st.session_state.table else []

        if selected_rows:
            row_index = selected_rows[0]
            project_id = df.iloc[row_index]['project_id'] 
            project = projects[project_id]

            with details.container():
                with st.expander(f"**{project.name}**", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        project_form(project)
                    with col2:
                        backend_form(project)
        else:
            details.info("Select a row to see details.")
        

def project_form(project):
    p = project.dump()

    if p['is_trained']:
        st.subheader("Trained")
        st.write(f"**Modified:** {p['modification_time']}")
        if st.button("Evaluate", key=f"eval_{p['project_id']}"):
            st.info(f"⚡ Evaluate action triggered for {p['name']}")

    else:
        st.subheader("NOT trained")
        st.info(":material/model_training:")
        st.badge("Training can be very resource-intensive!", color="orange", icon="⚠️")
        if st.button("Train", key=f"train_{p['project_id']}", type="primary"):
            st.info(f"⚡ Train action triggered for {p['name']}")

    uploaded_file = st.file_uploader("Upload a file to train/eval", key=p['project_id'], type=["tsv", "csv", "rdf", "xml", "ttl", "nt", "jsonl", "txt", "gz"])

    st.write("Analyzer: ", project.analyzer_spec)
    st.write("Transform: ", project.transform_spec)
    st.write(p)

def backend_form(project):
    p = project.dump()
    
    project_id = p['project_id']
    backend_id = p['backend']['backend_id']

    # Example backend data (could be read from annif project config)
    backend_configs = {
        "stwfsa": {
            "language": "en",
            "params": {
                "concept_type_uri": "",                   # URI of concept type to use
                "expand_abbreviation_with_punctuation": True,
                "expand_ampersand_with_spaces": True,
                "extract_any_case_from_braces": False,
                "extract_upper_case_from_braces": True,
                "handle_title_case": True,
                "remove_deprecated": True,
                "simple_english_plural_rules": True,
                "sub_thesaurus_type_uri": "",
                "thesaurus_relation_is_specialisation": True,
                "thesaurus_relation_type_uri": "",
                "use_txt_vec": False,
                "limit": 100                               # maximum number of suggested concepts
            },
        },
        "nn_ensemble": {
            "language": "en",
            "params": {
                
            }
        },
        "fasttext": {
            "language": "en",
            "params": {
                "dim": 100,
                "lr": 0.25,
                "epoch": 5,
                "minCount": 1,
                "loss": "hs",
                "bucket": 2000000,
                "lrUpdateRate": 100,
                "maxn": 0,
                "minn": 0,
                "neg": 5,
                "t": 0,
                "thread": 4,
                "wordNgrams": 1,
                "ws": 5,
                "pretrainedVectors": "", 
            },
        },
        "tfidf": {
            "language": "en",
            "params": {
                "analyzer": "word",
                "max_df": 0.95,
                "min_df": 2,
                "token_pattern": r"(?u)\b\w\w+\b",
                "ngram": 1,
                "max_features": None,
            },
        },
        "svc": {
            "language": "en",
            "params": {
                "kernel": "linear",
                "C": 1.0,
                "gamma": "scale",
                "class_weight": "balanced",
                "min_df": 1,
                "ngram": 1,
            },
        },
        "omikuji": {
            "language": "en",
            "params": {
                "cluster_balanced": True,
                "cluster_k": 2,
                "collapse_every_n_layers": 0,
                "max_depth": 20,
                "min_df": 1,
                "ngram": 1,
                "label_limit": 100,
            },
        },
        "mllm": {
            "language": "en",
            "params": {
                "model": "sentence‑transformers/all‑MiniLM‑L6‑v2",
                "dim": 384,
                "batch_size": 32,
                "max_leaf_nodes": 1000,
                "max_samples": 0.9,
                "min_samples_leaf": 20,
                "use_hidden_labels": False,
            },
        },
        "vw_multi": {
            "language": "en",
            "params": {
                "passes": 10,
                "loss_function": "logistic",
                "learning_rate": 0.5,
                "bit_precision": 32,
                "ngram": 1,
                "label_limit": 100,
            },
        },
        "yake": {
            "language": "en",
            "params": {
                "deduplication_algo": "levs",
                "deduplication_threshold": 0.9,
                "features": None,
                "label_types": ["prefLabel", "altLabel"],
                "max_ngram_size": 4,
                "num_keywords": 100,
                "remove_parentheses": False,
                "window_size": 1,
            },
        },
        "ensemble": {
            "language": "en",
            "params": {
                "backend_ids": ["fasttext", "tfidf"],
                "weights": [0.5, 0.5],
                "min_docs": 10,
            },
        },
        "dummy": {
            "language": "en",
            "params": {
                "subject_id": 0,
            },
        }
    }

    backend = backend_configs[backend_id]

    updated_params = {}

    st.subheader(f"{backend_id} parameters")

    for key, value in backend["params"].items():
        if isinstance(value, (int, float)):
            updated_params[key] = st.number_input(f"{key}", value=value, key=f"{project_id}_{backend_id}_{key}")
        elif isinstance(value, str):
            updated_params[key] = st.text_input(f"{key}", value=value, key=f"{project_id}_{backend_id}_{key}")
        else:
            updated_params[key] = st.text_input(f"{key}", value=str(value), key=f"{project_id}_{backend_id}_{key}")

    if st.button("Save Configuration", key=f"save_{project_id}_{backend_id}", type="primary"):
        st.success(f"Configuration for **{project_id}** saved successfully!")
        st.json({
            "backend_id": backend_id,
            "language": backend["language"],
            "params": updated_params,
        })

    if project.backend:
        st.write(project.backend.DEFAULT_PARAMETERS)
        st.write(project.backend.params)


####################################################

def main():
    st.set_page_config(page_title="cannif", layout="wide")
    st.markdown(
        "# <span style='color:red;'>can</span><span style='color:#002D72;'>nif</span>",
        unsafe_allow_html=True
    )

    version = get_annif_version()
    if version:
        st.caption(f"Annif {version} at {ANNIF_API}")

    projects = get_projects()

    list_projects(projects)

if __name__ == "__main__":
    main()
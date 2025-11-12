import streamlit as st
import pandas as pd
import requests
import re
import os
import json
from datetime import datetime
from annif.config import AnnifConfigDirectory, find_config
from annif.registry import AnnifRegistry
from annif.project import Access

# TODO: external dependencies
try:
    from readable_number import ReadableNumber
    import iso639
except:
    pass

ANNIF_API = "http://localhost:5000/v1"

def api_request(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    except Exception as e:
        st.error(f"Error connecting to Annif: {e}")
        return []

def get_annif_version():
    response = api_request(f"{ANNIF_API}/")
    return response["version"]

def get_vocabs():
    # TODO: check version for field (v1.4.0+)
    response = api_request(f"{ANNIF_API}/vocabs")
    return response["vocabs"] if response else []

def get_api_projects():
    response = api_request(f"{ANNIF_API}/projects")
    projects = response["projects"]
    
    # Flatten backend and vocab levels
    for project in projects:
        backend_info = project.get("backend", {})
        if isinstance(backend_info, dict) and "backend_id" in backend_info:
            project["backend"] = backend_info["backend_id"]

        vocab = project.get("vocab", {})
        if isinstance(vocab, dict) and "vocab_id" in vocab:
            project["vocab"] = vocab["vocab_id"]

    return projects

def get_local_projects():
    # Locate the configuration directory
    # Default is "projects.d"
    try:
        registry = AnnifRegistry(
            projects_config_path=find_config(),
            datadir="data",
            init_projects=False
        )
    except Exception as e:
        st.error(f"Error fetching local projects: {e}")

    # Get all available projects
    return registry.get_projects(min_access=Access.private)

def get_evaluation(project):
    registry = AnnifRegistry(
        projects_config_path=find_config(),
        datadir="data",
        init_projects=False
    )
    
    evaldir = 'data/eval'
    project_id = project.get('project_id')

    filepath = os.path.join(os.getcwd(), evaldir, f"{project_id}.json")

    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                metrics = json.load(f)

                # Calculate some useful rates 
                tp = metrics["True_positives"]
                fp = metrics["False_positives"]
                fn = metrics["False_negatives"]
            
                false_positive_rate = fp / (fp + tp) if (fp + tp) > 0 else 0
                false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0
                
                metrics["false_positive_rate"] = false_positive_rate
                metrics["false_negative_rate"] = false_negative_rate

                return metrics

        except Exception as e:
            st.error(f"Error loading {filepath}: {e}")
    else:
        return {}

# get local evaluation reults if they exist
def get_evaulations(projects):
    evaldir = 'eval'
    results = []

    for project in projects:
        evals = get_evaluation(project)
        
        if evals:
            results.append({**project, **evals})
        else:
            results.append(project)

    return results

# Displays an interactive table of project details
def list_projects(projects):
    if not projects:
        return

    # Show a sortable table of all projects
    with st.container():
        projects = get_evaulations(projects)

        df = pd.DataFrame(projects)
        
        df["available"] = df["is_trained"].apply(lambda x: "✓" if x else "")

        column_order = ["name", "vocab", "backend", "language", "modification_time", "available", "F1@5", "NDCG", "Recall_microavg", "false_positive_rate", "false_negative_rate", "Precision@1", "Precision@3", "Precision@5"]
        column_config = {
            "name": "Project",
            "vocab": "Vocab",
            "backend": "Backend",
            "language": "Language",
            "modification_time": st.column_config.DatetimeColumn("Modified"),
            "available": "Available",
            "Recall_microavg": "Recall",
            "false_positive_rate": "FPR",
            "false_negative_rate": "FNR"
        }

        st.dataframe(df, hide_index=True, column_config=column_config, column_order=column_order, key="table", selection_mode="single-row", on_select="rerun")

        # if there are metrics, show graphs
        # FIXME: better test
        try:
            metric_count = df.dropna(subset=["F1@5"]).shape[0]
            if metric_count:
                with st.expander("**Comparative Metrics**", expanded=True):

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.bar_chart(df.set_index("name").dropna(subset=["F1@5"]), sort="-F1@5", stack=False, y=["Precision@1","Precision@3","Precision@5"], x_label='')

                    with col2:
                        st.bar_chart(df.set_index("name").dropna(subset=["F1@5"]), sort="-F1@5", stack=False, y=["Recall_microavg", "false_positive_rate", "false_negative_rate"], x_label='')

                    with col3:
                        st.bar_chart(df.set_index("name").dropna(subset=["F1@5"]), sort="-F1@5", stack=False, y=["NDCG", "NDCG@5", "NDCG@10"], x_label='')
        except:
            pass


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

# Uses an api_project dict
def project_form(project):
    if None == project['is_trained']:
        pass

    elif "ensemble" == project['backend'] or "yake" == project['backend']:
        st.subheader("Training Not Required", divider="green")

    elif project['is_trained']:
        st.subheader("Trained", divider="green")

    else:
        st.subheader("Not Trained", divider="red")

    vocabs = get_vocabs()
    if vocabs:
        vocabs
    
        vocab_id = re.match(r"([^(]+)", project['vocab_spec']).group(1)
        vocab_ids = [item["vocab_id"] for item in vocabs if "vocab_id" in item]
        index = vocab_ids.index(vocab_id)

        st.selectbox("**Vocab**", vocab_ids, index)
        try:
            size = ReadableNumber(vocabs[index]['size'], use_shortform=True)
        except:
            size = metrics[vocabs[index]['size']]

        st.write(f"**Terms:** {size}")

    try:
        lang = iso639.Language.from_part1(project['language']).name
    except:
        lang = project['language']
    st.write(f"**Language:** {lang}")

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

    if project['modification_time']:
        dt = datetime.fromisoformat(project['modification_time'])
        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        st.write(f"**Modified:** {formatted_time}")

    metrics = get_evaluation(project)

    if None == project['is_trained']:
        pass
    
    elif metrics:
        pass

    elif "ensemble" == project['backend'] or "yake" == project['backend']:
        uploaded_file = st.file_uploader("**Upload File**", key=project['project_id'], type=["tsv", "csv", "json", "jsonl"])

        if st.button("Evaluate", key=f"eval_{project['project_id']}"):
            st.info(f"⚙️ Evaluate action triggered for {project['name']}")

    elif project['is_trained']:
        uploaded_file = st.file_uploader("**Upload File**", key=project['project_id'], type=["tsv", "csv", "json", "jsonl"])
        
        if st.button("Evaluate", key=f"eval_{project['project_id']}"):
            st.info(f"⚙️ Evaluate action triggered for {project['name']}")

    else:
        uploaded_file = st.file_uploader("**Upload File**", key=project['project_id'], type=["tsv", "csv", "json", "jsonl"])

        st.badge("Training can be very resource-intensive!", color="orange", icon="⚠️")
        if st.button("Train", key=f"train_{project['project_id']}", type="primary"):
            st.info(f"⚙️ Train action triggered for {project['name']}")

    if metrics:
        st.subheader("Evaluation", divider="grey")
        
        try:
            numdocs = ReadableNumber(metrics['Documents_evaluated'], use_shortform=True)
        except:
            numdocs = metrics['Documents_evaluated']
        st.write(f"**Documents Evaluated:** {numdocs}")

        data = {
            "Cutoff": ["@1", "@3", "@5"],
            "Precision": [
                metrics["Precision@1"],
                metrics["Precision@3"],
                metrics["Precision@5"]
            ]
        }

        df = pd.DataFrame(data).set_index("Cutoff")
        st.write('**Precision**')
        st.bar_chart(df, horizontal=True, sort=False)

        data = {
            "Metric": ["Recall", "FPR", "FNR"],
            "Percent": [
                metrics["Recall_microavg"] * 100,
                metrics["false_positive_rate"] * 100,
                metrics["false_negative_rate"] * 100
            ]
        }

        df = pd.DataFrame(data).set_index("Metric")
        st.write('**Recall**')
        st.bar_chart(df, horizontal=True, sort=False)

        data = {
            "Cutoff": ["@1", "@5", "@10"],
            "NDCG": [
                metrics["NDCG"],
                metrics["NDCG@5"],
                metrics["NDCG@10"]
            ]
        }

        df = pd.DataFrame(data).set_index("Cutoff")
        st.write('**NDCG**')
        st.bar_chart(df, horizontal=True, sort=False)
        # Display evaluation metrics

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

# Function to load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    # Load the CSS file
    local_css("style.css")
    
    st.set_page_config(page_title="cannif", layout="wide", page_icon=":material/surgical:")
    st.markdown("# <span style='color:red;'>can</span><span style='color:#002D72;'>nif</span>", unsafe_allow_html=True)

    version = get_annif_version()
    if version:
        st.caption(f"Annif {version} at {ANNIF_API}")

    api_projects = get_api_projects()
    list_projects(api_projects)
    st.caption(f"{len(api_projects)} projects")

    project_details(get_local_projects())
    

    st.write("🇨🇦🤝🇫🇮")

if __name__ == "__main__":
    main()
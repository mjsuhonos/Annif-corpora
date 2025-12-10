import streamlit as st
import pandas as pd
import requests
import re
import os
import json
import subprocess

from annif.config import find_config
from annif.registry import AnnifRegistry

ANNIF_API = "http://localhost:5000/v1"
DATA_DIR = "data"
EVAL_DIR = os.path.join(DATA_DIR, "eval")
UPLOADS_DIR = "uploads"

def api_request(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    except Exception as e:
        st.error(f"Error connecting to Annif: {e}")
        return {}

def get_annif_version():
    response = api_request(f"{ANNIF_API}/")
    return response.get("version")

def get_vocabs():
    response = api_request(f"{ANNIF_API}/vocabs") # Annif 1.4+ required for vocabs
    return response.get("vocabs")

def get_projects():
    response = api_request(f"{ANNIF_API}/projects")
    api_projects = response.get("projects") # array

    projects = {p.get("project_id"): p for p in api_projects}

    # use Annif module to get values not available from API
    try:
        registry = AnnifRegistry(
            projects_config_path=find_config(),
            datadir=DATA_DIR,
            init_projects=False
        )
        local_projects = registry.get_projects()
    except Exception as e:
        st.error(f"Error fetching local projects: {e}")

    for project_id, values in projects.items():
        backend = values.get("backend") or {}
        vocab = values.get("vocab") or {}

        # Flatten backend and vocab levels
        projects[project_id].update({
            "backend": backend.get("backend_id"),
            "vocab": vocab.get("vocab_id"),
            "vocab_size": vocab.get("size"),
        })

        if lp := local_projects.get(project_id):
            if lp.backend:
                projects[project_id].update({
                    "analyzer_spec": lp.analyzer_spec,
                    "vocab_spec": lp.vocab_spec,
                    "transform_spec": lp.transform_spec,
                    "default_params": lp.backend.default_params(),
                    "backend_params": lp.backend.params,
                })
            else:
                projects[project_id].update({
                    "is_trained": None,
                })

        # add evaluation metrics if they exist
        filepath = os.path.join(os.getcwd(), EVAL_DIR, project_id + ".json")

        try:
            metrics = json.load(open(filepath, 'r'))

            # Calculate some useful rates 
            tp = metrics["True_positives"]
            fp = metrics["False_positives"]
            fn = metrics["False_negatives"]
    
            false_positive_rate = fp / (fp + tp) if (fp + tp) > 0 else 0
            false_negative_rate = fn / (fn + tp) if (fn + tp) > 0 else 0
        
            metrics["false_positive_rate"] = false_positive_rate
            metrics["false_negative_rate"] = false_negative_rate
            
        except (FileNotFoundError, json.JSONDecodeError):
            metrics = {}

        projects[project_id] = {**values, **metrics}

    return projects

def list_projects(projects):
    project_list = list(projects.values())

    with st.container():
        column_config = {
            "name": "Project",
            "vocab": "Vocab",
            "backend": "Backend",
            "language": "Language",
            "modification_time": st.column_config.DatetimeColumn("Modified"),
            "is_trained": "Available",
            "Recall_microavg": "Recall",
            "false_positive_rate": "FPR",
            "false_negative_rate": "FNR"
        }
        column_order = ["name", "vocab", "backend", "language",
                        "modification_time", "is_trained", "F1@5",
                        "Precision@1", "Precision@3", "Precision@5",
                        "Recall_microavg", "false_positive_rate", "false_negative_rate", 
                        "NDCG", "NDCG@5", "NDCG@10"]

        # strip columns not required for dataframe display
        filtered_projects = [
            {k: d.get(k) for k in column_order}
            for d in project_list
        ]

        df = pd.DataFrame(filtered_projects)

        df["is_trained"] = df["is_trained"].apply(lambda x: "✓" if x else "-")

        st.dataframe(df, hide_index=True, column_config=column_config,
                    column_order=column_order, key="table",
                    selection_mode="single-row", on_select="rerun")

        # if there are metrics, show graphs
        if df["F1@5"].notna().any():
            df = df.set_index("name").dropna(subset=["F1@5"])
            
            with st.expander("**Comparative Metrics**", expanded=False, icon=":material/bar_chart:"):

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.bar_chart(df, sort="-F1@5", stack=False, x_label='',
                                y=["Precision@1","Precision@3","Precision@5"])
                with col2:
                    st.bar_chart(df, sort="-F1@5", stack=False, x_label='',
                                y=["Recall_microavg", "false_positive_rate", "false_negative_rate"])
                with col3:
                    st.bar_chart(df, sort="-F1@5", stack=False, x_label='',
                                y=["NDCG", "NDCG@5", "NDCG@10"])

def project_details(projects):
    # Get the selected row index (Streamlit stores it in session state)
    table_state = st.session_state.get("table", {})
    selected_rows = table_state.get("selection", {}).get("rows", [])

    if selected_rows:
        row_index = selected_rows[0]
        project_list = list(projects.values())

        # FIXME: don't like relying on row index
        project = project_list[row_index]

        with st.expander(f"**{project.get('name')}**", expanded=True, icon=":material/assignment:"):
            col1, col2 = st.columns(2)
            with col1:
                project_form(project)
                eval_results(project)

            with col2:
                backend_form(project, projects.keys())

def vocab_form(project):
    vocabs = get_vocabs()

    x = st.session_state.get('new_vocab')
    x

    if not vocabs:
        return
        
    with st.container(border=True):
        vocab_ids = [item["vocab_id"] for item in vocabs if "vocab_id" in item]

        lang_code = project.get("language")
        try:
            import iso639
            lang = iso639.Language.from_part1(lang_code).name
        except Exception:
            lang = lang_code

        vocab_spec = project.get("vocab_spec")     # Present for loaded projects
        if vocab_spec:
            vocab_id = re.match(r"([^(]+)", vocab_spec).group(1)
            index = vocab_ids.index(vocab_id)
            vocab = vocabs[index]
            is_loaded = vocab.get("loaded", False)
            disabled = True
        else:
            vocab_id, vocab, is_loaded, index = "", {}, False, None
            disabled = False

        selected_id = st.selectbox("**Vocab ID**", vocab_ids, index=index, disabled=disabled, accept_new_options=True)
    
        if selected_id:
            vocab_id = selected_id
            if vocab_id in vocab_ids:
                index = vocab_ids.index(vocab_id)
                vocab = vocabs[index]
                is_loaded = True
                lang = vocab.get("languages", [lang])[0]

        if not is_loaded:
            st.badge("Use only letters, numbers, and underscores", icon=":material/check:")

        codes = vocab.get('languages') or ["en", "fi", "fr", "sv"]
        try:
            index = codes.index(lang)
        except:
            index = None

        lang_id = st.selectbox("**Language**", codes, index=index, disabled=disabled, accept_new_options=True)

        if is_loaded:
            try:
                from readable_number import ReadableNumber
                size = ReadableNumber(vocab.get('size'), use_shortform=True)
            except:
                size = vocab.get('size')
            st.write(f"**Terms:** {size}")
            
            project['vocab'] = vocab_id
            project['language'] = lang_id

        else:
            st.badge("Use only 2-letter ISO 639-1 language codes", icon=":material/check:")

            if not vocab_id:
                st.error('Please select a vocab')
            elif not lang_id:
                st.error('Please select a language')
            else:
                if upload_action(f"{vocab_id}_{lang_id}", "Load Vocab"):
                    is_loaded = True
                    st.session_state.new_vocab = [vocab_id, lang_id]
                #else:
                #    st.error('Please load the vocab first')

        #project['vocab_spec'] = f"{vocab_id}({lang_id})"

def project_form(project):
    ############################
    with st.expander('project'):
        st.json(project)
    ############################
    
    backend = project.get('backend')
    backends = ["dummy", "ensemble", "fasttext", "http", "mllm", "nn_ensemble",
                "omikuji", "pav", "stwfsa", "svc", "tfidf", "yake"]
    backend_index = backends.index(backend) if backend else 0

    is_trained = True if project.get('is_trained') else False
    trainable = False if "dummy" == backend or "ensemble" == backend or "yake" == backend else True
    evaluable = True if is_trained or not trainable else False

    if None == is_trained: # can't load backend
        st.subheader("Not Available", divider="red")
        return
    elif project.get('is_new'):
        project['name'] = st.text_input("**Name**", key='project_name')
    elif not trainable:
        st.subheader("Training Not Required", divider="green")
    elif is_trained:
        st.subheader("Trained", divider="green")
    else:
        st.subheader("Not Trained", divider="red")
    
    vocab_form(project)

    project['analyzer_spec'] = st.text_input("**Analyzer**",
        value=project.get('analyzer_spec'), disabled=is_trained,
        key=f"{project.get('analyzer_spec')}_analyzer")

    project['transform_spec'] = st.text_input("**Transform**",
        value=project.get('transform_spec'), disabled=is_trained,
        key=f"{project.get('transform_spec')}_transform"
    )

    if modtime := project.get('modification_time'):
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(modtime)
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            formatted_time = modtime
        st.write(f"**Modified:** {formatted_time}")

    if project.get('is_new'):
        project['backend'] = st.selectbox("**Backend**", backends, index=backend_index)

        if st.button('Create Project', key='save-project', type="primary"):
            # Check form values
            if not project.get('name'):
                st.error('Please provide a project name')
                return

            if new_vocab := st.session_state.get('new_vocab'):
                project['language'] = new_vocab[1]
                project['vocab'] = new_vocab[0]

            if not project.get('vocab'):
                st.error('Please select a loaded vocab')
                return
            elif not project.get('language'):
                st.error('Please select a language')
                return

            # TODO: use something more robust to mint IDs
            project['project_id'] = f"{project.get('vocab')}_{project.get('language')}_{project.get('backend')}".lower().replace(" ", "_")

            save_project(project)

            test_path = os.path.join(os.getcwd(), find_config(), f"{project.get('vocab')}_{project.get('language')}_load_vocab.cfg")

            if os.path.exists(test_path):
                os.remove(test_path)

            st.success("Project created successfully!")
            
            #st.rerun()
    elif evaluable:
        upload_action(project.get('project_id'), "Evaluate")
    elif trainable:
        upload_action(project.get('project_id'), "Train")
        st.warning("Training is very resource-intensive!", icon=":material/warning:")
        
    #if project.get("F1@5"): # already evaluated
    #elif "dummy" == backend:

def eval_results(project):
    if project.get("F1@5"):
        st.subheader("Evaluation", divider="grey")
        
        try:
            from readable_number import ReadableNumber
            numdocs = ReadableNumber(project.get('Documents_evaluated'), use_shortform=True)
        except:
            numdocs = project.get('Documents_evaluated')

        st.write(f"**Documents Evaluated:** {numdocs}")

        data = {"Cutoff": ["@1", "@3", "@5"],
                "Precision": [project["Precision@1"], project["Precision@3"], project["Precision@5"]]}
        show_bar_chart(data)

        data = {"Metric": ["Recall", "FPR", "FNR"],
                "Percent": [project["Recall_microavg"] * 100,
                            project["false_positive_rate"] * 100,
                            project["false_negative_rate"] * 100]}
        show_bar_chart(data)

        data = {"Cutoff": ["@1", "@5", "@10"],
                "NDCG": [project["NDCG"], project["NDCG@5"], project["NDCG@10"]]}
        show_bar_chart(data)

def show_bar_chart(data):
    it = iter(data)
    first_key = next(it)
    second_key = next(it)

    df = pd.DataFrame(data).set_index(first_key)
    st.write(f'**{second_key}**')
    st.bar_chart(df, horizontal=True, sort=False)

def upload_action(project_id, action):
    # TODO: use something more robust to mint IDs
    task_id = f"{project_id}_{action}".lower().replace(" ", "_")

    if task_id not in st.session_state:
        st.session_state[task_id] = None

    def is_task_running(task_id):
        proc = st.session_state.get(task_id)
        if proc is None:
            return False
        return proc.poll() is None
    
    # Show status
    if is_task_running(task_id):
        st.info(f"{action} is running", icon=":material/hourglass:")
        return
    #elif st.session_state["task_proc"] is not None:
    #    st.success(f"{action} for **{project_id}** successful!")
    
    # FIXME: this isn't right but throws an error:
    # streamlit.errors.StreamlitValueAssignmentNotAllowedError: Values for the widget with key 'wd1k_en_load_vocab' cannot be set using st.session_state.
    
    uploaded_file = st.file_uploader("**Upload File**", key=project_id,
                                    type=["tsv", "csv", "json", "jsonl"])

    # Save file to uploads folder
    if uploaded_file:
        base, ext = os.path.splitext(uploaded_file.name)
        file_path = os.path.join(UPLOADS_DIR, f"{task_id}{ext}")
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    placeholder = st.empty()

    if placeholder.button(action, key=f"{task_id}_button", type="primary"):
        if not uploaded_file:
            st.error("No file uploaded")
            return

        if not is_task_running(task_id):
            source_path = os.path.join(os.getcwd(), UPLOADS_DIR, f"{task_id}{ext}")

            if "Evaluate" == action:
                dest_path = os.path.join(os.getcwd(), EVAL_DIR, project_id + ".json")

                st.session_state[task_id] = subprocess.Popen(
                    ["annif", "eval", project_id, source_path, "-M", dest_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                st.info(f"Evaluation is running", icon=":material/hourglass:")

            elif "Load Vocab" == action:
                vocab_id, lang = project_id.split('_', 1)

                if '' == vocab_id:
                    st.error('Please provide a vocab ID')
                    return

                if 'None' == lang:
                    st.error('Please provide a language code')
                    return

                # Write a temporary project TOML file
                proj_path = os.path.join(os.getcwd(), find_config(), task_id + ".cfg")
                with open(proj_path, "w") as file:
                    file.write(f"[{task_id}]\n")
                    file.write(f"backend = dummy\n")
                    file.write(f"language = {lang}\n")
                    file.write(f"vocab = {vocab_id}({lang})\n")

                with st.spinner("Loading vocab..."):
                    try:
                        result = subprocess.run(
                            ["annif", "load-vocab", "-L", lang, vocab_id, source_path],
                            capture_output=True, text=True, check=True)

                        st.success("Vocab loaded successfully!")
                        placeholder.write(' ') # Clear the button

                        # TODO: trigger reloading of the vocab part of the modal?

                    except subprocess.CalledProcessError as e:
                        st.error("Error loading vocab:")
                        st.code(e.stderr)
            else:
                st.warning(f"{action} is not implemented yet", icon=":material/warning:")

        return uploaded_file

    # TODO: remove the button if a vocab is loaded in session
    #if st.session_state.get('new_vocab'):
    #    placeholder.write(' ')

def save_project(project):
    # TODO: check required values
    project_id = project.get('project_id')
    name = project.get('name')
    backend = project.get('backend')
    vocab_id = project.get('vocab')
    lang = project.get('language')

    proj_path = os.path.join(os.getcwd(), find_config(), project_id + ".cfg")
    with open(proj_path, "w") as file:
        file.write(f"[{project_id}]\n")
        file.write(f"name = {name}\n")
        file.write(f"backend = {backend}\n")
        file.write(f"language = {lang}\n")
        file.write(f"vocab = {vocab_id}({lang})\n")
        # TODO: other values if they exist

def backend_form(project, keys):
    backend = project.get('backend')
    if not backend:
        st.error(f"Error fetching backend")
        return

    default_params = project.get('default_params')
    if not default_params:
        st.error(f"Error fetching default parameters")
        return

    params = project.get('backend_params')

    st.subheader(f"{backend} parameters", divider="gray")

    with st.container(border=True):
        filtered_backend = {}

        # FIXME: this needs to be refactored
        for key, default_value in default_params.items():
            key_id = f"{project.get('project_id')}_{project.get('backend_id')}_{key}"

            if key in params:
                try:
                    # Convert backend value to the type of default value
                    backend_value = type(default_value)(params[key])
                except (TypeError, ValueError):
                    backend_value = None

                if backend_value != default_value:
                    filtered_backend[key] = backend_value

            if isinstance(default_value, bool):
                form_value = st.checkbox(f"{key} :gray-badge[Default: {default_params.get(key)}]", value=params.get(key), key=key_id)
            elif isinstance(default_value, (int, float)):
                form_value = st.number_input(key, value=filtered_backend.get(key), key=key_id, placeholder=default_params.get(key))
            else:
                form_value = st.text_input(key, value=filtered_backend.get(key), key=key_id, placeholder=default_params.get(key))

            if None != form_value:
                filtered_backend[key] = form_value

        response = {
            "project_id": project.get('project_id'),
            "name": project.get('name'),
            "language": project.get('language'),
            "vocab": project.get('vocab'),
            "vocab_spec": project.get('vocab_spec'),
            "backend": {
                "backend_id": backend,
                "params": filtered_backend
            }
        }

        # Show list of sources for the ensemble
        if "ensemble" in backend:
            sources = project.get('backend_params').get('sources')

            if ":" in sources:
                source_list = [s.split(":")[0] for s in sources.split(",")]
            else:
                source_list = sources.split(",")

            new_sources = st.multiselect("Sources", keys, source_list)
            response['backend']['params']['sources'] = ",".join(new_sources)
            
            if ":" in sources:
                st.warning("Source weights have been ignored", icon=":material/warning:")

        if st.button("Save Configuration", key=f"save_{project.get('project_id')}_{backend}", type="primary"):
            save_project(response)

def new_buttons():
    @st.dialog("New Project")
    def project_modal():
        project_form({'is_new': True})

    if st.session_state.get("project_modal", False):
        st.session_state.project_modal = False
        project_modal()

    with st.container(horizontal=True):
        if st.button("New Project", icon=":material/add_box:"):
            st.session_state.project_modal = True
            st.rerun()

def main():
    st.set_page_config(page_title="cannif", layout="wide")

    st.markdown('<style>span[class^="st-"] { max-width: 100%; }</style>', unsafe_allow_html=True)
    st.markdown("<style>#cannif { font-family: Jost, sans-serif; }</style>", unsafe_allow_html=True)
    st.markdown("# <span style='color:red;'>can</span><span style='color:#002D72;'>nif</span>", unsafe_allow_html=True)

    if version := get_annif_version():
        st.caption(f"Annif {version} at {ANNIF_API}")
    else:
        exit()
    
    ############################
    st.session_state
    ############################
    
    new_buttons()

    projects = get_projects()

    list_projects(projects)

    project_details(projects)

    st.caption(f"{len(projects)} projects")

if __name__ == "__main__":
    main()
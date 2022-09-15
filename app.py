import streamlit as st
import pandas as pd
import monobinpy as mb
from pathlib import Path
import base64
import os
import inspect
from st_aggrid import AgGrid
from PIL import Image

#import styles
exec(open("styles.py").read())

#import custom functions
exec(open("_helpers.py").read())

#title
st.title("Streamlit UI for [monobinpy](https://pypi.org/project/monobinpy/) package")

#background picture
bg_url = os.getcwd() + "\\background.png"
set_bg(main_bg = bg_url)

#intro
st.markdown(Path("intro.md").read_text(), 
            unsafe_allow_html = True)
st.markdown("---")

#initiation session_state vars
if "db" not in st.session_state:
    st.session_state.file_path = 1
    st.session_state.db = None
    st.session_state.trg_opts = None
    st.session_state.dm_expanded = True
    st.session_state.ddc = False            #dummy data check    
    st.session_state.success = False
    st.session_state.res_sum = None
    st.session_state.res_rec = None
    st.session_state.clear_mb = False
    st.session_state.msg = "Please, select target, risk factors \
                            and setup binning algorithms in sidebar section."
    
#sidebar
image = Image.open(os.getcwd() + "\\settings.png")
ic1, ic2, ic3, ic4, ic5 = st.sidebar.columns(5)
ic3.image(image, use_column_width = False)
#data manager
st.sidebar.markdown(":house_buildings: **DATA MANAGER**")
upl_data = st.sidebar.file_uploader(key = f"{st.session_state.file_path}",
                                    label = "Import .csv file", 
                                    type = {"csv"})
#dummy upload
dummy_data = st.sidebar.button(label = "👊 Import dummy data",
                               on_click = dummy_upload)

#data upload
if upl_data is not None:
    data_upload()
st.sidebar.markdown("---")

if st.session_state.db is not None:
    #data manager - output
    dm = st.expander(label = "DATA MANAGER - import log", 
                     expanded = st.session_state.dm_expanded)
    dm.text("")
    if st.session_state.ddc:
        dm.markdown("<b><p style='color:#92d400;'>Dummy data uploaded!</p></b>",
                    unsafe_allow_html = True)
    else:
        if upl_data is not None:
            udn = "User data uploaded: " + upl_data.name + "!"
            dm.markdown(f"<b><p style='color:#92d400;'>{udn}</p></b>", 
                        unsafe_allow_html = True)
    tbl = df_info(db = st.session_state.db)
    dm.table(tbl)
    #monotonic binning
    mono_bin = st.expander(label = "MONOTONIC BINNING - target and risk factors selection", 
                           expanded = True)
    c1, c2 = mono_bin.columns(2)
    #trf = st.session_state.trg_opt
    target = c1.selectbox(label = "Select target variable",
                          options = st.session_state.trg_opts)
    rf_opts = [x for x in st.session_state.trg_opts if x != target]
    container = c2.container()
    rf_sel_all = c2.checkbox(label = "Select all risk factors",
                             value = False)
    if (rf_sel_all):
        rf = container.multiselect(label = "Select risk factors",
                                   options = rf_opts,
                                   default = rf_opts)
    else:
        rf = container.multiselect(label = "Select risk factors",
                                   options = rf_opts,
                                   default = None)
    st.sidebar.markdown(":runner: **MONOTONIC BINNING**")
    inputs = st.sidebar.container()
    bin_algo = inputs.selectbox(label = "Select binning algorithm",
                                options = ba)
    if bin_algo in ["sts_bin", "ndr_bin"]:
        bin_algo_select = "ndr_sts_bin" 
    else:
        bin_algo_select = bin_algo
    bin_ui = bin_algo_select + "_ui"  
    exec(eval(bin_ui))
    #run binning algo
    st.sidebar.button(label = "👊 Run binning algorithm",
                      on_click = binning,
                      args = [arg1])
    mb_container = mono_bin.empty()
    if st.session_state.success:
        with mb_container.container():
           c1_dwnl, c2_dwnl = st.columns(2)
           summ_rep = st.session_state.res_sum.to_csv().encode('utf-8')
           c1_dwnl.download_button(label = "Download summary report",
                                   data = summ_rep,
                                   file_name = "summary_report.csv",
                                   mime = "text/csv")
           reco_rep = st.session_state.res_rec.to_csv().encode('utf-8')
           c2_dwnl.download_button(label = "Download recoded database",
                                   data = reco_rep,
                                   file_name = "db_recoded.csv",
                                   mime = "text/csv")
           AgGrid(st.session_state.res_sum,
                  editable = True,
                  height = 400)
    else:
        mono_bin.warning(st.session_state.msg)
    
    if st.session_state.clear_mb:
        mb_container.empty()
            
    st.sidebar.markdown("---")
    
    
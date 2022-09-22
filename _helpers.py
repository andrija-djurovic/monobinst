# dummy upload
def dummy_upload():
    if "file_path" in st.session_state:
        st.session_state.file_path = st.session_state.file_path + 1
    url = "https://raw.githubusercontent.com/andrija-djurovic/monobinpy/main/gcd.csv"
    db = pd.read_csv(filepath_or_buffer = url)
    st.session_state.db = db
    st.session_state.dm_expanded = True
    st.session_state.trg_opts = db.columns
    st.session_state.ddc = True
    st.session_state.clear_mb = True
    st.session_state.success = False
    st.session_state.msg = "Please, select target, risk factors \
                            and setup binning algorithms in sidebar section."

# data upload
def data_upload():
    db = pd.read_csv(filepath_or_buffer = upl_data)
    st.session_state.db = db
    st.session_state.dm_expanded = True
    st.session_state.trg_opts = db.columns
    st.session_state.ddc = False
    st.session_state.clear_mb = True
    st.session_state.success = False
    st.session_state.msg = "Please, select target, risk factors \
                            and setup binning algorithms in sidebar section."

# print data frame info
@st.cache
def df_info(db):
    num_of_obs = db.shape[0]
    num_of_vars = len(db.columns)
    num_vars = db.select_dtypes(exclude=["object"]).columns.tolist()
    cat_vars = db.select_dtypes(include=["object"]).columns.tolist()
    Info = ["# of observations", "# of variables",
            "# of num variables", "# of cat variables"]
    Value = [num_of_obs, num_of_vars, len(num_vars), len(cat_vars)]
    res = pd.DataFrame({"Info": Info, "Value": Value})
    return(res)

# binning algos
ba = ["pct_bin", "cum_bin", "iso_bin", "woe_bin", "sts_bin", "ndr_bin"]

# pct_bin inputs
pct_bin_ui = inspect.cleandoc("""
    arg1 = inputs.text_input(label = "Special case elements",
                             value = "NaN, Inf, -Inf")
    arg2 = inputs.selectbox(label = "How to treat special cases",
                            options = ["together", "separately"])
    arg3 = inputs.number_input(label = "Number of starting groups",
                               min_value = 2,
                               max_value = 40,
                               value = 15,
                               step = 1)
    arg4 = inputs.selectbox(label = "Type of target variable",
                            options = ["guess", "bina", "cont"])
    arg5 = inputs.selectbox(label = "Force WoE trend (only for cont.)",
                            options = [True, False])
    arg6 = inputs.selectbox(label = "Force trend",
                            options = ["guess", "i", "d"])
""")

# cum_bin inputs
cum_bin_ui = inspect.cleandoc("""
    arg1 = inputs.text_input(label = "Special case elements",
                          value = "NaN, Inf, -Inf")
    arg2 = inputs.selectbox(label = "How to treat special cases",
                         options = ["together", "separately"])
    arg3 = inputs.number_input(label = "Number of starting groups",
                            min_value = 2,
                            max_value = 40,
                            value = 15,
                            step = 1)
    arg4 = inputs.selectbox(label = "Type of target variable",
                         options = ["guess", "bina", "cont"])
    arg5 = inputs.selectbox(label = "Force trend",
                         options = ["guess", "i", "d"])
""")

# iso_bin inputs
iso_bin_ui = inspect.cleandoc("""
    arg1 = inputs.text_input(label = "Special case elements",
                          value = "NaN, Inf, -Inf")
    arg2 = inputs.selectbox(label = "How to treat special cases",
                         options = ["together", "separately"])
    arg3 = inputs.selectbox(label = "Type of target variable",
                         options = ["guess", "bina", "cont"])
    arg4 = inputs.number_input(label = "Minimum pct. of observations per bin",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.05,
                            step = 0.01)
    arg5 = inputs.number_input(label = "Minimum avg. target rate per bin",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.05,
                            step = 0.01)
    arg6 = inputs.selectbox(label = "Force trend",
                         options = ["guess", "i", "d"])
""")

# woe_bin inputs
woe_bin_ui = inspect.cleandoc("""
    arg1 = inputs.text_input(label="Special case elements",
                          value="NaN, Inf, -Inf")
    arg2 = inputs.selectbox(label="How to treat special cases",
                         options=["together", "separately"])
    arg3 = inputs.selectbox(label="Type of target variable",
                         options=["guess", "bina", "cont"])
    arg4 = inputs.number_input(label = "Minimum pct. of observations per bin",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.05,
                            step = 0.01)
    arg5 = inputs.number_input(label = "Minimum avg. target rate per bin",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.05,
                            step = 0.01)
    arg6 = inputs.number_input(label = "WoE threshold",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.10,
                            step = 0.10)
    arg7 = inputs.selectbox(label ="Force trend",
                         options = ["guess", "i", "d"])
""")

# ndr_sts_bin inputs
ndr_sts_bin_ui = inspect.cleandoc("""
    arg1 = inputs.text_input(label = "Special case elements",
                          value = "NaN, Inf, -Inf")
    arg2 = inputs.selectbox(label = "How to treat special cases",
                         options = ["together", "separately"])
    arg3 = inputs.selectbox(label = "Type of target variable",
                         options = ["guess", "bina", "cont"])
    arg4 = inputs.number_input(label = "Minimum pct. of observations per bin",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.05,
                            step = 0.01)
    arg5 = inputs.number_input(label = "Minimum avg. target rate per bin",
                            min_value = 0.00,
                            max_value = 1.00,
                            value = 0.05,
                            step = 0.01)
    arg6 = inputs.number_input(label="p-value",
                            min_value=0.00,
                            max_value=1.00,
                            value=0.05,
                            step=0.01)
    arg7 = inputs.selectbox(label="Force trend",
                         options=["guess", "i", "d"])
""")

# binning
monobin_fun = [
    "mb.pct_bin(x = x, y = y, sc = arg1_s, sc_method = arg2,\
              g = arg3,y_type = arg4,\
              woe_trend = arg5,\
              force_trend = arg6)",
    "mb.cum_bin(x = x, y = y, sc = arg1_s, sc_method = arg2,\
              g = arg3, y_type = arg4,\
              force_trend = arg5)",
    "mb.iso_bin(x = x, y = y, sc = arg1_s, sc_method = arg2,\
                y_type = arg3,  min_pct_obs = arg4, \
               min_avg_rate = arg5, force_trend = arg6)",
    "mb.woe_bin(x = x, y = y, sc = arg1_s, sc_method = arg2,\
              y_type = arg3,  min_pct_obs = arg4,\
              min_avg_rate = arg5, woe_gap = arg6,\
              force_trend = arg7)",
    "mb.sts_bin(x = x, y = y, sc = arg1_s, sc_method = arg2,\
                y_type = arg3,  min_pct_obs = arg4,\
                min_avg_rate = arg5, p_val = arg6,\
                force_trend = arg7)",
    "mb.ndr_bin(x = x, y = y, sc = arg1_s, sc_method = arg2,\
                y_type = arg3,  min_pct_obs = arg4,\
                min_avg_rate = arg5, p_val = arg6,\
                force_trend = arg7)"
    ]
monobin_fun_dict = dict(zip(ba, monobin_fun))

def binning(sc):
    st.session_state.dm_expanded = False
    st.session_state.clear_mb = False
    
    rfl = len(rf)
    if rfl == 0:
        st.session_state.msg = "Please, select target, risk factors \
                                and setup binning algorithms in sidebar section."
        st.session_state.success = False
        st.session_state.clear_mb = True
        return()
        
    arg1_s = sc.split(",")
    arg1_s = [x.replace(" ", "") for x in arg1_s]
    arg1_s = [float(x) for x in arg1_s]
    y = st.session_state.db[target]
    mono_algo = monobin_fun_dict.get(bin_algo)
    res_sum = []
    res_rec = []
    for i in [*range(rfl)]:
        rf_l = rf[i]
        x = st.session_state.db[rf_l]
        res_l = eval(mono_algo)
        if len(res_l) == 1:
            next 
        else:
            res_l[0].insert(0, "rf", rf_l)
            res_sum = res_sum + [res_l[0].copy()]
            res_rec = res_rec + [pd.DataFrame(res_l[1].copy())]
    if len(res_sum) > 0:
        st.session_state.res_sum = pd.concat(res_sum, 
                                             axis = 0, 
                                             ignore_index = True)
        st.session_state.res_rec = pd.concat(res_rec, 
                                             axis = 1, 
                                             ignore_index = False)
        st.session_state.success = True
        st.session_state.clear_mb = False
    else:
        st.session_state.success = False
        st.session_state.clear_mb = True
        st.session_state.msg = "Binning cannot be performed for selected risk factor(s)."

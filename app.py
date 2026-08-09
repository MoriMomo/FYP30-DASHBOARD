"""
FYP B30 - Freshman Progress Dashboard (versi manual upload)
Upload file Excel (multi-sheet, 1 sheet = 1 kelas), dashboard otomatis
gabungin semua sheet & tampilkan visualisasi freshman yang belum sesuai target point.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FYP B30 Progress Dashboard", layout="wide")

GDRIVE_LOGBOOK_LINK = "https://drive.google.com/drive/folders/1hwEZYgQ_ZiW1GEQuFDDhQxUvwAS-XnrA?usp=sharing"

st.title("📊 FYP B30 - Freshman Progress Dashboard")

st.info(
    f"""
    **Status "Belum Sesuai"** menunjukkan adanya ketidaksesuaian antara data pada
    **File Monitoring FL** dengan data pada **Logbook** sebenarnya.

    Maka dari itu, masing-masing FYPL dimohon untuk mengecek kembali nama-nama FM
    yang tercantum di bawah ini dan melakukan crosscheck dengan bukti Logbook yang
    telah di-upload ke Google Drive.

    Mohon dipastikan kembali bahwa data pada File Monitoring FL sudah sesuai dengan
    bukti yang tersedia di Google Drive.

    📁 [Buka Google Drive - All Drive FYP Logbook]({GDRIVE_LOGBOOK_LINK})
    """
)

# ============================================================
# MAPPING PIC PER KELAS
# ============================================================
PIC_MAPPING = {
    "BBN01": "Jess", "BBN02": "Lyla", "BBN03": "Mengko", "BBN04": "Farah",
    "BBN05": "Farah", "BBN06": "Ken", "BBN07": "Jihan", "BBN08": "Kia",
    "BBN09": "Pitri", "BBN10": "Kia", "BBN11": "Nadira", "BBN12": "Juan",
    "BBN13": "Lyla", "BBN14": "Bayu", "BBN15": "Mengko", "BBN16": "Nata",
    "BBN17": "Refa", "BBN18": "Diana", "BBN19": "Diana", "BBN20": "Razka",
    "BBN21": "Nata", "BBN22": "Jihan", "BBN23": "Juan", "BBN24": "Tian",
    "BBN25": "Jess", "BBN26": "Megan", "BBN27": "Nadira", "BBN28": "Ais",
    "BBN29": "Refa", "BBN30": "Ais", "BBN31": "Kasih", "BBN32": "Ken",
    "BBN33": "Razka",
}

# ============================================================
# UPLOAD FILE
# ============================================================
uploaded_file = st.file_uploader("Upload file Excel terbaru", type=["xlsx", "xls"])

if uploaded_file is None:
    st.info("Upload file Excel dulu (format: 1 sheet = 1 kelas) buat lihat dashboard.")
    st.stop()


@st.cache_data
def load_data(file):
    xls = pd.ExcelFile(file)
    all_dfs = []
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        if df.empty:
            continue
        df["Kelas"] = sheet_name  # nama sheet = nama kelas
        all_dfs.append(df)

    df_all = pd.concat(all_dfs, ignore_index=True)
    df_all.columns = [c.strip() for c in df_all.columns]

    df_all["prediksi point"] = pd.to_numeric(df_all["prediksi point"], errors="coerce")
    df_all["point apps"] = pd.to_numeric(df_all["point apps"], errors="coerce")

    df_all["Status"] = df_all.apply(
        lambda r: "Belum Sesuai" if r["prediksi point"] != r["point apps"] else "Sesuai",
        axis=1,
    )

    # tambahin kolom PIC berdasarkan mapping kelas
    df_all["PIC"] = df_all["Kelas"].map(PIC_MAPPING).fillna("Belum ada PIC")

    return df_all


df = load_data(uploaded_file)

# ============================================================
# SIDEBAR FILTER
# ============================================================
st.sidebar.header("Filter")
kelas_list = sorted(df["Kelas"].unique())
selected_kelas = st.sidebar.multiselect("Kelas", kelas_list, default=kelas_list)
status_filter = st.sidebar.radio("Status", ["Semua", "Belum Sesuai", "Sesuai"])

pic_list = sorted(df["PIC"].unique())
selected_pic = st.sidebar.multiselect("PIC", pic_list, default=pic_list)

df_filtered = df[df["Kelas"].isin(selected_kelas) & df["PIC"].isin(selected_pic)]
if status_filter != "Semua":
    df_filtered = df_filtered[df_filtered["Status"] == status_filter]

# ============================================================
# SUMMARY CARDS
# ============================================================
total_freshman = len(df_filtered)


col1, col2, col3 = st.columns(3)
col1.metric("Total Freshman Yang Belum Selesai", total_freshman)


st.divider()

# ============================================================
# CHART: PER KELAS
# ============================================================
st.subheader("Belum Sesuai per Kelas")

summary_kelas = (
    df_filtered.groupby("Kelas")["Status"]
    .apply(lambda s: (s == "Belum Sesuai").sum())
    .reset_index(name="Jumlah Belum Sesuai")
    .sort_values("Jumlah Belum Sesuai", ascending=False)
)

fig = px.bar(
    summary_kelas,
    x="Kelas",
    y="Jumlah Belum Sesuai",
    color="Jumlah Belum Sesuai",
    color_continuous_scale="Reds",
    text="Jumlah Belum Sesuai",
)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TABEL PIC - STATISTIK PER PIC
# ============================================================
st.subheader("Statistik per PIC")

pic_summary = (
    df_filtered.groupby("PIC")
    .agg(
        Jumlah_Kelas=("Kelas", lambda s: s.nunique()),
        Kelas=("Kelas", lambda s: ", ".join(sorted(s.unique()))),
        Total_Freshman=("Status", "count"),
    )
    .reset_index()
)
pic_summary = pic_summary.sort_values("Total_Freshman", ascending=False)
pic_summary = pic_summary.rename(
    columns={
        "Jumlah_Kelas": "Jumlah Kelas",
        "Total_Freshman": "Total Freshman",
    }
)

st.dataframe(pic_summary, use_container_width=True, hide_index=True)

# ============================================================
# LEADERBOARD: PER FL
# ============================================================
st.subheader("Ranking FL berdasarkan Jumlah Freshman Belum Sesuai")

fl_summary = (
    df_filtered.groupby(["Kelas", "NAMA FRESHMEN LEADER"])["Status"]
    .apply(lambda s: (s == "Belum Sesuai").sum())
    .reset_index(name="Jumlah Belum Sesuai")
    .sort_values("Jumlah Belum Sesuai", ascending=False)
)
st.dataframe(fl_summary, use_container_width=True, hide_index=True)

# ============================================================
# TABEL DETAIL
# ============================================================
st.subheader("Detail Freshman")


def highlight_status(row):
    color = "background-color: #999999" if row["Status"] == "Belum Sesuai" else ""
    return [color] * len(row)


display_cols = [
    "Kelas",
    "PIC",
    "NAMA FRESHMEN LEADER",
    "NAMA FRESHMEN",
    "prediksi point",
    "point apps",
    "selisih",
    "Sesi yang 0",
    "Sesi yang Kosong",
    "Status",
]
display_cols = [c for c in display_cols if c in df_filtered.columns]

st.dataframe(
    df_filtered[display_cols].style.apply(highlight_status, axis=1),
    use_container_width=True,
    hide_index=True,
)

st.caption(f"Data dari file: {uploaded_file.name}")

st.divider()

st.info(
    f"""
    **Status "Belum Sesuai"** menunjukkan adanya ketidaksesuaian antara data pada
    **File Monitoring FL** dengan data pada **Logbook** sebenarnya.

    Maka dari itu, masing-masing FYPL dimohon untuk mengecek kembali nama-nama FM
    yang tercantum di atas dan melakukan crosscheck dengan bukti Logbook yang
    telah di-upload ke Google Drive.

    Mohon dipastikan kembali bahwa data pada File Monitoring FL sudah sesuai dengan
    bukti yang tersedia di Google Drive.

    📁 [Buka Google Drive - All Drive FYP Logbook]({GDRIVE_LOGBOOK_LINK})
    """
)
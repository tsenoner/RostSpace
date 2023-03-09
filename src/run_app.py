from pathlib import Path

from src.callbacks import get_callbacks
from src.preprocessing import DataPreprocessor
from src.structurecontainer import StructureContainer
from src.visualization.visualizator import Visualizator

# set paths
out_dir = Path("3FTx")
hdf_path = out_dir / "3FTx_mature_prott5.h5"
csv_path = out_dir / "3FTx.csv"
fasta_path = out_dir / "3FTx_mature.fasta"

# put UMAP parameters in dictionary
umap_paras = dict()
umap_paras["n_neighbours"] = 25
umap_paras["min_dist"] = 0.5
umap_paras["metric"] = "euclidean"

# Put TSNE parameters in dictionary
tsne_paras = dict()
tsne_paras["iterations"] = 1000
tsne_paras["perplexity"] = 30.0
tsne_paras["learning_rate"] = "auto"
tsne_paras["tsne_metric"] = "euclidean"

dim_red = "UMAP"
data_preprocessor = DataPreprocessor(
    output_d=out_dir,
    hdf_path=hdf_path,
    csv_path=csv_path,
    fasta_path=fasta_path,
    csv_separator=",",
    uid_col=0,
    html_cols=None,
    reset=False,
    dim_red=dim_red,
    umap_paras=umap_paras,
    tsne_paras=tsne_paras,
    verbose=False,
)

# Preprocessing
(
    df,
    fig,
    csv_header,
    original_id_col,
    embeddings,
    embedding_uids,
    distance_dic,
    fasta_dict,
) = data_preprocessor.data_preprocessing()

umap_paras_dict = data_preprocessor.get_umap_paras_dict(df)
tsne_paras_dict = data_preprocessor.get_tsne_paras_dict(df)

structure_container = StructureContainer(pdb_d=None, json_d=None)
ids = df.index.to_list()

# Create visualization object
visualizator = Visualizator(fig=fig, csv_header=csv_header, dim_red=dim_red)
app = visualizator.get_base_app(umap_paras, tsne_paras, original_id_col=ids)

get_callbacks(
    app=app,
    df=df,
    original_id_col=None,
    umap_paras=umap_paras,
    tsne_paras=tsne_paras,
    output_d=out_dir,
    csv_header=csv_header,
    embeddings=embeddings,
    embedding_uids=embedding_uids,
    distance_dic=distance_dic,
    umap_paras_dict=umap_paras_dict,
    tsne_paras_dict=tsne_paras_dict,
    fasta_dict=fasta_dict,
    struct_container=structure_container,
)
server = app.server
app.run_server()
# app = create_app(
#     out="../3FTx", hdf="../3FTx/3FTx_mature_prott5.h5", csv="../3FTx/3FTx.csv"
# )

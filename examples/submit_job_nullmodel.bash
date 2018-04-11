#!/bin/sh
#
CMD_ENTRY="/usr/local/analysis_pipeline/batchJob.py"
WD="-w /projects/topmed/analysts/kuraisa/freeze5b/compute_test_chr21"
DEB="-D 1"
NM="-n"
RD="--rd /usr/local/analysis_pipeline/runRscript.sh"
AT="-a 0"
RA1="--ra '/projects/topmed/devel/analysis_pipeline/R/null_model.R config/HCT_single_null_model.config --version 1.99.3' "
RA="--ra '/usr/local/analysis_pipeline/R/null_model.R config/HCT_single_null_model.config --version 1.99.3' "
DR="-d /projects "

DO_ENV="-e R_LIBS_USER=/projects/resources/gactools/R_packages/library "
DO_VOL="-v /projects:/projects "

D_CMD="docker run --rm -it $DO_ENV $DO_VOL uwgac/topmed-devel $CMD_ENTRY $WD $DEB $NM $RD $AT $RA $DR"
echo "Docker command:"
echo "$D_CMD"

# docker run --rm -it -e R_LIBS_USER=/projects/resources/gactools/R_packages/library -v /projects:/projects uwgac/topmed-master /usr/local/analysis_pipeline/batchJob.py -w /projects/topmed/analysts/kuraisa/freeze5b/compute_test_chr21 -D 1 -n --rd /usr/local/analysis_pipeline/runRscript.sh -a 0 --ra '/projects/topmed/devel/analysis_pipeline/R/null_model.R config/HCT_single_null_model.config --version 1.99.3' -d /projects

# docker run --rm -it -e R_LIBS_USER=/projects/resources/gactools/R_packages/library -v /projects:/projects uwgac/topmed-master

docker run --rm -it -v /nfs_mnt/projects:/projects -v /Users/royboy/.aws:/royaws uwgac/aws-master docker2aws.py -w /projects/topmed/analysts/kuraisa -a assoc -p "single --cluster_type AWS_Batch --verbose --cluster_file single_cluster_config.json /projects/topmed/analysts/sdmorris/freeze5/compute_test/assoc_single_sparse.config --chromosome 21 --print" -s /royaws/credentials

docker run --rm -it --privileged -v /nfs_mnt/projects:/projects -v /Users/royboy/.aws:/royaws uwgac/topmed-roybranch docker2aws.py -w /projects/topmed/analysts/kuraisa/freeze5b/compute_test_chr21 -a assoc -p "single --cluster_type AWS_Batch --verbose --cluster_file single_cluster_config.json /projects/topmed/analysts/sdmorris/freeze5/compute_test/assoc_single_sparse.config --chromosome 21 --print" -s /royaws/credentials

# nulll null_model
docker run --rm -it -v /projects:/projects uwgac/topmed-master /usr/local/analysis_pipeline/ap2batch.py -w /projects/topmed/analysts/kuraisa/freeze5b/compute_test_chr21 -D 1 -n --rd /usr/local/analysis_pipeline/runRscript.sh -a 0 --ra '/projects/topmed/devel/analysis_pipeline/R/null_model.R config/HCT_single_null_model.config --version 1.99.3' -d /projects

# grm
    docker run --rm -it -v /nfs_mnt/projects/topmed/analysts/kuraisa/freeze5b/grm_squeeze:/projects uwgac/topmed-roybranch
# from within docker
export NSLOTS=4
R -q --vanilla --args --version 1.99.3 --chromosome 22 HCT_grm.config < /projects/topmed/working_code/analysis_pipeline/R/grm.R

docker run --rm -it -w /topmed_admin/tmp -v /nfs_ebs/topmed_admin:/topmed_admin uwgac/topmed-roybranch ./ioperf.sh

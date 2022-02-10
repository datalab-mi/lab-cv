export IMAGE_NAME=lab-cv
export PROJECT_NAME=iafoule
export APP_PATH := $(shell pwd)
export VERSION := v0.1.2
export USER := $(shell whoami)
export NB_GPUS := 2
export NB_CPUS := 0 # this value is ignored if NB_GPUS is specified.
export REGION := gra
export PROJECT_DATA_RIGHTS := ro
dummy	:= $(shell touch artifacts)
include ./artifacts
# build locally the docker image
build:
	docker build -t $(IMAGE_NAME) .
run-locally:build
	docker run --rm -it -v ${APP_PATH}/group:/etc/group -v ${APP_PATH}/passwd:/etc/passwd --user=ovh:ovh $(IMAGE_NAME)

# Deploy job to ovh
deploy-job:
	ovhai job run \
		--gpu ${NB_GPUS} \
		--cpu ${NB_CPUS} \
		--name ${PROJECT_NAME}-${USER}-${NB_GPUS}GPU-${NB_CPUS}CPU \
		--label user=${USER}\
		--volume ${PROJECT_NAME}-home@${REGION}/${USER}:/workspace/home/${USER}:rw \
		--volume ${PROJECT_NAME}-home@${REGION}:/workspace/home:ro \
		--volume cclabeler-data@${REGION}:/workspace/cclabeler:ro \
		--volume ${PROJECT_NAME}-data@${REGION}:/workspace/data:${PROJECT_DATA_RIGHTS} \
		--volume lab-cv-${PROJECT_NAME}-notebook@${REGION}:/workspace/notebook:ro \
		--volume lab-cv-${PROJECT_NAME}-code@${REGION}:/workspace/code:ro \
		--volume share@${REGION}:/workspace/share:ro \
		--output json \
		ghcr.io/datalab-mi/${IMAGE_NAME}:${VERSION} > job.json \
		$(command)

#usage: make stop-job JOB=xxxxx
stop-job:
	ovhai job stop $(JOB)

list-job:
	ovhai job list

# open the job in notebook
jobid=$(grep -Po '"id":.*?[^\\]"' job.json |awk -F':' '{print $2}')
open-job:
	@echo $(jobid)

data-upload:
	ovhai data upload ${REGION} $(DST) $(SRC)

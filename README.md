# kipoi-docker
This is an attempt to reduce  and eventully eliminate complexities related to creating and invoking model specific conda environments. The docker images are hosted here -
```https://hub.docker.com/repository/docker/haimasree/kipoi-docker```

# Building the docker images

First, we need to build the base image which activates a conda environment made with python 3.6 with kipoi installed in it.
```
cd dockerfiles
docker build -f dockerfiles/Dockerfile.base -t haimasree/kipoi-docker:kipoi-base-env ..
```
Note: The model specific Dockefiles are sensitive to the name and tag of the base image right now. 
After the base image is built, build any other image using the following template
```
docker build -f Dockerfile.<model-group-name-in-lowercase> -t haimasree/kipoi-docker:<image-name> ..
```
For more information on which model group (or model) can be run with which docker image, see ```test-containers/image-name-to-models.json``` where each  image in docker hub repository haimasree/kipoi-docker is mapped to models they can run. 

# Running the images
For an interactive experience, run the following -
```
docker run -it haimasree/kipoi-docker:kipoisplice
```
This will give you an interactive shell with the relevant conda environment kipoi-KipoiSplice.
To run your custom kipoi cli calls directly,
```
docker run haimasree/kipoi-docker:kipoisplice kipoi test KipoiSplice/4 --source=kipoi
```

## Testing the containers

### Manual

We use pytest and docker-py to test the containers.
First in an isolated conda environment or pipenv do the following -
```
pip install -r requirements.txt
```

Currently, there are two ways to test the containers along with the models.
- Test all of 2137 models in their respective containers using the following
  - ```pytest test-containers/test_all.py ```
- Test any one model at a time
  - ```pytest test-containers/test_models_from_command_line.py --model=KipoiSplice/4,Basenji```
  - ```pytest test-containers/test_models_from_command_line.py --model=HAL```
- Test all model groups with one representative model per group
  - ```pytest test-containers/test_models_from_command_line.py --all```
  
 ### CI
 
 Alternatively, look into the job named test in the workflow in ```.github/workflows/test-images.yml```

## Mapping between model and docker images

To know which model group/model is represented by which docker image pleae take a look at https://github.com/haimasree/kipoi-containers/blob/main/test-containers/model-group-to-image-name.json

Due to conflicting package requirements, all models in group MMSplice could not be represented by a single docker image. MMSplice/mtsplice has its own docker image named haimasree/kipoi-docker:mmsplice-mtsplice and the rest can be tested with haimasree/kipoi-docker:mmsplice

## Singularity support

The images in ```haimasree/kipoi-docker``` repo in dockerhub can be easily converted into a local singularity image using ```./build-singularity-container.sh```. If no argument is provided, all existing images will be converted and a sample model will be tested against the singularity image as a sanity check. Otherwise, ```./build-singularity-container.sh -i <name of the docker image> -m <suitable model group name>``` will convert a docker image in ```haimasree:kipoi-docker``` repo into a singularity image and test the named model. For example,  ```./build-singularity-container.sh -i sharedpy3keras2 -m Basset``` will test Basset with the singularity container made locally from haimasree/kipoi-docker:sharedpy3keras2
# Legis

DESC HEREZ

## Installation

### Legis pipeline

1. Install Anaconda
2. Create `legis` environment
```
conda create --name legis python=3.6 -f environment.yaml 
```

### Docker
Unix-based OS: 
Windows-based: https://docs.docker.com/docker-for-windows/install/


## Usage

## Run the Neo4j service
Before proceeding, make sure the the docker service is running.
Working directory should be `base_path_to_legis/legis`.

Unix-based OS:

```
./run.sh
```

Windows-based:
1. Change `$HOME` to your preferred graph storage directory. 
3. Run the command below. Note: Change the `\` to '\\' of the host parameters only, e.g. `-v some_path\\neo4j\data:/data`

```
docker run \
    --rm \
    --name legis \
    -p7474:7474 -p7687:7687 \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/test \
    neo4j:latest
```
*Note: haven't checked if this will work*


## Run the Legis Graphinificator

1. Activate `legis` env
2. Run pipeline
```
python legis.py
```

## Exploring the Graph
1. Open Neo4j through browser:
```
http://localhost:7474/browser/
```
Visualizing the whole graph: 
```
MATCH (n)<-[r]->(b) RETURN n,r,b
```

## TO DO:
* Authors:
    * Add senator data in the pipeline
    * Add party reps in the pipeline
* Node properties (Please follow the template)
    * Bills
    * Authors
* Security
    * Environment vars
    * Change creds
* Variable consistency
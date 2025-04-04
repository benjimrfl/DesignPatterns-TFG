# DesignPatterns-LLMs
This proyects aims to automatically analize the capabilities of LLMs of interpretate design patterns

## Index
1. [Usage](#usage)
    1. [Example](#example)
2. [Repository structure](#repository-structure)
3. [Deployment](#deployment)
    1. [Installation](#installation)
    2. [Execution](#execution)
    3. [Docker](#docker)
  

This app cab be also deployed with docker: 
docker-compose up --build

## Usage

To view the API documentation, access the following URL:

```
http://localhost:8000/docs
```

Or

```
http://localhost:8000/redoc
```

### Example

In this section we show how to use the app with the following example. We need to have POET and EVA api deployed; if you are running it in local, please make sure it is being used the correct url at the api_client.

We are going to make a request to the http://localhost:8000/antipatterns/evaluate endpoint:


````json
{
  "code": "class TextFileProcessor {\n    public void openFile() {\n        System.out.println(\"Opening text file...\");\n    }\n\n    public void readData() {\n        System.out.println(\"Reading data from text file...\");\n    }\n\n    public void processData() {\n        System.out.println(\"Processing text file data...\");\n    }\n\n    public void closeFile() {\n        System.out.println(\"Text file closed.\");\n    }\n}\n\nclass XMLFileProcessor {\n    public void openFile() {\n        System.out.println(\"Opening XML file...\");\n    }\n\n    public void readData() {\n        System.out.println(\"Reading data from XML file...\");\n    }\n\n    public void processData() {\n        System.out.println(\"Processing XML file data...\");\n    }\n\n    public void closeFile() {\n        System.out.println(\"XML file closed.\");\n    }\n\n    public void validateData() {\n        System.out.println(\"Validating XML file data...\");\n    }\n}\n\nclass BinaryFileProcessor {\n    public void openFile() {\n        System.out.println(\"Opening binary file...\");\n    }\n\n    public void readData() {\n        System.out.println(\"Reading data from binary file...\");\n    }\n\n    public void processData() {\n        System.out.println(\"Processing binary file data...\");\n    }\n\n    public void closeFile() {\n        System.out.println(\"Binary file closed.\");\n    }\n}",
  "antipatterns": [
    "Template Method"
  ]
}
````


To evaluate this input, we need to be running the language model provided by [Ollama](https://ollama.com/). After that, the app will be work to give us a result of the evaluation. You can see the logs for furtherinformation of what is happening at the console.

````json
{
    "passed cases / total tests": "1 / 1",
    "failed cases / total tests": "0 / 1",
    "evaluation success rate": 100.0,
    "failed cases": []
}
````

This is the same with the endpoint http://localhost:8000/patterns/evaluate, but changing the json provided like:

````json
{
    "code": "interface TransportVehicle {\n    void transport();\n    void deliver();\n}\n\nclass Ship implements TransportVehicle {\n    private String model;\n    private int year;\n    private int maxSpeed;\n\n    public Ship(String model, int year, int maxSpeed) {\n        this.model = model;\n        this.year = year;\n        this.maxSpeed = maxSpeed;\n    }\n\n    public String getModel() {\n        return this.model;\n    }\n\n    public int getYear() {\n        return this.year;\n    }\n\n    public int getMaxSpeed() {\n        return this.maxSpeed;\n    }\n    \n    @Override\n    public void transport() {\n        System.out.println(\"The ship \" + getModel() + \" is transporting. \");\n    }\n\n    @Override\n    public void deliver() {\n        System.out.println(\"The ship \" + getModel() + \" is delivering. \");\n    }\n}\n\nclass Truck implements TransportVehicle {\n    private String model;\n    private int year;\n    private int maxSpeed;\n\n    public Truck(String model, int year, int maxSpeed) {\n        this.model = model;\n        this.year = year;\n        this.maxSpeed = maxSpeed;\n    }\n\n    public String getModel() {\n        return this.model;\n    }\n\n    public int getYear() {\n        return this.year;\n    }\n\n    public int getMaxSpeed() {\n        return this.maxSpeed;\n    }\n    \n    @Override\n    public void transport() {\n        System.out.println(\"The truck \" + getModel() + \" is transporting. \");\n    }\n\n    @Override\n    public void deliver() {\n        System.out.println(\"The truck \" + getModel() + \" is delivering. \");\n    }\n}",
    "pattern": "C.",
    "patternList": [
        "Visitor",
        "Observer",
        "Factory method"
    ]
}

````

Being the letter A, B or C, corresponding to the items respectively. Again we face a similar output:

````json
{
    "passed cases / total tests": "1 / 1",
    "failed cases / total tests": "0 / 1",
    "evaluation success rate": 100.0,
    "failed cases": []
}
````

In case some test failed, we would see some description about the case that failed:

````json
{
    "passed cases / total tests": "0 / 1",
    "failed cases / total tests": "1 / 1",
    "evaluation success rate": 0.0,
    "failed cases": [
        {
            "query": "Given the following code: \"interface TransportVehicle {\n    void transport();\n    void deliver();\n}\n\nclass Ship implements TransportVehicle {\n    private String model;\n    private int year;\n    private int maxSpeed;\n\n    public Ship(String model, int year, int maxSpeed) {\n        this.model = model;\n        this.year = year;\n        this.maxSpeed = maxSpeed;\n    }\n\n    public String getModel() {\n        return this.model;\n    }\n\n    public int getYear() {\n        return this.year;\n    }\n\n    public int getMaxSpeed() {\n        return this.maxSpeed;\n    }\n    \n    @Override\n    public void transport() {\n        System.out.println(\"The ship \" + getModel() + \" is transporting. \");\n    }\n\n    @Override\n    public void deliver() {\n        System.out.println(\"The ship \" + getModel() + \" is delivering. \");\n    }\n}\n\nclass Truck implements TransportVehicle {\n    private String model;\n    private int year;\n    private int maxSpeed;\n\n    public Truck(String model, int year, int maxSpeed) {\n        this.model = model;\n        this.year = year;\n        this.maxSpeed = maxSpeed;\n    }\n\n    public String getModel() {\n        return this.model;\n    }\n\n    public int getYear() {\n        return this.year;\n    }\n\n    public int getMaxSpeed() {\n        return this.maxSpeed;\n    }\n    \n    @Override\n    public void transport() {\n        System.out.println(\"The truck \" + getModel() + \" is transporting. \");\n    }\n\n    @Override\n    public void deliver() {\n        System.out.println(\"The truck \" + getModel() + \" is delivering. \");\n    }\n}\", which design pattern from these options is being applied? Option A) Factory method Option B) Observer Option C) Visitor. Provide a response restricted with one of the values of the list including the letter of the option (A, B or C), whitout any explanation",
            "expected_result": "C.",
            "generated_result": "A"
        }
    ]
}
````

### Repository structure

This repository is structured as follows:

- `docker/.dockerignore`: This file tells Docker which files and directories to ignore when building an image.
- `Dockerfile`: This file is a script containing a series of instructions and commands used to build a Docker image.
- `docker/docker-compose.yml`: This YAML file allows you to configure application services, networks, and volumes in a
  single file, facilitating the orchestration of containers.
- `api_client/`: Contains the code source to make request to the necessary endpoints.
- `app.py`: The source code to execute this app in local
- `src/`: This directory contains the source code for the project.
- `.gitignore`: This file is used by Git to exclude files and directories from version control.
- `requirements.txt`: This file lists the Python libraries required by the project.

## Deployment

### Installation

If you haven't downloaded the project yet, first clone the repository:

```bash
git clone https://github.com/javvazzam/DesignPatterns-LLMs.git
```

To install the project, run the following command:

```bash
pip install -r requirements.txt
```

### Execution

To run the project, execute the following command from the root directory:

```bash
python app.py
```

Or

```bash
uvicorn app:app --reload
```

This will run on port 8000. However, if you wish to change the port, you can do so with the following command:

```bash
uvicorn app:app --reload --port 8001 
```

### Docker

To run Docker Compose execute the following command:

```bash
docker-compose up --build
```

This will run on port that you defined in the Dockerfile.

To stop the container, execute the following command:

```bash
docker-compose down
```

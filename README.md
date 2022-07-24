# Operationalizing Machine Learning

In this project, we will continue to work with the Bank Marketing dataset. We will use Azure to configure a cloud-based machine learning production model, deploy it, and consume it. We will also create, publish, and consume a pipeline.

## Architectural Diagram
An architectural diagram is an image that helps visualize the flow of operations from start to finish. it shows the various stages that are critical to the overall flow.

<img src="/pictures/architectural_diagram.png" title="architectural diagram"  width="200">

## Key Steps
This project is composed of several steps :
1. Authentication
2. Create and run Auto ML Experiment
3. Deploy the best model
4. Enable logging
5. Swagger Documentation
6. Consume model endpoints
7. Benchmark the endpoint using Apache bench
8. Create and publish a pipeline
9. Documentation

<img src="/pictures/pipeline.png" title="pipeline"  width="700">

Let's review all of them.
1. Authentication 

In that step, we create the Service Principal (SP) and allow the SP access to our previously created workspace. In order to achieve that step, simply run run script *scripts\Workspace_create.ps1*, and everything will be automatically done for you.
<br>
Created workspace :
<img src="/pictures/workspace.png" title="workspace"  width="700">
<br>
Created service principal :
<img src="/pictures/service_principal.png" title="service principal"  width="700">
<br>
Workspace share :
<img src="/pictures/ml_workspace_share.png" title="ml workspace share"  width="700">

2. Create and run Auto ML Experiment

At this point, security is enabled and authentication is completed. In this step, we will create an experiment using Automated ML, configure a compute cluster, and use that cluster to run the experiment.

- Create a new Automated ML job
<img src="/pictures/Create_new_Automated_ML_job.png" title="new Automated ML job"  width="700">

- Select and upload the Bankmarketing dataset
<img src="/pictures/upload_Bankmarketing_dataset.png" title="upload the Bankmarketing dataset"  width="700">

- Create a new Automated ML experiment and select target column

- Configure a new compute cluster. Select Standard_DS12_v2 for the Virtual Machine Size and select 1 as the number of minimum nodes.
<img src="/pictures/new_compute_cluster.png" title="new compute cluster"  width="700">

- Run the experiment using *Classification*, ensure *Explain best model* is checked. On *Exit criterion*, reduce the default (3 hours) to 1 and reduce the *Concurrency* from default to 5 (this number should always be less than the number of the compute cluster). Also set up the validation and test type.
<img src="/pictures/select_classification.png" title="select classification"  width="700">
<img src="/pictures/validation_and_test_type.png" title="validation and test type"  width="700">

At the end of the process, you should see something similar to that :
<img src="/pictures/run_Auto_ML_Experiment_final.png" title="Auto ML Experiment"  width="700">

3. Deploy the best model. After the experiment run completes, a summary of all the models and their metrics are shown, including explanations. The Best Model will be shown in the Details tab. In the Models tab, it will come up first (at the top). Deploying the Best Model will allow to interact with the HTTP API service and interact with the model by sending data over POST requests.

In my case, I found that **Voting Ensemble** was the best model with a score of 0.95.
<img src="/pictures/all_models.png" title="All trained models"  width="700">
<br>
Bellow are some metrics for that model :
<img src="/pictures/voting_ensemble_metrics.png" title="voting ensemble metrics"  width="700">
<br>
Confusion matrix :
<img src="/pictures/voting_ensemble_confusion_matrix.png" title="voting ensemble confusion matrix"  width="700">
<br>
Interstingly, Azure allows you to explain your model. In order to retrieve an explanation for your model, you need to first create a compute cluster
<img src="/pictures/model_explanation.png" title="model explanation"  width="700">
<br>
Now, let's deploy the model. You first need to create an inference cluster :
<img src="/pictures/inference_cluster.png" title="inference cluster"  width="700">
<br>
Then you can deploy your model. As you can see, **Application Insights** is so far not enabled :
<img src="/pictures/deploy_model.png" title="deploy model"  width="300">

4. Enable logging
Now that the Best Model is deployed, enable **Application Insights** and retrieve logs. Although this is configurable at deploy time with a check-box, it is useful to be able to run code that will enable it for you. The detailed steps are:
- Create a new virtual environment with Python3 (commands are in file *python_config.txt*)
- Download the **config.json** from the Azure portal and make sure to place it close to **logs.py**
- run **logs.py** in order to enable **Application Insights** and see the logs
<img src="/pictures/logs.png" title="logs"  width="400">

You should now see that Application insights is enabled and a url is provided for it :
<img src="/pictures/application_insights_enabled.png" title="application insights enabled"  width="400">
<br>
That url allows you to monitor your endpoint :
<br>
<img src="/pictures/application_insights.png" title="application insights"  width="400">

5. Swagger Documentation
In this step, we will consume the deployed model using **Swagger**. Azure provides a Swagger JSON file for deployed models. Head to the Endpoints section, and find your deployed model there, it should be the first one on the list.

A few things you need to pay attention to:

- **swagger.sh** will download the latest Swagger container, and it will run it on port 80. If you don't have permissions for port 80 on your computer, update the script to a higher number (above 9000 is a good idea).

- serve.py will start a Python server on port 8000. This script needs to be right next to the downloaded swagger.json file. NOTE: this will not work if swagger.json is not on the same directory.

Here are the steps for that part :

- Download swagger.json : wget http://path/to/swagger.json. The http address is to be found on the enpoint section on the azure portal, under **Swagger URI**.

- Run : **bash swagger.sh**

- Run : **python swagger.py**

- Visit http://localhost:8000/swagger.json You will have a similar result :
<img src="/pictures/swagger.png" title="swagger"  width="400">

6. Consume model endpoints
Once the model is deployed, azure provides us with a **consume.p**y script to interact with the trained model. You simply need to modify the values for variable data inside the script.
<img src="/pictures/consume_script.png" title="consume script"  width="700">

When you use that script, you will obtain results such as :
<br>
<img src="/pictures/consume_example.png" title="consume example"  width="500">

7. Benchmark the endpoint using Apache bench

A benchmark is used to create a baseline or acceptable performance measure. Benchmarking HTTP APIs is used to find the average response time for a deployed model.

One of the most significant metrics is the response time since Azure will timeout if the response times are longer than sixty seconds. Apache Benchmark is an easy and popular tool for benchmarking HTTP services.

- fill in the **endpoint http** and the **secret key**

- Run **benchmark.sh**

You should have similar results :
<br>
<img src="/pictures/benchmark1.png" title="benchmark"  width="500">
<img src="/pictures/benchmark2.png" title="benchmark"  width="500">

8. Create and publish a pipeline

A great way to automate workflows is via Pipelines. Published pipelines allow external services to interact with them so that they can do work more efficiently. For this part of the project, we will use the Jupyter Notebook.

Different steps can have different arguments and parameters :

- Create a Pipeline

The **Pipeline** class is the most common Python SDK when dealing with Pipelines. Aside from accepting a workspace and allowing multiple steps to be passed in, it uses a description that is useful to identify it later.
```
from azureml.pipeline.core import Pipeline

pipeline = Pipeline(
    description="pipeline_with_automlstep",
    workspace=ws, 
    steps=[automl_step])
```

- Using Pipeline Parameters

Pipeline parameters are also available as a class. You configure this class with the various different parameters needed so that they can later be used. In this example, the avg_rate_param is used in the arguments attribute of the PythonScriptStep.

```
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import PipelineParameter

avg_rate_param = PipelineParameter(name="avg_rate", default_value=0.5)
train_step = PythonScriptStep(script_name="train.py",
                              arguments=["--input", avg_rate_param],
                              target=compute_target,
                              source_directory=project_folder)
```

- Scheduling a recurring Pipeline

To schedule a Pipeline, you must use the ScheduleRecurrence class which has the information necessary to set the interval. Once that has been created, it has to be passed into the create() method of the Schedule class as a recurrence value.

```
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule

hourly = ScheduleRecurrence(frequency="Hourly", interval=4)
pipeline_schedule = Schedule.create(ws, name="RecurringSchedule", 
                            description="Trains model every few hours",
                            pipeline_id=pipeline_id, 
                            experiment_name="Recurring_Pipeline_name", 
                            recurrence=hourly)
```

- Batch Inference Pipeline

One of the core responsibilities of a batch inference pipeline is to run in parallel. For this to happen, you must use the ParallelRunConfig class which helps define the configuration needed to run in parallel. Some important aspects of this are the script that will do the work (entry_script), how many failures it should tolerate (error_threshold), and the number of nodes/batches needed to run (mini_batch_size, 5 in this example).

```
from azureml.pipeline.steps import ParallelRunConfig

parallel_run_config = ParallelRunConfig(
    source_directory='scripts',
    entry_script="scoring.py",
    mini_batch_size="5",
    error_threshold=4,
    output_action="append_row",
    environment=batch_env,
    compute_target=aml_target,
    node_count=5)

parallelrun_step = ParallelRunStep(
    name="batch-score",
    parallel_run_config=parallel_run_config,
    inputs=[batch_data_set.as_named_input('batch_data')],
    output=output_dir,
    arguments=[],
    allow_reuse=True
)

# create the pipeline
pipeline = Pipeline(workspace=ws, steps=[parallerun_step])
```

For this part of the project, xe will use the Jupyter Notebook **aml-pipelines-automated-ml-step.ipynb**. As we run though the cells, here are some of the resources programmatically created for us by the SDK :

Compute cluster :
<br>
<img src="/pictures/compute_cluster_sdk.png" title="compute cluster sdk"  width="700">

Pipeline :
<br>
<img src="/pictures/pipeline_sdk.png" title="pipeline sdk"  width="700">

Run Detail :
<br>
<img src="/pictures/run_detail_widget.png" title="run detail"  width="700">

Pipeline Endpoint :
<br>
<img src="/pictures/pipeline_endpoint.png" title="pipeline endpoint"  width="700">

Our Endpoint is now accessible through postman :
<br>
<img src="/pictures/endpoint.png" title="postman endpoint"  width="700">

## Screen Recording
*TODO* Provide a link to a screen recording of the project in action.

## Standout Suggestions
Dear viewer, I would appreciate so much any suggestions you could provide so that I can improve this project. I would like to become better with the Azure tools and MLOps. Thanks!!

# Script to get_logs of all runs and experiments in AML
from authentication import ws
from azureml.pipeline.core import PipelineEndpoint
from authentication import ws
from azureml.core.experiment import Experiment
from azureml.core import Run
import pandas as pd
# Get the published pipeline and trigger a run
#published_pipeline = PublishedPipeline.get(workspace=ws, name="My_Published_Pipeline")
#pipeline_endpoint = PipelineEndpoint.publish(
       # workspace=ws, 
       # name="PipelineEndpointTest",
       # description="Test description Notebook",
       # pipeline=published_pipeline
       # )

# Get pipeline runs from experiment
def experiment_details(sample_exp_name=None):
    collection_dict={}
    experiment_details = sample_exp_name.list(ws)
    for exp in experiment_details:
        get_run_details = exp.get_runs()
        for j,v in enumerate(get_run_details):
            parent_run_details = v.get_details()
            parent_run_status = parent_run_details['status']
            parent_runid = parent_run_details['runId']
            kv = str(exp) + '_' + str(v) + '_' + str(j)
            collection_dict[kv] = {
                    'experiment':str(exp), 
                    'parent_runId': parent_runid,
                    'parent_run_status':parent_run_status
                    }
    return collection_dict

def main():
    exp_name='forecasting_for_energy_prices'
    expObject = Experiment(ws, name=exp_name)
    final_result = experiment_details(sample_exp_name=expObject)
    df = pd.DataFrame(final_result)
    df = df.T
    # Get latest completed pipeline run and the right run ID
    df = df[ df['parent_run_status'] == 'Completed'][:1].reset_index()
    run_id = df.at[0,'parent_runId']
    print(f'Run ID is: {run_id}')

    pipeline_run = Run(experiment=expObject, run_id = run_id)
    print (type(pipeline_run))

    # Publish a completed, latest pipeline
    published_pipeline1 = pipeline_run.publish_pipeline(
            name="My_Published_Pipeline",
            description="My Published Pipeline Description",
            version="1.0"
            )

if __name__ == "__main__":
    main()

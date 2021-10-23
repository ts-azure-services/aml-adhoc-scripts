# Script to get_logs of all runs and experiments in AML
from azureml.core import Workspace, Run
from azureml.core.experiment import Experiment
import pandas as pd

# Get inventory from experiments
def getRunInventory(sample_exp_name=None, workspace=None):
    collection_dict={}
    experiment_details = sample_exp_name.list(workspace)
    for exp in experiment_details:
        get_run_details = exp.get_runs()
        for j,v in enumerate(get_run_details):
            parent_run_details = v.get_details()
            parent_run_status = parent_run_details['status']
            parent_runid = parent_run_details['runId']
            children_runs = v.get_children()

            if children_runs is not None:        
                for k,w in enumerate(children_runs):
                    child_run_details = w.get_details()
                    child_run_status = child_run_details['status']
                    child_runid = child_run_details['runId']                    

                    # All children return a generator, even if there are no sub-children
                    new_children = w.get_children()
                    temp_test = w.get_children()

                    # Test for emptiness on generator
                    proceed = 0
                    try:
                        next_item = next(temp_test)
                        proceed = 1
                    except StopIteration:
                        proceed = 0

                    if proceed == 1:
                        for l,x in enumerate(new_children):
                            sub_children_run_details = x.get_details()
                            sub_children_status = sub_children_run_details['status']
                            sub_childrenrunid = sub_children_run_details['runId']

                            key = str(exp) + '_' + str(v) + '_' + str(j) + '_' + str(w) + '_' + str(k) + '_' + str(x) + '_' + str(l)
                            collection_dict[key] = {
                                'experiment':str(exp), 
                                'parent_runId': parent_runid,
                                'parent_run_status':parent_run_status,
                                'child_runId': child_runid,
                                'child_run_status':child_run_status,
                                'sub_child_runId': sub_childrenrunid,
                                'sub_child_run_status': sub_children_status
                                }
                    else:
                        key = str(exp) + '_' + str(v) + '_' + str(j) + '_' + str(w) + '_' + str(k) #+ '_' + str(x) + '_' + str(l)
                        collection_dict[key] = {
                            'experiment':str(exp), 
                            'parent_runId': parent_runid,
                            'parent_run_status':parent_run_status,
                            'child_runId': child_runid,
                            'child_run_status':child_run_status,
                            # 'sub_child_runId': sub_childrenrunid,
                            # 'sub_child_run_status': sub_children_status
                            }
            else:
                key = str(exp) + '_' + str(v) + '_' + str(j) + '_' + str(w) + '_' + str(k)
                collection_dict[key] = {
                        'experiment':str(exp), 
                        'parent_runId': parent_runid,
                        'parent_run_status':parent_run_status,
                        'child_runId': child_runid,
                        'child_run_status':child_run_status
                        }
    return collection_dict

def main():
    # Get workspace object
    ws = Workspace.from_config()

    # Get inventory from experiments
    exp_object = Experiment(workspace=ws, name='forecasting_for_energy_prices')
    inventory = getRunInventory(
        sample_exp_name=exp_object, 
        workspace=ws)
    df = pd.DataFrame(inventory)
    df = df.T

    # Download structured inventory
    df.to_csv('experiment_inventory.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    main()

## awsbatch ##

This project both python scripts and JSON files used for managing AWS batch service associated with the TOPMed pipeline.

The  JSON files are specified when executing AWS cli for batch services.  For example,

    aws --region us-east-1 batch register-job-definition --cli-input-json ./topmed_jobdef_general.json

The above command creates an AWS batch job definition.  Note it configuration of AWS cli specifies the credentials with the necessary permissions for executing the AWS batch command.

The python scripts execute AWS batch services using AWS bot3.  For example, 

    delete_runnable_jobs.py

The above command deletes all runnable jobs in a queue specified within the script.  Note this type of script is needed because of the limited capabilities to do similar operations via AWS batch console.

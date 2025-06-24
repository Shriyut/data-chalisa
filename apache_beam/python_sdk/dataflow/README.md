#### assurance pipeline commands

```
python3 -m assurance_pipeline --runner DataflowRunner --project us-gcp-ame-con-ff12d-npd-1 --staging_location gs://us-gcp-ame-con-ff12d-npd-1-dataflow-stage/demo_run/staging/ach --template_location gs://us-gcp-ame-con-ff12d-npd-1-dataflow-stage/demo_run/templates/sj_dev2 --region us-east4 --requirements_file requirements.txt --patchingBqTableId abc_framework.patching_audit_log --instanceId tds-design --lookupTableId tds_lookup_test --projectId us-gcp-ame-con-ff12d-npd-1 --patchingTableId tds_patching_test --hoganTableId tds_hg_mock --hoganFieldMappingFilePath gs://shrijha-dev-bkt/hogan_mapping.txt
```

```
gcloud dataflow jobs run assurance-pipeline --gcs-location gs://us-gcp-ame-con-ff12d-npd-1-dataflow-stage/demo_run/templates/sj_dev2 --region us-east4 --max-workers=5 --staging-location gs://us-gcp-ame-con-ff12d-npd-1-dataflow-stage/demo_run/temp/ach --worker-machine-type=n1-standard-4 --parameters patchingBqTableId=abc_framework.patching_audit_log,instanceId=tds-design,lookupTableId=tds_lookup_test,patchingTableId=tds_patching_test,projectId=us-gcp-ame-con-ff12d-npd-1,hoganTableId=tds_hg_mock,hoganFieldMappingFilePath=gs://shrijha-dev-bkt/hogan_mapping.txt
```
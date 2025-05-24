from seqerakit import seqeraplatform
import logging
import ssl
import os

#os.environ['JAVA_TOOL_OPTIONS'] = '-Djavax.net.ssl.trustStore="c:\\Program Files\\Amazon Corretto\\jdk20.0.1_9\\lib\\security\\cacerts"'  

print(os.environ["TOWER_ACCESS_TOKEN"])

logging.basicConfig(level=logging.DEBUG)


# Customise the entries below as required
workspace = "CP_RD/Bioinformatics"  # Name of your Workspace
compute_env = "tf-epa-dev-seqera-poc-compute-8vcpu"  # Name of your Compute Environment

run_name = "hello-world-seqerakit-test1"

tw = seqeraplatform.SeqeraPlatform()
pipeline_run = tw.launch(
    '-Djavax.net.ssl.trustStore=/home/ubuntu/cacerts',
    "--workspace",
    workspace,
    "--compute-env",
    compute_env,
    "--name",
    run_name,
    "--revision",
    "master",
    "--wait",
    "SUBMITTED",
    "https://github.com/nextflow-io/hello"
)
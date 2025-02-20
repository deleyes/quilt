import requests
import json

api_url = "https://seqera-poc.epa.cloud.syngenta.org/api"
endpoint = "/workflow/launch"
api_token = "eyJ0aWQiOiAxfS41OTNkMDQ5NTI5NTViYmRmMmM2NDMwZGM5NTAwNTQxNjdiZmI3MGI5"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

workspaceId = 93998348070498

# payload = {
#     "launch" : {
#         "runName": "ampliseq_testt",
#         "pipeline": "nf_core_ampliseq_test",
#         "paramsText": "{\"outdir\": \"s3://epa-dev-seqera-bucket/outdir/ampliseq_test/20250216\"}",
#     }
# }

# payload = {
#     "launch" : {
#         "runName": "ampliseq_test",
#         "computeEnvId": "2g1sdjWJIHqLd2hJW1dNO7",
#         "pipeline": "https://gitlab.com/syngentagroup/bioinformatics-resistance-analysis-poc/seqera-poc/ampliseq",
#         "workDir": "s3://epa-dev-seqera-bucket/workdir",
#         "revision": "main",
#         "configText": """
#             aws {client {storageEncryption = 'AES256'}}
#             plugins {
#                 id 'nf-quilt'
#             }
#             """,
#         "paramsText": "{\"outdir\": \"quilt+s3://epa-dev-quilt-poc#package=ampliseq/output_root\", \"raise_filter_stacksize\": false}",
#         "preRunScript": """#!/bin/bash 
#             echo "Start"
#             keytool -printcert -rfc -sslserver seqera-poc.epa.cloud.syngenta.org:443  >  /PRIVATE_CERT.pem
#             keytool -import -trustcacerts -cacerts -storepass changeit -noprompt -alias TARGET_ALIAS -file /PRIVATE_CERT.pem
#             cp /PRIVATE_CERT.pem /etc/pki/ca-trust/source/anchors/PRIVATE_CERT.pem
#             update-ca-trust""",
#         "configProfiles": ["test"], 
#     }
# }

payload = {
    "launch" : {
        "runName": "ampliseq_test",
        "computeEnvId": "2g1sdjWJIHqLd2hJW1dNO7",
        "pipeline": "https://gitlab.com/syngentagroup/bioinformatics-resistance-analysis-poc/seqera-poc/ampliseq",
        "workDir": "s3://epa-dev-seqera-bucket/workdir",
        "revision": "main",
        "configText": """
            aws {client {storageEncryption = 'AES256'}}
            """,
        "paramsText": "{\"outdir\": \"s3://epa-dev-seqera-bucket/outdir/ampliseq_test/20250220_module/\", \"raise_filter_stacksize\": false}",
        "preRunScript": """#!/bin/bash 
            echo "Start"
            keytool -printcert -rfc -sslserver seqera-poc.epa.cloud.syngenta.org:443  >  /PRIVATE_CERT.pem
            keytool -import -trustcacerts -cacerts -storepass changeit -noprompt -alias TARGET_ALIAS -file /PRIVATE_CERT.pem
            cp /PRIVATE_CERT.pem /etc/pki/ca-trust/source/anchors/PRIVATE_CERT.pem
            update-ca-trust""",
        "configProfiles": ["test"], 
    }
}

# response = requests.get(f"{api_url}{endpoint}?workspaceId={workspaceId}", headers=headers, verify=False)
# print(response)

response = requests.post(f"{api_url}{endpoint}?workspaceId={workspaceId}", headers=headers, json=payload, verify=False)

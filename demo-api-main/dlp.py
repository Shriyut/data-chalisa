from google.cloud import dlp_v2
import logging, yaml, os, inspect

# Load app_config
config_filename = "config/config.yaml"
with open(config_filename, "r") as config_file:
    app_config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

#GCP_PROJECT = os.environ.get('GCP_PROJECT')
GCP_PROJECT = "us-gcp-ame-con-ff12d-npd-1"
#LOGGING_LEVEL = os.environ.get('GCP_LOGGING_LEVEL')

# Configure the basic logging level per the app_config
#logging.basicConfig(level=int(LOGGING_LEVEL))

# === Helper Function for DLP Config ===
def _get_crypto_replace_ffx_config(info_type_name):
    """Creates the FFX config using KMS wrapped key."""
    custom_alphabet_string = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz -@.+_()"
    return dlp_v2.CryptoReplaceFfxFpeConfig(
        crypto_key=dlp_v2.CryptoKey(
            kms_wrapped=dlp_v2.KmsWrappedCryptoKey(
                wrapped_key=app_config['DEID_WRAPPED_KEY'],
                crypto_key_name=app_config['CRYPTO_KEY_NAME']
            )
        ),
        # Specify the alphabet: NUMERIC, HEXADECIMAL, UPPER_CASE_ALPHA_NUMERIC, or ALPHA_NUMERIC (default)
        # Choose the smallest alphabet that fits your data type for better security.
        # Use COMMON_INFO_TYPE_ALPHABET to let DLP choose based on the infoType.
        # common_alphabet=dlp_v2.CryptoReplaceFfxFpeConfig.FfxCommonNativeAlphabet.HEXADECIMAL,
        custom_alphabet = custom_alphabet_string,
        # Surrogate info types are optional placeholders added to the output
        surrogate_info_type=dlp_v2.InfoType(name=info_type_name)
    )

def _get_primitive_transformation(info_type_name):
    """Gets the primitive transformation using FFX."""
    return dlp_v2.PrimitiveTransformation(
        crypto_replace_ffx_fpe_config=_get_crypto_replace_ffx_config(info_type_name)
    )

def _get_infotype_transformations(dynamic_info_types):
    """Builds the list of transformations for specified INFO_TYPES."""
    return dlp_v2.InfoTypeTransformations(
        transformations=[
            dlp_v2.InfoTypeTransformations.InfoTypeTransformation(
                info_types=[dlp_v2.InfoType(name=info_type_name)],
                primitive_transformation=_get_primitive_transformation(info_type_name),
            )
            for info_type_name in dynamic_info_types
        ]
    )

# Inspect the input text for sensitive data and return findings
def inspect_text(text, dynamic_info_types):
    module = "{}.{}".format(__name__,inspect.currentframe().f_code.co_name)
    response = {
        "status": "success",
        "http_status_code": 200,
        "message": "Input text inspected successfully. Found {} items.",
        "findings": [],
    }
    # dlp = google.cloud.dlp_v2.DlpServiceClient()
    parent = "projects/{}".format(GCP_PROJECT)
    
    info_types=[dlp_v2.InfoType(name=info_type) for info_type in dynamic_info_types]
    inspect_config = {
        "info_types": info_types,
        "include_quote": True
    }

    item = {"value": text}

    # --- Initialize DLP Client ---
    dlp = dlp_v2.DlpServiceClient()

    # Call the API
    dlp_response = dlp.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    result = ""
    if dlp_response.result.findings:
        for finding in dlp_response.result.findings:
            try:
                this_finding = {
                    "quote": finding.quote,
                    "info_type": finding.info_type.name,
                    "likelihood": finding.likelihood,
                }
            except AttributeError:
                pass
            except Exception as e:
                error_message = "Error processing DLP Inspection: {}".format(e)
                logging.error("{} | {}".format(module,error_message))
                response['status'] = "error"
                response['message'] = error_message
                response['http_status_code'] = 500
                return response

            response['findings'].append(this_finding)
    
    # All good. Return response
    response['message'] = response["message"].format(len(response['findings']))
    logging.info("{} | {}".format(module,response['message']))
    return response

# De-identify the input text based on the specified action
def deidentify_data(input_data, dynamic_info_types):
    module = "{}.{}".format(__name__,inspect.currentframe().f_code.co_name)
    response = {
        "status": "success",
        "http_status_code": 200,
        "message": "Input text de-identified successfully.",
        "deidentified_text": "",
    }
    try:
        # Initialize DLP Client
        dlp = dlp_v2.DlpServiceClient()
        
        # DLP works on text content, so serialize the JSON input
        item = dlp_v2.ContentItem(value=input_data)

        # Construct the Inspect and Deidentify Configs
        
        inspect_config = dlp_v2.InspectConfig(
            info_types=[dlp_v2.InfoType(name=info_type) for info_type in dynamic_info_types],
            custom_info_types=[
            dlp_v2.CustomInfoType(
                info_type=dlp_v2.InfoType(name=info_type_name),
                surrogate_type=dlp_v2.CustomInfoType.SurrogateType()
            )
            for info_type_name in dynamic_info_types
            ]
        )
        deidentify_config = dlp_v2.DeidentifyConfig(
            info_type_transformations=_get_infotype_transformations(dynamic_info_types),
            transformation_error_handling=dlp_v2.TransformationErrorHandling(
                leave_untransformed=dlp_v2.TransformationErrorHandling.LeaveUntransformed()
            )
        )

        # Call DLP API
        parent = "projects/{}".format(GCP_PROJECT)  
        dlp_response = dlp.deidentify_content(
            request={
                "parent": parent,
                "deidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": item,
            }
        )
        
        # Deserialize the result back into JSON
        response['deidentified_text'] = dlp_response.item.value
    except Exception as e:
        error_message = "Unexpected error during de-identification: {}".format(e)
        logging.error(error_message)
        response['message'] = error_message
    
    # All good. Return response
    logging.info("{} | De-Identified Data: {}".format(module, response['deidentified_text']))
    logging.info("{} | {}".format(module,response['message']))
    return response


# Re-identify the input text based on the specified action
def reidentify_data(input_data, dynamic_info_types):
    module = "{}.{}".format(__name__, inspect.currentframe().f_code.co_name)
    response = {
        "status": "success",
        "http_status_code": 200,
        "message": "Input text re-identified successfully.",
        "reidentified_text": "",
    }
    try:
        # Initialize DLP Client
        dlp = dlp_v2.DlpServiceClient()
        
        # DLP works on text content, so serialize the JSON input
        item = dlp_v2.ContentItem(value=input_data)

        # Construct the Inspect and Reidentify Configs
        inspect_config = dlp_v2.InspectConfig(
            info_types=[dlp_v2.InfoType(name=info_type) for info_type in dynamic_info_types],
            custom_info_types=[
            dlp_v2.CustomInfoType(
                info_type=dlp_v2.InfoType(name=info_type_name),
                surrogate_type=dlp_v2.CustomInfoType.SurrogateType()
            )
            for info_type_name in dynamic_info_types
            ]
        )
        deidentify_config = dlp_v2.DeidentifyConfig(
            info_type_transformations=_get_infotype_transformations(dynamic_info_types),
            transformation_error_handling=dlp_v2.TransformationErrorHandling(
                leave_untransformed=dlp_v2.TransformationErrorHandling.LeaveUntransformed()
            )
        )

        # Call DLP API
        parent = "projects/{}".format(GCP_PROJECT)


        dlp_response = dlp.reidentify_content(
            request={
                "parent": parent,
                "reidentify_config": deidentify_config,
                "inspect_config": inspect_config,
                "item": item,
            }
        )

        # Deserialize the result back into JSON
        response['reidentified_text'] = dlp_response.item.value
    except Exception as e:
        error_message = "Unexpected error during re-identification: {}".format(e)
        logging.error(error_message)
        response['message'] = error_message
    
    # All good. Return response
    logging.info("{} | De-Identified Data: {}".format(module, input_data))
    logging.info("{} | {}".format(module, response['message']))
    return response
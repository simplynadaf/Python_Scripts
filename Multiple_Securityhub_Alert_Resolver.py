import boto3

def resolve_security_hub_alert_by_titles(alert_titles, max_results=5):
    securityhub = boto3.client('securityhub')

    for alert_title in alert_titles:
        next_token = None
        while True:
            # Include the NextToken parameter only if it is not None
            params = {'Filters': {'Title': [{'Value': alert_title, 'Comparison': 'EQUALS'}]}, 'MaxResults': max_results}
            if next_token:
                params['NextToken'] = next_token

            response = securityhub.get_findings(**params)

            # Check if there are findings in the response
            if 'Findings' in response and response['Findings']:
                for alert in response['Findings']:
                    # Update the workflow status to RESOLVED for each alert
                    securityhub.batch_update_findings(
                        FindingIdentifiers=[
                            {'Id': alert['Id'], 'ProductArn': alert['ProductArn']}
                        ],
                        Workflow={'Status': 'RESOLVED'}
                    )
                    print(f"Resolved alert with Title: {alert_title}, Id: {alert['Id']}")

                # Check if there are more findings to process
                next_token = response.get('NextToken')
                if not next_token:
                    break
            else:
                print(f"No findings found for alert with Title: {alert_title}")
                break

def lambda_handler(event, context):
    # Specify the alert titles
    alert_titles = ['AWSControlTower_AWS-GR_EC2_INSTANCE_NO_PUBLIC_IP', 'Another_Alert_Title']

    # Resolve Security Hub alerts by titles in batches
    resolve_security_hub_alert_by_titles(alert_titles, max_results=5)

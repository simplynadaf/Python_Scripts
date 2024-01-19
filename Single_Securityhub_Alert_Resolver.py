import boto3

def resolve_security_hub_alert_by_title(alert_title):
    securityhub = boto3.client('securityhub')

    # Get findings to get details about the alerts
    response = securityhub.get_findings(
        Filters={
            'Title': [{'Value': alert_title, 'Comparison': 'EQUALS'}]
        }
    )

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
    else:
        print("No findings found for alert with Title:", alert_title)

def lambda_handler(event, context):
    # Specify the alert title
    alert_title = 'AWSControlTower_AWS-GR_EC2_INSTANCE_NO_PUBLIC_IP'

    # Resolve Security Hub alerts by title
    resolve_security_hub_alert_by_title(alert_title)


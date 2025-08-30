# Cloud Incidence Response Bot
This project implements an automated incidence and response pipeline for GuardDuty findings.
When GuardDuty flags a compromised EC2 instance, 
1. An EventBridge rule captures the finding
2. A lambda function is triggered and it
    - logs the finding and extracts the instance ID
    - Tags the instance with 'Compromised=True' and DetectedAt=<timestamp>`
    - Replaces the instances security group with a quarantined SG with no inbound access


# architectural description
- GuardDuty detects suspicious activity
- EventBridge routes finding to Lambda
- Lambda tags and isolated instance by swapping SG
- Compromised EC2 instance is quarantined automatically

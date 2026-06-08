# Conductor Pipeline - Bayer/Monsanto

**Enterprise ETL/ELT Platform for Global Salesforce Consolidation**

I played a key role in the design and implementation of the Conductor Pipeline, a scalable hybrid ETL platform that supported the migration and consolidation of data from 13 regional Salesforce organizations into a single global instance.

## Project Overview

Multiple upstream teams extracted capability-specific data from regional Salesforce orgs and published it to Kafka streams. The Conductor Pipeline served as the critical downstream bridge: ingesting raw data from Kafka, performing complex transformations in PostgreSQL, and reliably loading it into the target global Salesforce organization using CapStorm while maintaining full traceability.

## Technical Stack
- **Salesforce**: Salesforce APIs, Heroku Connect, CapStorm
- **Orchestration**: Python, Bash, Linux/CRON
- **Databases**: PostgreSQL (AWS RDS + Heroku)
- **Messaging**: Kafka
- **Cloud**: AWS (EC2, S3, Athena, RDS, IAM)
- **Other**: HashiCorp Vault, DynamoDB (config), Jira

## My Key Contributions
- Designed multi-stage PostgreSQL schemas (Stage → Current → Load) with triggers and custom functions for data enrichment, ID mapping, and validation.
- Built a metadata-driven Python orchestrator to manage complex, multi-step workflows with parallel processing.
- Developed reusable Python toolkit for encryption, credential management, auditing, and ID transformation logic.
- Handled performance tuning, error handling, auditing, and long-term archiving to S3/Athena.
- Collaborated across Java, Salesforce, and business teams in an agile environment.

## Challenges Overcome
- Complex insert + update logic across long-running parallel operations between regional and global orgs.
- Salesforce API throttling using multi-threading and multiple integration accounts.
- Maintaining data consistency and full traceability for millions of records.

This project combined deep data architecture, PostgreSQL mastery, Python automation, and cross-team coordination at enterprise scale.

---

Detailed technical write-up available upon request.

---


[Back to Projects](../README.md#featured-projects) | [Back to Home](../README.md)

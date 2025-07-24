# Sample Java Application

This directory simulates a Java project that uses the reusable workflow to build and push a Docker image to Amazon ECR.

The workflow located in `.github/workflows/docker-deploy.yml` calls the reusable workflow with two build arguments: `JAR_NAME` and `JAVA_OPTS`.

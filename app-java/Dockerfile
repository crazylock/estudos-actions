# Simple Java application image
FROM eclipse-temurin:17-jre as runtime
WORKDIR /app
COPY target/app.jar /app/app.jar
ENTRYPOINT ["java","-jar","/app/app.jar"]

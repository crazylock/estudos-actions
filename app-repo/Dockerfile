# Etapa de build
FROM eclipse-temurin:17-jdk as build

WORKDIR /app
COPY Main.java .

# Compilar
RUN javac Main.java

# Etapa final
FROM amazoncorretto:17

WORKDIR /app
COPY --from=build /app/Main.class .

CMD ["java", "Main"]

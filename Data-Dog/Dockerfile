# Use a lightweight base image with Java
FROM openjdk:17-slim

# Set working directory
WORKDIR /app

# Copy your Java source code
COPY App.java .

# Compile the Java app
RUN javac App.java

# Copy entrypoint script that logs system info
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# --- Datadog integration labels ---
LABEL "com.datadoghq.ad.check_names"='["http_check"]'
LABEL "com.datadoghq.ad.init_configs"='[{}]'
LABEL "com.datadoghq.ad.instances"='[{"name": "java-app", "url": "http://%%host%%:8080"}]'
LABEL "com.datadoghq.ad.logs"='[{"source": "java", "service": "java-app"}]'

# Run custom entrypoint that prints OS and Java version
CMD ["./entrypoint.sh"]

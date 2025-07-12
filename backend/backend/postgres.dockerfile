FROM postgres:17.5-alpine

# Set environment variables
ENV POSTGRES_DB=backend
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

EXPOSE 5432
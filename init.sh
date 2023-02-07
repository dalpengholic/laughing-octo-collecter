#!/bin/sh

# Start the services defined in the docker-compose.yml file in detached mode (background)
# and exit if any service's container exits.
docker-compose up --abort-on-container-exit

# Check the exit status of the previous command
if [ $? -eq 0 ]; then
  # If the exit status is 0, it means that the web-scraping container has successfully completed and exited with code 0.
  echo "The web-scraping container exited with code 0, stopping standalone-chrome"
  
  docker-compose down

else
  # If the exit status is not 0, it means that the web-scraping container has encountered an error or was interrupted before it completed.
  echo "The web-scraping container did not exit with code 0, keeping standalone-chrome running"

  docker-compose down
fi

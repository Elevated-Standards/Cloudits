#!/bin/bash

# Get the current year
YEAR=$(date +%Y)

# Get the current month name
MONTH=$(date +%B)

# Get the current day of the month
DAY=$(date +%d)

# Calculate the start date (31 days ago) in ISO 8601 format
START_DATE=$(date -u -d "31 days ago" +"%Y-%m-%dT%H:%M:%SZ")

# Get the current date and time in ISO 8601 format
END_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Print the values (optional)
echo "Year: $YEAR"
echo "Month: $MONTH"
echo "Day: $DAY"
echo "Start Date: $START_DATE"
echo "End Date: $END_DATE"

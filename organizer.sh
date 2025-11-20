#!/bin/bash
# organizer.sh

# Create archive directory if it doesn't exist
if [ ! -d "archive" ]; then
    mkdir archive
    echo "Created archive directory"
fi

# Create or initialize log file
log_file="organizer.log"
echo "=== Archive operation started at $(date) ===" >> "$log_file"

# Find all CSV files in current directory
for csv_file in *.csv; do
    # Skip if no CSV files found
    if [ "$csv_file" = "*.csv" ]; then
        echo "No CSV files found to archive"
        break
    fi
    
    # Generate timestamp
    timestamp=$(date +"%Y%m%d-%H%M%S")
    
    # Create new filename with timestamp
    base_name="${csv_file%.*}"
    extension="${csv_file##*.}"
    new_filename="${base_name}-${timestamp}.${extension}"
    
    # Log the action
    echo "Archiving: $csv_file -> archive/$new_filename" >> "$log_file"
    
    # Log file content
    echo "Content of $csv_file:" >> "$log_file"
    cat "$csv_file" >> "$log_file"
    echo "--- End of $csv_file content ---" >> "$log_file"
    
    # Move and rename the file
    mv "$csv_file" "archive/$new_filename"
    
    echo "Successfully archived: $csv_file"
done

echo "=== Archive operation completed at $(date) ===" >> "$log_file"
echo ""
echo "All CSV files have been archived to the 'archive' directory"
echo "Details logged to: $log_file"

archives=("scpe" "csis")

max_attempts=3
wait_time=3

rm -rf /common
mkdir /common
mkdir /common/processed_ttl

for archive in "${archives[@]}"; do
    mkdir /home/output_ttl_files/$archive
    for dir in "/input_pdf_files/$archive"/*; do
        if [ -d "$dir" ]; then
            mkdir /home/output_ttl_files/$archive/$(basename "$dir")
            for file in "$dir"/*; do
                if [ -f "$file" ]; then
                    cp "$file" /common/$(basename "$file" .pdf).pdf
                    attempts=0
                    while [ $attempts -lt $max_attempts ]; do
                        bash ./run.sh /common/$(basename "$file" .pdf).pdf
                        cp /common/processed_ttl/$(basename "$file" .pdf | tr '[:upper:]' '[:lower:]').ttl /home/output_ttl_files/$archive/$(basename "$dir")/$(basename "$file" .pdf).ttl
                        if [ $? -eq 0 ]; then
                            break
                        else
                            echo "Attempt $((attempts + 1)) failed. Retrying in $wait_time seconds..."
                            sleep $wait_time
                            attempts=$((attempts + 1))
                        fi
                    done
                    if [ $attempts -ge $max_attempts ]; then
                        echo "Scraping for file $file failed after $max_attempts attempts. Skipping it."
                    fi
                fi
            done
        fi
    done
done

python3 merge_ttl_files.py

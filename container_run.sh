archives=("scpe" "csis")

rm -rf /common
mkdir /common
mkdir /common/processed_ttl

for archive in "${archives[@]}"; do
    archive_dir=/home/output_ttl_files/$archive
    if [ ! -d "$archive_dir" ]; then
        mkdir $archive_dir
    fi
    for dir in "/input_pdf_files/$archive"/*; do
        if [ -d "$dir" ]; then
            volume_dir=/home/output_ttl_files/$archive/$(basename "$dir")
            if [ ! -d "$volume_dir" ]; then
                mkdir $volume_dir
            fi
            for file in "$dir"/*; do
                if [ -f "$file" ]; then
                    cp "$file" /common/$(basename "$file" .pdf).pdf
                    bash ./run.sh /common/$(basename "$file" .pdf).pdf
                    final_basename=$(basename "$file" .pdf | tr '[:upper:]' '[:lower:]' | tr -d '_')
                    if [ -e "/common/processed_ttl/$final_basename.ttl" ]; then
                        cp /common/processed_ttl/$final_basename.ttl /home/output_ttl_files/$archive/$(basename "$dir")/$(basename "$file" .pdf).ttl
                    else
                        echo "Grobid failed with scraping file, information from it will be skipped"
                    fi

                fi
            done
        fi
    done
done

python3 merge_ttl_files.py

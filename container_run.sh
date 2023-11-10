archives=("scpe" "csis")

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
                    bash ./run.sh /common/$(basename "$file" .pdf).pdf
                    cp /common/processed_ttl/$(basename "$file" .pdf | tr '[:upper:]' '[:lower:]').ttl /home/output_ttl_files/$archive/$(basename "$dir")/$(basename "$file" .pdf).ttl
                fi
            done
        fi
    done
done

python3 merge_ttl_files.py

#!/usr/bin/env bash
# This script is used to bootstrap the database with data.

# DB_NAME="plateup"
# DB_USER="tonyyao"

api_url="https://plateupseeds.com"

large_seeds=$(ls -1 /Users/tonyyao/workspace/plateup-detect-default-seed/seeds_sorted/large | sed "s/.jpg//g")
medium_seeds=$(ls -1 /Users/tonyyao/workspace/plateup-detect-default-seed/seeds_sorted/medium | sed "s/.jpg//g")
small_seeds=$(ls -1 /Users/tonyyao/workspace/plateup-detect-default-seed/seeds_sorted/small | sed "s/.jpg//g")
default_seeds=$(ls -1 /Users/tonyyao/workspace/plateup-detect-default-seed/seeds_sorted/default | sed "s/.jpg//g")

create_all_large_seeds() {
    echo "creating large seeds"
    for seed in $large_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "large"}' \
        ${api_url}/seeds/
    done
    echo
}
create_all_medium_seeds() {
    echo "creating large seeds"
    for seed in $medium_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "medium"}' \
        ${api_url}/seeds/
    done
    echo
}
create_all_small_seeds() {
    echo "creating large seeds"
    for seed in $small_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "small"}' \
        ${api_url}/seeds/
    done
    echo
}
create_all_default_seeds() {
    echo "creating large seeds"
    for seed in $default_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "default"}' \
        ${api_url}/seeds/
    done
    echo
}


main() {
    create_all_large_seeds
    create_all_medium_seeds
    create_all_small_seeds
    create_all_default_seeds
}

main

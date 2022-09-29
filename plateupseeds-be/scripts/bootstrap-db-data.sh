#!/usr/bin/env bash
# This script is used to bootstrap the database with data.

# DB_NAME="plateup"
# DB_USER="tonyyao"

create_user() {
    echo "Creating users..."
    for _ in {1..10}; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{}' \
        http://localhost:8000/users/
    done
    echo
}

create_seeds() {
    echo "Creating seed..."
    large_seeds="134A2LUQ 1GXWKYT5 1PZAXGMU"
    for seed in $large_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "large"}' \
        http://localhost:8000/seeds/
    done
    medium_seeds="13PHVLPQ 143FHP45 1DGCJH6T"
    for seed in $medium_seeds; do
        curl -s -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "medium"}' \
        http://localhost:8000/seeds/
    done
    small_seeds="11ADKUG2 11D481H5 14FQI5P1"
    for seed in $small_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "small"}' \
        http://localhost:8000/seeds/
    done
    default_seeds="12R532YO 14MERAVX 15K2YDNS"
    for seed in $default_seeds; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"seed_name": "'$seed'", "seed_type": "default"}' \
        http://localhost:8000/seeds/
    done
    echo
}

create_likes() {
    # user 1 likes seeds 1, 2, 3, 4, 5, 6
    user_id="1"
    seed_ids="1 2 3 4 5 6"
    echo "Creating likes for user 1..."
    for seed_id in $seed_ids; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"user_id": "'$user_id'", "seed_id": "'$seed_id'", "is_like": true}' \
        http://localhost:8000/likes/
    done
    echo

    # user 2 likes seeds 1, 2, 3
    user_id="2"
    seed_ids="1 2 3"
    echo "Creating likes for user 2..."
    for seed_id in $seed_ids; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"user_id": "'$user_id'", "seed_id": "'$seed_id'", "is_like": "true"}' \
        http://localhost:8000/likes/
    done

    # user 3 dislikes seeds 1, 2, 3, 4, 5, 6
    user_id="3"
    seed_ids="1 2 3 4 5 6"
    echo "Creating dislikes for user 3..."
    for seed_id in $seed_ids; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"user_id": "'$user_id'", "seed_id": "'$seed_id'", "is_like": "false"}' \
        http://localhost:8000/likes/
    done

    # user 4 dislikes seeds 1, 2, 3
    user_id="4"
    seed_ids="1 2 3"
    echo "Creating dislikes for user 4..."
    for seed_id in $seed_ids; do
        curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"user_id": "'$user_id'", "seed_id": "'$seed_id'", "is_like": "false"}' \
        http://localhost:8000/likes/
    done
}

main() {
    create_user
    create_seeds
    create_likes
}

main

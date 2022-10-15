function getSeedUrl(seedName: string, seedType: string) {
    return `${MEDIA_URL}/${seedType}/${seedName}.jpg`;
}
function getSeedUrlHighQuality(seedName: string) {
    return `${MEDIA_URL}/high_quality/${seedName}.jpg`;
}
function toggle(isLikedButton: boolean) {
    if (isLikedButton && this.userLiked) {
        this.deleteLike();
    } else if (!isLikedButton && this.userDisliked) {
        this.deleteLike();
    } else {
        this.updateLike(isLikedButton);
    }
}
function deleteLike() {
    fetch(`${API_URL}/likes/`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: this.userId,
            seed_id: this.seedId,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            this.fetchLikes();
        });
}
function updateLike(isLikedButton: boolean) {
    fetch(`${API_URL}/likes/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            user_id: this.userId,
            seed_id: this.seedId,
            is_like: isLikedButton,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            this.fetchLikes();
        });
}

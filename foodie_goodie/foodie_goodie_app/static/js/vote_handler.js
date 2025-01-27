function vote(postId, voteType) {
    fetch("/vote-post/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: new URLSearchParams({
            'post_id': postId,
            'vote_type': voteType
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.new_vote_count !== undefined) {
            document.getElementById("vote-count-" + postId).innerText = data.new_vote_count;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

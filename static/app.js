let image = document.getElementById(`c`);

let currentUsername = initialUsername;

let sendRating = (rating) => {
    $.get(`/rate/${currentUsername}/${rating}/`, function(data, status){
        $.getJSON('/new/', { get_param: 'url' }, function(data) {
            let response = data["url"];
            if (response === "empty") {
                $("#current-img").remove();
                $("#real").remove();
                $("#fake").remove();
                $("#alert").append(`There are no more images to rate!`)
            } else {
                $("#current-img").attr("src", response);
                let username = response.substring(13);
                username = username.substring(0, username.length - 5);
                currentUsername = username;
            }
        });
    });
};

$("#real").click(function() {
    sendRating(1);
});

$("#fake").click(function() {
    sendRating(0);
});

$(document).keypress(function(event) {
    if (event.charCode == 97) {
        sendRating(0);
    } else if (event.charCode == 108) {
        sendRating(1);
    }
});


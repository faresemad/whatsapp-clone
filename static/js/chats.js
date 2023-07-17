document.querySelector('#roomInput').focus();
document.querySelector('#roomInput').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        // check if room name is written or not
        if (document.querySelector('#roomInput').value.length < 1) {
            alert("Please enter a room name");
            return false;
        }
        document.querySelector('#roomConnect').click();
    }
};

document.querySelector('#roomConnect').onclick = function (e) {
    if (document.querySelector('#roomInput').value.length < 1) {
        alert("Please enter a room name");
        return false;
    }
    var roomName = document.querySelector('#roomInput').value;
    window.location.pathname = '/' + roomName + '/';
};

// on double click of room name, redirect to room
document.querySelector("#roomSelect").ondblclick = function () {
    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    window.location.pathname = "/" + roomName + "/";
}
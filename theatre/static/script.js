
function hideFlashMessage() {
    if(document.getElementById("flash") != null)
        document.getElementById("flash").style.display = "none";
}
setTimeout(function() {hideFlashMessage();}, 5000);
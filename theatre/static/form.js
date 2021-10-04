function categoryChange(){
    var category = document.getElementById("category").value;

}

function showhide(){  
    var div = document.getElementById("spinner-div");
    var title = document.getElementById("title").value;
    var year = document.getElementById("year").value;
    var file_path = document.getElementById("path").value;
    var poster_path = document.getElementById("poster_path").value;
    if( title == "" || year == "" || file_path == "" || poster_path == ""){
        return;
    }
    if (div.style.display != "none") 
    {  
        div.style.display = "none";  
    }  
    else
    {  
        div.style.display = "block";  
    }  
}

function deleteEpisode(e){
    e.parentNode.parentNode.removeChild(e.parentNode);
    total_episode--;
    console.log(total_episode);
    if(total_episode > 1)
    document.getElementById("movie-label-"+total_episode)
        .insertAdjacentHTML('afterend', '<img id="remove_episode" src="/static/cancel.png"\
        onclick="deleteEpisode(this)" style="cursor: pointer; margin-left: 2rem;"/>');
}

total_episode = 0;

function toggleAddButton(val){
    document.getElementById("add-episode").style.display = val;
}

function toggleCategory(){
    var category = document.getElementById("category").value;
    if(category == "series"){
        toggleAddButton("block");
        var tmp = document.getElementById("input-container");
        tmp.parentNode.removeChild(tmp);
        addEpisode();
    }
    else {
        total_episode = 0;
        toggleAddButton("none");
        var div = document.getElementById("path-list");
        var n = div.childNodes.length;
        while(n>2){
            div.removeChild(div.firstChild);
            n--;
        }
        div.insertAdjacentHTML('afterbegin', '<div id="input-container" class="mb-4">\
            <label for="path" id="movie-label">Select Video File</label>\
            <input class="form-control-file" id="path" name="path" required="" type="file">\
            </div>')
    }
}

function addEpisode(){
    var form_group = document.getElementById("add-episode");
    var e = document.getElementById("remove_episode");
    if(e != null ) e.parentNode.removeChild(e);
    total_episode++;
    var html = '<div id="input-container-' + total_episode + '" class="mb-4">\
    <label for="path" id="movie-label-' + total_episode +'">Select Episode ' + total_episode + '</label>';
    if(total_episode > 1)
        html += '<img id="remove_episode" src="/static/cancel.png"\
     onclick="deleteEpisode(this)" style="cursor: pointer; margin-left: 2rem;"/>';

    html += '<input class="form-control-file" id="path" name="path" required="" type="file"></div>';
    form_group.insertAdjacentHTML('beforebegin', html);
}
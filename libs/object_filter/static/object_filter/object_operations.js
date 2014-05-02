$(document).ready(function () {
    $('#scrolling-pane').on("dblclick", ".element-root", function(event){
        //console.log("dblclicked", event, $(event.currentTarget).attr("full_path"));
        $.getJSON("/ui_framework/start?full_path="+encodeURI($(event.currentTarget).attr("full_path")),
            function(data){});
    });
    $("#obj-pane").on("click", "#delButton", function(e){
        $.getJSON("/objsys/do_json_operation/?cmd=rm&ufs_url="+encodeURI($(this).parents(".element-root").attr("ufs_url")));
    });
    $("#obj-pane").on("click", "#delDirectories", function(e){
        $.getJSON("/objsys/rm_objs_for_path/?ufs_url="+encodeURI($(this).parents(".element-root").attr("ufs_url")));
    });

    $("#obj-pane").on("mouseenter", ".element-root", function(e){
        //The this pointer is pointing to ".element-root"
        $("#toolBar").remove();
        $(this).append('<div id="toolBar" class="tool-bar-class">' +
                            '<p id="delButton">delete</p>' +
                            '<p id="delDirectories">delete dir</p>' +
                            '<p id="open-dir-button">Open dir</p>' +
                        '</div>');
        //console.log("created tool bar for ", e.target);
    });
    $("#obj-pane").on("click", "#open-dir-button", function(event){
        var fullPath = $(this).parents(".element-root").attr("full_path");
        var pathEnd = fullPath.lastIndexOf("/");
        var path = fullPath.substr(0, pathEnd);
        $.getJSON("/ui_framework/start?"+encodeURI(path), function(data){});
    });
});

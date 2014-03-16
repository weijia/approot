
function genHtml(data)
{
    //console.log(data);
    var resHtml = ""
    $.each(data.objects, function(key, value)
    {
        var objName = "";
        if(value.object_name)
        {
            objName = value.object_name;
        }
        else
        {
            objName = value.full_path.substring(value.full_path.lastIndexOf("/")+1);
        }
        var desc_content
        if ((null!=value.descriptions)&&(value.descriptions.length>0))
            desc_content = value.descriptions[0].content.replace(/"/g,'');
        else
            desc_content = "";
        resHtml += String.format('<div class="element-root" style="position:relative" ufs_url="{0}" full_path="{1}">'+
                    '<img class="element-thumb" src="{6}?target={5}" title="{0} {1} {4}"/>' +
                    '<ul class="tag-list tag-list-no-autocomplete">{2}</ul>{3}</div>',
                    value.ufs_url, value.full_path, '<li>'+value.tags.join('</li><li>')+'</li>',
                    objName, desc_content,
                    encodeURI(value.full_path),
                    gThumbServerBase
        );
    });
    if(null != data.meta.next){
        $("#next-page-pane").html(String.format('<a href="{0}">Next Page</a>', data.meta.next));
    }
    else{
        $("#next-page-pane").html(String.format('<a href="{0}">Next Page</a>', data.meta.next));
    }
    $("#obj-pane").append(resHtml);
    //$('.tag-list-no-autocomplete').tagit().removeClass('tag-list-no-autocomplete');
    $('.tag-list-no-autocomplete').tagit({
                                            autocomplete:{ appendTo: "#obj-pane",
                                                    source: function( request, response ) {
                                                            $.getJSON("/objsys/get_tags/").success(function( data ) {
                                                                    //console.log(data);
                                                                    var res = new Array();
                                                                    if(0 == data.length){
                                                                        return [];
                                                                    }

                                                                    for(var i=0; i< data.length; i++)
                                                                    {
                                                                        res.push({label: data[i], value: data[i]});
                                                                    }
                                                                    return response(res);
                                                                });

                                                    }
                                            },
                                            beforeTagRemoved: function(event, ui){
                                                //console.log(ui, ui.tag);
                                                //ui.tag.parents('.element-root').attr('ufs_url')
                                                var req = $.getJSON('/objsys/remove_tag/?ufs_url='+encodeURIComponent(ui.tag.parents('.element-root').attr('ufs_url'))+
                                                                    '&tag='+ui.tagLabel);
                                            },
                                            beforeTagAdded: function(event, ui){
                                                if(ui.duringInitialization) return;
                                                var req = $.getJSON('/objsys/add_tag/?ufs_url='+encodeURIComponent($(this).parents('.element-root').attr('ufs_url'))+
                                                                    '&tag='+ui.tagLabel);
                                            }
                                        })
        .removeClass('tag-list-no-autocomplete');
}

$(document).ready(function() {



    var parent = null;
    //console.log('-----------------', $('#content').length);
    if(0 == $('#content').length){
        console.log('using window');
        parent = $(window);
    }
    else
    {
        parent = $('#content').parent();
    }
    parent.infinitescroll({
        // other options
        dataType: 'json',
        //debug: true,
        binder: parent,
        pathParse: function(){return [];},
        path: function(){var href = $("#next-page-pane a").attr("href"); return href;},
        appendCallback: false,
        navSelector  : "#navigation-pane",            
                       // selector for the paged navigation (it will be hidden)
        nextSelector : "#next-page-pane a:first",    
                       // selector for the NEXT link (to page 2)
        //itemSelector : "#content div.post"          
                       // selector for all items you'll retrieve
        contentSelector: '#obj-pane'
        }, function(json, opts) {
            console.log("loading new page");
            console.log(json);
            // Get current page
            var page = opts.state.currPage; 
            // Do something with JSON data, create DOM elements, etc ..
            genHtml(json);
        });
    /*
    $('#content').parent().scroll(function(e){$("#main-container").trigger("scrolling", e);});
    $(window).scroll(function(e){$("#main-container").trigger("scrolling", e);});
    $("#main-container").bind("scrolling", function(e, originalEvent) {
        //console.log("scrolling", e, originalEvent);
        var target = $(originalEvent.currentTarget);
        //console.log(target, target.parent());
        //console.log(target.scrollTop(), target.height(), target.scrollTop() + target.height() + 200, $('#main-container').height());

        if(target.scrollTop() + target.height() + 200 > $('#main-container').height()) {
            //console.log($(window).scrollTop() + $(window).height(), $(document).height());
            //var new_div = '<div class="new_block"></div>';
            //$('.main_content').append(new_div.load('/path/to/script.php'));
            var href = $("#next-page-pane a").attr("href");
            if(href != null)
            {
                console.log(href);
                $.ajax({
                    url: href,
                    dataType: "json",
                    success: function( data ) {
                        genHtml(data);
                    }
                });
            }
        }
    });*/
    var url = "/objsys/api/ufsobj/ufsobj/?";
    if($("#query-base").length > 0)
    {
        url = $("#query-base").val();
    }
    console.log("loading url:",url);
    $.ajax({
            url: url,
            dataType: "json",
            data: {
                        tag: $("#tag").val(),
                        format: "json"
                  },
            success: function( data ) {
                genHtml(data);
            }
        });
    
});

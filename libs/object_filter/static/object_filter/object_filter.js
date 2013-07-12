$(document).ready(function() {



    $('#scrolling-pane').on("dblclick", ".element-root", function(event){
        console.log("dblclicked", event, $(event.currentTarget).attr("full_path"));
        
        $.getJSON("/ui_framework/start?"+$(event.currentTarget).attr("full_path"), function(data){});
    });

    $("#detail-view-button").button().click(
                                            function () {
                                                            $("#obj-pane").removeClass("thumb-view");
                                                            $("#obj-pane").addClass("detailed-view");
                                                        }
    );


    function genHtml(data)
    {
        console.log(data);
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
            resHtml += String.format('<div class="element-root" ufs_url="{0}" full_path="{1}">'+
                        '<img class="element-thumb" src="/thumb/?target={5}" title="{0} {1} {4}"/><ul class="tag-list tag-list-no-autocomplete">{2}</ul>{3}</div>',
                        value.ufs_url, value.full_path, '<li>'+value.tags.join('</li><li>')+'</li>', 
                        objName, value.description.replace(/"/g,''),
                        encodeURI(value.full_path));
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
                                                    var req = $.getJSON('/objsys/add_tag/?ufs_url='+encodeURIComponent($(this).parents('.element-root').attr('ufs_url'))+
                                                                        '&tag='+ui.tagLabel);
                                                }
                                            })
            .removeClass('tag-list-no-autocomplete');
    }
    $('#full-path, #ufs-url, #tag').autocomplete({
        source: function( request, response ) {
            //console.log(request, response, this);
            //console.log(this.element[0].id);
            //var query = this.element[0].id.replace("-", "_")+"__contains";
            $("#obj-pane").html("");

            if(this.element[0].id == "full-path"){
                var queryData = {
                        full_path__iendswith: request.term,
                        format: "json"
                    };
            }
            else if(this.element[0].id == "ufs-url") {
                var queryData = {
                        ufs_url__contains: request.term,
                        format: "json"
                    };
            }
            else{
                var queryData = {
                        tag: request.term,
                        format: "json"
                    };
            }
            var url = "/objsys/api/ufsobj/ufsobj/?";
            if($("#query-base").length > 0)
            {
                url = $("#query-base").val();
            }
            $.ajax({
                    url: url,
                    dataType: "json",
                    data: queryData,
                    success: function( data ) {
                        genHtml(data);
                    }
                });
                

        }
    });//End of $('path-contains').autocomplete({
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

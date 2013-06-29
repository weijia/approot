;(function($) {
    //////////////////////////////
    //Internal functions
    //////////////////////////////


    var methods = {
        init : function( settings ) {
            return this.each(function() {
            
                /////////////////////////////////////
                //Default settings for this plugin
                /////////////////////////////////////
                var _defaultSettings = {
                    listSource: null,
                    //listId: 'classroom_list',
                    getLi: function (data, settings){
                            if(settings.checkbox)
                            {
                                //Show a checkbox in li
                                return '<li class="ui-widget-content json-list-item" item_id="' + data[i].id + '">' + data[i].name + 
                                            '<input type="checkbox" checked="true"/></li>';
                            }
                            else
                            {
                                return '<li class="ui-widget-content json-list-item" item_id="' + data[i].id + '">' + data[i].name + "</li>";
                            }
                        },
                    callback: function (){
                    },
                    selected: function(){},
                    unselected: function (){},
                    draggable: false,
                    checkbox: false,
                    //itemClass: "selection_pane",
                    refreshPositions: true,
                    method: "selectable"
                };
                //Create actual settings
                var _settings = $.extend(_defaultSettings, settings);
            
                //Store settings data
                var $this = $(this);
                var data = $this.data('json_list');
                var divElem = this;

                //If the code is already initialized
                if ( !data ) {
                    /*
                     Do more setup stuff here
                    */
                    $(this).data('json_list', {
                       target : $this,
                       _settings: _settings
                    });
                }
                ////////////////////////////////////
                ////////////////////////////////////
                $this.html('<div class="ui-json-list-container"><ol></ol></div>');
                
                /*
                $("ol", divElem).selectable({
                    selected: _settings.selected,
                    unselected: _settings.unselected
                });*/
                if(_defaultSettings.method == "selectable")
                {
                    $("ol", divElem).selectable({
                        selected: _settings.selected,
                        unselected: _settings.unselected
                    });
                }
                else if(_defaultSettings.method == "sortable")
                {
                    $("ol", divElem).sortable({
                        selected: _settings.selected,
                        unselected: _settings.unselected
                    });
                    //$("ol", divElem).disableSelection();
                }
                if(null == _settings.listSource)
                {
                    _settings.listSource = $this.attr("src");
                }
                var req = $.getJSON(_settings.listSource);
                req.ref = $(this);
                req.success(function (data, textStatus, jqXHR){

                    var res = "";
                    var listJqueryObj = jqXHR.ref;
                    var jsonListData = listJqueryObj.data('json_list');
                    if(0 == data.length)
                    {
                        alert("No item defined from source: " + jsonListData._settings.listSource);
                    }
                    for(i = 0; i < data.length; i++)
                    {
                        res += jsonListData._settings.getLi(data, jsonListData._settings);
                    }
                    $("ol", divElem).html(res);
                    if(jsonListData._settings.draggable)
                    {
                        $("li", divElem).each(function(){
                            //Set a fix width so the item size will not change when dragged
                            $(this).css("width", $(this).width());
                            $(this).draggable({
                                    zIndex: 999,
                                    revert: true,      // will cause the event to go back to its
                                    revertDuration: 0,  //  original position after the drag
                                    helper: "clone",
                                    refreshPositions: _settings.refreshPositions,
                                    /*
                                    start: function(event, ui)
                                    {
                                        ui.
                                    },*/
                                    lastElement: "forIeToAvoidLastCommaIssue"
                                });
                        });
                    }
                    jsonListData._settings.callback($("li", divElem));
                });

            
            });//End of return this.each(function() {
        },//End of init : function( settings ) {
        getItems: function(){
            return $("li", this);
        }
    };//End of var methods = {
    
    
    
    //The following codes are common processing codes do not need to be modified
    $.fn.json_list = function( method ) {
        // Method calling logic
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
        }    

    };
})(jQuery);

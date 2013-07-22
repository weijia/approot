$(document).ready(function() {
    function request_op(event, target_url) {
        //console.log($(event.currentTarget).parents("tr").index());
        //console.log("debug: waiting-repair-table button.edit");
        //var o = $( "#waiting-repair-table" ).data("tableData").objects[$(event.currentTarget).parents("tr").attr("id")];
        var dbObj = $('#object-table').dataTable();
        console.log($(event.target));
        var aPos = dbObj.fnGetPosition($(event.target).parents("tr")[0]);
        var nRow = $(event.target).parents("tr")[0];
        var aData = dbObj.fnGetData(nRow);
        console.log(aData, aData.ufs_url);
        /*var jqTds = $('>td', nRow);

         for(var i = 0; i<3; i++){
         jqTds[i].innerHTML = '<input type="text" value="'+jqTds[i].innerText+'">';
         }
         $('button.edit', $(nRow)).text('save').addClass("save").removeClass("edit").after('<button class="cancel">Cancel Edit</button>');
         */
         $.getJSON(target_url + encodeURI(aData.ufs_url));
    }
    $('#object-table').on("click", "button.start", function(e){
        request_op(e, "/connection/start_diagram/?ufs_url=");
    });
    $('#object-table').on("click", "button.stop", function(e){
        request_op(e, "/connection/stop_diagram/?ufs_url=");
    });
    $('#object-table').on("click", "button.auto-start", function(e){});
    $('#object-table').dataTable({bJQueryUI:true,
        "sAjaxSource": "/connection/diagram_list/",
        "sAjaxDataProp": "objects",
        "fnServerData": function ( sSource, aoData, fnCallback ) {
            //aoData.push({"name": "format", "value": "json"});

            console.log("requesting", sSource, aoData);
            $.ajax( {
                "dataType": 'json',
                "type": "GET",
                "url": sSource,
                "data": aoData,
                "success": function(data, result, req){
                    for(var i=0; i<data.objects.length; i++){
                        data.objects[i].operations = '<button class="start">Start</button>' +
                             '<button class="stop">Stop</button>' +
                            '<button class="auto-start">Auto start</button>';
                    }
                    fnCallback(data);
                }
            } );//End of $.ajax( {
        },
        "aoColumns": [
                        { "mDataProp": "ufs_url" },
                        { "mDataProp": "full_path" },
                        { "mDataProp": "description" },
                        { "mDataProp": "operations" }
                    ]
    });
    
});

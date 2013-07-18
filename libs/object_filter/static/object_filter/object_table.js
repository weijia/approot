$(document).ready(function() {

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
                        data.objects[i].operations = "<button class='start'>Start</button> <button class='stop'>Stop</button>";
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

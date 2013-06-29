var JsonDataTables = {
        options: {
            listSource: null,
            //listId: 'classroom_list',
            getLi: function (data, index){
                        var liHtml = "";
                        $.each(data.objects[index], function(key, value){
                            liHtml += String.format('<td {0}="{1}">{1}</td>', key, value);
                        });
                        return liHtml;
                },
            callback: function (){
            },
            notSelectedText: "Not selected",
            width: 200,
            selected: function(){},
            unselected: function (){}
        },

        _init : function( settings ) {
            var element = this.element;
            var options = this.options;
            if(null == options.listSource)
            {
                options.listSource = element.attr("src");
            }

            var req = $.getJSON(options.listSource);
            //req.ref = this;
            req.success(function (data, textStatus, jqXHR){
                    /*var titles = {"url","fullpath","uuid"};
                    var tableHtml = '<table id="result-table"><thead><tr>' + 
                        $.each(titles, function(key, value){
                            '<th>'+ value + '</th>'
                        });*/
                    var tableHtml = '<table id="result-table"><thead><tr>';
                    tableHtml += '<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>'
                    tableHtml += '</tr></thead><tbody></tbody><tfoot><tr>';
                    tableHtml += '<td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td>'
                    tableHtml += '</tr></tfoot></table>';
                    element.html(tableHtml);
                    //console.log(data);
                    $.each(data.objects, function(key, value){
                        var line = '<tr class="json-datatable-row" itemIndex="'+key+'">';
                        line += options.getLi(data, key);
                        line += '</tr>';
                        
                        $( "tbody", element ).append(line);
                        
                    });
                    $( "#result-table .scheduling-row" ).click(function(event){

                    });
                    $( "#result-table" ).dataTable({bJQueryUI:true/*,
                                                    "bPaginate": false*/});

            
            });


        }

};
$.widget("ui.json_data_tables", JsonDataTables);

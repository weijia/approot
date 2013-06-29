$(document).ready(function () {
    $( "#confirm-diagram" ).click(function(){
        console.log("confirm-clicked");
        var connectionList = jsPlumb.getConnections();
        var processorList = {};
        var taskList = [];
        for (var i=0;i<connectionList.length;i++)
        {
            console.log(connectionList[i], i, connectionList);
            //Output for the processor
            if(undefined != connectionList[i].sourceId)
            {
                if(undefined == processorList[connectionList[i].sourceId])
                {
                    processorList[connectionList[i].sourceId] = {"inputs":[], "outputs":[], "ufs_url":null}
                    taskList.push(connectionList[i].sourceId);
                }
            }
            processorList[connectionList[i].sourceId]["outputs"].push(i);
            processorList[connectionList[i].sourceId]["ufs_url"] = $("#"+connectionList[i].sourceId).data("data").data;
            
            //Input for the processor
            if(undefined != connectionList[i].targetId)
            {
                if(undefined == processorList[connectionList[i].targetId])
                {
                    processorList[connectionList[i].targetId] = {"inputs":[], "outputs":[], "ufs_url":null}
                    taskList.push(connectionList[i].targetId);
                }
            }
            
            processorList[connectionList[i].targetId]["inputs"].push(i);
            processorList[connectionList[i].targetId]["ufs_url"] = $("#"+connectionList[i].targetId).data("data").data;
            
            console.log(processorList);
            console.log($("#"+connectionList[i].targetId).data("data").data);
            
        }
        for(var processorIndex = 0; processorIndex < taskList.length; processorIndex++)
        {
            var processor_id = taskList[processorIndex];
            processorList[processor_id]["params"] = $("#"+processor_id+" input").val();
        }
        
        console.log(JSON.stringify(processorList));

        $.post('/connection/save_diagram/',
            JSON.stringify({"diagram_id": diagram_id, "processorList": processorList}),
            function(data) {
                //$('.result').html(data);
                console.log(data);
            }
        );

    });
});
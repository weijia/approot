var ObjList = {
    options: {url: null, callback: null},
    _init: function(){
        /*
        var self = this;
        this.element.click(function(){
            self.move();
        });
        */
        var elemInInit = this.element;
        var optionsInInit = this.options;
        //var optionsInReady = optionsInInit;
        if(null == optionsInInit.url) return;
        $.getJSON(optionsInInit.url, function(data){
            //In this function $(this) is the xhr request
            for(i = 0; i < data.length; i++)
            {
                //$(curContainerBlocksElem).container_blocks("genEvent", data[i].classroomId.pk, data[i].start, data[i].end, "New test class", data[i].id, data[i].teacherList);
                /*var attrs = "";
                $.each(data[i], function(key, value){
                    attrs = key + '= "' + value + '" ';
                });*/
                $(String.format('<div class="element-root" style="float:left">{0}</div>', data[i].data)).appendTo(elemInInit).data("data", data[i]);
            }
            if(null == optionsInInit.callback) return;
            optionsInInit.callback($('.element-root', elemInInit), data);
        });
    }/*,
    move: function(){
        this.element.css (this._newPoint());
    }*/
}

$.widget ('ufs.objlist', ObjList);
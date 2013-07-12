
function loadContent(url)
{   /*
    $.ajax({
          url: url,
          success: function(data){
                //In this function $(this) is the xhr request
                $( '#content' ).html(data);
                delete url;
                $( '#content a' ).click(function(e){
                    loadContent($(e.target).attr("href"));
                    e.preventDefault();
                });
                //The following is used to fix date time plugin control in django admin pages
                if(! (typeof DateTimeShortcuts === 'undefined')) {
                    // variable is undefined
                    console.log("Call DateTimeShortcuts.init() to fix date time plugin control in django admin pages");
                    DateTimeShortcuts.init();
                }
            }
    });*/
    jQuery.ajaxSetup({ cache:true});
    console.log(url);
    $( '#content' ).load(url, function(){
        delete url;
        $( '#content a' ).click(function(e){
            loadContent($(e.target).attr("url"));
            e.preventDefault();
        });
        //The following is used to fix date time plugin control in django admin pages
        if(! (typeof DateTimeShortcuts === 'undefined')) {
            // variable is undefined
            console.log("Call DateTimeShortcuts.init() to fix date time plugin control in django admin pages");
            DateTimeShortcuts.init();
        }
        
    });
}

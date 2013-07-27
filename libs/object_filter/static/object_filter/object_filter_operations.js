function getFilterParams() {
    var queryParam = "";
    var full_path = $("#full-path").val();
    if (full_path != "") {
        queryParam += "&full_path_contains=" + encodeURI(full_path);
    }
    var ufs_url = $("#ufs-url").val();
    if (ufs_url != "") {
        queryParam += "&url_contains=" + encodeURI(ufs_url);
    }
    var existing_tags = $("#tag").val();
    if (existing_tags != "") {
        queryParam += "&existing_tags=" + encodeURI(existing_tags);
    }
    return queryParam;
}

$(document).ready(function () {
    $('#full-path, #ufs-url, #tag').autocomplete({
        source: function (request, response) {
            //console.log(request, response, this);
            //console.log(this.element[0].id);
            //var query = this.element[0].id.replace("-", "_")+"__contains";
            $("#obj-pane").html("");

            if (this.element[0].id == "full-path") {
                var queryData = {
                    full_path__iendswith: request.term,
                    format: "json"
                };
            }
            else if (this.element[0].id == "ufs-url") {
                var queryData = {
                    ufs_url__contains: request.term,
                    format: "json"
                };
            }
            else {
                var queryData = {
                    tag: request.term,
                    format: "json"
                };
            }
            var url = "/objsys/api/ufsobj/ufsobj/?";
            if ($("#query-base").length > 0) {
                url = $("#query-base").val();
            }
            $.ajax({
                url: url,
                dataType: "json",
                data: queryData,
                success: function (data) {
                    genHtml(data);
                }
            });
        }
    });//End of $('path-contains').autocomplete({


    $("#detail-view-button").button().click(
                                            function () {
                                                            $("#obj-pane").removeClass("thumb-view");
                                                            $("#obj-pane").addClass("detailed-view");
                                                        }
    );
    $("#thumb-view-button").button().click(
                                            function () {
                                                            $("#obj-pane").removeClass("detailed-view");
                                                            $("#obj-pane").addClass("thumb-view");
                                                        }
    );
    $("#export-tags-button").button().click(
                function () {
                                var queryParam = "";
                                queryParam += getFilterParams(queryParam);
                                $.getJSON("/object_filter/export_tags/?"+queryParam);
                            }
    );
    $("#apply-tags-button").button().click(
                function () {
                                var tags = $("#using-tags-input").val();
                                if(tags == "") return;
                                var queryParam = "tags="+tags;
                                queryParam += getFilterParams(queryParam);
                                $.getJSON("/objsys/apply_tags_to/?"+queryParam);
                            }
    );
    $("#remove-tags-button").button().click(
                function () {
                                var tags = $("#using-tags-input").val();
                                if(tags == "") return;
                                var queryParam = "tags="+tags;
                                queryParam += getFilterParams(queryParam);
                                $.getJSON("/objsys/remove_tags_from/?"+queryParam);
                            }
    );
});

/**
 * Created by edison on 14-9-12.
 */
;(function ($, document, window) {


    var entity = {
        removeImage: function() {
//            console.log("OKOKO");
            $('#images').find('.btn').on('click', function(){
//                console.log(this);
                var image = $(this);
//                console.log(image.parent().parent());
                var index = image.attr('data-image');
                $.ajax({
                    url: this.href,
                    type: "POST",
                    dataType:'json',
                    data: {"index": index},
                    success: function(data) {
                        image.parent().parent().remove();
                    }
                });
                return false;
            });
        },

        removeBuyLink: function() {
            $('#buylinks').find('.btn-link').on('click', function(){
                var buy_link = $(this);
                //console.log(buy_link);

                var index = buy_link.attr('data-index');
                //console.log(index)
                var url = "/management/entity/" + index + "/buy/link/remove/";
                $.ajax({
                    url:url,
                    type: "POST",
                    dataType: "json",
                    success: function(data) {
                        buy_link.parent().remove();
                    }
                });
            });
            return false;
        }

    };

    var dashboard = {
        selectedChar: function() {
            var selection_chart = $('#selectionChart');
            var like_chart = $('#likeChart');
            var category_chart = $('#categoryChart');

            if (selection_chart[0]){
                var selection_ctx = selection_chart.get(0).getContext("2d");
                var like_ctx = like_chart.get(0).getContext("2d");
                var category_ctx = category_chart.get(0).getContext("2d");
                $.ajax({
                    url:"/management/dashboard/",
                    type: "get",
                    dataType: "json",
                    success : function(res) {
                        //console.log(res);
                        var labels = new Array();
                        var d = new Array();
                        var like_total = new Array();
                        $(res.selection).each(function(index){
                            //console.log(row.id)
                            var val = res.selection[index];
                            //console.log(val.selected_total);
                            labels.push(val.pub_date);
                            d.push(parseInt(val.selected_total));
                            like_total.push(parseInt(val.like_total));
                        });
                        var data = {
                            labels: labels,
                            datasets: [
                                {
                                    label: "publish selection ",
                                    fillColor: "rgba(151,187,205,0.2)",
                                    strokeColor: "rgba(151,187,205,1)",
                                    pointColor: "rgba(151,187,205,1)",
                                    pointStrokeColor: "#fff",
                                    pointHighlightFill: "#fff",
                                    pointHighlightStroke: "rgba(220,220,220,1)",
                                    data: d
                                }
                            ]
                        };
                        var like_data = {
                            labels: labels,
                            datasets: [
                                {
                                    label: "publish selection ",
                                    fillColor: "rgba(151,187,205,0.2)",
                                    strokeColor: "rgba(151,187,205,1)",
                                    pointColor: "rgba(151,187,205,1)",
                                    pointStrokeColor: "#fff",
                                    pointHighlightFill: "#fff",
                                    pointHighlightStroke: "rgba(220,220,220,1)",
                                    data: like_total
                                }
                            ]
                        };
                        var selectionLineChart = new Chart(selection_ctx).Line(data);
                        var likeBarChart = new Chart(like_ctx).Bar(like_data);

                        var category_labels = new Array();
                        var category_data = new Array();
                        $(res.category).each(function(index){
                            //console.log(row.id)
                            var val = res.category[index];
                            //console.log(val.selected_total);
                            category_labels.push(val.label);
                            category_data.push(parseInt(val.value));
                            //like_total.push(parseInt(val.like_total));
                        });

                        var category_data_list = {
                            labels: category_labels,
                            datasets: [
                                {
                                    label: "publish selection ",
                                    fillColor: "rgba(151,187,205,0.2)",
                                    strokeColor: "rgba(151,187,205,1)",
                                    pointColor: "rgba(151,187,205,1)",
                                    pointStrokeColor: "#fff",
                                    pointHighlightFill: "#fff",
                                    pointHighlightStroke: "rgba(220,220,220,1)",
                                    data: category_data
                                }
                            ]
                        };
                        var categoryPolarArea = new Chart(category_ctx).Bar(category_data_list);
                    }
                })
            }
        }
    };

    var comment = {
        remove: function(){
            var comment_list = $("#comment");
            comment_list.find(".btn").on('click', function(){
                console.log("OKOKOKO");
            })
        }
    };

    (function init() {
//        console.log($.find());
        entity.removeImage();
        entity.removeBuyLink();
        dashboard.selectedChar();

        comment.remove();
//        note.post();
    })();
})(jQuery, document, window);
//修改case——加载页面的初始化js

/*获取该case的接口数据*/
function initCaseBoard(){

    var paths = window.location.pathname.split('/')
    var caseId = paths[paths.length-2]

    $.get('/cases/update/'+caseId+'/', function(data, status, jrXHR){
        var method = data["info"]["method"];
        var prior = data["info"]["prior"];
        var group_id = data["info"]["group_id"];

        $(".select-table-cell").find("option[value='"+method+"']").attr("selected", "selected") //请求方法
        $(".prior-select").find("option[text='"+prior+"']").attr("selected", "selected");  //优先级
        $(".case-group-select").find("option[value='"+group_id+"']").attr("selected", "selected") //case分组

    })

}

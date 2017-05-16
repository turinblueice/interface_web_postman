
$(document).ready(function(){
    if(sessionStorage.caseSelected == undefined)
        sessionStorage.caseSelected = "";

    /*更新已选中的case列表*/
    function updateCasesSelected(){
        var caseSelectedObj = new Object();
        var caseSelectedArray = sessionStorage.caseSelected.split(',').slice(0, -1)
        for(var i=0; i<caseSelectedArray.length; i++){
            caseSelectedObj[caseSelectedArray[i]] = true
        }

        return caseSelectedObj
    }


    // 初始化已勾选的case
    var caseSelectedObj = updateCasesSelected();
    $("input[type=checkbox]").each(function(){
        if(caseSelectedObj[$(this).attr('value')]==true)
        {
            $(this).attr('checked', true)
        }

    })

    //checkbox 绑定方法
    $("input[type=checkbox]").change(function(){
        var id = $(this).attr('value');
        if($(this).is(':checked')){
            sessionStorage.caseSelected += (id+",")
        }
        else
            sessionStorage.caseSelected = sessionStorage.caseSelected.replace(id+",", '')
    })


    //绑定提交case按钮方法
    $("#btn-submit").click(function(){
        var sendData = {'cases': sessionStorage.caseSelected};
        $.post('/cases/cases-submit/', sendData, function(data, status){
            alert(data)
        })

    })


    //删除URL操作
    $(".delete").click(
        function(){
            var status = confirm("确定删除该接口case?")
            if(status){
                //点击确定
                var _this = $(this);
                var deleteIdObj = {'id': $(this).parent().parent().find('input[type=checkbox]').attr('value')}

                $.post('/cases/delete/', deleteIdObj, function(data, status, jqXHR){

                    if(data['succ']){
                        console.log(data);
                        _this.parent().parent().remove()
                    }

                })
                return true
            }
            else{
                //点击取消

                return false
            }
        }
    )

    //选择分组展示case操作
    $("select").change(function(){
        var selectedGroupId = $(this).val()
        window.location = "/cases/"+selectedGroupId+"/"

    })

});
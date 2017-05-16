//接口主面板的js

// 显示参数的key-value行
var keyValueHtml = '<div class="param-pairs"><div><input class="key-v" value={0}></div>'+
'<div><input class="key-v" value={1}></div><div class="cancel"><button></button></div></div>'

// 显示消息返回的header行
var rspHeaderHtml = "<div><div class=\"rsp-header-key\">{0}</div><div><img src=\"/static/image/right.png\"></div><div>{1}</div></div>"

// 显示测试结果的行
var rspTestsHtml = "<div><div class=\"rsp-test-key\">{0}</div><div class=\"test-{1}\">{2}</div></div>"


function processor(){

    $(".param").hide(); /*参数列表隐藏*/

    //判断当前select是否为get, 若为get则body tab置为灰色
    if($(".head-cell select").val()==="get")
        $("#req-body-tab button").attr("disabled", "disabled")

    /*参数列表显示方法*/
    function displayParamsTable(paramBlock){

        if(paramBlock.css("display")!=='none'){

            var url = $("#url").val();
            if(!url.IsNullEmptyOrSpace()){

                //首先清除已有参数列表显示
                $(".param").empty()

                var paramStrList = url.split('?');
                var params = new Array();
                if (paramStrList.length>1 && !paramStrList[1].IsNullEmptyOrSpace()){
                    var params = paramStrList[1].split('&');
                }

                var tmpKeyValueHtml = '';
                for(var i in params){
                    if(!params[i].IsNullEmptyOrSpace()){
                        var keyValuePairs = params[i].split('=');
                        var key = keyValuePairs[0];
                        var value = keyValuePairs.length==1 ? '' : keyValuePairs[1];
                        tmpKeyValueHtml += keyValueHtml.format(key, value)

                    }
                }
                if(!tmpKeyValueHtml.IsNullEmptyOrSpace())
                    $(".param").html(tmpKeyValueHtml)
            }
        }
    }

    /*切换显示方式*/
    function displayToggle(div){

        state = div.css('display');
        if(state=='none')
            div.css('display', 'table');
        else
            div.css('display', 'none');

    }


    /*
     * 点击参数,展示请求url的key-value面板
     */
    $("#parameter").click(function(){

        var paramBlock = $(".param");
        //paramBlock.toggle();
        displayToggle(paramBlock)
        displayParamsTable(paramBlock)
    })

    /*从参数面板中组装url*/
    function getUrlFromParamBoard(url){

        var prefix = url.slice(0, url.indexOf("?")+1);
        var postfix = ""
        $(".param-pairs").each(function(){
            var pairs = $(this).find(".key-v").eq(0).val();
            if(!pairs.IsNullEmptyOrSpace()){
                pairs += "=";
                pairs += $(this).find(".key-v").eq(1).val();
                pairs += "&";
                postfix += pairs;
            }
        })

        postfix = postfix.slice(0, -1);
        prefix = postfix.IsNullEmptyOrSpace()?prefix.slice(0, -1):prefix;

        return prefix+postfix
    }

    /*参数修改联动url*/
    $(".param").delegate(".key-v", "keyup", function(){
        var url = $("#url").val();
        url = getUrlFromParamBoard(url);
        $("#url").val(url);
    })

    /*url修改联动参数*/
    $("#url").keyup(function(){
        var paramBlock = $(".param");
        displayParamsTable(paramBlock);
    })

    /*点击参数键值对的叉按钮*/
    $(".param").delegate("div.cancel", 'click', function(){

        $(this).parent().remove()  //删除当前行
        var url = $("#url").val();
        url = getUrlFromParamBoard(url);
        $("#url").val(url);   //设置新组装的url
    })

    /*参数面板下键值对的处理*/
    $(".param").delegate("input", "click", function(){

        var paramNum = $(".param-pairs").size();
        var rowParent = $(this).parent().parent();
        var num = rowParent.index()
        if(num===paramNum-1){
            //当前点击的元素是总元素中的最后一个
            var newParam = rowParent.clone();
            newParam.find("input").each(function(){
                $(this).val("")
            })
            $(".param").append(newParam);
        }
    })

    /*tab切换方法*/
    function tabSwitch(idPrefix, display){
        /*点击各tab的响应*/
        $("#"+idPrefix+"-bar button").focus(function(){
            $("#"+idPrefix+"-bar .focus").css('display', 'none');
            jQuery(".focus", this).css('display', 'block'); //显示tab下的选中标记
            var id = jQuery(this).parent().attr("id");
            var boardId = id.slice(0, id.length-3)+'board';
            $("#"+idPrefix+"-board .tab-board").css('display', 'none'); //隐藏其他面板
            $("#"+boardId).css('display', display); //显示该tab下的面板
        })
    }

    tabSwitch("req", 'table');
    tabSwitch("rsp", 'block');

    /*request请求部分默认焦点在headers,默认显示header tab*/
    $("#req-header-tab button").trigger('focus')

    /*Headers tab下key-value键值对点击的处理*/
    $("#req-header-board").delegate("input", "click", function(){

        var reqHeaderParamNum = $("#req-header-board .tab-row").size();
        var rowParent = $(this).parent().parent()
        var num = rowParent.index()

        if(num===reqHeaderParamNum-1){
            //当前点击的元素是总元素中的最后一个
            var newRow = rowParent.clone()
            newRow.find("input").val("")
            $("#req-header-board").append(newRow)
        }
    })

    /*点击Headers tab下的X按钮*/
    $("#req-header-board").delegate("div.cancel", 'click', function(){
        var rowCount = $("#req-header-board .tab-row").size()

        if(rowCount>1){
            $(this).parent().remove()
        }
    })

    /*添加Body下输入键值对的托管事件,包括增加和删除每行键值对*/
    function addBodyTabInputKeyVDelegate(selector){

        $(selector).delegate("input", "click", function(){

            var reqHeaderParamNum = $(selector+" .tab-row").size();
            var rowParent = $(this).parent().parent()
            var num = rowParent.index()
            if(num===reqHeaderParamNum-1){
                //当前点击的元素是总元素中的最后一个
                $(selector).append(rowParent.clone())
            }
        })

        /*点击body tab下的X按钮*/
        $(selector).delegate("div.cancel", 'click', function(){
            var rowCount = $(selector+" .tab-row").size()

            if(rowCount>1){
                $(this).parent().remove()
            }
        })
    }

    addBodyTabInputKeyVDelegate("#form-urlencoded");  /*Body tab下键值对的处理-x-www-form-urlencoded*/
    addBodyTabInputKeyVDelegate("#form-data")  /*Body tab下键值对的处理-form-data*/

    /*Cookie tab下key-value键值对点击的处理*/
    $("#req-cookie-board").delegate("input", "click", function(){

        var reqCookieParamNum = $("#req-cookie-board .tab-row").size();
        var rowParent = $(this).parent().parent()
        var num = rowParent.index()

        if(num===reqCookieParamNum-1){
            //当前点击的元素是总元素中的最后一个
            var newRow = rowParent.clone()
            newRow.find("input").val("")
            $("#req-cookie-board").append(newRow)
        }
    })

    /*点击Cookies tab下的X按钮*/
    $("#req-cookie-board").delegate("div.cancel", 'click', function(){
        var rowCount = $("#req-cookie-board .tab-row").size()

        if(rowCount>1){
            $(this).parent().remove()
        }
    })

    /*点击radio的响应*/
    $(".radio-bar input").click(function(){

        var id = $(this).val()
        $("div.content-type").css('display', 'none');//隐藏其他面板
        $("#"+id).css('display', 'table'); //显示该radio的面板
    })

    /*select 选择请求方法的操作*/
    $(".head-cell select").change(function(){
        var selected = $(this).val()

        if(selected=="get")
            $("#req-body-tab button").attr("disabled", "disabled")
        else
            $("#req-body-tab button").removeAttr("disabled")

    })

    /*识别抓取tests Tab下的内容, 获取测试用例语句*/
    function getTestsFromTestsBoard(boardId){
        var testTabBoard = $('#'+boardId+' textarea')
        var testTabText = testTabBoard.val().trim()
        var lines = testTabText.split("\n")
        var newLines = new Array()
        for(var i=0; i<lines.length; i++){
            var line = lines[i].trim()
            if(!line.IsNullEmptyOrSpace()){
                line = line.replaceAll("'", "\"");
                newLines.push(line)
            }
        }
        return newLines
    }

    /*执行tests tab下执行语句的方法,获取执行结果*/
    /*
     *@param lines 测试语句
     *
     *
    */
    function getTestResult(lines){
        var testResults = new Array();
        for(var i=0; i<lines.length; i++)
        {
            var line = lines[i];
            var result = null;
            try{
                result = eval(line)?"Pass":"Fail";  //eval结果为true/false/undefined
            }
            catch(err){
                result = "Error: "+err.message
            }

            var match = line.match(/^tests\["\S+"\]=/g)
            if(match!=null) //匹配字符串中的tests[casename], 只记录tests[]所在行
            {
                var caseName = match[0].slice(7, -3);
                testResults[caseName] = result
            }
        }
        return testResults
    }

    /*test 测试结果面板显示*/
    function displayTestResults(testResults){
        var testsBoard = $("#rsp-test-board");
        testsBoard.empty()

        for(var key in testResults){
            var result = testResults[key];
            var status = result.split(":", 1)[0].toLowerCase();
            var rspTestsNode = rspTestsHtml.format(key, status, result);
            testsBoard.append(rspTestsNode)
        }
    }

    /*初始化Tests tab下的协议变量, 执行测试*/
    /*
     *@param jsonData  返回的json格式对象, object类型
     *
     *
     */
    function startTestBoardRunning(rspData){

        //初始化协议变量,将协议变量设置为全局变量
        window.responseBody = rspData;
        window.tests = new Object();

        var lines = getTestsFromTestsBoard("req-tests-board")
        var testResults = getTestResult(lines);
        displayTestResults(testResults);

    }


    /*
        组装请求信息
    */
    function mkRequestInfo(url){

        var method = $(".head-cell select").val().trim();
        var headersDict = null;
        var dataDict = null;
        var cookiesDict = null;

        /*组装请求*/

        /*组装请求头*/
        var headers = $("#req-header-board .tab-row")
        headers.each(function(){
            var key = $(this).find('.board-input').first().val().trim();
            var value = $(this).find('.board-input').last().val().trim();
            if(!key.IsNullEmptyOrSpace()&&!value.IsNullEmptyOrSpace()) //key value非空则视为有效值
            {
                headersDict = headersDict==null?new Object():headersDict;
                headersDict[key] = value
            }
        })

        /*组装请求头中的网络媒体类型 content-type*/
        var mimeType = $("input[type='radio'][name='content-type']:checked").next().text()

        /*非get方法下,组装body的请求参数*/
        if($(".head-cell select").val()!="get")
        {
            if(mimeType==="x-www-form-urlencoded"){
                $("#form-urlencoded .tab-row").each(function(){
                    var key = $(this).find('.board-input').first().val().trim();
                    var value = $(this).find('.board-input').last().val().trim();
                    if(!key.IsNullEmptyOrSpace()&&!value.IsNullEmptyOrSpace()) //key value非空则视为有效值
                    {
                        dataDict = dataDict==null?new Object():dataDict;
                        dataDict[key] = value
                    }
                })
            }
        }

        /*组装cookie*/
        var cookies = $("#req-cookie-board .tab-row")
        cookies.each(function(){
            var key = $(this).find('.board-input').first().val().trim();
            var value = $(this).find('.board-input').last().val().trim();
            if(!key.IsNullEmptyOrSpace()&&!value.IsNullEmptyOrSpace()) //key value非空则视为有效值
            {
                cookiesDict = cookiesDict==null?new Object():cookiesDict;
                cookiesDict[key] = value
            }
        })

        /*组装tests*/
        var testsLines = getTestsFromTestsBoard("req-tests-board")

        var reqDict = {"url":url, "method":method}

        reqDict["params"] = "{}";  // 预留参数
        reqDict["headers"] = headersDict!=null?JSON.stringify(headersDict):"{}";
        reqDict["data"] = dataDict!=null?JSON.stringify(dataDict):"{}";
        reqDict["cookies"] = cookiesDict!=null?JSON.stringify(cookiesDict):"{}";
        reqDict["tests"] = testsLines.join(";")+';'  //确保最后一行以分号结束


        if(/^\/cases\/update-board\/\d+\/$/g.test(window.location.pathname)){
            //如果当前访问的是case修改面板
            var paths = window.location.pathname.split('/');
            var caseId = paths[paths.length-2];
            reqDict["id"] = caseId
        }

        return reqDict

    }


    /* 获取请求参数和URL,构造request,并获取请求结果 */
    /*
    * @param url 网址URL
    *
    */
    function mkRequest(url){

        var requestObj = mkRequestInfo(url);

        ///////////*将请求传递给服务器端,获取请求结果*/////////////////////
        $.post('/processor/upload_req/', requestObj, function(data, status, jqxhr){

            contentType = jqxhr.getResponseHeader('content-type')
            cookieStr = jqxhr.getResponseHeader('rsp-cookie')

            /*处理cookie*/
            cookies = cookieStr.split('|')
            cookieBoardNode = $("#rsp-cookie-board")

            //加载cookie前, 先删除上一次请求获得的cookie显示节点
            $("#rsp-cookie-board .tab").each(function(){
                if($(this).index()!=0)
                    $(this).remove()
            })

            for(var i=0; i<cookies.length; i++){
                var cookieAttrs = cookies[i].split('&')
                var cookie = new Object();
                for(var j=0; j<cookieAttrs.length; j++)
                {
                    attrs = cookieAttrs[j].split('@')
                    cookie[attrs[0]] = attrs[1]
                }
                var cookieNode = $("#rsp-cookie-board .tab").first().clone()

                cookieNode.find(".tab-cell").each(function(){
                    var id = $(this).attr("id")
                    var textNode = $(this).find('div')
                    textNode.text(cookie[id.split('-')[1]])
                    textNode.css('font-weight', 'normal')
                    textNode.css('font-size', '12px')

                })
                cookieBoardNode.append(cookieNode)
            }

            /*处理header*/
            var rspHeaderNode = $("#rsp-header-board")
            var headers = jqxhr.getResponseHeader('rsp-header')

            //加载header前, 先删除上一次请求获得的header显示节点
            $("#rsp-header-board > div").each(function(){
                    $(this).remove()
            })

            var headerAttrs = headers.split('&')
            for(var i=0; i<headerAttrs.length; i++)
            {
                var attrs = headerAttrs[i].split('@')
                var newRspHeaderStr = rspHeaderHtml.format(attrs[0], attrs[1])
                rspHeaderNode.append(newRspHeaderStr)
            }

            // 每次请求显示请求结果,触发点击显示body事件
            $("#rsp-body-tab button").trigger("focus");
            if(contentType.indexOf('application/json')!=-1)
            {
                dataStr = JSON.stringify(data, undefined, 4)
                /*获取返回的数据, 展示json内容*/
                $("#rsp-body-options select").find("option[value='json']").attr("selected", "selected");
                /*显示test内容*/
                getTestsFromTestsBoard("req-tests-board")
            }
            else if(contentType.indexOf('text/html')!=-1)
            {
                $("#rsp-body-options select").find("option[value='html']").attr("selected", "selected");
                dataStr = htmlEncode(data)
            }
            $("#rsp-body-show pre").html(dataStr)

            startTestBoardRunning(data);

        })

    }

    /*
        保存请求,将此次请求作为case存储到后台数据库
    */
    function saveRequestCase(url, caseName, caseDescription, casePrior, caseGroup){
        var requestObj = mkRequestInfo(url);
        requestObj['name'] = caseName;
        requestObj['description'] = caseDescription;
        requestObj['prior'] = casePrior;
        requestObj['group'] = caseGroup;

        $.post('/processor/save_request/', requestObj, function(data, status, jqxhr){

            if(data.code==0)
                alert("保存成功")
            else
                alert(data["msg"])
        })
    }

    /*绑定发送按钮*/
    $("button.send").click(function(){
        //首先检查URL是否合法
        var url = $("#url").val().trim();
        if(IsURL(url))
            mkRequest(url);
        else{
            alert("输入的网址为非法URL");
            $("#url").focus();
            $("#url").select();
        }
    })

    /*绑定保存按钮*/
    $("button.save-req").click(function(){
        //首先检查URL是否合法
        var url = $("#url").val().trim();
        if(IsURL(url))
        {
            $("#mask").css("display", "block")
            $("#case-frame").css("display", "block")
            var defaultName = $("#url").val().trim();
            if($("#case-name").val().IsNullEmptyOrSpace())
                $("#case-name").val(defaultName)  //默认case名称为URL

            $.get('/processor/get_groups/', function(data, status, jqxhr){

                var groupsSelected = $(".case-group-select").find("option[selected='selected']")  //获取当前已选中的group

                var groups = data['groups'];
                var optionsStr = "";
                for(var index in groups){

                    var selectedStr = ""
                    if(groupsSelected.size()==1&&groups[index]['id']==groupsSelected.eq(0).val()){

                        selectedStr = " selected=selected"
                    }

                    var optionStr = "<option value="+groups[index]['id']+selectedStr+">"+groups[index]['name']+"</option>";
                    optionsStr += optionStr;
                }
                $("#case-frame .group-select select").empty();
                $("#case-frame .group-select select").append(optionsStr);
            })
        }
        else
        {
            alert("输入的网址为非法URL");
            $("#url").focus();
            $("#url").select();
        }
    })

    /*遮罩行为绑定*/
    $("#mask").click(function(){
        $(this).css("display", "none")
        $("#case-frame").css("display", "none")
    })

    /*遮罩下按钮行为绑定*/
    $("#frame-cancel").click(function(){
        $("#case-frame").css("display", "none")
        $("#mask").css("display", "none")
    })

    $("#frame-ok").click(function(){

        var caseName = $("#case-name").val();
        var caseDescription = $("#case-frame textarea").val();
        var prior = $("#case-frame .prior-select select").val();
        var group = $("#add-group").val() || $("#case-frame .group-select select").find("option:selected").text();

        $("#case-frame").css("display", "none")
        $("#mask").css("display", "none")

        var url = $("#url").val().trim();

        saveRequestCase(url, caseName, caseDescription, prior, group);
    })


};
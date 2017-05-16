/*
 * 判断当前字符串是否为空字符串或者只包含空格、换行、tab字符
 */
String.prototype.IsNullEmptyOrSpace=function(){
  if(this==null) return true;
  return this.replace(/\s/g, '').length == 0;
};

/**
 * 替换所有匹配exp的字符串为指定字符串
 * @param exp 被替换部分的正则
 * @param newStr 替换成的字符串
 */
String.prototype.replaceAll = function (exp, newStr) {
    return this.replace(new RegExp(exp, "gm"), newStr);
};

/**
 * 原型：字符串格式化
 * @param args 格式化参数值
 */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length < 1) {
        return result;
    }

    var data = arguments; // 如果模板参数是数组
    if (arguments.length == 1 && typeof (args) == "object") {
        // 如果模板参数是对象
        data = args;
    }
    for ( var key in data) {
        var value = data[key];
        if (undefined != value) {
            result = result.replaceAll("\\{" + key + "\\}", value);
        }
    }
    return result;
}

/*
 * 判断字符串是不是url
 *
 *@param str_url 待测试url
 */

function IsURL(str_url){
    var strRegex = "^((https|http|ftp|rtsp|mms)?://)"
        + "?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?" //ftp的user@
        + "(([0-9]{1,3}\\.){3}[0-9]{1,3}" // IP形式的URL- 199.194.52.184
        + "|" // 允许IP和DOMAIN（域名）
        + "([0-9a-z_!~*'()-]+\\.)*" // 域名- www.
        + "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\\." // 二级域名
        + "[a-z]{2,6})" // first level domain- .com or .museum
        + "(:[0-9]{1,4})?" // 端口- :80
        + "((/?)|" // a slash isn't required if there is no file name
        + "(/[0-9a-zA-Z_!~*'(\\.;?:@&=+$,%#-]+)+/?)$";
    var re=new RegExp(strRegex);
    if(re.test(str_url)){
       return (true);
    }
    else{
         return (false);
    }
}


/*html转义方法,将HTML码转码为转义后的字符串*/
function htmlEncode(value){
  //create a in-memory div, set it's inner text(which jQuery automatically encodes)
  //then grab the encoded contents back out.  The div never exists on the page.
  return $('<div/>').text(value).html();
}

/*将转义后的字符串解码为html码*/
function htmlDecode(value){
  return $('<div/>').html(value).text();
}

/*初始化侧边栏*/
function initSideBar(){

    sidePath = window.location.pathname.split('/')[1];
    $(".side-bar>div>div").removeAttr('class');

    switch(sidePath){
        case "":
            $("#index").attr("class", "curr-page");
            break;
        case "processor":
            $("#addCase").attr("class", "curr-page");
            break;
        case "cases":
            $("#caseSelect").attr("class", "curr-page");
            break;
        case "report-square":
            $("#reportSquare").attr("class", "curr-page");
            break;
        default:
            ;
    }

}
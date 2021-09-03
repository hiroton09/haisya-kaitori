// JavaScript Document

function Acc() {

//cgiアク解用
document.write('<img src="http://www.haisha-kaitori.com/cgi/analyze/analyze.cgi?'+ screen.width + 'x' + screen.height + '&amp;' + screen.colorDepth + '&amp;' + document.referrer + '" alt="" width="1" height="1">');


//phpアク解用
document.write('<img src="http://www.haisha-kaitori.com/php/w3a/writelog.php?ref='+document.referrer+'" width="1" height="1">');

}
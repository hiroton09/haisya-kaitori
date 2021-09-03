// JavaScript Document

/*
 Author : http://www.yomotsu.net
 created: 2007/04/05
 Licensed under the GNU Lesser General Public License version 2.1
 
 input、textareaの初期値を自動でクリアする
*/

/* clearDefaultValue
----------------------------------------*/
function yomotsuClearDefaultValue(){
	var input = document.getElementsByTagName("input");
	var textarea = document.getElementsByTagName("textarea");

	/* input */
	for (i=0;i<input.length;i++){
		if((input[i].getAttribute("type") == "text")||(input[i].getAttribute("type") == null)){
			if (input[i].value == input[i].defaultValue){
				input[i].className += " default-value"
			}
			input[i].onfocus = function(){
				if (this.value == this.defaultValue){
					this.value = "";
					this.className = this.className.replace(/ default-value/, "");
				}
			}
			input[i].onblur = function(){
				if (this.value == ""){
					this.value = this.defaultValue;
					this.className += " default-value"
				}
			}
		}
	}
	/* textarea */
	for (i=0;i<textarea.length;i++){
		if (textarea[i].value == textarea[i].defaultValue){
			textarea[i].className += " default-value"
		}
		textarea[i].onfocus = function(){
			if (this.value == this.defaultValue){
				this.value = "";
				this.className = this.className.replace(/ default-value/, "");
			}
		}
		textarea[i].onblur = function(){
			if (this.value == ""){
				this.value = this.defaultValue;
				this.className += " default-value"
			}
		}
	}	
}

addEvent(window, 'load', yomotsuClearDefaultValue);

/* add event
----------------------------------------*/

function addEvent(obj, evType, fn){
	if (obj.addEventListener){
		obj.addEventListener(evType, fn, false);
		return true;
	}
	else if (obj.attachEvent){
		var r = obj.attachEvent("on"+evType, fn);
		return r;
	}
	else {
		return false;
	}
}